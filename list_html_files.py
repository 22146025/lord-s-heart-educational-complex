#!/usr/bin/env python3
"""
Script to list all HTML files in the project
"""

import os
from pathlib import Path

def list_html_files():
    """List all HTML files in the project directory"""
    
    project_dir = Path(__file__).resolve().parent
    
    print("🔍 Searching for HTML files...")
    print(f"📁 Project directory: {project_dir}")
    print()
    
    html_files = []
    
    # Search for HTML files in the project directory
    for file_path in project_dir.rglob("*.html"):
        if file_path.is_file():
            # Get relative path from project directory
            relative_path = file_path.relative_to(project_dir)
            html_files.append(str(relative_path))
    
    if html_files:
        print("✅ Found HTML files:")
        for i, file_path in enumerate(sorted(html_files), 1):
            print(f"  {i}. {file_path}")
        
        print()
        print("🌐 URLs to access these files:")
        for file_path in sorted(html_files):
            # Remove .html extension for URL
            url_path = file_path.replace('.html', '')
            print(f"  • http://127.0.0.1:8000/{url_path}.html")
        
        print()
        print("📋 Quick test links:")
        for file_path in sorted(html_files):
            url_path = file_path.replace('.html', '')
            print(f"  <a href='/{url_path}.html'>{file_path}</a>")
            
    else:
        print("❌ No HTML files found in the project directory")
        print("Make sure your HTML files are in the root project directory")

if __name__ == "__main__":
    list_html_files()
