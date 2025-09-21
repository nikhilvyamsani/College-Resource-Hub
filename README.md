# College Resource Hub

A centralized platform for students to upload, share, and access comprehensive study resources including notes, past exam papers, and study guides.

## Features

- **Secure Authentication**: JWT-based user authentication with role-based access
- **Resource Management**: Upload/download study materials with file validation
- **Smart Organization**: Advanced categorization by subject and semester
- **Quality Assurance**: Student-driven rating system for resource quality
- **Intelligent Search**: Search resources by title, description, subject, and tags
- **Smart Dashboard**: Top-rated and most-downloaded resources display

## Technology Stack

### Backend

- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Robust database for data management
- **SQLAlchemy**: ORM for database operations
- **JWT**: Secure authentication tokens
- **Bcrypt**: Password hashing

### Frontend

- **React.js**: Component-based UI framework
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls

## Quick Start

### Backend Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure environment:

```bash
# Update .env file with your database credentials
DATABASE_URL=postgresql://username:password@localhost/resource_hub
SECRET_KEY=your-secret-key-here
```

3. Start the backend server:

```bash
python main.py
```

The API will be available at `http://localhost:8001`

### Frontend Setup

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm start
```

The application will be available at `http://localhost:3000`

## API Endpoints

### Authentication

- `POST /register` - User registration
- `POST /login` - User login

### Resources

- `GET /resources` - Get all resources with filtering
- `POST /upload` - Upload new resource
- `GET /download/{resource_id}` - Download resource
- `POST /rate/{resource_id}` - Rate a resource

### Dashboard

- `GET /dashboard` - Get dashboard data

## Database Schema

### Users

- id, username, email, hashed_password, is_admin, created_at

### Resources

- id, title, description, filename, file_path, subject, semester, uploader_id, upload_date, download_count, average_rating

### Tags

- id, name

### Ratings

- id, resource_id, user_id, rating, feedback, created_at

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload Resources**: Share study materials with title, description, subject, and tags
3. **Browse Resources**: Filter by subject, semester, or search by keywords
4. **Download Materials**: Access resources uploaded by other students
5. **Rate Resources**: Provide ratings and feedback to help others find quality content
6. **Dashboard**: View top-rated and most popular resources

## Project Structure

```
├── main.py              # FastAPI application
├── database.py          # Database models and configuration
├── auth.py             # Authentication utilities
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies
├── src/
│   ├── App.js          # Main React component
│   ├── components/     # React components
│   └── App.css         # Styles
└── public/
    └── index.html      # HTML template
```
