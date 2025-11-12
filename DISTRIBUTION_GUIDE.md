# Distribution Guide - For IT/Admin

This guide explains how to build and distribute the Show Schedule Creator to your sales reps as a standalone application.

## Overview

Instead of requiring reps to install Python and run Terminal commands, we package everything into a single application file:

- **Mac**: `.app` bundle (like any Mac application)
- **Windows**: `.exe` executable (double-click to run)

## Building the Application

### For Mac

**One-time setup:**
```bash
cd ShowScheduleCreator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Build the app:**
```bash
./build_mac_app.sh
```

This creates: `dist/ThousandHillsScheduleCreator.app`

### For Windows

**One-time setup:**
```cmd
cd ShowScheduleCreator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Build the exe:**
```cmd
build_windows_exe.bat
```

This creates: `dist\ThousandHillsScheduleCreator.exe`

## Distributing to Sales Reps

### Option 1: USB Drive
1. Copy the `.app` or `.exe` file to a USB drive
2. Give to each rep with instructions below

### Option 2: Email/Cloud Storage
1. Zip the application file
2. Upload to Google Drive, Dropbox, etc.
3. Send download link with instructions

### Option 3: Network Share
1. Place the application on a shared network drive
2. Reps can copy it from there

## User Instructions

### For Mac Users

**Installation:**
1. Copy `ThousandHillsScheduleCreator.app` to your Applications folder (or anywhere)
2. Right-click the app and select "Open" (first time only)
3. Click "Open" when macOS asks for confirmation

**Using the app:**
1. Double-click the app icon
2. Your browser will open automatically
3. Drag and drop your PDF or click "Choose File"
4. Download your branded PDF

**Notes:**
- The app needs to be "opened" with right-click the first time due to macOS security
- After the first time, regular double-click will work
- The app stays running until you close the window

### For Windows Users

**Installation:**
1. Copy `ThousandHillsScheduleCreator.exe` anywhere on your computer
2. Double-click to run
3. If Windows shows a security warning, click "More info" then "Run anyway" (first time only)

**Using the app:**
1. Double-click the exe file
2. Your browser will open automatically
3. Drag and drop your PDF or click "Choose File"
4. Download your branded PDF

**Notes:**
- Windows Defender may scan the file first time
- The exe can be run from Desktop, Documents, or anywhere
- The app stays running until you close the command window

## Troubleshooting Distribution Issues

### Mac: "App is damaged and can't be opened"

This happens when the file was downloaded from the internet. Fix:

```bash
# Remove quarantine flag
xattr -cr /path/to/ThousandHillsScheduleCreator.app
```

Or distribute with this instruction for users:
```bash
xattr -cr ~/Downloads/ThousandHillsScheduleCreator.app
```

### Mac: "App can't be opened because Apple cannot check it for malicious software"

**For users:**
1. Right-click (or Control-click) the app
2. Click "Open"
3. Click "Open" in the dialog

**For IT:** Code sign the app with an Apple Developer certificate to avoid this.

### Windows: "Windows protected your PC"

**For users:**
1. Click "More info"
2. Click "Run anyway"

**For IT:** Code sign the exe with a Windows code signing certificate to avoid this.

### Build Fails

**Common issues:**

1. **"No module named 'pyinstaller'"**
   - Solution: `pip install pyinstaller`

2. **"templates not found"**
   - Solution: Make sure you're in the ShowScheduleCreator directory when building

3. **Build succeeds but app crashes**
   - Solution: Check that all dependencies are in requirements.txt
   - Try: `pip install -r requirements.txt --upgrade`

## Code Signing (Optional but Recommended)

To avoid security warnings:

### Mac Code Signing
Requires Apple Developer account ($99/year):
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" \
  dist/ThousandHillsScheduleCreator.app
```

### Windows Code Signing
Requires Windows code signing certificate:
```cmd
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com \
  dist\ThousandHillsScheduleCreator.exe
```

## Updates

When you update the code:

1. Pull latest changes from git
2. Run the build script again
3. Distribute the new version to reps
4. Reps simply replace the old file with the new one

## File Sizes

- **Mac .app**: ~50-80 MB (includes Python runtime)
- **Windows .exe**: ~40-70 MB (includes Python runtime)

These are one-file bundles with everything needed to run.

## Security Notes

- The application runs a local web server (port 5000)
- Only accessible from the user's own computer (127.0.0.1)
- No external network access required
- PDFs are processed locally, not uploaded to any server
- Temporary files are cleaned up automatically

## Support

If reps have issues:

1. **Check their Python/system versions** (though shouldn't matter with bundled app)
2. **Antivirus interference**: Some aggressive antivirus may block the app
3. **Permissions**: Make sure they can write to the folder where app is located
4. **Port conflicts**: If port 5000 is in use, app won't start (rare)

For port conflicts, rebuild with a different port in `launcher.py`:
```python
app.run(debug=False, host='127.0.0.1', port=5001)  # Changed from 5000
```

## Alternative: Web-Hosted Version

If distributing standalone apps is problematic, consider:

1. Deploy to a web server (AWS, Heroku, etc.)
2. Reps just visit a URL - no installation needed
3. Requires ongoing hosting costs
4. Need to secure with authentication

See `DEPLOYMENT.md` for web hosting options (to be created if needed).
