from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from database import get_db, User, Resource, Tag, Rating, Base, engine
from auth import get_password_hash, verify_password, create_access_token, verify_token
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="College Resource Hub")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ResourceResponse(BaseModel):
    id: int
    title: str
    description: str
    filename: str
    subject: str
    semester: str
    uploader: str
    upload_date: datetime
    download_count: int
    average_rating: float
    tags: List[str]

class RatingCreate(BaseModel):
    rating: int
    feedback: Optional[str] = None

# Auth endpoints
@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Resource endpoints
@app.post("/upload")
async def upload_resource(
    title: str = Form(...),
    description: str = Form(...),
    subject: str = Form(...),
    semester: str = Form(...),
    tags: str = Form(""),
    file: UploadFile = File(...),
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    
    # Save file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create resource
    resource = Resource(
        title=title,
        description=description,
        filename=file.filename,
        file_path=file_path,
        subject=subject,
        semester=semester,
        uploader_id=user.id
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    
    # Add tags
    if tags:
        tag_names = [tag.strip() for tag in tags.split(",")]
        for tag_name in tag_names:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
            resource.tags.append(tag)
        db.commit()
    
    return {"message": "Resource uploaded successfully", "id": resource.id}

@app.get("/resources", response_model=List[ResourceResponse])
async def get_resources(
    subject: Optional[str] = Query(None),
    semester: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Resource)
    
    if subject:
        query = query.filter(Resource.subject == subject)
    if semester:
        query = query.filter(Resource.semester == semester)
    if search:
        query = query.filter(or_(
            Resource.title.contains(search),
            Resource.description.contains(search)
        ))
    
    resources = query.order_by(Resource.average_rating.desc()).all()
    
    return [
        ResourceResponse(
            id=r.id,
            title=r.title,
            description=r.description,
            filename=r.filename,
            subject=r.subject,
            semester=r.semester,
            uploader=r.uploader.username,
            upload_date=r.upload_date,
            download_count=r.download_count,
            average_rating=r.average_rating,
            tags=[tag.name for tag in r.tags]
        ) for r in resources
    ]

@app.get("/download/{resource_id}")
async def download_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource.download_count += 1
    db.commit()
    
    return {"download_url": f"/uploads/{resource.filename}"}

@app.post("/rate/{resource_id}")
async def rate_resource(
    resource_id: int,
    rating_data: RatingCreate,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Check if user already rated
    existing_rating = db.query(Rating).filter(
        Rating.resource_id == resource_id,
        Rating.user_id == user.id
    ).first()
    
    if existing_rating:
        existing_rating.rating = rating_data.rating
        existing_rating.feedback = rating_data.feedback
    else:
        new_rating = Rating(
            resource_id=resource_id,
            user_id=user.id,
            rating=rating_data.rating,
            feedback=rating_data.feedback
        )
        db.add(new_rating)
    
    db.commit()
    
    # Update average rating
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.resource_id == resource_id).scalar()
    resource.average_rating = round(avg_rating, 2) if avg_rating else 0.0
    db.commit()
    
    return {"message": "Rating submitted successfully"}

@app.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    top_rated = db.query(Resource).order_by(Resource.average_rating.desc()).limit(5).all()
    most_downloaded = db.query(Resource).order_by(Resource.download_count.desc()).limit(5).all()
    
    return {
        "top_rated": [{"id": r.id, "title": r.title, "rating": r.average_rating} for r in top_rated],
        "most_downloaded": [{"id": r.id, "title": r.title, "downloads": r.download_count} for r in most_downloaded]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)