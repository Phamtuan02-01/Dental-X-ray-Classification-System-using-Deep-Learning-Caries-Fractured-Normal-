// Dental AI System - JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('preview');
    const previewImage = document.getElementById('previewImage');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');

    if (uploadArea && fileInput) {
        // Click to upload - prevent double trigger
        uploadArea.addEventListener('click', function(e) {
            // Chỉ trigger khi click vào area, không phải input
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });

        // File selection
        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files);
            }
        });

        // Drag and drop
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.stopPropagation();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            e.stopPropagation();
            uploadArea.classList.remove('drag-over');
        });

        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
            uploadArea.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelect(files);
            }
        });
    }

    // Form submission with loading state
    if (uploadForm && submitBtn) {
        uploadForm.addEventListener('submit', function(e) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="btn-icon">⏳</span> Đang phân tích...';
            submitBtn.style.opacity = '0.7';
        });
    }

    // Handle file selection and preview
    function handleFileSelect(files) {
        if (files.length === 0) return;

        const file = files[0];
        
        // Validate file type
        const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            alert('Vui lòng chọn file ảnh (PNG, JPG, JPEG)');
            resetForm();
            return;
        }

        // Validate file size (16MB)
        const maxSize = 16 * 1024 * 1024;
        if (file.size > maxSize) {
            alert('Kích thước file không được vượt quá 16MB');
            resetForm();
            return;
        }

        // Show preview with smooth animation
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            uploadArea.style.display = 'none';
            previewArea.style.display = 'block';
            
            // Smooth fade-in animation
            previewArea.style.opacity = '0';
            setTimeout(function() {
                previewArea.style.transition = 'opacity 0.3s';
                previewArea.style.opacity = '1';
            }, 10);
            
            // Enable submit button
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.classList.add('pulse-animation');
            }
        };
        reader.readAsDataURL(file);
    }
});

// Reset form function
function resetForm() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('preview');
    
    if (fileInput) {
        fileInput.value = '';
    }
    
    if (uploadArea) {
        uploadArea.style.display = 'block';
    }
    
    if (previewArea) {
        previewArea.style.display = 'none';
    }
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });
});

// Animate probability bars on result page
document.addEventListener('DOMContentLoaded', function() {
    const probBars = document.querySelectorAll('.prob-bar');
    if (probBars.length > 0) {
        setTimeout(function() {
            probBars.forEach(function(bar) {
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(function() {
                    bar.style.width = width;
                }, 100);
            });
        }, 300);
    }
});
