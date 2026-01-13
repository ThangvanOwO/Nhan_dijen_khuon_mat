"""
Cấu hình cho hệ thống nhận diện khuôn mặt sử dụng face_recognition (Dlib)
Độ chính xác cao hơn LBPH (~95%+)
"""
import os

# Đường dẫn thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Thư mục chứa dữ liệu khuôn mặt
# Cấu trúc: dataset/ten_nguoi/anh1.jpg, anh2.jpg, ...
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

# File chứa encodings đã được trích xuất
ENCODINGS_FILE = os.path.join(BASE_DIR, "encodings.pickle")

# ==================== CẤU HÌNH NHẬN DIỆN ====================

# Ngưỡng tolerance cho face_recognition
# Giá trị càng thấp = càng nghiêm ngặt (ít false positive)
# Giá trị càng cao = càng dễ dãi (ít false negative)
# Khuyến nghị: 0.4 - 0.6
# - 0.4: Rất nghiêm ngặt, phù hợp bảo mật cao
# - 0.5: Cân bằng (khuyến nghị)
# - 0.6: Dễ dãi hơn, phù hợp khi cần nhận diện ở nhiều điều kiện
TOLERANCE = 0.5

# Phương pháp phát hiện khuôn mặt
# - "hog": Nhanh hơn, dùng CPU (khuyến nghị cho máy không có GPU)
# - "cnn": Chính xác hơn, cần GPU (CUDA)
DETECTION_METHOD = "cnn"  # Đã bật GPU!

# Model encoding
# - "small": 5 điểm landmark, nhanh hơn
# - "large": 68 điểm landmark, chính xác hơn
ENCODING_MODEL = "large"

# Số lần jitter khi tạo encoding (tăng = chính xác hơn nhưng chậm hơn)
# Khuyến nghị: 1 cho realtime, 10-100 cho training
NUM_JITTERS = 1
NUM_JITTERS_TRAINING = 10

# ==================== CẤU HÌNH CAMERA ====================

# Index của camera (0 = camera mặc định)
CAMERA_INDEX = 0

# Kích thước frame hiển thị (tăng để nhận diện xa tốt hơn)
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Resize frame để xử lý nhanh hơn
# - 0.25: Nhanh nhưng chỉ nhận diện gần
# - 0.5: Cân bằng, nhận diện xa tốt hơn (khuyến nghị)
# - 1.0: Chậm nhất, nhận diện xa nhất
FRAME_RESIZE_SCALE = 0.35

# Số frame skip giữa các lần detect (tăng = nhanh hơn nhưng ít mượt)
FRAME_SKIP = 3

# ==================== CẤU HÌNH XỬ LÝ ÁNH SÁNG ====================

# Bật/tắt cải thiện ánh sáng (CLAHE)
# True: Tự động cân bằng ánh sáng (tốt cho môi trường sáng/tối không đều)
# False: Tắt (nhanh hơn, phù hợp khi ánh sáng ổn định)
ENHANCE_LIGHTING = True

# CLAHE clip limit (2.0 - 4.0)
# Giá trị cao hơn = contrast mạnh hơn
CLAHE_CLIP_LIMIT = 2.0

# CLAHE tile grid size (kích thước vùng xử lý)
CLAHE_TILE_SIZE = (8, 8)

# ==================== CẤU HÌNH HIỂN THỊ ====================

# Màu sắc (BGR format)
COLOR_KNOWN = (0, 255, 0)      # Xanh lá - Người đã biết
COLOR_UNKNOWN = (0, 0, 255)    # Đỏ - Người lạ
COLOR_TEXT = (255, 255, 255)   # Trắng - Text

# Font
FONT = "FONT_HERSHEY_SIMPLEX"
FONT_SCALE = 0.6
FONT_THICKNESS = 2

# Tạo thư mục dataset nếu chưa có
os.makedirs(DATASET_DIR, exist_ok=True)
