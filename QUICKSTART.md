# 🚀 Quick Start Guide

Get your Arabic Novel Parser up and running in 5 minutes!

## Option 1: Windows Users (Easiest)

1. **Double-click** `setup.bat`
2. Wait for setup to complete
3. In the terminal that appears, type:
   ```
   streamlit run app.py
   ```
4. Your browser will open automatically to the app

## Option 2: macOS/Linux Users

1. Open terminal in this folder
2. Run:
   ```bash
   bash setup.sh
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Start the app:
   ```bash
   streamlit run app.py
   ```

## Option 3: Manual Setup

If the automated scripts don't work, follow these steps:

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
streamlit run app.py
```

## 🧪 Test Your Setup

Before uploading your own files, try the included test file:

1. Click "Choose a TXT file"
2. Select `example_input.txt`
3. Click "Process File"
4. You should see 5 chapters detected

If this works, your setup is complete! ✅

## 📝 Prepare Your File

Make sure your file:
- Is in `.txt` format
- Uses **UTF-8 encoding** (important for Arabic text)
- Follows this format:

```
**الفصل 1: Chapter Title Here**
Content of the chapter...

**الفصل 2: Another Title**
More content...
```

## ⚠️ Common Issues

**"Command not recognized"** → Make sure Python is installed
**"File encoding error"** → Convert your file to UTF-8 (use VS Code or Notepad++)
**"Streamlit not found"** → Ensure venv is activated

## 📖 Full Documentation

See `README.md` for complete documentation, troubleshooting, and deployment instructions.

---

**Ready to get started?** Pick your option above and start parsing! 🎉
