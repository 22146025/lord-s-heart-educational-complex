# Frontend-Backend Connection Setup Guide

## Overview
This guide explains how to connect your HTML frontend to the Django backend API.

## What's Been Done

### 1. Backend API (Django)
- ✅ Complete Django REST API created
- ✅ Admissions endpoints: `/api/admissions/`
- ✅ Contact endpoints: `/api/contact/`
- ✅ User management endpoints: `/api/users/`
- ✅ CORS configured for frontend access
- ✅ Database models and validation ready

### 2. Frontend Integration (HTML + JavaScript)
- ✅ Created `api.js` for API communication
- ✅ Updated `admissions.html` to include API script
- ✅ Updated `contact.html` to include API script
- ✅ Form field mapping configured
- ✅ Success/error message handling added

## How to Run the Complete System

### Step 1: Start the Django Backend
```bash
# Navigate to your project directory
cd "copy LORD'S HEART EDUCATIONAL COMPLEX - Copy"

# Activate virtual environment (if you created one)
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Start the Django server
python manage.py runserver
```

### Step 2: Serve the Frontend
You have several options to serve your HTML files:

#### Option A: Using Python's built-in server
```bash
# In a new terminal, navigate to your project directory
cd "copy LORD'S HEART EDUCATIONAL COMPLEX - Copy"

# Start a simple HTTP server
python -m http.server 5500
```

#### Option B: Using Live Server (VS Code extension)
1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

#### Option C: Using Node.js http-server
```bash
# Install http-server globally
npm install -g http-server

# Serve the files
http-server -p 5500
```

### Step 3: Test the Connection

1. **Open your frontend**: Go to `http://localhost:5500` (or whatever port you're using)
2. **Test Admissions Form**: 
   - Go to the Admissions page
   - Fill out the form
   - Submit and check for success message
3. **Test Contact Form**:
   - Go to the Contact page
   - Fill out the form
   - Submit and check for success message

### Step 4: Check Admin Panel
1. Go to `http://localhost:8000/admin/`
2. Login with your superuser credentials
3. Check the "Admissions Management" and "Contact Management" sections
4. You should see submitted applications and messages

## API Endpoints Available

### Admissions API
- `POST /api/admissions/` - Submit new application
- `GET /api/admissions/` - List applications (public view)
- `GET /api/admissions/statistics/` - Get statistics (admin only)

### Contact API
- `POST /api/contact/` - Submit new message
- `GET /api/contact/` - List messages (admin only)
- `GET /api/contact/statistics/` - Get statistics (admin only)

### Users API
- `GET /api/users/` - List users (admin only)
- `POST /api/users/` - Create user (admin only)

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Make sure Django server is running on port 8000
   - Check that CORS settings are properly configured
   - Try using `CORS_ALLOW_ALL_ORIGINS = True` for development

2. **Form Not Submitting**
   - Check browser console for JavaScript errors
   - Verify that `api.js` is loaded in your HTML files
   - Ensure form field names match the expected API format

3. **API Connection Failed**
   - Verify Django server is running: `http://localhost:8000/api/`
   - Check that the API_BASE_URL in `api.js` is correct
   - Ensure no firewall is blocking the connection

4. **Database Issues**
   - Run migrations: `python manage.py migrate`
   - Check if database file exists: `db.sqlite3`
   - Create superuser if needed: `python manage.py createsuperuser`

### Debug Steps

1. **Check Django Server Logs**
   ```bash
   python manage.py runserver --verbosity=2
   ```

2. **Check Browser Console**
   - Open Developer Tools (F12)
   - Look for errors in Console tab
   - Check Network tab for failed requests

3. **Test API Directly**
   ```bash
   # Test admissions endpoint
   curl -X POST http://localhost:8000/api/admissions/ \
     -H "Content-Type: application/json" \
     -d '{"surname":"TEST","first_name":"John","date_of_birth":"2015-01-01","age":8,"gender":"male","place_of_birth":"Test","region_of_birth":"Test","home_town":"Test","region_of_home_town":"Test","postal_address":"Test","place_of_residence":"Test","father_contact":"123456789"}'
   ```

## Production Deployment

For production, you should:

1. **Security Settings**
   - Set `DEBUG = False`
   - Configure proper `SECRET_KEY`
   - Remove `CORS_ALLOW_ALL_ORIGINS = True`
   - Set specific `CORS_ALLOWED_ORIGINS`

2. **Database**
   - Use PostgreSQL instead of SQLite
   - Configure `DATABASE_URL` in environment variables

3. **Static Files**
   - Run `python manage.py collectstatic`
   - Configure proper static file serving

4. **Web Server**
   - Use Gunicorn or uWSGI
   - Configure Nginx or Apache as reverse proxy

## File Structure
```
copy LORD'S HEART EDUCATIONAL COMPLEX - Copy/
├── # Frontend Files
├── index.html
├── admissions.html          # ✅ Connected to API
├── contact.html            # ✅ Connected to API
├── api.js                  # ✅ API integration script
├── main.js
├── styles.css
├── images/
│
├── # Backend Files
├── school_management/       # Django project
├── admissions/             # Admissions app
├── contact/                # Contact app
├── users/                  # Users app
├── requirements.txt
├── manage.py
├── db.sqlite3             # Database (created after migration)
└── README.md
```

## Next Steps

1. **Test the complete system** using the steps above
2. **Customize the forms** as needed for your school
3. **Add more features** like file uploads, email notifications
4. **Deploy to production** when ready

The system is now fully connected! Your HTML forms will submit data to the Django backend, which will store it in the database and make it available in the admin panel.
