// Thousand Hills Vacations - Show Schedule Creator
// Frontend JavaScript

let currentFilename = null;

// Get DOM elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultSection = document.getElementById('resultSection');
const resultMessage = document.getElementById('resultMessage');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const previewBtn = document.getElementById('previewBtn');
const downloadBtn = document.getElementById('downloadBtn');
const newUploadBtn = document.getElementById('newUploadBtn');
const retryBtn = document.getElementById('retryBtn');

// File input change handler
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
});

// Drag and drop handlers
uploadBox.addEventListener('dragover', function(e) {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', function(e) {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', function(e) {
    e.preventDefault();
    uploadBox.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
        handleFileUpload(file);
    } else {
        showError('Please upload a PDF file.');
    }
});

// Handle file upload
async function handleFileUpload(file) {
    // Validate file type
    if (file.type !== 'application/pdf') {
        showError('Invalid file type. Please upload a PDF file.');
        return;
    }

    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showError('File is too large. Maximum size is 16MB.');
        return;
    }

    // Show progress
    hideAllSections();
    progressSection.style.display = 'block';
    progressText.textContent = 'Uploading and processing your PDF...';

    // Create form data
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Upload file
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            currentFilename = data.filename;
            showSuccess(data);
        } else {
            showError(data.error || 'An error occurred while processing the file.');
        }
    } catch (error) {
        showError('Network error. Please check your connection and try again.');
        console.error('Upload error:', error);
    }
}

// Show success section
function showSuccess(data) {
    hideAllSections();
    resultSection.style.display = 'block';
    resultMessage.textContent = `Your branded PDF is ready! (${data.schedule_items} schedule items processed)`;
}

// Show error section
function showError(message) {
    hideAllSections();
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

// Hide all sections
function hideAllSections() {
    uploadBox.style.display = 'none';
    progressSection.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// Reset to upload view
function resetToUpload() {
    hideAllSections();
    uploadBox.style.display = 'block';
    fileInput.value = '';
    currentFilename = null;
}

// Preview button handler
previewBtn.addEventListener('click', function() {
    if (currentFilename) {
        window.open(`/preview/${currentFilename}`, '_blank');
    }
});

// Download button handler
downloadBtn.addEventListener('click', function() {
    if (currentFilename) {
        window.location.href = `/download/${currentFilename}`;
    }
});

// New upload button handler
newUploadBtn.addEventListener('click', resetToUpload);

// Retry button handler
retryBtn.addEventListener('click', resetToUpload);

// Initialize
console.log('Thousand Hills Vacations - Show Schedule Creator loaded');
