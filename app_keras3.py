"""
Flask Web Application - Nhận diện bệnh răng từ X-quang
Sử dụng Ensemble Model với CBAM + Focal Loss (Keras 3)
"""
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'

import numpy as np
import shutil
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import keras
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input
from focal_loss import SparseCategoricalFocalLoss
from custom_layers_keras3 import (KerasMean, KerasMax, channel_attention_module,
                                   spatial_attention_module, cbam_block)
from image_analyzer import analyze_image_features, classify_severity_level, is_dental_xray
from medical_advice import get_medical_advice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Định nghĩa các lớp bệnh
CLASS_NAMES = ['Caries', 'Fractured', 'Normal']
CLASS_NAMES_VN = {
    'Caries': 'Sâu răng',
    'Fractured': 'Gãy răng',
    'Normal': 'Bình thường'
}

# Đường dẫn models
MODEL_DIR = 'models'
MODEL_VERSIONS = ['v1', 'v2', 'v3', 'v4']

# Biến global để lưu models
loaded_models = []
resnet50_model = None


def allowed_file(filename):
    """Kiểm tra định dạng file được phép"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def load_resnet50_model():
    """Load ResNet50 model"""
    global resnet50_model
    
    if resnet50_model:
        return resnet50_model
    
    model_path = os.path.join(MODEL_DIR, 'best_resnet50.h5')
    model_path = os.path.join(os.path.dirname(__file__), model_path)
    model_path = os.path.normpath(model_path)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Không tìm thấy model ResNet50 tại: {model_path}")
    
    try:
        # Workaround cho Unicode path
        import tempfile
        import shutil
        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        shutil.copy2(model_path, temp_path)
        
        # Load model - ResNet50 thường không cần custom objects
        model = keras.models.load_model(temp_path, compile=False)
        
        os.unlink(temp_path)
        
        # Compile lại
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        resnet50_model = model
        print("✓ Loaded ResNet50 model")
        return model
    
    except Exception as e:
        raise RuntimeError(f"Lỗi khi load ResNet50 model: {str(e)}")


def load_ensemble_models():
    """Load tất cả models cho ensemble"""
    global loaded_models
    
    if loaded_models:
        return loaded_models
    
    custom_objects = {
        'SparseCategoricalFocalLoss': SparseCategoricalFocalLoss,
        'Mean': KerasMean,
        'Max': KerasMax,
        'channel_attention_module': channel_attention_module,
        'spatial_attention_module': spatial_attention_module,
        'cbam_block': cbam_block
    }
    
    models = []
    for version in MODEL_VERSIONS:
        model_path = os.path.join(MODEL_DIR, f'best_teeth_cbam_focal_{version}.h5')
        model_path = os.path.join(os.path.dirname(__file__), model_path)
        model_path = os.path.normpath(model_path)
        
        if os.path.exists(model_path):
            try:
                # Workaround cho Unicode path
                import tempfile
                import shutil
                with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp_file:
                    temp_path = tmp_file.name
                
                shutil.copy2(model_path, temp_path)
                
                # Load model với Keras 3
                with keras.utils.custom_object_scope(custom_objects):
                    model = keras.models.load_model(temp_path, compile=False)
                
                os.unlink(temp_path)
                
                # Compile lại
                model.compile(
                    optimizer='adam',
                    loss=SparseCategoricalFocalLoss(gamma=2),
                    metrics=['accuracy']
                )
                models.append(model)
                print(f"✓ Loaded model: {version}")
            except Exception as e:
                print(f"✗ Error loading {version}: {str(e)}")
        else:
            print(f"⚠ Model not found: {model_path}")
    
    if not models:
        raise RuntimeError("Không tìm thấy model nào! Vui lòng đặt file .h5 vào thư mục models/")
    
    loaded_models = models
    print(f"\n✅ Đã load {len(models)} models cho ensemble")
    return models


def predict_with_resnet50(img_path):
    """
    Dự đoán ảnh sử dụng ResNet50 model
    """
    model = load_resnet50_model()
    
    # Load và preprocess ảnh
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    # Prediction
    probs = model.predict(img_array, verbose=0)
    
    # Lấy kết quả
    predicted_class_idx = np.argmax(probs[0])
    predicted_class = CLASS_NAMES[predicted_class_idx]
    confidence = probs[0][predicted_class_idx] * 100
    
    # Tạo dict xác suất cho tất cả các class
    probabilities = {
        CLASS_NAMES_VN[cls]: float(probs[0][idx] * 100)
        for idx, cls in enumerate(CLASS_NAMES)
    }
    
    return {
        'class': predicted_class,
        'class_vn': CLASS_NAMES_VN[predicted_class],
        'confidence': float(confidence),
        'probabilities': probabilities
    }


def predict_image(img_path):
    """
    Dự đoán ảnh sử dụng ensemble model
    """
    models = load_ensemble_models()
    
    # Load và preprocess ảnh
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    # Ensemble prediction
    ensemble_probs = np.zeros((1, len(CLASS_NAMES)))
    
    for model in models:
        probs = model.predict(img_array, verbose=0)
        ensemble_probs += probs
    
    ensemble_probs /= len(models)
    
    # Lấy kết quả
    predicted_class_idx = np.argmax(ensemble_probs[0])
    predicted_class = CLASS_NAMES[predicted_class_idx]
    confidence = ensemble_probs[0][predicted_class_idx] * 100
    
    # Tạo dict xác suất cho tất cả các class
    probabilities = {
        CLASS_NAMES_VN[cls]: float(ensemble_probs[0][idx] * 100)
        for idx, cls in enumerate(CLASS_NAMES)
    }
    
    return {
        'class': predicted_class,
        'class_vn': CLASS_NAMES_VN[predicted_class],
        'confidence': float(confidence),
        'probabilities': probabilities
    }


@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Xử lý upload và dự đoán ảnh"""
    if 'file' not in request.files:
        flash('Không tìm thấy file!', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Chưa chọn file!', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Kiểm tra xem ảnh có phải X-quang nha khoa không
            is_valid, confidence_score, reason = is_dental_xray(filepath)
            
            if not is_valid:
                # Ảnh không hợp lệ - hiển thị thông báo
                return render_template('invalid_image.html',
                                     filename=filename,
                                     reason=reason,
                                     confidence=f"{confidence_score:.1f}")
            
            # Dự đoán bệnh bằng ML model
            result = predict_image(filepath)
            
            # Phân tích đặc trưng ảnh để đánh giá mức độ nghiêm trọng
            image_features = analyze_image_features(filepath)
            severity_level = classify_severity_level(
                image_features['severity_score'],
                result['class']
            )
            
            # Lấy lời khuyên y khoa
            medical_advice = get_medical_advice(result['class'], severity_level)
            
            # Thêm thông tin mới vào result
            result['severity_level'] = severity_level
            result['severity_score'] = image_features['severity_score']
            result['image_features'] = image_features
            result['medical_advice'] = medical_advice
            
            return render_template('result.html',
                                 filename=filename,
                                 prediction=result['class_vn'],
                                 confidence=f"{result['confidence']:.2f}",
                                 probabilities=result['probabilities'],
                                 severity_level=severity_level,
                                 severity_score=f"{image_features['severity_score']:.1f}",
                                 medical_advice=medical_advice,
                                 image_features=image_features)
        
        except Exception as e:
            flash(f'Lỗi khi xử lý ảnh: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    else:
        flash('Định dạng file không hợp lệ! Chỉ chấp nhận PNG, JPG, JPEG', 'error')
        return redirect(url_for('index'))


@app.route('/compare_models', methods=['GET', 'POST'])
def compare_models():
    """So sánh kết quả giữa CBAM Ensemble và ResNet50"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Không tìm thấy file!', 'error')
            return redirect(url_for('compare_models'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('Chưa chọn file!', 'error')
            return redirect(url_for('compare_models'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"compare_models_{filename}")
            file.save(filepath)
            
            try:
                # Dự đoán với CBAM Ensemble
                cbam_result = predict_image(filepath)
                cbam_result['model_name'] = 'CBAM Ensemble'
                cbam_result['model_desc'] = f'{len(loaded_models)} models với CBAM + Focal Loss'
                
                # Dự đoán với ResNet50
                resnet_result = predict_with_resnet50(filepath)
                resnet_result['model_name'] = 'ResNet50'
                resnet_result['model_desc'] = 'Single ResNet50 model'
                
                # So sánh
                comparison = {
                    'same_prediction': cbam_result['class'] == resnet_result['class'],
                    'confidence_diff': abs(cbam_result['confidence'] - resnet_result['confidence'])
                }
                
                return render_template('compare_models.html',
                                     filename=f"compare_models_{filename}",
                                     cbam_result=cbam_result,
                                     resnet_result=resnet_result,
                                     comparison=comparison,
                                     show_results=True)
            
            except FileNotFoundError as e:
                flash(f'Lỗi: {str(e)}. Vui lòng đặt file best_resnet50.h5 vào thư mục models/', 'error')
                return redirect(url_for('compare_models'))
            except Exception as e:
                flash(f'Lỗi khi xử lý ảnh: {str(e)}', 'error')
                return redirect(url_for('compare_models'))
        
        else:
            flash('Định dạng file không hợp lệ! Chỉ chấp nhận PNG, JPG, JPEG', 'error')
            return redirect(url_for('compare_models'))
    
    return render_template('compare_models.html', show_results=False)


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    print("\n" + "="*50)
    print("🦷 KHỞI ĐỘNG ỨNG DỤNG NHẬN DIỆN BỆNH RĂNG")
    print("="*50)
    try:
        load_ensemble_models()
        print("\n🚀 Server đang chạy tại: http://127.0.0.1:5000")
        print("="*50 + "\n")
        # Sử dụng cổng từ biến môi trường cho production (Render)
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=False, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"\n❌ Lỗi khởi động: {str(e)}")
        print("Vui lòng kiểm tra lại models trong thư mục models/\n")
