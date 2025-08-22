# Installation Troubleshooting Guide

## Quick Fix Options

### Option 1: Try the Windows-friendly requirements (Recommended)
```bash
pip install -r requirements-windows.txt
```

### Option 2: Install packages one by one
```bash
pip install Django==4.2.7
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install django-filter==23.3
pip install Pillow==10.1.0
pip install python-decouple==3.8
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0
```

### Option 3: Skip problematic packages temporarily
```bash
# Install everything except psycopg2-binary
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 django-filter==23.3 Pillow==10.1.0 python-decouple==3.8 gunicorn==21.2.0 whitenoise==6.6.0
```

## Common Issues and Solutions

### Issue 1: psycopg2-binary build failure
**Error**: `Microsoft Visual C++ 14.0 or greater is required`

**Solutions**:
1. **Skip for now** (use SQLite instead):
   ```bash
   pip install -r requirements-windows.txt
   ```

2. **Install Visual C++ Build Tools**:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "C++ build tools" workload

3. **Use pre-compiled wheel**:
   ```bash
   pip install --only-binary=all psycopg2-binary==2.9.9
   ```

### Issue 2: Pillow installation problems
**Error**: `The headers or library files could not be found`

**Solutions**:
1. **Install system dependencies** (Windows):
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

2. **Use pre-compiled version**:
   ```bash
   pip install --only-binary=all Pillow==10.1.0
   ```

### Issue 3: General build failures
**Error**: `setup.py or pyproject.toml issues`

**Solutions**:
1. **Update pip and setuptools**:
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Clear pip cache**:
   ```bash
   pip cache purge
   ```

3. **Use isolated installation**:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

## Step-by-Step Installation Process

### Step 1: Prepare your environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel
```

### Step 2: Try installation methods in order

**Method 1**: Windows-friendly requirements
```bash
pip install -r requirements-windows.txt
```

**Method 2**: If Method 1 fails, install core packages only
```bash
pip install Django==4.2.7
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install django-filter==23.3
pip install python-decouple==3.8
pip install whitenoise==6.6.0
```

**Method 3**: If you need PostgreSQL later
```bash
# Install PostgreSQL driver separately
pip install psycopg2-binary==2.9.9 --no-binary :all:
```

### Step 3: Verify installation
```bash
# Check if Django is installed
python -c "import django; print(django.get_version())"

# Check if DRF is installed
python -c "import rest_framework; print(rest_framework.VERSION)"
```

## Database Configuration

### For Development (SQLite - Recommended)
The project is already configured to use SQLite by default. No additional setup needed.

### For Production (PostgreSQL)
If you need PostgreSQL later:

1. **Install PostgreSQL server** on your system
2. **Install psycopg2-binary**:
   ```bash
   pip install psycopg2-binary==2.9.9
   ```
3. **Update settings.py** to use PostgreSQL:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## Next Steps After Installation

Once installation is successful:

1. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Start the server**:
   ```bash
   python manage.py runserver
   ```

4. **Test the API**:
   - Go to: http://localhost:8000/api/
   - Go to: http://localhost:8000/admin/

## Still Having Issues?

If you're still experiencing problems:

1. **Check your Python version**:
   ```bash
   python --version
   ```
   (Python 3.8+ is recommended)

2. **Check your pip version**:
   ```bash
   pip --version
   ```

3. **Try using conda instead**:
   ```bash
   conda create -n school-management python=3.11
   conda activate school-management
   conda install django djangorestframework
   pip install -r requirements-windows.txt
   ```

4. **Share the exact error message** so I can provide more specific help.

## Success Indicators

You'll know everything is working when:
- ✅ All packages install without errors
- ✅ `python manage.py runserver` starts successfully
- ✅ You can access http://localhost:8000/admin/
- ✅ You can access http://localhost:8000/api/
