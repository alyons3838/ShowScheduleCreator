"""
Configuration file for Thousand Hills Vacations Brand Guide
"""

# Brand Colors (from brand guide)
BRAND_COLORS = {
    'primary_red': '#C31D1D',
    'highlight_yellow': '#F7C500',
    'golf_green': '#006633',
    'charcoal_black': '#2B2B2B',
    'white': '#FFFFFF',
    'gray': '#D9D9D9'
}

# RGB values for ReportLab (normalized to 0-1)
BRAND_COLORS_RGB = {
    'primary_red': (195/255, 29/255, 29/255),
    'highlight_yellow': (247/255, 197/255, 0/255),
    'golf_green': (0/255, 102/255, 51/255),
    'charcoal_black': (43/255, 43/255, 43/255),
    'white': (1, 1, 1),
    'gray': (217/255, 217/255, 217/255)
}

# Typography
PRIMARY_FONT = 'Helvetica'  # ReportLab built-in, similar to Arial/Helvetica Neue
PRIMARY_FONT_BOLD = 'Helvetica-Bold'
ACCENT_FONT = 'Times-Roman'  # Similar to Georgia/Playfair Display

# Brand messaging
BRAND_TAGLINE = "Your home in the heart of Branson."
BRAND_NAME = "Thousand Hills Vacations"

# App Configuration
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'pdf'}
