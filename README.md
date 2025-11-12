# Thousand Hills Vacations - Show Schedule Creator

Transform bland show schedule PDFs into beautifully branded documents with Thousand Hills Vacations styling.

## For End Users (Sales Reps)

**Looking to use the app?** See [USER_GUIDE.md](USER_GUIDE.md) for simple instructions.

**Getting the app:**
- Ask your IT department for the application file
- Mac: `ThousandHillsScheduleCreator.app`
- Windows: `ThousandHillsScheduleCreator.exe`
- Just double-click to run - no installation needed!

## For IT/Administrators

**Need to build and distribute the app?** See [DISTRIBUTION_GUIDE.md](DISTRIBUTION_GUIDE.md) for complete instructions on creating standalone applications for your team.

**Quick build:**
- Mac: `./build_mac_app.sh`
- Windows: `build_windows_exe.bat`

---

## Features

- **PDF Upload**: Simple drag-and-drop or file selection interface
- **Automatic Parsing**: Extracts schedule data from plain PDFs
- **Brand Styling**: Applies Thousand Hills Vacations brand guidelines:
  - Official brand colors (Primary Red, Highlight Yellow, Golf Green)
  - Professional typography
  - Branded headers and footers
  - Decorative accent bars
- **PDF Generation**: Creates polished, professional show schedules
- **Preview & Download**: View and download your branded PDFs

## Brand Guidelines

This application follows the official Thousand Hills Vacations brand guide:

- **Colors**: Primary Red (#C31D1D), Highlight Yellow (#F7C500), Golf Green (#006633)
- **Typography**: Montserrat-style fonts (Helvetica family)
- **Tone**: Warm, approachable, and professional
- **Messaging**: "Your home in the heart of Branson."

## Requirements

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd ShowScheduleCreator
```

### 2. Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

1. Open a terminal in the project directory

2. Activate your virtual environment (if using one):
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

5. Upload your show schedule PDF and download the branded version!

### Using the Application

1. **Upload**: Drag and drop your PDF or click "Choose File"
2. **Process**: The app will automatically parse and brand your schedule
3. **Preview**: Click "Preview" to view in your browser
4. **Download**: Click "Download PDF" to save the branded version

## Project Structure

```
ShowScheduleCreator/
├── app.py                 # Main Flask application
├── config.py             # Brand configuration and settings
├── pdf_parser.py         # PDF text extraction and parsing
├── pdf_generator.py      # Branded PDF generation
├── requirements.txt      # Python dependencies
├── static/
│   ├── styles.css       # Brand-styled CSS
│   └── script.js        # Frontend JavaScript
├── templates/
│   └── index.html       # Main web interface
├── uploads/             # Temporary upload storage
└── downloads/           # Generated PDFs
```

## Customization

### Modifying Brand Colors

Edit `config.py` to adjust brand colors:

```python
BRAND_COLORS = {
    'primary_red': '#C31D1D',
    'highlight_yellow': '#F7C500',
    'golf_green': '#006633',
    # ...
}
```

### Adjusting PDF Layout

Modify `pdf_generator.py` to change:
- Table styling
- Header/footer content
- Font sizes
- Decorative elements

### Customizing the Parser

If your PDFs have a specific format, adjust the parsing logic in `pdf_parser.py`:
- Time patterns
- Show name extraction
- Detail parsing

## Technical Details

### PDF Processing

- **Parsing**: Uses `pdfplumber` to extract text from uploaded PDFs
- **Pattern Matching**: Identifies time-based schedules and show information
- **Flexible Parser**: Adapts to different schedule formats

### PDF Generation

- **Library**: ReportLab for PDF creation
- **Styling**: Custom paragraph styles and table formatting
- **Branding**: Automatic application of brand colors and elements

### Web Interface

- **Backend**: Flask web framework
- **Frontend**: Vanilla JavaScript (no frameworks required)
- **File Handling**: Secure upload/download with size limits

## Troubleshooting

### "Module not found" errors
- Make sure you've activated your virtual environment
- Run `pip install -r requirements.txt` again

### "Port already in use"
- Change the port in `app.py`: `app.run(port=5001)`

### Upload fails
- Check file size (max 16MB)
- Ensure file is a valid PDF
- Check upload/download folders have write permissions

### PDF parsing issues
- The parser expects structured schedule data
- Check `pdf_parser.py` and adjust patterns for your specific PDF format

## Security Notes

For production use:
- Change the `SECRET_KEY` in `app.py`
- Implement user authentication if needed
- Add rate limiting for uploads
- Use HTTPS
- Configure proper file cleanup

## License

Copyright © 2024 Thousand Hills Vacations. All rights reserved.

## Support

For issues or questions, contact your IT department or the application administrator.

---

**Thousand Hills Vacations**
*Your home in the heart of Branson.*
