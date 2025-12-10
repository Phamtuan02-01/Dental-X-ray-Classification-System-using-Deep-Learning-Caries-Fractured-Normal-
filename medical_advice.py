"""
Database lời khuyên y khoa cho các loại bệnh răng
Dựa trên kiến thức nha khoa cơ bản
"""

# Lời khuyên chi tiết cho từng loại bệnh và mức độ
MEDICAL_ADVICE = {
    'Caries': {
        'Nhẹ': {
            'title': 'Sâu Răng Nhẹ',
            'description': 'Lớp men răng bắt đầu bị tổn thương, chưa lan sâu vào ngà răng.',
            'symptoms': [
                'Có thể chưa có triệu chứng đau rõ rệt',
                'Xuất hiện các đốm trắng hoặc nâu nhạt trên bề mặt răng',
                'Có thể nhạy cảm nhẹ với thức ăn ngọt hoặc lạnh'
            ],
            'risks': [
                'Nếu không điều trị, sẽ tiến triển thành sâu răng trung bình',
                'Vi khuẩn sẽ tiếp tục phá hủy men răng',
                'Tốn chi phí điều trị cao hơn nếu để muộn'
            ],
            'recommendations': [
                '✓ Đặt lịch khám nha sĩ trong vòng 1-2 tuần',
                '✓ Điều trị: Cạo vôi răng, trám răng composite',
                '✓ Tăng cường vệ sinh răng miệng (đánh răng 2 lần/ngày)',
                '✓ Sử dụng kem đánh răng có fluoride',
                '✓ Hạn chế đồ ngọt, nước ngọt có ga',
                '✓ Súc miệng nước muối loãng sau bữa ăn'
            ],
            'urgency': 'Không khẩn cấp',
            'urgency_color': 'warning',  # yellow/orange
            'icon': '⚠️'
        },
        'Trung bình': {
            'title': 'Sâu Răng Trung Bình',
            'description': 'Lỗ sâu đã lan từ men răng vào ngà răng, gây tổn thương rõ rệt.',
            'symptoms': [
                'Đau răng khi ăn đồ ngọt, nóng, lạnh',
                'Có lỗ sâu nhìn thấy được trên bề mặt răng',
                'Thức ăn thường bị mắc kẹt trong lỗ sâu',
                'Có thể có mùi hôi miệng'
            ],
            'risks': [
                'Nguy cơ lan sang tủy răng gây viêm tủy',
                'Đau răng dữ dội nếu không điều trị kịp thời',
                'Có thể cần điều trị nội nha (lấy tủy)',
                'Nguy cơ nhiễm trùng lan sang răng khác'
            ],
            'recommendations': [
                '⚠️ Cần khám nha sĩ TRONG TUẦN NÀY',
                '✓ Điều trị: Trám răng, có thể cần trám lót',
                '✓ Tránh để thức ăn vào lỗ sâu',
                '✓ Giảm đau tạm thời: Paracetamol (nếu cần)',
                '✓ Súc miệng nước muối ấm 3-4 lần/ngày',
                '✓ Tránh đồ quá nóng, quá lạnh',
                '✓ Không nên trì hoãn điều trị'
            ],
            'urgency': 'Cần khám sớm',
            'urgency_color': 'danger-light',  # orange
            'icon': '⚠️'
        },
        'Nặng': {
            'title': 'Sâu Răng Nặng',
            'description': 'Lỗ sâu đã lan sâu gần hoặc tới tủy răng, gây tổn thương nghiêm trọng.',
            'symptoms': [
                'Đau răng dữ dội, liên tục, nhất là ban đêm',
                'Sưng nướu, áp xe quanh răng',
                'Lỗ sâu lớn, có thể thấy tủy răng',
                'Đau lan ra má, thái dương',
                'Khó ăn uống, mất ngủ'
            ],
            'risks': [
                'NGUY CƠ CAO mất răng nếu không điều trị',
                'Viêm tủy răng cấp tính',
                'Áp xe răng, nhiễm trùng lan rộng',
                'Có thể gây sốt, sưng má',
                'Nguy cơ nhiễm trùng máu nếu không xử lý'
            ],
            'recommendations': [
                '🚨 KHẨN CẤP - Khám nha sĩ NGAY trong 1-2 ngày',
                '✓ Điều trị: Nội nha (lấy tủy), bọc răng sứ',
                '✓ Có thể cần nhổ răng nếu quá nặng',
                '✓ Uống thuốc giảm đau theo chỉ định (Ibuprofen/Paracetamol)',
                '✓ Kháng sinh nếu có nhiễm trùng (theo đơn bác sĩ)',
                '✓ Chườm lạnh vùng má để giảm sưng',
                '✓ Nằm đầu cao khi ngủ',
                '⚠️ KHÔNG TỰ Ý DÙNG THUỐC KHÔNG RÕ NGUỒN GỐC'
            ],
            'urgency': 'KHẨN CẤP',
            'urgency_color': 'danger',  # red
            'icon': '🚨'
        }
    },
    'Fractured': {
        'Nhẹ': {
            'title': 'Gãy/Nứt Răng Nhẹ',
            'description': 'Vết nứt nhỏ hoặc mẻ răng nhẹ ở phần men, chưa ảnh hưởng đến ngà răng.',
            'symptoms': [
                'Nhạy cảm khi cắn nhai',
                'Có thể thấy vết nứt nhỏ trên bề mặt răng',
                'Đau nhói khi ăn đồ lạnh',
                'Răng có thể sắc, cấn lưỡi hoặc má'
            ],
            'risks': [
                'Vết nứt có thể lan sâu hơn',
                'Nguy cơ nhiễm khuẩn qua vết nứt',
                'Có thể gây tổn thương nướu, má',
                'Ảnh hưởng thẩm mỹ'
            ],
            'recommendations': [
                '✓ Khám nha sĩ trong vòng 1-2 tuần',
                '✓ Điều trị: Trám răng, mài nhẵn cạnh sắc',
                '✓ Có thể dùng composite để tái tạo hình dạng răng',
                '✓ Tránh cắn thức ăn cứng bằng răng bị nứt',
                '✓ Đánh răng nhẹ nhàng vùng răng nứt',
                '✓ Tránh đồ quá lạnh, quá nóng'
            ],
            'urgency': 'Không khẩn cấp',
            'urgency_color': 'warning',
            'icon': '⚠️'
        },
        'Nặng': {
            'title': 'Gãy Răng Nặng',
            'description': 'Gãy lớn từ men đến ngà răng, có thể lộ tủy răng.',
            'symptoms': [
                'Đau dữ dội, nhất là khi cắn',
                'Mất phần lớn thân răng',
                'Chảy máu nướu hoặc tủy răng',
                'Rất nhạy cảm với nhiệt độ',
                'Khó ăn uống'
            ],
            'risks': [
                'NGUY CƠ CAO mất răng',
                'Nhiễm trùng tủy răng',
                'Tổn thương thần kinh răng',
                'Ảnh hưởng nghiêm trọng đến chức năng nhai',
                'Có thể cần nhổ răng'
            ],
            'recommendations': [
                '🚨 KHẨN CẤP - Khám nha sĩ NGAY trong 24 giờ',
                '✓ Bảo quản mảnh răng gãy trong sữa/nước muối (nếu có)',
                '✓ Điều trị: Nội nha + bọc răng sứ hoặc cấy implant',
                '✓ Chườm lạnh giảm sưng',
                '✓ Uống thuốc giảm đau (Ibuprofen/Paracetamol)',
                '✓ Ăn mềm, tránh dùng răng bị gãy',
                '✓ Giữ vệ sinh răng miệng cẩn thận',
                '⚠️ Không trì hoãn - có thể mất răng vĩnh viễn'
            ],
            'urgency': 'KHẨN CẤP',
            'urgency_color': 'danger',
            'icon': '🚨'
        }
    },
    'Normal': {
        'title': 'Răng Khỏe Mạnh',
        'description': 'Không phát hiện dấu hiệu bệnh lý trên ảnh X-quang.',
        'recommendations': [
            '✓ Tiếp tục duy trì vệ sinh răng miệng tốt',
            '✓ Đánh răng 2 lần/ngày với kem đánh răng có fluoride',
            '✓ Dùng chỉ nha khoa mỗi ngày',
            '✓ Súc miệng nước muối sau bữa ăn',
            '✓ Khám nha sĩ định kỳ 6 tháng/lần',
            '✓ Hạn chế đồ ngọt, nước ngọt có ga',
            '✓ Ăn nhiều rau xanh, trái cây giàu vitamin',
            '✓ Uống đủ nước mỗi ngày'
        ],
        'urgency': 'Khám định kỳ',
        'urgency_color': 'success',
        'icon': '✅'
    }
}


def get_medical_advice(disease_class, severity_level=None):
    """
    Lấy lời khuyên y khoa dựa trên loại bệnh và mức độ
    
    Args:
        disease_class: 'Caries', 'Fractured', hoặc 'Normal'
        severity_level: 'Nhẹ', 'Trung bình', 'Nặng' (None nếu Normal)
    
    Returns:
        dict: Thông tin lời khuyên chi tiết
    """
    if disease_class == 'Normal':
        return MEDICAL_ADVICE['Normal']
    
    if disease_class in MEDICAL_ADVICE and severity_level:
        if severity_level in MEDICAL_ADVICE[disease_class]:
            return MEDICAL_ADVICE[disease_class][severity_level]
    
    # Fallback
    return {
        'title': 'Cần khám nha sĩ',
        'description': 'Vui lòng đến nha sĩ để được tư vấn chính xác.',
        'recommendations': ['Khám nha sĩ để được chẩn đoán chính xác'],
        'urgency': 'Cần khám',
        'urgency_color': 'info',
        'icon': 'ℹ️'
    }


def get_severity_color(severity_level):
    """
    Lấy màu sắc tương ứng với mức độ nghiêm trọng
    
    Returns:
        str: Bootstrap color class
    """
    colors = {
        'Nhẹ': 'warning',      # Yellow/Orange
        'Trung bình': 'orange', # Orange
        'Nặng': 'danger',      # Red
        None: 'success'        # Green (Normal)
    }
    return colors.get(severity_level, 'info')


def get_severity_icon(severity_level):
    """
    Lấy icon tương ứng với mức độ nghiêm trọng
    """
    icons = {
        'Nhẹ': '⚠️',
        'Trung bình': '⚠️',
        'Nặng': '🚨',
        None: '✅'
    }
    return icons.get(severity_level, 'ℹ️')


if __name__ == '__main__':
    # Test
    print("Database lời khuyên y khoa đã sẵn sàng!")
    
    # Test get advice
    advice = get_medical_advice('Caries', 'Nặng')
    print(f"\nTest - {advice['title']}:")
    print(f"Urgency: {advice['urgency']}")
    print(f"Icon: {advice['icon']}")
