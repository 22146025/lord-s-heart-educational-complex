"""
Views for the school_management project.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os

def homepage(request):
    """Serve the main homepage (index.html)"""
    try:
        with open(os.path.join(settings.BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix static file references for Django
        content = content.replace('href="styles.css"', 'href="/static/styles.css"')
        content = content.replace('src="images/', 'src="/static/images/')
        content = content.replace('src="styles.css"', 'src="/static/styles.css"')
        content = content.replace('src="main.js"', 'src="/static/main.js"')
        content = content.replace('src="api.js"', 'src="/static/api.js"')
        
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("""
        <html>
        <head>
            <title>LORD'S HEART EDUCATIONAL COMPLEX</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; text-align: center; }
                .nav { margin: 30px 0; }
                .nav a { display: inline-block; margin: 10px; padding: 12px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }
                .nav a:hover { background: #2980b9; }
                .status { background: #27ae60; color: white; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎓 LORD'S HEART EDUCATIONAL COMPLEX</h1>
                <div class="status">
                    ✅ School Management System Backend is running successfully!
                </div>
                <div class="nav">
                    <a href="/admin/">🔧 Admin Panel</a>
                    <a href="/api/">📡 API Endpoints</a>
                    <a href="/admissions.html">📝 Admissions Page</a>
                    <a href="/contact.html">📧 Contact Page</a>
                    <a href="/about.html">ℹ️ About Page</a>
                    <a href="/academics.html">📚 Academics Page</a>
                    <a href="/gallery.html">🖼️ Gallery Page</a>
                    <a href="/news.html">📰 News Page</a>
                </div>
                <p><strong>Backend Features:</strong></p>
                <ul>
                    <li>✅ Django REST API for admissions and contact forms</li>
                    <li>✅ User management and authentication</li>
                    <li>✅ Admin panel for data management</li>
                    <li>✅ Database with SQLite (ready for PostgreSQL)</li>
                    <li>✅ CORS configured for frontend integration</li>
                </ul>
            </div>
        </body>
        </html>
        """, content_type='text/html')

def serve_html(request, filename):
    """Serve HTML files from the root directory"""
    try:
        # Add .html extension if not present
        if not filename.endswith('.html'):
            filename = filename + '.html'
        
        file_path = os.path.join(settings.BASE_DIR, filename)
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix static file references for Django
            content = content.replace('href="styles.css"', 'href="/static/styles.css"')
            content = content.replace('src="images/', 'src="/static/images/')
            content = content.replace('src="styles.css"', 'src="/static/styles.css"')
            content = content.replace('src="main.js"', 'src="/static/main.js"')
            content = content.replace('src="api.js"', 'src="/static/api.js"')
            
            return HttpResponse(content, content_type='text/html')
        else:
            # Get list of available HTML files
            available_files = [f for f in os.listdir(settings.BASE_DIR) if f.endswith('.html')]
            
            return HttpResponse(f"""
            <html>
            <head>
                <title>File Not Found</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                    .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .error {{ background: #e74c3c; color: white; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .files {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .files a {{ color: #3498db; text-decoration: none; }}
                    .files a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔍 File Not Found</h1>
                    <div class="error">
                        The file <strong>{filename}</strong> was not found at: <code>{file_path}</code>
                    </div>
                    
                    <h2>📁 Available HTML files in your project:</h2>
                    <div class="files">
                        {chr(10).join([f'<p><a href="/{f}">📄 {f}</a></p>' for f in sorted(available_files)]) if available_files else '<p>No HTML files found in the project directory.</p>'}
                    </div>
                    
                    <p><a href="/">← Back to Homepage</a></p>
                </div>
            </body>
            </html>
            """, status=404)
    except Exception as e:
        return HttpResponse(f"""
        <html>
        <head><title>Error</title></head>
        <body>
            <h1>Error serving file</h1>
            <p>Error: {str(e)}</p>
            <p><a href="/">← Back to Homepage</a></p>
        </body>
        </html>
        """, status=500)
