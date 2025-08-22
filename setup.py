#!/usr/bin/env python
"""
Setup script for LORD'S HEART EDUCATIONAL COMPLEX School Management System
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if not env_file.exists() and env_example.exists():
        print("\nCreating .env file from template...")
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✓ .env file created successfully")
            print("⚠️  Please edit .env file with your configuration before running the server")
            return True
        except Exception as e:
            print(f"✗ Failed to create .env file: {e}")
            return False
    elif env_file.exists():
        print("✓ .env file already exists")
        return True
    else:
        print("⚠️  No env.example file found, please create .env file manually")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("LORD'S HEART EDUCATIONAL COMPLEX - School Management System")
    print("Setup Script")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("✗ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create virtual environment if it doesn't exist
    venv_path = Path('venv')
    if not venv_path.exists():
        print("\nCreating virtual environment...")
        if not run_command('python -m venv venv', 'Creating virtual environment'):
            print("✗ Failed to create virtual environment")
            sys.exit(1)
    
    # Determine activation command based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
        python_cmd = 'venv\\Scripts\\python'
    else:  # Unix/Linux/Mac
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
        python_cmd = 'venv/bin/python'
    
    # Install requirements
    if not run_command(f'{pip_cmd} install -r requirements.txt', 'Installing dependencies'):
        print("✗ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Run migrations
    if not run_command(f'{python_cmd} manage.py makemigrations', 'Creating database migrations'):
        print("✗ Failed to create migrations")
        sys.exit(1)
    
    if not run_command(f'{python_cmd} manage.py migrate', 'Applying database migrations'):
        print("✗ Failed to apply migrations")
        sys.exit(1)
    
    # Create static and media directories
    for directory in ['static', 'media', 'logs']:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created {directory} directory")
    
    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the development server: python manage.py runserver")
    print("4. Access the admin interface at: http://localhost:8000/admin/")
    print("5. Access the API at: http://localhost:8000/api/")
    print("\nFor more information, see README.md")
    print("=" * 60)


if __name__ == '__main__':
    main()
