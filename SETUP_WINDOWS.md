# AI Mock Interview System - Windows Setup Guide

## Quick Setup (5 minutes)

### Step 1: Get Gemini API Key
1. Open browser and go to: https://makersuite.google.com/app/apikeys
2. Click "Create API Key"
3. Copy the generated API key
4. Keep it safe - you'll need it in Step 3

### Step 2: Open Command Prompt
1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to your project folder:
   ```
   cd "Desktop\New folder (3)"
   ```

### Step 3: Run Quick Start Script
```bash
quick_start.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Create .env file

### Step 4: Update .env File
1. Open `.env` file in Notepad
2. Replace `your_gemini_api_key_here` with your actual API key
3. Save and close

### Step 5: Start Application
In Command Prompt, run:
```bash
python app.py
```

You should see:
```
WARNING in flask.app: * Running on http://127.0.0.1:5000
```

### Step 6: Open in Browser
Visit: http://localhost:5000

---

## Manual Setup (if Quick Start fails)

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
```bash
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Wait for all packages to install (2-3 minutes).

### 4. Create .env File
```bash
copy .env.example .env
```

### 5. Edit .env File
- Open `.env` in Notepad
- Add your Gemini API key
- Save

### 6. Run Application
```bash
python app.py
```

### 7. Open Browser
Go to: http://localhost:5000

---

## Getting Gemini API Key (Detailed)

### Free Google AI Studio Approach
1. Visit: https://makersuite.google.com/app/apikeys
2. Sign in with your Google account (or create one)
3. Click "Create API Key"
4. Click "Create API key in new project"
5. System generates your API key automatically
6. Copy the key
7. Paste in .env file

**Note**: Free tier includes:
- 60 requests per minute
- Sufficient for testing and development
- No credit card required

---

## Troubleshooting

### Issue: "Python is not recognized"
**Problem**: Python not in system PATH

**Solution**:
1. Uninstall Python
2. Download from python.org
3. During installation, **check "Add Python to PATH"**
4. Reinstall and restart Command Prompt

### Issue: "ModuleNotFoundError: No module named 'google'"
**Problem**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "GEMINI_API_KEY not found"
**Problem**: .env file not created or API key not added

**Solution**:
1. Verify `.env` file exists in project folder
2. Open .env in Notepad
3. Check it has: `GEMINI_API_KEY=your_key_here`
4. Save and close
5. Restart Flask application

### Issue: "Port 5000 already in use"
**Problem**: Another application using port 5000

**Solution Option 1 - Stop other application**:
```bash
netstat -ano | findstr :5000
```

**Solution Option 2 - Use different port**:
Edit app.py, last line:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to 5001
```

### Issue: "Cannot find file resume"
**Problem**: Uploads folder permissions

**Solution**:
1. Create `uploads` folder manually if missing
2. Right-click folder → Properties
3. Security → Edit → Everyone → Full Control
4. Apply changes

### Issue: Voice input not working
**Problem**: Browser doesn't support Web Speech API

**Solution**: 
- Use Chrome, Firefox, or Edge (not Internet Explorer)
- Check microphone permissions
- Allow website to access microphone

---

## File Structure Verification

Check that you have these files:

```
Desktop/New folder (3)/
├── app.py                          ✓
├── requirements.txt                ✓
├── README.md                       ✓
├── .env.example                    ✓
├── .gitignore                      ✓
├── quick_start.bat                 ✓
│
├── services/
│   ├── __init__.py                 ✓
│   ├── gemini_service.py           ✓
│   ├── resume_parser.py            ✓
│   └── evaluator.py                ✓
│
├── templates/
│   ├── index.html                  ✓
│   ├── upload.html                 ✓
│   ├── domain.html                 ✓
│   ├── interview.html              ✓
│   └── result.html                 ✓
│
├── static/
│   ├── css/
│   │   └── style.css               ✓
│   └── js/
│       └── script.js               ✓
│
├── uploads/                        ✓
└── .env                            ✓ (create this)
```

---

## Testing the Application

### Test 1: Home Page
- URL: http://localhost:5000/
- Should see: "Welcome to AI Mock Interview System"
- Click: "Start Mock Interview"

### Test 2: Upload Resume
- Click: "Start Mock Interview"
- Upload a PDF, DOC, or DOCX file (max 5MB)
- Click: "Upload Resume"
- Should see: "Resume uploaded successfully ✓"

### Test 3: Domain Selection
- Should see 5 domain cards
- Click any domain
- Should see loading message: "Generating personalized interview questions..."

### Test 4: Interview Page
- Should see Question 1 of 10
- See progress bar
- See either MCQ options (Q1-5) or text area (Q6-10)
- Click "🔊 Listen" to hear question
- Try voice input (if using Chrome)

### Test 5: Submit and Results
- Answer all 10 questions
- Click "Submit Interview & Get Results"
- Should see results page with score

---

## Restarting the Application

If you need to restart:

1. Press `Ctrl + C` in Command Prompt (stops Flask)
2. Run again: `python app.py`
3. Refresh browser (or go to http://localhost:5000)

---

## Virtual Environment Notes

**Why use Virtual Environment?**
- Isolates project dependencies
- Prevents version conflicts
- Keeps your system Python clean

**To activate in future:**
```bash
cd "Desktop\New folder (3)"
venv\Scripts\activate
python app.py
```

**To deactivate:**
```bash
deactivate
```

---

## Running on Different Port

To run on port 8000 instead of 5000:

Edit `app.py`, last line:
```python
if __name__ == '__main__':
    app.run(debug=True, port=8000)
```

Then visit: http://localhost:8000

---

## Browser Support

| Feature | Chrome | Firefox | Edge | Safari |
|---------|--------|---------|------|--------|
| UI | ✅ | ✅ | ✅ | ✅ |
| Voice Input | ✅ | ✅ | ✅ | ⚠️ |
| Voice Output | ✅ | ✅ | ✅ | ✅ |
| File Upload | ✅ | ✅ | ✅ | ✅ |

**Recommended**: Chrome or Firefox for best experience

---

## Performance Tips

1. **Fast API responses**: Ensure internet connection is stable
2. **Faster question generation**: Use a detailed resume
3. **Better voice**: Speak clearly, use good microphone
4. **Smooth experience**: Close other tabs to free up browser memory

---

## Need More Help?

1. Check `README.md` for detailed documentation
2. Look at console errors: Right-click → Inspect → Console tab
3. Check Flask console for error messages
4. Verify .env file has correct API key
5. Try a different browser (Chrome recommended)

---

## Production Deployment

Never use `debug=True` in production!

For production deployment:
1. Change `FLASK_ENV=production`
2. Set `DEBUG=False` in app.py
3. Use a production WSGI server (Gunicorn)
4. Generate a strong SECRET_KEY
5. Use HTTPS

---

**Status**: Ready to Use ✅
**Version**: 1.0.0
