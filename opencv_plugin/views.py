"""
OpenCV Face Recognition Plugin - Views
































































































































































































































































































































































































































































































































































































{% endblock %}</script>    });        }            clearInterval(autoCaptureInterval);        if (autoCaptureInterval) {    window.addEventListener('beforeunload', function() {    // Cleanup on page leave        }        setTimeout(() => toast.remove(), 3000);        document.body.appendChild(toast);        toast.textContent = message;        toast.className = `fixed bottom-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-xl shadow-lg z-[200] animate-fade-in`;        };            'info': 'bg-blue-500'            'error': 'bg-red-500',            'success': 'bg-green-500',        const colors = {        const toast = document.createElement('div');    function showToast(message, type = 'info') {        }        `;            </button>                Encode Faces Now                <span class="material-symbols-outlined align-middle">memory</span>                    onclick="runEncode()">            <button id="btnEncode" class="w-full py-3 px-6 bg-gradient-to-r from-yellow-600 to-orange-600 rounded-xl font-bold hover:from-yellow-500 hover:to-orange-500 transition-all"            <p class="text-sm text-yellow-400 mb-3">⚠️ Cần encode để cập nhật vào hệ thống nhận diện</p>        document.getElementById('encodeSection').innerHTML = `        document.getElementById('encodeSection').classList.add('hidden');        // Reset encode section                document.getElementById('btnSave').innerHTML = '<span class="material-symbols-outlined">save</span> Hoàn tất đăng ký';        document.getElementById('btnSave').disabled = true;        updateProgress();        `;            </div>                Chưa có ảnh nào            <div class="text-center text-slate-500 py-4 col-span-full">        document.getElementById('capturedGrid').innerHTML = `        capturedImages = [];        document.getElementById('phone').value = '';        document.getElementById('email').value = '';        document.getElementById('classId').value = '';        document.getElementById('fullName').value = '';        document.getElementById('studentId').value = '';        // Reset form                document.getElementById('resultModal').classList.remove('flex');        document.getElementById('resultModal').classList.add('hidden');    function closeModal() {        }        });            btn.disabled = false;            btn.innerHTML = `<span class="text-red-400">✗ Lỗi: ${error}</span>`;        .catch(error => {        })            }                btn.disabled = false;                btn.innerHTML = `<span class="text-red-400">✗ Lỗi: ${data.error}</span>`;            } else {                `;                    </div>                        <p class="text-sm text-slate-400 mt-1">Bạn có thể sử dụng camera nhận diện ngay.</p>                        <p class="text-green-400">✓ Đã encode và cập nhật vào hệ thống!</p>                    <div class="p-4 bg-green-500/10 rounded-xl">                document.getElementById('encodeSection').innerHTML = `            if (data.success) {        .then(data => {        .then(response => response.json())        })            }                'X-CSRFToken': '{{ csrf_token }}'                'Content-Type': 'application/json',            headers: {            method: 'POST',        fetch('{% url "opencv_plugin:encode_faces" %}', {                btn.innerHTML = '<span class="material-symbols-outlined animate-spin">progress_activity</span> Đang encode...';        btn.disabled = true;        const btn = document.getElementById('btnEncode');    function runEncode() {        }        });            btn.innerHTML = '<span class="material-symbols-outlined">save</span> Hoàn tất đăng ký';            btn.disabled = false;            showToast('Lỗi: ' + error, 'error');        .catch(error => {        })            }                btn.innerHTML = '<span class="material-symbols-outlined">save</span> Hoàn tất đăng ký';                btn.disabled = false;                showToast('Lỗi: ' + data.error, 'error');            } else {                document.getElementById('resultModal').classList.add('flex');                document.getElementById('resultModal').classList.remove('hidden');                document.getElementById('encodeSection').classList.remove('hidden');                document.getElementById('resultMessage').textContent = data.message;                document.getElementById('resultTitle').textContent = 'Đăng ký thành công!';            if (data.success) {        .then(data => {        .then(response => response.json())        })            })                phone: phone                email: email,                class_id: classId,                full_name: fullName,                student_id: studentId,            body: JSON.stringify({            },                'X-CSRFToken': '{{ csrf_token }}'                'Content-Type': 'application/json',            headers: {            method: 'POST',        fetch('{% url "opencv_plugin:save_registration" %}', {                btn.innerHTML = '<span class="material-symbols-outlined animate-spin">progress_activity</span> Đang lưu...';        btn.disabled = true;        const btn = document.getElementById('btnSave');                }            return;            showToast('Vui lòng nhập đầy đủ mã SV và họ tên!', 'error');        if (!studentId || !fullName) {                const phone = document.getElementById('phone').value.trim();        const email = document.getElementById('email').value.trim();        const classId = document.getElementById('classId').value.trim();        const fullName = document.getElementById('fullName').value.trim();        const studentId = document.getElementById('studentId').value.trim();                }            toggleAutoCapture();  // Turn off auto        if (autoCapture) {    function saveRegistration() {        }        showToast('Đã xóa tất cả ảnh đã chụp', 'info');        updateProgress();        `;            </div>                Chưa có ảnh nào            <div class="text-center text-slate-500 py-4 col-span-full">        document.getElementById('capturedGrid').innerHTML = `        capturedImages = [];                }            toggleAutoCapture();  // Turn off auto        if (autoCapture) {    function resetCaptures() {        }        }            showToast('Tự động chụp: TẮT', 'info');            }                autoCaptureInterval = null;                clearInterval(autoCaptureInterval);            if (autoCaptureInterval) {            toggle.classList.remove('active');        } else {            showToast('Tự động chụp: BẬT', 'info');            autoCaptureInterval = setInterval(capturePhoto, 500);  // Mỗi 0.5 giây            toggle.classList.add('active');        if (autoCapture) {                const toggle = document.getElementById('autoToggle');        autoCapture = !autoCapture;    function toggleAutoCapture() {        }        });            showToast('Lỗi: ' + error, 'error');            btn.classList.remove('capturing');        .catch(error => {        })            }                showToast(data.error, 'error');            } else {                showToast(`✓ Ảnh ${data.count}`, 'success');                addCapturedImage(data.image);            if (data.success) {                        btn.classList.remove('capturing');        .then(data => {        .then(response => response.json())        })            body: JSON.stringify({ person_name: personName })            },                'X-CSRFToken': '{{ csrf_token }}'                'Content-Type': 'application/json',            headers: {            method: 'POST',        fetch('{% url "opencv_plugin:capture_face" %}', {                btn.classList.add('capturing');        const btn = document.getElementById('captureBtn');                }            return;            document.getElementById('studentId').focus();            showToast('Vui lòng nhập mã học viên trước!', 'error');        if (!personName || personName === 'unknown') {        const personName = getPersonName();    function capturePhoto() {        }        updateProgress();                grid.scrollTop = grid.scrollHeight;        // Scroll to bottom                grid.appendChild(item);        item.innerHTML = `<img src="${imageData}" alt="Face ${capturedImages.length}">`;        item.className = 'captured-item';        const item = document.createElement('div');                }            grid.innerHTML = '';        if (capturedImages.length === 1) {        // Remove placeholder if first image                const grid = document.getElementById('capturedGrid');                capturedImages.push(imageData);    function addCapturedImage(imageData) {        }        document.getElementById('btnSave').disabled = count < 5;        // Enable save button if enough images                document.getElementById('captureCount').textContent = count;        document.getElementById('progressFill').style.width = `${Math.min(100, (count / MIN_SAMPLES) * 100)}%`;        document.getElementById('progressText').textContent = `${count} / ${MIN_SAMPLES}`;        const count = capturedImages.length;    function updateProgress() {        }        return document.getElementById('studentId').value.trim() || 'unknown';    function getPersonName() {        let autoCaptureInterval = null;    let autoCapture = false;    let capturedImages = [];    const MIN_SAMPLES = {{ min_samples }};<script>{% block extra_js %}{% endblock %}</div>    </div>        </div>            </button>                Đăng ký tiếp            <button onclick="closeModal()" class="flex-1 py-3 px-6 bg-green-600 hover:bg-green-500 rounded-xl font-bold transition-colors">            </a>                Trang chủ            <a href="{% url 'portal:home' %}" class="flex-1 py-3 px-6 bg-slate-700 hover:bg-slate-600 rounded-xl font-bold transition-colors">        <div class="flex gap-4">                </div>            </button>                Encode Faces Now                <span class="material-symbols-outlined align-middle">memory</span>                    onclick="runEncode()">            <button id="btnEncode" class="w-full py-3 px-6 bg-gradient-to-r from-yellow-600 to-orange-600 rounded-xl font-bold hover:from-yellow-500 hover:to-orange-500 transition-all"            <p class="text-sm text-yellow-400 mb-3">⚠️ Cần encode để cập nhật vào hệ thống nhận diện</p>        <div id="encodeSection" class="mb-6 hidden">                <p id="resultMessage" class="text-slate-400 mb-6"></p>        <h2 id="resultTitle" class="text-2xl font-bold mb-2">Đăng ký thành công!</h2>        </div>            <span class="material-symbols-outlined text-green-400 text-4xl">check_circle</span>        <div id="resultIcon" class="w-20 h-20 rounded-full bg-green-500/20 flex items-center justify-center mx-auto mb-4">    <div class="glass-card max-w-md w-full p-8 rounded-3xl text-center"><div id="resultModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-[100] hidden items-center justify-center p-4"><!-- Result Modal --></main>    </div>        </div>            </div>                </div>                    </button>                        Hoàn tất đăng ký                        <span class="material-symbols-outlined">save</span>                            onclick="saveRegistration()" disabled>                    <button id="btnSave" class="flex-1 py-3 px-6 bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl font-bold hover:from-green-500 hover:to-emerald-500 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"                                        </button>                        Làm mới                        <span class="material-symbols-outlined">refresh</span>                            onclick="resetCaptures()">                    <button id="btnReset" class="flex-1 py-3 px-6 bg-slate-700 hover:bg-slate-600 rounded-xl font-bold transition-colors flex items-center justify-center gap-2"                <div class="flex gap-4 mt-4">                <!-- Action buttons -->                                </div>                    </div>                        </div>                            Chưa có ảnh nào                        <div class="text-center text-slate-500 py-4 col-span-full">                    <div id="capturedGrid" class="captured-grid">                    </h3>                        Ảnh đã chụp (<span id="captureCount">0</span>)                        <span class="material-symbols-outlined text-green-400">collections</span>                    <h3 class="text-sm font-semibold mb-3 flex items-center gap-2">                <div class="glass-card rounded-xl p-4 mt-4">                <!-- Captured faces grid -->                                </div>                    </div>                        <div id="progressFill" class="progress-fill" style="width: 0%"></div>                    <div class="progress-bar">                    </div>                        <span id="progressText" class="text-sm font-bold text-green-400">0 / {{ min_samples }}</span>                        <span class="text-sm text-slate-400">Tiến độ thu thập</span>                    <div class="flex items-center justify-between mb-2">                <div class="glass-card rounded-xl p-4 mt-4">                <!-- Progress -->                                </div>                    </button>                        <span class="material-symbols-outlined text-white text-3xl">photo_camera</span>                    <button id="captureBtn" class="capture-btn" onclick="capturePhoto()">                                        <img id="cameraFeed" class="camera-feed" src="{% url 'opencv_plugin:register_feed' %}" alt="Camera">                <div class="camera-container">            <div class="lg:col-span-2">            <!-- Center: Camera -->                        </div>                </div>                    <p class="text-xs text-slate-500 mt-2">Tự động chụp mỗi 0.5 giây khi phát hiện khuôn mặt</p>                    </div>                        <span>Tự động chụp</span>                        <div id="autoToggle" class="toggle-switch"></div>                    <div class="auto-capture-toggle" onclick="toggleAutoCapture()">                <div class="mt-6">                <!-- Auto capture toggle -->                                </div>                    </div>                               placeholder="VD: 0901234567">                        <input type="tel" id="phone" class="form-input"                         <label class="form-label">Số điện thoại</label>                    <div>                                        </div>                               placeholder="VD: email@example.com">                        <input type="email" id="email" class="form-input"                         <label class="form-label">Email</label>                    <div>                                        </div>                               placeholder="VD: 24CDTH41" value="{{ class_id }}">                        <input type="text" id="classId" class="form-input"                         <label class="form-label">Lớp học</label>                    <div>                                        </div>                               placeholder="VD: Nguyễn Văn A" value="{{ full_name }}" required>                        <input type="text" id="fullName" class="form-input"                         <label class="form-label">Họ và tên *</label>                    <div>                                        </div>                        <p class="text-xs text-slate-500 mt-1">Dùng làm tên thư mục lưu ảnh</p>                               placeholder="VD: nguyen_van_a" value="{{ student_id }}" required>                        <input type="text" id="studentId" class="form-input"                         <label class="form-label">Mã học viên / Tên thư mục *</label>                    <div>                <div class="space-y-4">                                </h2>                    Thông Tin Học Viên                    <span class="material-symbols-outlined text-green-400">person</span>                <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">            <div class="glass-card rounded-2xl p-6">            <!-- Left: Form thông tin -->        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">                </div>            <p class="text-slate-400">Chụp ít nhất {{ min_samples }} ảnh để đăng ký khuôn mặt mới</p>            <h1 class="text-3xl font-bold mb-2">📸 Thu Thập Khuôn Mặt</h1>        <div class="text-center mb-6">    <div class="max-w-6xl mx-auto"><main class="relative z-10 flex-1 p-4 lg:p-8 overflow-y-auto"><!-- Main Content --></header>    </div>        </div>            <span class="text-xs font-medium text-green-400 uppercase tracking-wider">Đăng ký khuôn mặt</span>            <span class="material-symbols-outlined text-green-400">person_add</span>        <div class="flex items-center gap-2 px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-full">    <div class="flex items-center gap-4">    </a>        <span class="font-bold text-sm tracking-wide">Trang chủ</span>        <span class="material-symbols-outlined text-green-400 group-hover:scale-110 transition-transform">arrow_back</span>    <a href="{% url 'portal:home' %}" class="flex items-center gap-3 glass-card px-4 py-2 rounded-full hover:border-green-500/30 transition-all duration-300 group"><header class="relative z-50 flex items-center justify-between px-6 py-4 lg:px-12 w-full max-w-7xl mx-auto"><!-- Top Navigation --></div>    <div class="absolute -bottom-40 right-0 w-[500px] h-[500px] bg-emerald-600/20 rounded-full mix-blend-screen filter blur-[100px] opacity-60 animate-blob delay-200"></div>    <div class="absolute top-0 -left-40 w-[600px] h-[600px] bg-green-600/20 rounded-full mix-blend-screen filter blur-[100px] opacity-70 animate-blob"></div><div class="fixed inset-0 overflow-hidden pointer-events-none z-0"><!-- Ambient Background -->{% block content %}{% endblock %}</style>    }        left: 26px;    .toggle-switch.active::after {        }        transition: left 0.3s;        left: 2px;        top: 2px;        border-radius: 50%;        background: white;        height: 22px;        width: 22px;        position: absolute;        content: '';    .toggle-switch::after {        }        background: #22c55e;    .toggle-switch.active {        }        transition: background 0.3s;        position: relative;        border-radius: 13px;        background: #475569;        height: 26px;        width: 50px;    .toggle-switch {        }        cursor: pointer;        border-radius: 12px;        background: rgba(30, 41, 59, 0.8);        padding: 10px 16px;        gap: 10px;        align-items: center;        display: flex;    .auto-capture-toggle {        }        margin-bottom: 6px;        color: #94a3b8;        font-size: 14px;        display: block;    .form-label {        }        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.2);        border-color: #22c55e;    .form-input:focus {        }        transition: all 0.3s;        outline: none;        font-size: 14px;        color: white;        border-radius: 12px;        border: 1px solid rgba(255,255,255,0.1);        background: rgba(30, 41, 59, 0.8);        padding: 12px 16px;        width: 100%;    .form-input {        }        transition: width 0.3s;        background: linear-gradient(90deg, #22c55e, #4ade80);        height: 100%;    .progress-fill {        }        overflow: hidden;        border-radius: 5px;        background: rgba(255,255,255,0.1);        height: 10px;        width: 100%;    .progress-bar {        }        object-fit: cover;        height: 100%;        width: 100%;    .captured-item img {        }        border: 2px solid rgba(34, 197, 94, 0.5);        overflow: hidden;        border-radius: 10px;        height: 80px;        width: 80px;    .captured-item {        }        padding: 10px;        overflow-y: auto;        max-height: 200px;        gap: 8px;        grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));        display: grid;    .captured-grid {        }        50% { transform: translateX(-50%) scale(1.2); }        0%, 100% { transform: translateX(-50%) scale(1); }    @keyframes pulse {        }        animation: pulse 0.5s ease-in-out;        background: linear-gradient(135deg, #ef4444, #dc2626);    .capture-btn.capturing {        }        transform: translateX(-50%) scale(0.95);    .capture-btn:active {        }        box-shadow: 0 6px 30px rgba(34, 197, 94, 0.7);        transform: translateX(-50%) scale(1.1);    .capture-btn:hover {        }        box-shadow: 0 4px 20px rgba(34, 197, 94, 0.5);        transition: all 0.3s;        justify-content: center;        align-items: center;        display: flex;        cursor: pointer;        border: 4px solid white;        background: linear-gradient(135deg, #22c55e, #16a34a);        border-radius: 50%;        height: 80px;        width: 80px;        transform: translateX(-50%);        left: 50%;        bottom: 20px;        position: absolute;    .capture-btn {        }        display: block;        height: auto;        width: 100%;    .camera-feed {        }        border: 2px solid rgba(34, 197, 94, 0.3);        background: #1a1a2e;        overflow: hidden;        border-radius: 20px;        margin: 0 auto;        max-width: 720px;        width: 100%;        position: relative;    .camera-container {<style>{% block extra_css %}{% block title %}Đăng Ký Khuôn Mặt - Face Recognition{% endblock %}Stream video với nhận diện khuôn mặt real-time qua web
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
    
    # Lấy giờ LOCAL (giờ Việt Nam) thay vì UTC
    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc)  # Convert sang giờ local (Asia/Ho_Chi_Minh)
    today = now_local.date()
    current_time = now_local.time()
    
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


# =====================================================
# REGISTER FACE - Thu thập khuôn mặt cho dataset
# =====================================================

# Global register camera instance (riêng biệt với camera nhận diện)
register_camera = None
captured_faces = []  # Lưu tạm các ảnh đã chụp


class RegisterCamera:
    """Camera class cho việc thu thập khuôn mặt"""
    
    def __init__(self):
        self.video = None
        self.current_face_location = None
        self.enhance_enabled = True
        self.last_frame = None  # Lưu frame cuối cùng để capture
        self.last_face_locations = []  # Lưu vị trí face cuối
    
    def start(self):
        if self.video is None or not self.video.isOpened():
            self.video = cv2.VideoCapture(CAMERA_INDEX)
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            print("[INFO] Register Camera đã khởi động")
    
    def stop(self):
        if self.video is not None:
            self.video.release()
            self.video = None
            print("[INFO] Register Camera đã đóng")
    
    def get_frame(self):
        """Lấy frame và detect khuôn mặt"""
        if self.video is None:
            self.start()
        
        ret, frame = self.video.read()
        if not ret:
            return None, None
        
        frame = cv2.flip(frame, 1)
        
        # Enhance lighting nếu bật
        if self.enhance_enabled:
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_TILE_SIZE)
            l = clahe.apply(l)
            lab = cv2.merge([l, a, b])
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Lưu frame để dùng cho capture
        self.last_frame = frame.copy()
        
        # Detect khuôn mặt
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=FRAME_RESIZE_SCALE, fy=FRAME_RESIZE_SCALE)
        face_locations = face_recognition.face_locations(small_frame, model='hog')  # Dùng HOG cho nhanh
        
        # Scale lại và lưu
        scaled_locations = []
        for (top, right, bottom, left) in face_locations:
            top = int(top / FRAME_RESIZE_SCALE)
            right = int(right / FRAME_RESIZE_SCALE)
            bottom = int(bottom / FRAME_RESIZE_SCALE)
            left = int(left / FRAME_RESIZE_SCALE)
            scaled_locations.append((top, right, bottom, left))
        
        self.last_face_locations = scaled_locations
        
        display = frame.copy()
        self.current_face_location = None
        
        for (top, right, bottom, left) in scaled_locations:
            self.current_face_location = (top, right, bottom, left)
            
            # Vẽ khung xanh lá
            cv2.rectangle(display, (left, top), (right, bottom), (0, 255, 0), 3)
            
            # Vẽ text
            cv2.putText(display, "Phat hien khuon mat", (left, top - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        if len(scaled_locations) == 0:
            cv2.putText(display, "Khong phat hien khuon mat", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        elif len(scaled_locations) > 1:
            cv2.putText(display, f"Phat hien {len(face_locations)} khuon mat - Chi can 1!", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        else:
            cv2.putText(display, "San sang chup!", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Thêm timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(display, timestamp, (10, display.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        return display, frame  # display để stream, frame để capture
    
    def capture_face(self):
        """Chụp và trả về ảnh khuôn mặt từ frame đã lưu"""
        # Sử dụng frame và face locations đã lưu từ get_frame()
        if self.last_frame is None:
            return None, "Chưa có frame - đợi camera khởi động"
        
        if len(self.last_face_locations) == 0:
            return None, "Không phát hiện khuôn mặt"
        elif len(self.last_face_locations) > 1:
            return None, f"Phát hiện {len(self.last_face_locations)} khuôn mặt, chỉ cần 1"
        
        frame = self.last_frame.copy()
        
        # Crop khuôn mặt
        top, right, bottom, left = self.last_face_locations[0]
        
        # Mở rộng vùng crop một chút
        padding = 30
        top = max(0, top - padding)
        bottom = min(frame.shape[0], bottom + padding)
        left = max(0, left - padding)
        right = min(frame.shape[1], right + padding)
        
        face_img = frame[top:bottom, left:right]
        
        if face_img.size == 0:
            return None, "Không thể crop khuôn mặt"
        
        return face_img, None


def get_register_camera():
    """Lấy hoặc tạo register camera instance"""
    global register_camera
    if register_camera is None:
        register_camera = RegisterCamera()
    return register_camera


def gen_register_frames():
    """Generator để stream video cho register"""
    cam = get_register_camera()
    cam.start()
    
    while True:
        display, _ = cam.get_frame()
        if display is None:
            break
        
        ret, buffer = cv2.imencode('.jpg', display, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not ret:
            continue
        
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def register_camera_view(request):
    """Trang đăng ký khuôn mặt với camera"""
    # Lấy thông tin từ query params (nếu có từ trang register)
    student_id = request.GET.get('student_id', '')
    full_name = request.GET.get('full_name', '')
    class_id = request.GET.get('class_id', '')
    email = request.GET.get('email', '')
    
    context = {
        'student_id': student_id,
        'full_name': full_name,
        'class_id': class_id,
        'email': email,
        'min_samples': 20,  # Số ảnh tối thiểu cần chụp
    }
    return render(request, 'opencv_plugin/register_camera.html', context)


@gzip.gzip_page
def register_video_feed(request):
    """Streaming video cho register"""
    return StreamingHttpResponse(
        gen_register_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


@require_http_methods(["POST"])
def capture_face(request):
    """API chụp 1 ảnh khuôn mặt"""
    import json
    import base64
    
    try:
        data = json.loads(request.body) if request.body else {}
    except:
        data = {}
    
    person_name = data.get('person_name', 'unknown')
    
    cam = get_register_camera()
    face_img, error = cam.capture_face()
    
    if error:
        return JsonResponse({'success': False, 'error': error})
    
    # Tạo thư mục dataset
    dataset_dir = os.path.join(BASE_DIR, 'dataset', person_name)
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Đếm ảnh đã có
    existing = len([f for f in os.listdir(dataset_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
    
    # Lưu ảnh
    img_filename = f"{person_name}_{existing + 1}.jpg"
    img_path = os.path.join(dataset_dir, img_filename)
    cv2.imwrite(img_path, face_img)
    
    # Encode ảnh để gửi về client (preview)
    _, buffer = cv2.imencode('.jpg', face_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return JsonResponse({
        'success': True,
        'message': f'Đã lưu ảnh {existing + 1}',
        'count': existing + 1,
        'filename': img_filename,
        'image': f'data:image/jpeg;base64,{img_base64}'
    })


@require_http_methods(["POST"])
def save_registration(request):
    """API hoàn tất đăng ký - lưu thông tin student vào DB"""
    import json
    from portal.models import Class, Student
    
    try:
        data = json.loads(request.body) if request.body else {}
    except:
        data = {}
    
    student_id = data.get('student_id', '')
    full_name = data.get('full_name', '')
    class_id = data.get('class_id', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    
    if not student_id or not full_name:
        return JsonResponse({'success': False, 'error': 'Thiếu mã SV hoặc họ tên'})
    
    # Kiểm tra đã có ảnh chưa
    dataset_dir = os.path.join(BASE_DIR, 'dataset', student_id)
    if not os.path.exists(dataset_dir):
        return JsonResponse({'success': False, 'error': 'Chưa chụp ảnh khuôn mặt'})
    
    face_count = len([f for f in os.listdir(dataset_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
    if face_count < 5:
        return JsonResponse({'success': False, 'error': f'Cần ít nhất 5 ảnh (hiện có {face_count})'})
    
    # Tìm hoặc tạo Class
    class_obj = None
    if class_id:
        class_obj, _ = Class.objects.get_or_create(
            class_id=class_id,
            defaults={'name': f'Lớp {class_id}', 'is_active': True}
        )
    
    # Tạo hoặc cập nhật Student
    student, created = Student.objects.update_or_create(
        student_id=student_id,
        defaults={
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'class_obj': class_obj,
            'face_data': f'dataset/{student_id}/',
            'is_registered': True
        }
    )
    
    # Dừng camera
    global register_camera
    if register_camera is not None:
        register_camera.stop()
        register_camera = None
    
    return JsonResponse({
        'success': True,
        'message': f'Đã đăng ký {full_name} với {face_count} ảnh',
        'student_id': student_id,
        'face_count': face_count,
        'created': created,
        'next_step': 'Chạy encode_faces.py để cập nhật encodings'
    })


@require_http_methods(["POST"])
def encode_faces_api(request):
    """API chạy encode faces sau khi đăng ký"""
    import subprocess
    
    try:
        # Chạy script encode_faces.py
        result = subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, 'encode_faces.py')],
            capture_output=True,
            text=True,
            timeout=120  # 2 phút timeout
        )
        
        if result.returncode == 0:
            # Reload encodings vào camera
            global camera
            if camera is not None:
                camera._load_encodings()
            
            return JsonResponse({
                'success': True,
                'message': 'Đã encode và cập nhật encodings',
                'output': result.stdout
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Lỗi khi encode',
                'stderr': result.stderr
            })
    except subprocess.TimeoutExpired:
        return JsonResponse({'success': False, 'error': 'Timeout - quá 2 phút'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
