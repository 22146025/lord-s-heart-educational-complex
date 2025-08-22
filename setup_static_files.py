#!/usr/bin/env python3
"""
Script to set up static files for Django
"""

import os
import shutil
from pathlib import Path

def setup_static_files():
    """Set up static files for Django"""
    
    project_dir = Path(__file__).resolve().parent
    static_dir = project_dir / 'static'
    
    print("🔧 Setting up static files for Django...")
    
    # Create static directory if it doesn't exist
    static_dir.mkdir(exist_ok=True)
    
    # Files to move to static directory
    static_files = [
        'styles.css',
        'main.js',
        'api.js'
    ]
    
    # Move CSS and JS files
    for file_name in static_files:
        source_path = project_dir / file_name
        dest_path = static_dir / file_name
        
        if source_path.exists():
            shutil.copy2(source_path, dest_path)
            print(f"✅ Moved {file_name} to static directory")
        else:
            print(f"⚠️  {file_name} not found in project root")
    
    # Handle images directory
    images_source = project_dir / 'images'
    images_dest = static_dir / 'images'
    
    if images_source.exists():
        if images_dest.exists():
            shutil.rmtree(images_dest)
        shutil.copytree(images_source, images_dest)
        print("✅ Moved images directory to static directory")
    else:
        print("⚠️  images directory not found in project root")
    
    print("\n🎉 Static files setup complete!")
    print("📁 Your static files are now in the 'static' directory")
    print("🌐 Django will serve them from /static/ URLs")
    
    # List what's in static directory
    print("\n📋 Static directory contents:")
    for item in static_dir.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(static_dir)
            print(f"  📄 {relative_path}")

if __name__ == "__main__":
    setup_static_files()
