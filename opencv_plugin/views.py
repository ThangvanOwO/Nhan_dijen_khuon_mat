"""
OpenCV Face Recognition Plugin - Views
Stream video với nhận diện khuôn mặt real-time qua web
"""
import os
import sys
import pickle
import cv2
import face_recognition
import numpy as np
from datetime import datetime
from collections import deque

from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators import gzip
from django.conf import settings

# Import config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config_dlib import (
    ENCODINGS_FILE, TOLERANCE, DETECTION_METHOD,
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT,
    FRAME_RESIZE_SCALE, FRAME_SKIP,
    COLOR_KNOWN, COLOR_UNKNOWN, COLOR_TEXT,
    FONT_SCALE, FONT_THICKNESS,
    ENHANCE_LIGHTING, CLAHE_CLIP_LIMIT, CLAHE_TILE_SIZE
)


class FaceRecognitionCamera:
    """Camera class với face recognition tích hợp"""
    
    def __init__(self):
        self.video = None
        self.known_encodings = []
        self.known_names = []
        self.frame_count = 0
        self.face_locations = []
        self.face_names = []
        self.face_confidences = []
        self.current_tolerance = TOLERANCE
        self.enhance_enabled = ENHANCE_LIGHTING
        self.last_recognized = {}  # Lưu người đã nhận diện để tránh spam (30s gần đây)
        self.session_recognized = {}  # Lưu TẤT CẢ người đã nhận diện trong cả session
        
        # Load encodings
        self._load_encodings()
    
    def _load_encodings(self):
        """Tải encodings từ file pickle"""
        encodings_path = os.path.join(BASE_DIR, 'encodings.pickle')
        
        if os.path.exists(encodings_path):
            with open(encodings_path, 'rb') as f:
                data = pickle.load(f)
            self.known_encodings = data['encodings']
            self.known_names = data['names']
            print(f"[INFO] Đã tải {len(self.known_encodings)} encodings của {len(set(self.known_names))} người")
        else:
            print(f"[WARNING] Không tìm thấy file encodings: {encodings_path}")
    
    def start(self):
        """Khởi động camera"""
        if self.video is None or not self.video.isOpened():
            self.video = cv2.VideoCapture(CAMERA_INDEX)
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            print(f"[INFO] Camera {CAMERA_INDEX} đã khởi động")
    
    def stop(self):
        """Dừng camera"""
        if self.video is not None:
            self.video.release()
            self.video = None
            print("[INFO] Camera đã đóng")
    
    def enhance_lighting(self, frame):
        """Cải thiện ánh sáng với CLAHE"""
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_TILE_SIZE)
        l_enhanced = clahe.apply(l)
        lab_enhanced = cv2.merge([l_enhanced, a, b])
        return cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    
    def recognize_face(self, face_encoding):
        """Nhận diện một khuôn mặt"""
        if len(self.known_encodings) == 0:
            return "Unknown", 0.0
        
        distances = face_recognition.face_distance(self.known_encodings, face_encoding)
        min_distance_idx = np.argmin(distances)
        min_distance = distances[min_distance_idx]
        
        if min_distance <= self.current_tolerance:
            name = self.known_names[min_distance_idx]
            confidence = (1 - min_distance) * 100
            if confidence < 50:
                return "Unknown", confidence
            return name, confidence
        else:
            return "Unknown", 0.0
    
    def get_frame(self):
        """Lấy frame từ camera với face recognition"""
        if self.video is None:
            self.start()
        
        ret, frame = self.video.read()
        if not ret:
            return None, []
        
        # Lật frame (như gương)
        frame = cv2.flip(frame, 1)
        
        # Xử lý detect mỗi N frame
        recognized_people = []
        process_this_frame = (self.frame_count % FRAME_SKIP == 0)
        
        if process_this_frame:
            # Cải thiện ánh sáng nếu bật
            if self.enhance_enabled:
                frame_to_process = self.enhance_lighting(frame)
            else:
                frame_to_process = frame
            
            # Resize frame
            small_frame = cv2.resize(frame_to_process, (0, 0), 
                                     fx=FRAME_RESIZE_SCALE, fy=FRAME_RESIZE_SCALE)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Phát hiện khuôn mặt
            self.face_locations = face_recognition.face_locations(
                rgb_small_frame, model=DETECTION_METHOD
            )
            
            # Trích xuất encodings và nhận diện
            face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
            
            self.face_names = []
            self.face_confidences = []
            
            for face_encoding in face_encodings:
                name, confidence = self.recognize_face(face_encoding)
                self.face_names.append(name)
                self.face_confidences.append(confidence)
                
                # Lưu người đã nhận diện (tránh spam)
                if name != "Unknown":
                    now = datetime.now()
                    # Lưu vào session_recognized (giữ suốt session)
                    if name not in self.session_recognized:
                        self.session_recognized[name] = now
                    
                    # Lưu vào last_recognized (chỉ 30s gần đây, để hiển thị UI)
                    if name not in self.last_recognized or \
                       (now - self.last_recognized[name]).seconds > 5:
                        self.last_recognized[name] = now
                        recognized_people.append({
                            'name': name,
                            'confidence': confidence,
                            'time': now.strftime('%H:%M:%S')
                        })
        
        # Vẽ kết quả lên frame
        for (top, right, bottom, left), name, confidence in zip(
            self.face_locations, self.face_names, self.face_confidences
        ):
            # Scale lại tọa độ
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
            
            # Vẽ khung và tên
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS
            )
            cv2.rectangle(frame, (left, top - text_height - 10),
                         (left + text_width + 10, top), color, -1)
            cv2.putText(frame, label, (left + 5, top - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, COLOR_TEXT, FONT_THICKNESS)
        
        # Hiển thị thông tin
        info_lines = [
            f"Faces: {len(self.face_locations)}",
            f"Tolerance: {self.current_tolerance:.2f}",
            f"Light: {'ON' if self.enhance_enabled else 'OFF'}"
        ]
        
        y_offset = 25
        for line in info_lines:
            cv2.putText(frame, line, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            y_offset += 25
        
        # Thời gian
        time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, time_text, (10, frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        
        self.frame_count += 1
        
        return frame, recognized_people


# Global camera instance
camera = None


def get_camera():
    """Lấy hoặc tạo camera instance"""
    global camera
    if camera is None:
        camera = FaceRecognitionCamera()
    return camera


def gen_frames():
    """Generator để stream video frames"""
    cam = get_camera()
    cam.start()
    
    while True:
        frame, _ = cam.get_frame()
        if frame is None:
            break
        
        # Encode frame thành JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not ret:
            continue
        
        frame_bytes = buffer.tobytes()
        
        # Yield frame theo định dạng multipart
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# =====================================================
# Views
# =====================================================

def camera_view(request):
    """Trang hiển thị camera với nhận diện"""
    context = {
        'tolerance': TOLERANCE,
        'detection_method': DETECTION_METHOD,
    }
    return render(request, 'opencv_plugin/camera.html', context)


@gzip.gzip_page
def video_feed(request):
    """Streaming video response"""
    return StreamingHttpResponse(
        gen_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


@require_http_methods(["POST"])
def set_tolerance(request):
    """API điều chỉnh tolerance"""
    import json
    try:
        data = json.loads(request.body)
        new_tolerance = float(data.get('tolerance', TOLERANCE))
        new_tolerance = max(0.1, min(1.0, new_tolerance))
        
        cam = get_camera()
        cam.current_tolerance = new_tolerance
        
        return JsonResponse({
            'success': True,
            'tolerance': new_tolerance
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST"])
def toggle_enhance(request):
    """API bật/tắt enhance lighting"""
    cam = get_camera()
    cam.enhance_enabled = not cam.enhance_enabled
    
    return JsonResponse({
        'success': True,
        'enhance_enabled': cam.enhance_enabled
    })


@require_http_methods(["GET"])
def get_recognized(request):
    """API lấy danh sách người đã nhận diện"""
    cam = get_camera()
    
    # Lấy những người được nhận diện trong 30 giây gần đây
    now = datetime.now()
    recent = []
    for name, time in cam.last_recognized.items():
        if (now - time).seconds < 30:
            recent.append({
                'name': name,
                'time': time.strftime('%H:%M:%S')
            })
    
    return JsonResponse({
        'success': True,
        'data': recent
    })


@require_http_methods(["GET"])
def get_all_recognized(request):
    """API lấy TẤT CẢ người đã nhận diện trong session (không giới hạn 30s)"""
    cam = get_camera()
    
    all_people = []
    for name, time in cam.last_recognized.items():
        all_people.append({
            'name': name,
            'time': time.strftime('%H:%M:%S'),
            'date': time.strftime('%Y-%m-%d')
        })
    
    # Sắp xếp theo thời gian
    all_people.sort(key=lambda x: x['time'])
    
    return JsonResponse({
        'success': True,
        'count': len(all_people),
        'data': all_people
    })


@require_http_methods(["POST"])
def end_session(request):
    """
    API kết thúc phiên điểm danh
    - Tạo/lấy Session (buổi học) cho ngày hôm nay
    - Lưu tất cả người đã nhận diện vào bảng Attendance
    - Dừng camera
    - Trả về danh sách đã lưu
    
    Ưu tiên: Session (buổi) → Class (lớp) → Student (học viên)
    """
    import json
    from django.utils import timezone
    from portal.models import Class, Student, Session, Attendance
    
    cam = get_camera()
    
    saved_records = []
    errors = []
    now = timezone.now()
    today = now.date()
    current_time = now.time()
    
    # Lấy thông tin lớp và buổi học từ request (nếu có)
    try:
        data = json.loads(request.body) if request.body else {}
    except:
        data = {}
    
    class_id = data.get('class_id', 'DEFAULT')
    session_type = data.get('session_type', 'morning')  # morning, afternoon, evening
    session_number = int(data.get('session_number', 1))
    session_topic = data.get('topic', '')
    
    # Map session_type sang tên tiếng Việt
    session_type_names = {
        'morning': 'Buổi sáng',
        'afternoon': 'Buổi chiều',
        'evening': 'Buổi tối'
    }
    session_type_name = session_type_names.get(session_type, 'Buổi học')
    
    # Tạo topic nếu không có
    if not session_topic:
        session_topic = f"{session_type_name} - Buổi {session_number}"
    
    # 1. Tìm hoặc tạo Lớp học (Class)
    class_obj, class_created = Class.objects.get_or_create(
        class_id=class_id,
        defaults={
            'name': f'Lớp {class_id}',
            'description': 'Lớp học tự động tạo từ hệ thống điểm danh',
            'is_active': True
        }
    )
    
    # 2. Tạo Session ID theo format: LOP_NGAY_BUOI_SO
    session_id = f"{class_id}_{today.strftime('%Y%m%d')}_{session_type}_{session_number}"
    
    # Tìm session đã có với cùng ID (cùng lớp, ngày, buổi, số thứ tự)
    existing_session = Session.objects.filter(session_id=session_id).first()
    
    if existing_session:
        session = existing_session
        session.status = 'completed'
        session.end_time = current_time
        session.session_number = session_number
        session.session_type = session_type
        session.save()
    else:
        session = Session.objects.create(
            session_id=session_id,
            class_obj=class_obj,
            session_number=session_number,
            session_type=session_type,
            date=today,
            start_time=current_time,
            end_time=current_time,
            topic=session_topic,
            status='completed',
            notes=f"Loại: {session_type_name}, Buổi số: {session_number}"
        )
    
    # 3. Lưu điểm danh cho từng người đã nhận diện trong session
    # Sử dụng session_recognized (lưu tất cả người trong cả session) thay vì last_recognized
    people_to_save = cam.session_recognized if cam.session_recognized else cam.last_recognized
    
    for name, rec_time in people_to_save.items():
        try:
            # Tìm hoặc tạo Student
            student, student_created = Student.objects.get_or_create(
                student_id=name,
                defaults={
                    'full_name': name,
                    'class_obj': class_obj,
                    'face_data': f'dataset/{name}/',
                    'is_registered': True
                }
            )
            
            # Nếu student chưa có lớp, gán vào lớp hiện tại
            if not student.class_obj:
                student.class_obj = class_obj
                student.save()
            
            # Tạo bản ghi điểm danh (Attendance)
            attendance, att_created = Attendance.objects.get_or_create(
                session=session,
                student=student,
                defaults={
                    'status': 'present',
                    'check_in_time': rec_time.time(),
                    'confidence': 95.0,
                    'camera_id': 'CAM01'
                }
            )
            
            if not att_created:
                # Đã điểm danh rồi, cập nhật check_out_time
                attendance.check_out_time = rec_time.time()
                attendance.save()
            
            saved_records.append({
                'name': name,
                'student_id': student.student_id,
                'class_name': class_obj.name,
                'session_id': session.session_id,
                'check_in': attendance.check_in_time.strftime('%H:%M:%S') if attendance.check_in_time else None,
                'status': attendance.status,
                'created': att_created
            })
            
        except Exception as e:
            errors.append({
                'name': name,
                'error': str(e)
            })
    
    # Dừng camera và reset session
    global camera
    if camera is not None:
        camera.session_recognized = {}  # Reset session data
        camera.last_recognized = {}
        camera.stop()
        camera = None
    
    return JsonResponse({
        'success': True,
        'message': f'Đã lưu {len(saved_records)} bản ghi điểm danh',
        'date': str(today),
        'session': {
            'id': session.session_id,
            'class': class_obj.name,
            'topic': session.topic,
            'attendance_count': session.get_attendance_count(),
            'attendance_rate': session.get_attendance_rate()
        },
        'saved': saved_records,
        'errors': errors
    })


def stop_camera(request):
    """Dừng camera"""
    global camera
    if camera is not None:
        camera.stop()
        camera = None
    return JsonResponse({'success': True, 'message': 'Camera stopped'})
