# Static Files Fix Guide

## 🎯 **The Problem**
Your CSS and images aren't loading because Django needs to serve static files through its static file system.

## ✅ **The Solution**

### **Step 1: Set up static files**
Run this command to move your files to the static directory:
```bash
python setup_static_files.py
```

### **Step 2: Restart Django server**
```bash
python manage.py runserver
```

### **Step 3: Test your pages**
Visit your pages again - CSS and images should now load!

## 🔧 **What the fix does:**

1. **Moves files to static directory**:
   - `styles.css` → `static/styles.css`
   - `main.js` → `static/main.js`
   - `api.js` → `static/api.js`
   - `images/` → `static/images/`

2. **Updates HTML references**:
   - `href="styles.css"` → `href="/static/styles.css"`
   - `src="images/..."` → `src="/static/images/..."`

3. **Django serves static files**:
   - CSS: http://127.0.0.1:8000/static/styles.css
   - Images: http://127.0.0.1:8000/static/images/filename.jpg
   - JS: http://127.0.0.1:8000/static/main.js

## 🎉 **Expected Results:**

After running the fix:
- ✅ CSS styles will load properly
- ✅ Images will display correctly
- ✅ JavaScript will work
- ✅ All pages will look as intended

## 🚨 **If you still have issues:**

1. **Check the static directory**:
   ```bash
   ls static/
   ```

2. **Verify file paths**:
   - CSS should be at: `static/styles.css`
   - Images should be at: `static/images/`
   - JS should be at: `static/main.js`

3. **Check browser console** for any remaining 404 errors

## 📁 **File Structure After Fix:**

```
your-project/
├── static/
│   ├── styles.css
│   ├── main.js
│   ├── api.js
│   └── images/
│       ├── image1.jpg
│       ├── image2.jpg
│       └── ...
├── index.html
├── admissions.html
├── contact.html
└── ...
```

Run `python setup_static_files.py` and your styling should work perfectly!
