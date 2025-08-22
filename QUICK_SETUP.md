# Quick Setup Guide - Fix DEBUG Issue

## 🚨 The Problem
You're seeing Django debug error pages because `DEBUG = True` is set. This shows detailed error information which isn't safe for production.

## ✅ The Solution

### Step 1: Create Environment File
Run this command to create your `.env` file:
```bash
python create_env.py
```

### Step 2: Install Dependencies (if not done yet)
```bash
# Try the Windows-friendly version first
pip install -r requirements-windows.txt

# If that fails, install core packages only
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 django-filter==23.3 python-decouple==3.8 whitenoise==6.6.0
```

### Step 3: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin User
```bash
python manage.py createsuperuser
```

### Step 5: Start the Server
```bash
python manage.py runserver
```

## 🎯 What This Fixes

1. **DEBUG Setting**: Now uses environment variables properly
2. **Security**: DEBUG defaults to `False` for safety
3. **Environment**: Proper `.env` file with development settings
4. **Database**: SQLite database ready to use

## 🔍 Test Your Setup

After running the server, visit:
- **Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/
- **Frontend**: Open your HTML files in a browser

## 🛠️ If You Still See Errors

### Option 1: Manual .env Creation
If `create_env.py` doesn't work, create a `.env` file manually with:
```
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Option 2: Temporary Fix
If you need to test quickly, you can temporarily set DEBUG in settings.py:
```python
DEBUG = True  # Only for development!
```

## 🎉 Success Indicators
- ✅ No more debug error pages
- ✅ Django admin accessible at /admin/
- ✅ API endpoints working at /api/
- ✅ Forms submitting successfully

## 📞 Need Help?
If you're still having issues, share the exact error message and I'll help you troubleshoot!
