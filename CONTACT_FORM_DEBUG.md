# Contact Form Debug Guide

## 🚨 **The Problem**
Contact form submission is failing with "failed to send message" error.

## 🔍 **Debugging Steps**

### **Step 1: Test the API directly**
```bash
python test_contact_api.py
```

### **Step 2: Check browser console**
1. Open your browser's Developer Tools (F12)
2. Go to the Console tab
3. Try submitting the contact form
4. Look for any error messages

### **Step 3: Check Django server logs**
Look at your terminal where Django is running for any error messages.

### **Step 4: Verify the form is connected**
The contact form should have:
- `class="contact-form"`
- `id="contactForm"`
- Proper event listener from `api.js`

## 🔧 **Common Issues & Solutions**

### **Issue 1: CORS Error**
**Error**: `Access to fetch at 'http://127.0.0.1:8000/api/contact/' from origin 'http://127.0.0.1:8000' has been blocked by CORS policy`

**Solution**: CORS is already configured in settings.py

### **Issue 2: CSRF Token Error**
**Error**: `CSRF verification failed`

**Solution**: The API is configured to allow POST requests without CSRF for public forms

### **Issue 3: Form not submitting**
**Error**: No network request appears in browser

**Solution**: Check if `api.js` is loading and the form has the correct class

### **Issue 4: API endpoint not found**
**Error**: `404 Not Found`

**Solution**: Make sure Django server is running and the URL is correct

## 🧪 **Manual Testing**

### **Test 1: Check if API endpoint exists**
Visit: http://127.0.0.1:8000/api/contact/
You should see the API response.

### **Test 2: Test with curl**
```bash
curl -X POST http://127.0.0.1:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","message":"Test message"}'
```

### **Test 3: Check admin panel**
After successful submission, check the admin panel at http://127.0.0.1:8000/admin/ to see if the message was saved.

## 🎯 **Expected Behavior**

When the contact form works correctly:
1. ✅ Form submits without page reload
2. ✅ Success message appears
3. ✅ Form fields clear
4. ✅ Message appears in Django admin panel
5. ✅ No errors in browser console

## 📞 **If Still Having Issues**

1. **Check the exact error message** in browser console
2. **Verify Django server is running**
3. **Test the API directly** with the test script
4. **Check if all static files are loading** (CSS, JS)

Run `python test_contact_api.py` to verify the backend is working!
