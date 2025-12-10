# 🦷 AI Dental Diagnosis - Ứng Dụng Nhận Diện Bệnh Răng

Ứng dụng Web Flask sử dụng **Deep Learning Ensemble** với **CBAM Attention** và **Focal Loss** để phân loại bệnh răng từ ảnh X-quang.

---

## ✨ Tính Năng Chính

### 🏠 Trang chủ - Phân tích bình thường
- Upload ảnh X-quang răng (PNG, JPG, JPEG)
- Phân loại tự động 3 loại bệnh:
  - **Sâu răng** (Caries) 🦷
  - **Gãy răng** (Fractured) ⚠️
  - **Bình thường** (Normal) ✅
- Hiển thị xác suất chi tiết cho từng loại
- Sử dụng **CBAM Ensemble Model** (4 models)

### 🤖 So sánh Models
- Upload 1 ảnh để so sánh kết quả giữa **CBAM Ensemble** và **ResNet50**
- Hiển thị side-by-side comparison
- Thống kê chênh lệch độ tin cậy
- Kiểm tra xem 2 models có dự đoán giống nhau không

---

## 🚀 Hướng Dẫn Cài Đặt

### 1. Yêu cầu hệ thống
- Python 3.11+ (khuyến nghị Python 3.11.5)
- RAM: 4GB+ (8GB khuyến nghị)
- Dung lượng: ~500MB cho models

### 2. Clone/Download dự án
```bash
cd "C:\Khóa Luận\App"
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Cấu trúc thư mục
Đảm bảo có đầy đủ các file sau:
```
App/
├── app_keras3.py                  # Main Flask application
├── custom_layers_keras3.py        # CBAM custom layers (Keras 3)
├── requirements.txt               # Danh sách thư viện
├── models/                        # Thư mục chứa models
│   ├── best_teeth_cbam_focal_v1.h5  (CBAM Ensemble - 28-31 MB mỗi file)
│   ├── best_teeth_cbam_focal_v2.h5
│   ├── best_teeth_cbam_focal_v3.h5
│   ├── best_teeth_cbam_focal_v4.h5
│   └── best_resnet50.h5             (ResNet50 model)
├── static/
│   ├── css/
│   │   └── style.css              # Giao diện + animations
│   ├── js/
│   │   └── script.js              # Upload logic + drag-drop
│   └── uploads/                   # Thư mục lưu ảnh (tự động tạo)
└── templates/
    ├── index.html                 # Trang chủ - upload ảnh
    ├── result.html                # Hiển thị kết quả phân tích
    └── compare_models.html        # So sánh 2 models
```

### 5. Chạy ứng dụng
```bash
python app_keras3.py
```

Mở trình duyệt và truy cập: **http://127.0.0.1:5000**

---

## 📦 Dependencies

```
Flask==3.0.0           # Web framework
Werkzeug==3.0.1        # WSGI utilities
tensorflow==2.15.0     # Backend cho Keras
keras==3.12.0          # Standalone Keras 3
numpy==1.24.3          # Numerical computing
Pillow==10.1.0         # Image processing
focal-loss==0.0.7      # Focal Loss implementation
```

> **⚠️ Quan trọng:** Phải dùng **Keras 3 standalone** (không phải `tf.keras`) vì models được train với Keras 3.

---

## 🏗️ Kiến Trúc Model

### 🧠 CBAM Ensemble
- **Base Model**: MobileNetV2 (pretrained on ImageNet)
- **Attention**: CBAM (Convolutional Block Attention Module)
  - Channel Attention (GlobalAvgPool + GlobalMaxPool)
  - Spatial Attention (7×7 Conv)
- **Loss Function**: Sparse Categorical Focal Loss (γ=2)
- **Ensemble**: 4 models voting (v1, v2, v3, v4)
- **Total Parameters**: ~3M per model

### 🎯 ResNet50
- **Architecture**: ResNet50 (pretrained on ImageNet)
- **Loss Function**: Sparse Categorical Crossentropy
- **Output**: 3 classes (Caries, Fractured, Normal)

### 📐 Training Details
- **Dataset**: Tufts Dental Database (~3000 ảnh X-quang)
- **Input Size**: 224×224×3
- **Augmentation**: Rotation, Flip, Zoom, Shift, Brightness
- **Split**: Train/Val/Test = 70/15/15
- **Epochs**: 50 với Early Stopping
- **Batch Size**: 32

---

## 🔧 Troubleshooting

### ❌ Lỗi `UnicodeDecodeError` với đường dẫn "Khóa Luận"
**Giải pháp:** Đã implement workaround tự động trong code:
```python
# app_keras3.py tự động copy model vào tempfile trước khi load
shutil.copy2(model_path, temp_path)
model = keras.models.load_model(temp_path)
```

### ❌ Lỗi `ModuleNotFoundError: focal_loss`
```bash
pip install focal-loss
```

### ❌ Lỗi `ImportError: ops from tensorflow.keras`
**Nguyên nhân:** Dùng nhầm `tf.keras` thay vì `keras` standalone.  
**Giải pháp:** Đã fix trong `custom_layers_keras3.py`:
```python
import keras  # ✅ Đúng
# from tensorflow import keras  # ❌ Sai
```

### ❌ Model không load được
**Kiểm tra:**
1. Có đủ 5 file `.h5` trong thư mục `models/` (4 CBAM + 1 ResNet50)
2. Tên file đúng format: `best_teeth_cbam_focal_v1.h5` (v1-v4) và `best_resnet50.h5`
3. File không bị corrupt

---

## 🌐 Routes

| Route | Method | Mô tả |
|-------|--------|-------|
| `/` | GET | Trang chủ - upload ảnh (CBAM Ensemble) |
| `/predict` | POST | Xử lý upload và trả về kết quả |
| `/compare_models` | GET/POST | So sánh CBAM Ensemble vs ResNet50 |

---

## 🎨 Giao Diện

- **Responsive Design**: Tối ưu cho desktop & mobile
- **Animations**: Fade-in, pulse, spin effects
- **Color Scheme**: 
  - Primary: `#3498db` (Blue)
  - Success: `#27ae60` (Green)
  - Warning: `#f39c12` (Orange)
  - Danger: `#e74c3c` (Red)
- **Icons**: Unicode emoji (🦷⚠️✅🤖🏠)

---

## 📊 Hiệu Suất

- **Load Time**: ~10 giây (load 4 models CBAM + 1 ResNet50 lần đầu)
- **Prediction Time**: ~2-3 giây/ảnh
- **Ensemble Accuracy**: **~92%** trên test set
  - Caries Detection: **~89%**
  - Fractured Detection: **~93%**
  - Normal Detection: **~95%**

---

## 🔐 Bảo Mật

- File upload giới hạn 16MB
- Chỉ chấp nhận ảnh: PNG, JPG, JPEG
- Filename sanitization với `secure_filename()`
- Secret key cho Flask sessions (đổi trong production!)

---

## 📝 License

MIT License - Tự do sử dụng cho mục đích học tập và nghiên cứu.

---

## 👨‍💻 Tác Giả

**Khóa Luận Tốt Nghiệp 2025**  
Đề tài: *Ứng dụng Deep Learning trong chẩn đoán bệnh răng từ ảnh X-quang*

---

## 🙏 Credits

- **Dataset**: Tufts Dental Database
- **Framework**: Flask, TensorFlow, Keras
- **Architecture**: MobileNetV2 + CBAM, ResNet50
- **Loss Function**: Focal Loss (Lin et al., 2017)

---

**⭐ Nếu thấy hữu ích, hãy star repo này nhé!**

---

## 🚀 Hướng Dẫn Cài Đặt

### 1. Yêu cầu hệ thống
- Python 3.11+ (khuyến nghị Python 3.11.5)
- RAM: 4GB+ (8GB khuyến nghị)
- Dung lượng: ~500MB cho models

### 2. Clone/Download dự án
```bash
cd "C:\Khóa Luận\App"
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Cấu trúc thư mục
Đảm bảo có đầy đủ các file sau:
```
App/
├── app_keras3.py                  # Main Flask application
├── custom_layers_keras3.py        # CBAM custom layers (Keras 3)
├── requirements.txt               # Danh sách thư viện
├── .gitignore                     # Git ignore patterns
├── models/                        # Thư mục chứa 4 models
│   ├── best_teeth_cbam_focal_v1.h5  (28-31 MB mỗi file)
│   ├── best_teeth_cbam_focal_v2.h5
│   ├── best_teeth_cbam_focal_v3.h5
│   └── best_teeth_cbam_focal_v4.h5
├── static/
│   ├── css/
│   │   └── style.css              # Giao diện + animations
│   ├── js/
│   │   └── script.js              # Upload logic + drag-drop
│   └── uploads/                   # Thư mục lưu ảnh (tự động tạo)
└── templates/
    ├── index.html                 # Trang chủ - upload ảnh
    ├── result.html                # Hiển thị kết quả phân tích
    ├── about.html                 # Giới thiệu hệ thống
    ├── history.html               # Lịch sử phân tích
    ├── compare.html               # So sánh nhiều ảnh
    └── stats.html                 # Thống kê hệ thống
```

### 5. Chạy ứng dụng
```bash
python app_keras3.py
```

Mở trình duyệt và truy cập: **http://127.0.0.1:5000**

---

## 📦 Dependencies

```
Flask==3.0.0           # Web framework
Werkzeug==3.0.1        # WSGI utilities
tensorflow==2.15.0     # Backend cho Keras
keras==3.12.0          # Standalone Keras 3
numpy==1.24.3          # Numerical computing
Pillow==10.1.0         # Image processing
focal-loss==0.0.7      # Focal Loss implementation
```

> **⚠️ Quan trọng:** Phải dùng **Keras 3 standalone** (không phải `tf.keras`) vì models được train với Keras 3.

---

## 🏗️ Kiến Trúc Model

### 🧠 Deep Learning Stack
- **Base Model**: MobileNetV2 (pretrained on ImageNet)
- **Attention**: CBAM (Convolutional Block Attention Module)
  - Channel Attention (GlobalAvgPool + GlobalMaxPool)
  - Spatial Attention (7×7 Conv)
- **Loss Function**: Sparse Categorical Focal Loss (γ=2)
- **Ensemble**: 4 models voting (v1, v2, v3, v4)

### 📐 Model Specifications
- **Input Size**: 224×224×3
- **Architecture**: MobileNetV2 → CBAM → Dense → Softmax
- **Output**: 3 classes (Caries, Fractured, Normal)
- **Optimizer**: Adam
- **Total Parameters**: ~3M per model

### 🎯 Training Details
- **Dataset**: Tufts Dental Database (~3000 ảnh X-quang)
- **Augmentation**: Rotation, Flip, Zoom, Shift, Brightness
- **Split**: Train/Val/Test = 70/15/15
- **Epochs**: 50 với Early Stopping
- **Batch Size**: 32

---

## 🔧 Troubleshooting

### ❌ Lỗi `UnicodeDecodeError` với đường dẫn "Khóa Luận"
**Giải pháp:** Đã implement workaround tự động trong code:
```python
# app_keras3.py tự động copy model vào tempfile trước khi load
shutil.copy2(model_path, temp_path)
model = keras.models.load_model(temp_path)
```

### ❌ Lỗi `ModuleNotFoundError: focal_loss`
```bash
pip install focal-loss
```

### ❌ Lỗi `ImportError: ops from tensorflow.keras`
**Nguyên nhân:** Dùng nhầm `tf.keras` thay vì `keras` standalone.  
**Giải pháp:** Đã fix trong `custom_layers_keras3.py`:
```python
import keras  # ✅ Đúng
# from tensorflow import keras  # ❌ Sai
```

### ❌ Model không load được
**Kiểm tra:**
1. Có đủ 4 file `.h5` trong thư mục `models/`
2. Tên file đúng format: `best_teeth_cbam_focal_v1.h5` (v1-v4)
3. File không bị corrupt (mỗi file ~28-31 MB)

### ❌ Click 2 lần mới chọn được ảnh
**Đã fix:** JavaScript có check `event.target !== fileInput` để tránh double-trigger.

---

## 🌐 API Endpoints

| Route | Method | Mô tả |
|-------|--------|-------|
| `/` | GET | Trang chủ - upload ảnh |
| `/predict` | POST | Xử lý upload và trả về kết quả |
| `/about` | GET | Giới thiệu hệ thống |
| `/history` | GET | Lịch sử 20 ảnh gần nhất |
| `/compare` | GET/POST | So sánh nhiều ảnh (tối đa 4) |
| `/stats` | GET | Thống kê hệ thống |

---

## 🎨 Giao Diện

- **Responsive Design**: Tối ưu cho desktop & mobile
- **Animations**: Fade-in, pulse, spin effects
- **Color Scheme**: 
  - Primary: `#3498db` (Blue)
  - Success: `#27ae60` (Green)
  - Warning: `#f39c12` (Orange)
  - Danger: `#e74c3c` (Red)
- **Icons**: Unicode emoji (🦷⚠️✅📊📜)

---

## 📊 Hiệu Suất

- **Load Time**: ~10 giây (load 4 models lần đầu)
- **Prediction Time**: ~2-3 giây/ảnh
- **Accuracy**: 
  - Ensemble Accuracy: **~92%** trên test set
  - Caries Detection: **~89%**
  - Fractured Detection: **~93%**
  - Normal Detection: **~95%**

---

## 🔐 Bảo Mật

- File upload giới hạn 16MB
- Chỉ chấp nhận ảnh: PNG, JPG, JPEG
- Filename sanitization với `secure_filename()`
- Secret key cho Flask sessions (đổi trong production!)

---

## 📝 License

MIT License - Tự do sử dụng cho mục đích học tập và nghiên cứu.

---

## 👨‍💻 Tác Giả

**Khóa Luận Tốt Nghiệp 2025**  
Đề tài: *Ứng dụng Deep Learning trong chẩn đoán bệnh răng từ ảnh X-quang*

---

## 🙏 Credits

- **Dataset**: Tufts Dental Database
- **Framework**: Flask, TensorFlow, Keras
- **Architecture**: MobileNetV2 + CBAM
- **Loss Function**: Focal Loss (Lin et al., 2017)

---

## 📧 Liên Hệ

Nếu có vấn đề hoặc câu hỏi, vui lòng mở issue hoặc liên hệ qua email.

---

**⭐ Nếu thấy hữu ích, hãy star repo này nhé!**
