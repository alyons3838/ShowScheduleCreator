# Mac Setup Guide

## Step-by-Step Installation

### 1. Check Python Installation

First, verify Python is installed:

```bash
python3 --version
```

You should see Python 3.8 or higher. If not installed, install via:
- **Homebrew**: `brew install python3`
- **Official installer**: Download from https://www.python.org/downloads/

### 2. Navigate to Project Directory

```bash
cd /path/to/ShowScheduleCreator
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
```

If you get a "command not found" error, try:
```bash
/usr/bin/python3 -m venv venv
```

### 4. Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### 5. Upgrade pip (Recommended)

```bash
pip install --upgrade pip
```

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

**Common Issues:**
- If you get SSL errors, try: `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt`
- If you get permission errors, make sure your virtual environment is activated

### 7. Run the Application

```bash
python app.py
```

Or:
```bash
python3 app.py
```

### 8. Open in Browser

Navigate to: **http://127.0.0.1:5000**

## Troubleshooting

### Error: "Permission denied" when running run.sh

**Solution:**
```bash
chmod +x run.sh
./run.sh
```

### Error: "python3: command not found"

**Solution:**
Install Python 3:
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
```

### Error: "No module named 'flask'" or similar

**Solution:**
Make sure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Address already in use" or "Port 5000 is already allocated"

**Solution 1:** Kill the process using port 5000:
```bash
lsof -ti:5000 | xargs kill -9
```

**Solution 2:** Use a different port - edit `app.py` and change:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Changed from 5000 to 5001
```

### Virtual environment won't activate

**Solution:**
Try these alternatives:
```bash
# Option 1
. venv/bin/activate

# Option 2
source ./venv/bin/activate

# Option 3 (if using fish shell)
source venv/bin/activate.fish

# Option 4 (if using csh)
source venv/bin/activate.csh
```

### Can't install pdfplumber or reportlab

**Solution:**
Install system dependencies first:
```bash
# On Mac with Homebrew
brew install libxml2 libxslt

# Then try installing requirements again
pip install -r requirements.txt
```

### "zsh: no such file or directory" when running ./run.sh

**Solution:**
Make sure you're in the correct directory:
```bash
cd ShowScheduleCreator
ls -la run.sh  # Should show the file
chmod +x run.sh
./run.sh
```

## Manual Step-by-Step (If Scripts Don't Work)

1. **Open Terminal**

2. **Navigate to project:**
   ```bash
   cd /path/to/ShowScheduleCreator
   ```

3. **Create venv:**
   ```bash
   python3 -m venv venv
   ```

4. **Activate:**
   ```bash
   source venv/bin/activate
   ```

5. **Install:**
   ```bash
   pip install Flask==3.0.0
   pip install pdfplumber==0.11.0
   pip install reportlab==4.0.7
   pip install Pillow==10.1.0
   pip install Werkzeug==3.0.1
   ```

6. **Run:**
   ```bash
   python app.py
   ```

7. **Open browser to:** http://127.0.0.1:5000

## Still Having Issues?

Please provide:
1. The exact error message you're seeing
2. Output of: `python3 --version`
3. Output of: `which python3`
4. Your macOS version: `sw_vers`

This will help diagnose the specific issue.
