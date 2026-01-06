#!/usr/bin/env python3
"""
Script 1: Trích xuất face encodings từ dataset
Tạo file encodings.pickle chứa vector 128 chiều cho mỗi khuôn mặt

Sử dụng: python encode_faces.py
"""
import os
import sys
import pickle
import cv2
import face_recognition
from datetime import datetime
from config_dlib import (
    DATASET_DIR, ENCODINGS_FILE, 
    DETECTION_METHOD, ENCODING_MODEL, NUM_JITTERS_TRAINING
)


def print_header():
    """In header"""
    print("\n" + "="*60)
    print("    TRÍCH XUẤT FACE ENCODINGS (128D VECTORS)")
    print("    Sử dụng: face_recognition (Dlib)")
    print("="*60)


def get_image_paths():
    """Lấy danh sách tất cả ảnh trong dataset"""
    image_paths = []
    
    if not os.path.exists(DATASET_DIR):
        print(f"[LỖI] Thư mục dataset không tồn tại: {DATASET_DIR}")
        return []
    
    for person_name in sorted(os.listdir(DATASET_DIR)):
        person_dir = os.path.join(DATASET_DIR, person_name)
        
        if not os.path.isdir(person_dir):
            continue
        
        for image_name in os.listdir(person_dir):
            if image_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                image_paths.append({
                    'path': os.path.join(person_dir, image_name),
                    'name': person_name
                })
    
    return image_paths


def encode_faces():
    """Trích xuất face encodings từ tất cả ảnh trong dataset"""
    
    print_header()
    
    # Lấy danh sách ảnh
    print("\n[INFO] Đang quét thư mục dataset...")
    image_data = get_image_paths()
    
    if not image_data:
        print("\n[LỖI] Không tìm thấy ảnh nào trong dataset!")
        print(f"      Hãy thêm ảnh vào thư mục: {DATASET_DIR}")
        print("      Cấu trúc: dataset/ten_nguoi/anh1.jpg, anh2.jpg, ...")
        return False
    
    # Thống kê
    person_counts = {}
    for item in image_data:
        name = item['name']
        person_counts[name] = person_counts.get(name, 0) + 1
    
    print(f"\n[INFO] Tìm thấy {len(image_data)} ảnh của {len(person_counts)} người:")
    for name, count in sorted(person_counts.items()):
        print(f"  - {name}: {count} ảnh")
    
    # Danh sách lưu encodings
    known_encodings = []
    known_names = []
    
    # Xử lý từng ảnh
    print(f"\n[INFO] Đang trích xuất encodings...")
    print(f"       Detection method: {DETECTION_METHOD}")
    print(f"       Encoding model: {ENCODING_MODEL}")
    print(f"       Num jitters: {NUM_JITTERS_TRAINING}")
    print("-"*60)
    
    start_time = datetime.now()
    success_count = 0
    fail_count = 0
    
    for i, item in enumerate(image_data, 1):
        image_path = item['path']
        name = item['name']
        
        # Hiển thị tiến độ
        progress = f"[{i}/{len(image_data)}]"
        print(f"{progress} Đang xử lý: {os.path.basename(image_path)}", end=" ")
        
        try:
            # Đọc ảnh (face_recognition sử dụng RGB)
            image = face_recognition.load_image_file(image_path)
            
            # Phát hiện khuôn mặt
            face_locations = face_recognition.face_locations(
                image, 
                model=DETECTION_METHOD
            )
            
            if len(face_locations) == 0:
                print("-> Không tìm thấy khuôn mặt!")
                fail_count += 1
                continue
            
            if len(face_locations) > 1:
                print(f"-> Cảnh báo: {len(face_locations)} khuôn mặt, lấy khuôn mặt đầu tiên")
            
            # Trích xuất encoding (128D vector)
            encodings = face_recognition.face_encodings(
                image,
                known_face_locations=face_locations,
                num_jitters=NUM_JITTERS_TRAINING,
                model=ENCODING_MODEL
            )
            
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(name)
                success_count += 1
                print("-> OK")
            else:
                print("-> Không thể trích xuất encoding!")
                fail_count += 1
                
        except Exception as e:
            print(f"-> Lỗi: {str(e)}")
            fail_count += 1
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print("-"*60)
    print(f"\n[THỐNG KÊ]")
    print(f"  - Thành công: {success_count}/{len(image_data)} ảnh")
    print(f"  - Thất bại: {fail_count}/{len(image_data)} ảnh")
    print(f"  - Thời gian: {elapsed:.2f} giây")
    print(f"  - Trung bình: {elapsed/len(image_data):.2f} giây/ảnh")
    
    if success_count == 0:
        print("\n[LỖI] Không có encoding nào được tạo!")
        return False
    
    # Lưu encodings vào file pickle
    print(f"\n[INFO] Đang lưu encodings vào {ENCODINGS_FILE}...")
    
    data = {
        "encodings": known_encodings,
        "names": known_names
    }
    
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)
    
    # Thống kê người đã đăng ký
    unique_names = list(set(known_names))
    
    print("\n" + "="*60)
    print("    HOÀN TẤT!")
    print("="*60)
    print(f"\n[✓] Đã lưu {len(known_encodings)} encodings của {len(unique_names)} người")
    print(f"[✓] File: {ENCODINGS_FILE}")
    
    print("\n[DANH SÁCH NGƯỜI ĐÃ ĐĂNG KÝ]")
    for name in sorted(unique_names):
        count = known_names.count(name)
        print(f"  - {name}: {count} encodings")
    
    print("\n[TIẾP THEO] Chạy: python recognize_video.py")
    
    return True


if __name__ == "__main__":
    encode_faces()
