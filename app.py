"""
Thousand Hills Vacations - Show Schedule Creator
Main Flask Application
"""
from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from pdf_parser import ShowScheduleParser
from pdf_generator import BrandedPDFGenerator
from config import UPLOAD_FOLDER, DOWNLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thousand-hills-vacations-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process PDF"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_{filename}")
        file.save(upload_path)

        # Parse the PDF
        parser = ShowScheduleParser(upload_path)
        schedule_data = parser.parse_schedule()
        metadata = parser.get_metadata()

        # Generate branded PDF
        output_filename = f"branded_{timestamp}_{filename}"
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)

        generator = BrandedPDFGenerator(output_path)
        generator.generate_schedule(schedule_data, metadata)

        # Clean up uploaded file
        os.remove(upload_path)

        return jsonify({
            'success': True,
            'filename': output_filename,
            'message': 'PDF successfully branded!',
            'schedule_items': len(schedule_data)
        })

    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download the generated PDF"""
    try:
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/preview/<filename>')
def preview_file(filename):
    """Preview the generated PDF in browser"""
    try:
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='application/pdf')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'app': 'Thousand Hills Show Schedule Creator'})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Thousand Hills Vacations - Show Schedule Creator")
    print("="*60)
    print("\nServer starting at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
