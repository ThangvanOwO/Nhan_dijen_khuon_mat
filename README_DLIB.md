# 🎭 Hệ Thống Nhận Diện Khuôn Mặt - Phiên Bản Dlib

Hệ thống nhận diện khuôn mặt thời gian thực sử dụng **face_recognition** (Dlib) với độ chính xác **>95%**.

## 🚀 So sánh với phiên bản LBPH

| Đặc điểm | LBPH (OpenCV) | face_recognition (Dlib) |
|----------|---------------|------------------------|
| Độ chính xác | ~60-70% | **>95%** |
| Xử lý góc nghiêng | Kém | **Tốt** |
| Xử lý ánh sáng yếu | Kém | **Tốt** |
| Tốc độ | Nhanh | Trung bình |
| GPU support | Không | Có (CUDA) |

## 📋 Yêu Cầu Hệ Thống

- **OS**: CachyOS / Arch Linux / Ubuntu
- **Python**: 3.8+
- **RAM**: 4GB+ (khuyến nghị 8GB)
- **Camera**: Webcam

## 🔧 Cài Đặt

### Bước 1: Cài đặt dependencies hệ thống (Arch Linux / CachyOS)

```bash
# Cập nhật hệ thống
sudo pacman -Syu

# Cài đặt các gói cần thiết để build Dlib
sudo pacman -S --needed \
    base-devel \
    cmake \
    gcc \
    python \
    python-pip \
    python-numpy \
    opencv \
    python-opencv

# (Tùy chọn) Cài thêm các gói hỗ trợ
sudo pacman -S --needed \
    openblas \
    lapack \
    boost \
    boost-libs
```

### Bước 2: Tạo môi trường ảo Python

```bash
cd /home/thang/Downloads/Code/face_recognition_project

# Tạo virtual environment
python -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate   # Linux/macOS

# (Nếu dùng fish shell)
# bash -c "source venv/bin/activate && exec fish"
```

### Bước 3: Cài đặt thư viện Python

```bash
# Upgrade pip trước
pip install --upgrade pip setuptools wheel

# Cài cmake cho Python (cần cho dlib)
pip install cmake

# Cài dlib (có thể mất 5-15 phút để build)
pip install dlib

# Cài face_recognition và các thư viện khác
pip install face_recognition opencv-python numpy pillow
```

### Lỗi thường gặp khi cài Dlib

**Lỗi: "CMake must be installed"**
```bash
pip install cmake
```

**Lỗi: "Cannot find X11"**
```bash
sudo pacman -S libx11 libxext
```

**Lỗi: Memory không đủ khi build**
```bash
# Tạo swap file tạm thời
sudo dd if=/dev/zero of=/swapfile bs=1M count=4096
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Sau khi cài xong, có thể xóa
sudo swapoff /swapfile
sudo rm /swapfile
```

## 📁 Cấu Trúc Dự Án

```
face_recognition_project/
├── config_dlib.py          # Cấu hình (tolerance, camera, ...)
├── requirements_dlib.txt   # Thư viện Python
│
├── collect_faces_dlib.py   # Thu thập ảnh khuôn mặt
├── encode_faces.py         # Tạo encodings (128D vectors)
├── recognize_video.py      # Nhận diện thời gian thực
│
├── dataset/                # Thư mục ảnh
│   ├── nguyen_van_a/
│   │   ├── nguyen_van_a_1.jpg
│   │   └── ...
│   └── tran_thi_b/
│       └── ...
│
└── encodings.pickle        # File encodings (sau khi train)
```

## 🎯 Hướng Dẫn Sử Dụng

### Bước 1: Thu thập dữ liệu

```bash
python collect_faces_dlib.py
```

- Nhập tên người cần đăng ký
- Nhấn **SPACE** để chụp ảnh
- Nhấn **'a'** để bật chế độ tự động
- Thu thập **20-50 ảnh** ở nhiều góc độ

**Tips để có độ chính xác cao:**
- Chụp ảnh ở nhiều góc: chính diện, nghiêng 15°, 30°, 45°
- Thay đổi ánh sáng
- Có và không có kính
- Biểu cảm khác nhau

### Bước 2: Tạo encodings

```bash
python encode_faces.py
```

Script sẽ:
- Đọc tất cả ảnh từ `dataset/`
- Phát hiện khuôn mặt bằng Dlib
- Trích xuất vector 128 chiều cho mỗi khuôn mặt
- Lưu vào `encodings.pickle`

### Bước 3: Nhận diện thời gian thực

```bash
python recognize_video.py
```

**Phím tắt:**
| Phím | Chức năng |
|------|-----------|
| `q` / `ESC` | Thoát |
| `s` | Chụp ảnh màn hình |
| `+` | Tăng tolerance |
| `-` | Giảm tolerance |

## ⚙️ Tùy Chỉnh

Chỉnh sửa file `config_dlib.py`:

### Ngưỡng Tolerance

```python
# Giá trị: 0.0 - 1.0
# Thấp = nghiêm ngặt (ít false positive, có thể miss người quen)
# Cao = dễ dãi (nhận đúng người quen hơn, nhưng có thể nhầm)

TOLERANCE = 0.5   # Mặc định, cân bằng
# TOLERANCE = 0.4   # Nghiêm ngặt (bảo mật cao)
# TOLERANCE = 0.6   # Dễ dãi (môi trường thân thiện)
```

### Phương pháp Detection

```python
# "hog": Nhanh, dùng CPU (khuyến nghị)
# "cnn": Chính xác hơn, cần GPU CUDA

DETECTION_METHOD = "hog"
```

### Tối ưu hiệu năng

```python
# Giảm kích thước frame để xử lý nhanh hơn
FRAME_RESIZE_SCALE = 0.25   # 1/4 kích thước

# Tăng số frame skip (detect ít hơn, nhanh hơn)
FRAME_SKIP = 2   # Detect mỗi 2 frame
```

## 📊 Giải Thích Thuật Toán

### Face Encoding (128D Vector)

face_recognition sử dụng Deep Learning model được huấn luyện trên hàng triệu khuôn mặt để tạo ra vector 128 chiều đại diện cho mỗi khuôn mặt.

**Đặc điểm:**
- Các vector của cùng một người sẽ gần nhau trong không gian 128D
- Các vector của người khác sẽ xa nhau
- Sử dụng khoảng cách Euclidean để so sánh

### So sánh khoảng cách

```
distance = ||encoding_1 - encoding_2||

if distance < tolerance:
    -> Cùng một người
else:
    -> Khác người
```

**Giá trị distance điển hình:**
- `< 0.4`: Rất giống (chắc chắn cùng người)
- `0.4 - 0.5`: Giống (có thể cùng người)
- `0.5 - 0.6`: Hơi giống (có thể cùng hoặc khác)
- `> 0.6`: Khác (gần như chắc chắn khác người)

## 🛠️ Xử Lý Lỗi

### Camera không mở được

```bash
# Kiểm tra camera
ls /dev/video*

# Kiểm tra quyền
sudo usermod -a -G video $USER
# (Đăng xuất và đăng nhập lại)
```

### FPS thấp

1. Giảm `FRAME_RESIZE_SCALE` xuống 0.2 hoặc thấp hơn
2. Tăng `FRAME_SKIP` lên 3-4
3. Dùng `DETECTION_METHOD = "hog"` thay vì `"cnn"`

### Nhận diện sai

1. Thu thập thêm ảnh ở nhiều điều kiện
2. Điều chỉnh `TOLERANCE`:
   - Hay nhận nhầm người lạ → Giảm tolerance
   - Hay không nhận ra người quen → Tăng tolerance
3. Chạy lại `encode_faces.py`

## 📝 So Sánh Chi Tiết

| Tiêu chí | OpenCV LBPH | face_recognition (Dlib) |
|----------|-------------|-------------------------|
| **Công nghệ** | Hand-crafted features | Deep Learning |
| **Vector size** | Histogram | 128D embedding |
| **Góc nghiêng** | Max ~15° | Max ~45° |
| **Ánh sáng** | Nhạy cảm | Robust |
| **Tốc độ detect** | ~30ms | ~100ms (HOG), ~300ms (CNN) |
| **Độ chính xác** | 60-75% | 95-99% |
| **Training** | Cần nhiều ảnh/người | Ít ảnh hơn (5-10 đủ) |

## 📜 License

MIT License
