from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resource_hub.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for resource tags
resource_tags = Table('resource_tags', Base.metadata,
    Column('resource_id', Integer, ForeignKey('resources.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(String, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    filename = Column(String)
    file_path = Column(String)
    subject = Column(String, index=True)
    semester = Column(String, index=True)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    upload_date = Column(DateTime, default=datetime.utcnow)
    download_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    
    uploader = relationship("User")
    tags = relationship("Tag", secondary=resource_tags, back_populates="resources")
    ratings = relationship("Rating", back_populates="resource")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    resources = relationship("Resource", secondary=resource_tags, back_populates="tags")

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resource = relationship("Resource", back_populates="ratings")
    user = relationship("User")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()