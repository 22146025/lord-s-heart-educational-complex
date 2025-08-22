#!/usr/bin/env python3
"""
Test script to verify Django setup is working correctly
"""

import os
import sys
import django
from pathlib import Path

def test_django_setup():
    """Test if Django is properly configured"""
    
    print("🔧 Testing Django Setup...")
    
    # Add the project directory to Python path
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
    
    try:
        # Setup Django
        django.setup()
        print("✅ Django setup successful!")
        
        # Test imports
        from django.conf import settings
        print(f"✅ Settings loaded: {settings.DEBUG}")
        
        # Test database
        from django.db import connection
        connection.ensure_connection()
        print("✅ Database connection successful!")
        
        # Test apps
        from admissions.models import AdmissionApplication
        from contact.models import ContactMessage
        from users.models import UserProfile
        print("✅ All models imported successfully!")
        
        # Test URLs
        from django.urls import reverse
        print("✅ URL configuration working!")
        
        print("\n🎉 All tests passed! Your Django setup is working correctly.")
        print("\n📋 Next steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py createsuperuser")
        print("4. Run: python manage.py runserver")
        print("5. Visit: http://127.0.0.1:8000/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you've installed dependencies: pip install -r requirements-windows.txt")
        print("2. Make sure you have a .env file: python create_env.py")
        print("3. Check if all files are in the correct locations")
        return False

if __name__ == "__main__":
    test_django_setup()
