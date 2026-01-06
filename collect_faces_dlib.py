#!/usr/bin/env python3
"""
Script bổ sung: Thu thập ảnh khuôn mặt cho dataset
Sử dụng face_recognition để detect chính xác hơn

Sử dụng: python collect_faces_dlib.py
"""
import os
import sys
import cv2
import face_recognition
from datetime import datetime
from config_dlib import (
    DATASET_DIR, DETECTION_METHOD,
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
)


def collect_faces():
    """Thu thập ảnh khuôn mặt từ webcam"""
    
    print("\n" + "="*60)
    print("    THU THẬP DỮ LIỆU KHUÔN MẶT")
    print("    Sử dụng: face_recognition (Dlib)")
    print("="*60)
    
    # Nhập thông tin
    person_name = input("\nNhập tên người (VD: nguyen_van_a): ").strip()
    if not person_name:
        print("[LỖI] Tên không được để trống!")
        return
    
    num_samples = input("Số ảnh cần thu thập (mặc định 30): ").strip()
    num_samples = int(num_samples) if num_samples.isdigit() else 30
    
    # Tạo thư mục
    person_dir = os.path.join(DATASET_DIR, person_name)
    os.makedirs(person_dir, exist_ok=True)
    
    # Đếm ảnh đã có
    existing = len([f for f in os.listdir(person_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
    print(f"[INFO] Đã có {existing} ảnh trong thư mục")
    
    # Mở webcam
    print(f"\n[INFO] Đang mở camera {CAMERA_INDEX}...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print("[LỖI] Không thể mở camera!")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    print("\n" + "-"*60)
    print("HƯỚNG DẪN:")
    print("  - Nhấn SPACE để chụp ảnh")
    print("  - Nhấn 'a' để bật/tắt chế độ tự động")
    print("  - Nhấn 'q' để thoát")
    print("  - Xoay mặt nhiều hướng để có dữ liệu tốt hơn")
    print("-"*60 + "\n")
    
    count = existing
    auto_capture = False
    auto_frame_count = 0
    
    while count < num_samples + existing:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        
        # Detect khuôn mặt
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model=DETECTION_METHOD)
        
        display = frame.copy()
        
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(display, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Auto capture
        if auto_capture and len(face_locations) == 1:
            auto_frame_count += 1
            if auto_frame_count % 10 == 0:  # Mỗi 10 frame
                top, right, bottom, left = face_locations[0]
                face_img = frame[top:bottom, left:right]
                if face_img.size > 0:
                    count += 1
                    img_path = os.path.join(person_dir, f"{person_name}_{count}.jpg")
                    cv2.imwrite(img_path, face_img)
                    print(f"[✓] Đã lưu ảnh {count}/{num_samples + existing}")
        
        # Hiển thị thông tin
        info = f"Nguoi: {person_name} | Anh: {count}/{num_samples + existing}"
        cv2.putText(display, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        mode = "Auto: ON" if auto_capture else "Auto: OFF"
        color = (0, 255, 0) if auto_capture else (0, 0, 255)
        cv2.putText(display, mode, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        if len(face_locations) == 0:
            cv2.putText(display, "Khong phat hien khuon mat!", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        cv2.imshow("Thu thap du lieu - Nhan 'q' de thoat", display)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:
            break
        elif key == ord('a'):
            auto_capture = not auto_capture
            auto_frame_count = 0
            print(f"[INFO] Chế độ tự động: {'BẬT' if auto_capture else 'TẮT'}")
        elif key == ord(' '):
            if len(face_locations) == 1:
                top, right, bottom, left = face_locations[0]
                face_img = frame[top:bottom, left:right]
                if face_img.size > 0:
                    count += 1
                    img_path = os.path.join(person_dir, f"{person_name}_{count}.jpg")
                    cv2.imwrite(img_path, face_img)
                    print(f"[✓] Đã lưu ảnh {count}/{num_samples + existing}")
            else:
                print("[!] Cần đúng 1 khuôn mặt trong khung hình!")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n[HOÀN TẤT] Đã thu thập {count - existing} ảnh mới")
    print(f"[INFO] Tổng số ảnh: {count}")
    print(f"\n[TIẾP THEO] Chạy: python encode_faces.py")


if __name__ == "__main__":
    collect_faces()
