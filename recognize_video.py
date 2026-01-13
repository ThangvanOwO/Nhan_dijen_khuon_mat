#!/usr/bin/env python3
"""
Script 2: Nhận diện khuôn mặt thời gian thực từ webcam
Sử dụng face_recognition (Dlib) với encodings đã được trích xuất

Sử dụng: python recognize_video.py
"""
import os
import sys
import pickle
import shutil
import cv2
import face_recognition
import numpy as np
from datetime import datetime
from collections import deque
from config_dlib import (
    DATASET_DIR,
    ENCODINGS_FILE, TOLERANCE, DETECTION_METHOD,
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT,
    FRAME_RESIZE_SCALE, FRAME_SKIP,
    COLOR_KNOWN, COLOR_UNKNOWN, COLOR_TEXT,
    FONT_SCALE, FONT_THICKNESS,
    ENHANCE_LIGHTING, CLAHE_CLIP_LIMIT, CLAHE_TILE_SIZE
)


class FPSCounter:
    """Đếm FPS với smoothing"""
    
    def __init__(self, window_size=30):
        self.timestamps = deque(maxlen=window_size)
    
    def tick(self):
        self.timestamps.append(datetime.now())
    
    def get_fps(self):
        if len(self.timestamps) < 2:
            return 0.0
        
        elapsed = (self.timestamps[-1] - self.timestamps[0]).total_seconds()
        if elapsed <= 0:
            return 0.0
        
        return (len(self.timestamps) - 1) / elapsed


def enhance_lighting(frame):
    """
    Cải thiện ánh sáng cho ảnh quá sáng hoặc quá tối
    Sử dụng CLAHE (Contrast Limited Adaptive Histogram Equalization)
    
    Args:
        frame: Ảnh BGR từ OpenCV
    
    Returns:
        Ảnh đã được cân bằng ánh sáng (vẫn là BGR)
    """
    # Chuyển sang LAB color space
    # L = Lightness, A = Green-Red, B = Blue-Yellow
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    # Tách các kênh
    l, a, b = cv2.split(lab)
    
    # Áp dụng CLAHE chỉ lên kênh L (lightness)
    # clipLimit: giới hạn contrast (2.0-3.0 thường tốt)
    # tileGridSize: kích thước vùng xử lý
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_TILE_SIZE)
    l_enhanced = clahe.apply(l)
    
    # Ghép lại các kênh
    lab_enhanced = cv2.merge([l_enhanced, a, b])
    
    # Chuyển về BGR
    enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    
    return enhanced


def load_encodings():
    """Tải encodings đã lưu từ file pickle"""
    
    if not os.path.exists(ENCODINGS_FILE):
        print(f"[LỖI] Không tìm thấy file encodings: {ENCODINGS_FILE}")
        print("      Hãy chạy: python encode_faces.py")
        return None, None
    
    print(f"[INFO] Đang tải encodings từ {ENCODINGS_FILE}...")
    
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
    
    encodings = data["encodings"]
    names = data["names"]
    
    unique_names = list(set(names))
    print(f"[INFO] Đã tải {len(encodings)} encodings của {len(unique_names)} người")
    
    return encodings, names


def recognize_face(face_encoding, known_encodings, known_names, tolerance):
    """
    Nhận diện một khuôn mặt
    
    Args:
        face_encoding: Vector 128D của khuôn mặt cần nhận diện
        known_encodings: List các encodings đã biết
        known_names: List tên tương ứng
        tolerance: Ngưỡng khoảng cách (thấp = nghiêm ngặt)
    
    Returns:
        (name, confidence): Tên và độ tin cậy (1 - distance)
    """
    
    if len(known_encodings) == 0:
        return "Unknown", 0.0
    
    # Tính khoảng cách Euclidean tới tất cả encodings đã biết
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    
    # Tìm khoảng cách nhỏ nhất
    min_distance_idx = np.argmin(distances)
    min_distance = distances[min_distance_idx]
    
    # Kiểm tra ngưỡng
    if min_distance <= tolerance:
        name = known_names[min_distance_idx]
        # Chuyển distance thành confidence (0-100%)
        confidence = (1 - min_distance) * 100
        # Nếu confidence < 50% thì coi như Unknown
        if confidence < 50:
            return "Unknown", confidence
        return name, confidence
    else:
        return "Unknown", 0.0


def print_header():
    """In header"""
    print("\n" + "="*60)
    print("    NHẬN DIỆN KHUÔN MẶT THỜI GIAN THỰC")
    print("    Sử dụng: face_recognition (Dlib)")
    print("="*60)


def delete_person_data(person_name):
    """Xóa dữ liệu của một người khỏi dataset và cập nhật encodings"""
    person_dir = os.path.join(DATASET_DIR, person_name)
    
    if not os.path.exists(person_dir):
        print(f"[!] Không tìm thấy thư mục: {person_name}")
        return False
    
    # Xóa thư mục ảnh
    try:
        shutil.rmtree(person_dir)
        print(f"[✓] Đã xóa thư mục: {person_dir}")
    except Exception as e:
        print(f"[LỖI] Không thể xóa thư mục: {e}")
        return False
    
    # Cập nhật file encodings
    if os.path.exists(ENCODINGS_FILE):
        try:
            with open(ENCODINGS_FILE, "rb") as f:
                data = pickle.load(f)
            
            # Lọc bỏ encodings của người bị xóa
            new_encodings = []
            new_names = []
            removed_count = 0
            
            for enc, name in zip(data["encodings"], data["names"]):
                if name != person_name:
                    new_encodings.append(enc)
                    new_names.append(name)
                else:
                    removed_count += 1
            
            # Lưu lại
            with open(ENCODINGS_FILE, "wb") as f:
                pickle.dump({"encodings": new_encodings, "names": new_names}, f)
            
            print(f"[✓] Đã xóa {removed_count} encodings của {person_name}")
            return True
        except Exception as e:
            print(f"[LỖI] Không thể cập nhật encodings: {e}")
            return False
    
    return True


def print_instructions():
    """In hướng dẫn"""
    print("\n" + "-"*60)
    print("HƯỚNG DẪN:")
    print("  - Nhấn 'q' hoặc ESC để thoát")
    print("  - Nhấn 's' để chụp ảnh màn hình")
    print("  - Nhấn 'd' để xóa người đang nhận diện")
    print("  - Nhấn '+' để tăng tolerance")
    print("  - Nhấn '-' để giảm tolerance")
    print("  - Nhấn 'l' để bật/tắt cải thiện ánh sáng")
    print("-"*60)
    print(f"\nCẤU HÌNH:")
    print(f"  - Tolerance: {TOLERANCE}")
    print(f"  - Detection: {DETECTION_METHOD}")
    print(f"  - Frame scale: {FRAME_RESIZE_SCALE}")
    print(f"  - Frame skip: {FRAME_SKIP}")
    print(f"  - Light Enhance: {'ON' if ENHANCE_LIGHTING else 'OFF'}")
    print("-"*60 + "\n")


def run_recognition():
    """Chạy nhận diện khuôn mặt từ webcam"""
    
    print_header()
    
    # Tải encodings
    known_encodings, known_names = load_encodings()
    
    if known_encodings is None:
        return
    
    # Mở webcam
    print(f"\n[INFO] Đang mở camera {CAMERA_INDEX}...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print("[LỖI] Không thể mở camera!")
        print("      Thử đổi CAMERA_INDEX trong config_dlib.py")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    print_instructions()
    
    # Khởi tạo FPS counter
    fps_counter = FPSCounter()
    
    # Biến lưu kết quả detect (để giữ giữa các frame skip)
    face_locations = []
    face_names = []
    face_confidences = []
    
    # Người đang được chọn để xóa
    selected_person = None
    
    # Tolerance có thể điều chỉnh runtime
    current_tolerance = TOLERANCE
    
    # Biến bật/tắt enhance lighting runtime
    enhance_enabled = ENHANCE_LIGHTING
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[LỖI] Không thể đọc frame từ camera!")
            break
        
        # Lật frame (như gương)
        frame = cv2.flip(frame, 1)
        
        # Chỉ xử lý detect mỗi N frame
        process_this_frame = (frame_count % FRAME_SKIP == 0)
        
        if process_this_frame:
            # Cải thiện ánh sáng nếu được bật
            if enhance_enabled:
                frame_to_process = enhance_lighting(frame)
            else:
                frame_to_process = frame
            
            # Resize frame để xử lý nhanh hơn
            small_frame = cv2.resize(frame_to_process, (0, 0), fx=FRAME_RESIZE_SCALE, fy=FRAME_RESIZE_SCALE)
            
            # Chuyển từ BGR (OpenCV) sang RGB (face_recognition)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Phát hiện khuôn mặt
            face_locations = face_recognition.face_locations(
                rgb_small_frame,
                model=DETECTION_METHOD
            )
            
            # Trích xuất encodings
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            # Nhận diện từng khuôn mặt
            face_names = []
            face_confidences = []
            
            for face_encoding in face_encodings:
                name, confidence = recognize_face(
                    face_encoding, 
                    known_encodings, 
                    known_names, 
                    current_tolerance
                )
                face_names.append(name)
                face_confidences.append(confidence)
        
        # Vẽ kết quả lên frame gốc
        for (top, right, bottom, left), name, confidence in zip(face_locations, face_names, face_confidences):
            # Scale lại tọa độ về kích thước gốc
            top = int(top / FRAME_RESIZE_SCALE)
            right = int(right / FRAME_RESIZE_SCALE)
            bottom = int(bottom / FRAME_RESIZE_SCALE)
            left = int(left / FRAME_RESIZE_SCALE)
            
            # Chọn màu
            if name == "Unknown":
                color = COLOR_UNKNOWN
                label = "Unknown"
            else:
                color = COLOR_KNOWN
                label = f"{name} ({confidence:.1f}%)"
            
            # Vẽ khung
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Vẽ background cho text
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS
            )
            
            cv2.rectangle(
                frame,
                (left, top - text_height - 10),
                (left + text_width + 10, top),
                color, -1
            )
            
            # Vẽ tên
            cv2.putText(
                frame, label,
                (left + 5, top - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SCALE, COLOR_TEXT, FONT_THICKNESS
            )
        
        # Tính FPS
        fps_counter.tick()
        fps = fps_counter.get_fps()
        
        # Hiển thị thông tin
        enhance_status = "ON" if enhance_enabled else "OFF"
        info_lines = [
            f"FPS: {fps:.1f}",
            f"Faces: {len(face_locations)}",
            f"Tolerance: {current_tolerance:.2f}",
            f"Method: {DETECTION_METHOD.upper()}",
            f"Light Enhance: {enhance_status}"
        ]
        
        y_offset = 25
        for line in info_lines:
            cv2.putText(
                frame, line,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 255, 255), 2
            )
            y_offset += 25
        
        # Hiển thị thời gian
        time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(
            frame, time_text,
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, COLOR_TEXT, 1
        )
        
        # Hiển thị frame
        cv2.imshow("Face Recognition - Nhan 'q' de thoat", frame)
        
        frame_count += 1
        
        # Xử lý phím nhấn
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:  # q hoặc ESC
            break
        
        elif key == ord('s'):  # Chụp ảnh
            screenshot_name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(screenshot_name, frame)
            print(f"[✓] Đã lưu: {screenshot_name}")
        
        elif key == ord('+') or key == ord('='):  # Tăng tolerance
            current_tolerance = min(current_tolerance + 0.05, 1.0)
            print(f"[INFO] Tolerance: {current_tolerance:.2f}")
        
        elif key == ord('-'):  # Giảm tolerance
            current_tolerance = max(current_tolerance - 0.05, 0.1)
            print(f"[INFO] Tolerance: {current_tolerance:.2f}")
        
        elif key == ord('l'):  # Bật/tắt enhance lighting
            enhance_enabled = not enhance_enabled
            status = "BẬT" if enhance_enabled else "TẮT"
            print(f"[INFO] Cải thiện ánh sáng: {status}")
        
        elif key == ord('d'):  # Xóa người đang nhận diện
            # Tìm người đang được nhận diện (không phải Unknown)
            known_faces = [name for name in face_names if name != "Unknown"]
            if known_faces:
                person_to_delete = known_faces[0]  # Lấy người đầu tiên
                print(f"\n[?] Bạn có muốn xóa '{person_to_delete}'? Nhấn 'y' để xác nhận, phím khác để hủy.")
                confirm_key = cv2.waitKey(0) & 0xFF
                if confirm_key == ord('y'):
                    if delete_person_data(person_to_delete):
                        # Tải lại encodings
                        known_encodings, known_names = load_encodings()
                        if known_encodings is None:
                            known_encodings = []
                            known_names = []
                        print(f"[✓] Đã xóa và tải lại dữ liệu!")
                else:
                    print("[INFO] Đã hủy xóa.")
            else:
                print("[!] Không có người nào đang được nhận diện để xóa.")
    
    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n[INFO] Đã đóng chương trình.")


if __name__ == "__main__":
    run_recognition()
