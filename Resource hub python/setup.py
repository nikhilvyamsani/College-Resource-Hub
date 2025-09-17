#!/usr/bin/env python3
"""
Setup script for College Resource Hub
"""

import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError:
        return False

def setup_backend():
    """Setup backend dependencies"""
    print("Setting up backend...")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install Python dependencies")
        return False
    
    print("Backend setup complete!")
    return True

def setup_frontend():
    """Setup frontend dependencies"""
    print("Setting up frontend...")
    
    # Install Node.js dependencies
    if not run_command("npm install"):
        print("Failed to install Node.js dependencies")
        return False
    
    print("Frontend setup complete!")
    return True

def create_database():
    """Create database tables"""
    print("Creating database tables...")
    
    try:
        from database import Base, engine
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Failed to create database tables: {e}")
        return False

def main():
    """Main setup function"""
    print("College Resource Hub Setup")
    print("=" * 30)
    
    # Setup backend
    if not setup_backend():
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        sys.exit(1)
    
    # Create database tables
    if not create_database():
        sys.exit(1)
    
    print("\nSetup complete!")
    print("\nTo start the application:")
    print("1. Backend: python main.py")
    print("2. Frontend: npm start")
    print("\nThe application will be available at:")
    print("- Backend API: http://localhost:8000")
    print("- Frontend: http://localhost:3000")

if __name__ == "__main__":
    main()