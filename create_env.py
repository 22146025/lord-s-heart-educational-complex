#!/usr/bin/env python3
"""
Script to create a .env file for the Django project
"""

import os
import secrets

def create_env_file():
    """Create a .env file with development settings"""
    
    # Generate a secure secret key
    secret_key = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
    
    env_content = f"""# Django Settings
SECRET_KEY=django-insecure-{secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Email Settings (optional for development)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static and Media Files
STATIC_ROOT=staticfiles
MEDIA_ROOT=media

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:5000,http://127.0.0.1:5000

# Security Settings (for production)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 You can now edit the .env file to customize your settings.")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print("\n📋 Please create a .env file manually with this content:")
        print("=" * 50)
        print(env_content)
        print("=" * 50)
        return False

if __name__ == "__main__":
    print("🔧 Creating .env file for Django project...")
    create_env_file()
