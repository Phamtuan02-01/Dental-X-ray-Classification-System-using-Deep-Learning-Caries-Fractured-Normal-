"""
Module phân tích ảnh X-quang răng để ước lượng mức độ nghiêm trọng
Sử dụng Computer Vision để trích xuất đặc trưng ảnh
"""
import cv2
import numpy as np
from PIL import Image


def analyze_image_features(img_path):
    """
    Phân tích đặc trưng ảnh X-quang để ước lượng mức độ nghiêm trọng
    
    Args:
        img_path: Đường dẫn đến ảnh X-quang
    
    Returns:
        dict: {
            'severity_score': float (0-100),
            'dark_area_ratio': float,
            'contrast_level': float,
            'edge_intensity': float
        }
    """
    # Đọc ảnh
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Không thể đọc ảnh: {img_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Phân tích vùng tối (dark regions - có thể là vùng sâu răng)
    dark_area_ratio = analyze_dark_regions(gray)
    
    # 2. Đo độ tương phản (contrast)
    contrast_level = calculate_contrast(gray)
    
    # 3. Phân tích cạnh (edge detection - phát hiện vết nứt/gãy)
    edge_intensity = analyze_edges(gray)
    
    # 4. Phân tích histogram
    hist_variance = analyze_histogram(gray)
    
    # Tính severity score tổng hợp (0-100)
    severity_score = calculate_severity_score(
        dark_area_ratio,
        contrast_level,
        edge_intensity,
        hist_variance
    )
    
    return {
        'severity_score': float(severity_score),
        'dark_area_ratio': float(dark_area_ratio),
        'contrast_level': float(contrast_level),
        'edge_intensity': float(edge_intensity),
        'hist_variance': float(hist_variance)
    }


def analyze_dark_regions(gray_img):
    """
    Phân tích tỷ lệ vùng tối trong ảnh (vùng sâu răng thường tối hơn)
    
    Returns:
        float: Tỷ lệ vùng tối (0-1)
    """
    # Threshold để tìm vùng tối
    # X-quang: vùng sâu răng thường có intensity thấp
    _, binary = cv2.threshold(gray_img, 80, 255, cv2.THRESH_BINARY_INV)
    
    # Tính tỷ lệ pixel tối
    dark_pixels = np.sum(binary == 255)
    total_pixels = binary.size
    dark_ratio = dark_pixels / total_pixels
    
    return min(dark_ratio * 2, 1.0)  # Scale up và cap ở 1.0


def calculate_contrast(gray_img):
    """
    Tính độ tương phản của ảnh
    Độ tương phản cao có thể chỉ ra vùng tổn thương rõ ràng
    
    Returns:
        float: Mức độ tương phản (0-1)
    """
    # Tính standard deviation của intensity
    std_dev = np.std(gray_img)
    
    # Normalize (std của ảnh 8-bit thường trong khoảng 0-70)
    contrast = min(std_dev / 70.0, 1.0)
    
    return contrast


def analyze_edges(gray_img):
    """
    Phân tích cường độ cạnh (phát hiện vết nứt, gãy)
    
    Returns:
        float: Cường độ cạnh (0-1)
    """
    # Sử dụng Canny edge detection
    edges = cv2.Canny(gray_img, 50, 150)
    
    # Tính tỷ lệ edge pixels
    edge_pixels = np.sum(edges > 0)
    total_pixels = edges.size
    edge_ratio = edge_pixels / total_pixels
    
    # Scale up (edge ratio thường rất nhỏ)
    return min(edge_ratio * 10, 1.0)


def analyze_histogram(gray_img):
    """
    Phân tích histogram để đánh giá phân bố intensity
    
    Returns:
        float: Độ phân tán histogram (0-1)
    """
    hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
    hist = hist.flatten() / hist.sum()  # Normalize
    
    # Tính variance của histogram
    variance = np.var(hist)
    
    # Normalize (variance thường rất nhỏ)
    return min(variance * 10000, 1.0)


def calculate_severity_score(dark_ratio, contrast, edge_intensity, hist_var):
    """
    Tính tổng hợp severity score từ các đặc trưng
    
    Args:
        dark_ratio: Tỷ lệ vùng tối (0-1)
        contrast: Độ tương phản (0-1)
        edge_intensity: Cường độ cạnh (0-1)
        hist_var: Độ phân tán histogram (0-1)
    
    Returns:
        float: Severity score (0-100)
    """
    # Trọng số cho từng đặc trưng
    weights = {
        'dark_ratio': 0.4,      # Vùng tối quan trọng nhất
        'contrast': 0.25,       # Độ tương phản
        'edge_intensity': 0.25, # Cường độ cạnh (gãy/nứt)
        'hist_var': 0.1         # Độ phân tán
    }
    
    # Tính weighted average
    score = (
        dark_ratio * weights['dark_ratio'] +
        contrast * weights['contrast'] +
        edge_intensity * weights['edge_intensity'] +
        hist_var * weights['hist_var']
    ) * 100
    
    return min(score, 100.0)


def classify_severity_level(severity_score, disease_class):
    """
    Phân loại mức độ nghiêm trọng dựa trên severity score và loại bệnh
    
    Args:
        severity_score: Điểm severity (0-100)
        disease_class: Loại bệnh ('Caries', 'Fractured', 'Normal')
    
    Returns:
        str: Mức độ ('Nhẹ', 'Trung bình', 'Nặng', hoặc None nếu Normal)
    """
    if disease_class == 'Normal':
        return None
    
    if disease_class == 'Caries':
        # Phân loại sâu răng
        if severity_score < 35:
            return 'Nhẹ'
        elif severity_score < 65:
            return 'Trung bình'
        else:
            return 'Nặng'
    
    elif disease_class == 'Fractured':
        # Phân loại gãy răng (thường nghiêm trọng hơn)
        if severity_score < 50:
            return 'Nhẹ'
        else:
            return 'Nặng'
    
    return None


def is_dental_xray(img_path):
    """
    Kiểm tra xem ảnh có phải X-quang nha khoa không
    
    Phân tích:
    - Màu sắc (grayscale hoặc blue-tinted X-ray)
    - Phân bố histogram (high contrast, bimodal distribution)
    - Tỷ lệ vùng sáng/tối
    - Độ phức tạp màu sắc
    
    Args:
        img_path: Đường dẫn đến ảnh
    
    Returns:
        tuple: (is_valid, confidence, reason)
            - is_valid (bool): True nếu là ảnh X-quang nha khoa
            - confidence (float): Độ tin cậy (0-100)
            - reason (str): Lý do (nếu không hợp lệ)
    """
    try:
        # Đọc ảnh
        img = cv2.imread(img_path)
        if img is None:
            return False, 0, "Không thể đọc file ảnh"
        
        # Chuyển sang grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 1. Kiểm tra màu sắc - X-quang thường là grayscale hoặc blue-tinted
        color_score = check_color_distribution(img)
        
        # 2. Kiểm tra độ tương phản - X-quang có contrast cao
        contrast_score = check_contrast_level(gray)
        
        # 3. Kiểm tra phân bố histogram - X-quang có bimodal distribution
        histogram_score = check_histogram_pattern(gray)
        
        # 4. Kiểm tra tỷ lệ vùng sáng/tối
        brightness_score = check_brightness_distribution(gray)
        
        # Tính tổng điểm
        total_score = (
            color_score * 0.3 +
            contrast_score * 0.25 +
            histogram_score * 0.25 +
            brightness_score * 0.2
        )
        
        # Threshold: >= 60 là hợp lệ
        is_valid = total_score >= 60
        
        # Xác định lý do nếu không hợp lệ
        reason = ""
        if not is_valid:
            if color_score < 50:
                reason = "Ảnh có quá nhiều màu sắc, không giống ảnh X-quang (X-quang thường là ảnh xám)"
            elif contrast_score < 50:
                reason = "Độ tương phản thấp, không đặc trưng của ảnh X-quang"
            elif histogram_score < 50:
                reason = "Phân bố sáng tối không giống ảnh X-quang nha khoa"
            else:
                reason = "Đặc điểm ảnh không phù hợp với ảnh X-quang nha khoa"
        
        return is_valid, total_score, reason
    
    except Exception as e:
        return False, 0, f"Lỗi khi phân tích ảnh: {str(e)}"


def check_color_distribution(img):
    """
    Kiểm tra phân bố màu sắc
    X-quang thường là grayscale hoặc blue-tinted, không có nhiều màu
    
    Returns:
        float: Score 0-100
    """
    # Tách các kênh màu
    b, g, r = cv2.split(img)
    
    # Tính độ lệch chuẩn giữa các kênh
    # X-quang: các kênh tương tự nhau (grayscale) hoặc blue dominant
    std_bg = np.std(b.astype(float) - g.astype(float))
    std_br = np.std(b.astype(float) - r.astype(float))
    std_gr = np.std(g.astype(float) - r.astype(float))
    
    avg_std = (std_bg + std_br + std_gr) / 3
    
    # X-quang grayscale: avg_std thấp (~0-20)
    # X-quang blue-tinted: avg_std trung bình (~20-50)
    # Ảnh màu thông thường: avg_std cao (>50)
    
    if avg_std < 15:
        return 100  # Perfect grayscale
    elif avg_std < 30:
        return 80   # Grayscale or slight blue tint
    elif avg_std < 50:
        return 60   # Acceptable blue tint
    elif avg_std < 80:
        return 30   # Too colorful
    else:
        return 0    # Definitely not X-ray


def check_contrast_level(gray_img):
    """
    Kiểm tra độ tương phản
    X-quang có contrast cao (vùng răng sáng, background tối)
    
    Returns:
        float: Score 0-100
    """
    # Tính standard deviation - đo độ tương phản
    std_dev = np.std(gray_img)
    
    # X-quang nha khoa thường có std_dev cao (40-70)
    # Ảnh thông thường có std_dev thấp hơn hoặc rất cao
    
    if 40 <= std_dev <= 70:
        return 100
    elif 30 <= std_dev <= 80:
        return 70
    elif 20 <= std_dev <= 90:
        return 40
    else:
        return 20


def check_histogram_pattern(gray_img):
    """
    Kiểm tra phân bố histogram
    X-quang nha khoa có bimodal distribution (2 peak: background tối + răng sáng)
    
    Returns:
        float: Score 0-100
    """
    # Tính histogram
    hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256]).flatten()
    
    # Smooth histogram
    from scipy.ndimage import gaussian_filter1d
    try:
        hist_smooth = gaussian_filter1d(hist, sigma=5)
    except:
        hist_smooth = hist
    
    # Tìm peaks
    from scipy.signal import find_peaks
    try:
        peaks, _ = find_peaks(hist_smooth, distance=30, prominence=100)
        num_peaks = len(peaks)
        
        # X-quang nha khoa thường có 2-3 peaks
        if num_peaks == 2 or num_peaks == 3:
            return 100
        elif num_peaks == 1 or num_peaks == 4:
            return 60
        else:
            return 30
    except:
        # Fallback: kiểm tra variance
        variance = np.var(hist)
        if variance > 1000:
            return 70
        else:
            return 40


def check_brightness_distribution(gray_img):
    """
    Kiểm tra tỷ lệ vùng sáng/tối
    X-quang nha khoa có cả vùng rất tối (background) và vùng sáng (răng)
    
    Returns:
        float: Score 0-100
    """
    # Đếm pixel trong các vùng
    dark_pixels = np.sum(gray_img < 80)
    bright_pixels = np.sum(gray_img > 150)
    total_pixels = gray_img.size
    
    dark_ratio = dark_pixels / total_pixels
    bright_ratio = bright_pixels / total_pixels
    
    # X-quang nha khoa: 20-50% dark, 10-40% bright
    score = 0
    
    if 0.2 <= dark_ratio <= 0.5:
        score += 50
    elif 0.1 <= dark_ratio <= 0.6:
        score += 30
    
    if 0.1 <= bright_ratio <= 0.4:
        score += 50
    elif 0.05 <= bright_ratio <= 0.5:
        score += 30
    
    return score


if __name__ == '__main__':
    # Test module
    print("Module phân tích ảnh X-quang đã sẵn sàng!")
