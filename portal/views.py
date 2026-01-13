from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Avg
from .models import Student, AttendanceRecord, Camera, SystemStats
import json


def home(request):
    """Trang chủ - Portal chính"""
    # Lấy thống kê
    total_students = Student.objects.count()
    
    # Tính tỷ lệ điểm danh hôm nay
    today = timezone.now().date()
    today_attendance = AttendanceRecord.objects.filter(
        date=today, 
        status__in=['present', 'late']
    ).count()
    
    if total_students > 0:
        attendance_rate = round((today_attendance / total_students) * 100, 1)
    else:
        attendance_rate = 0
    
    # Số camera đang hoạt động
    active_cameras = Camera.objects.filter(status='active').count()
    
    context = {
        'total_students': total_students or 1248,  # Default value nếu chưa có data
        'attendance_rate': attendance_rate or 96.4,
        'active_cameras': active_cameras or 8,
        'avg_scan_time': 0.8,
        'opencv_plugin_url': settings.OPENCV_PLUGIN_URL,
        'admin_url': settings.ADMIN_DASHBOARD_URL,
        'register_url': settings.REGISTER_FACE_URL,
    }
    return render(request, 'portal/home.html', context)


def admin_dashboard(request):
    """Trang Admin Dashboard"""
    # Thống kê tổng quan
    total_students = Student.objects.count()
    registered_students = Student.objects.filter(is_registered=True).count()
    
    today = timezone.now().date()
    today_records = AttendanceRecord.objects.filter(date=today)
    
    context = {
        'total_students': total_students,
        'registered_students': registered_students,
        'today_present': today_records.filter(status='present').count(),
        'today_late': today_records.filter(status='late').count(),
        'today_absent': total_students - today_records.count(),
        'recent_records': AttendanceRecord.objects.select_related('student')[:20],
        'cameras': Camera.objects.all(),
    }
    return render(request, 'portal/admin_dashboard.html', context)


def register_face(request):
    """Trang đăng ký khuôn mặt mới"""
    context = {
        'opencv_plugin_url': settings.OPENCV_PLUGIN_URL,
    }
    return render(request, 'portal/register.html', context)


def scan_camera(request):
    """
    Trang scan camera - PLACEHOLDER cho plugin OpenCV
    Anh sẽ thay thế view này bằng plugin OpenCV riêng
    """
    context = {
        'message': 'Placeholder cho plugin OpenCV - Thay thế bằng plugin của anh'
    }
    return render(request, 'portal/scan_placeholder.html', context)


# =====================================================
# API Endpoints
# =====================================================

@require_http_methods(["GET"])
def api_stats(request):
    """API trả về thống kê realtime"""
    total_students = Student.objects.count() or 1248
    today = timezone.now().date()
    today_attendance = AttendanceRecord.objects.filter(
        date=today,
        status__in=['present', 'late']
    ).count()
    
    if total_students > 0:
        attendance_rate = round((today_attendance / total_students) * 100, 1)
    else:
        attendance_rate = 96.4
    
    active_cameras = Camera.objects.filter(status='active').count() or 8
    
    return JsonResponse({
        'success': True,
        'data': {
            'total_students': total_students,
            'attendance_rate': attendance_rate,
            'active_cameras': active_cameras,
            'avg_scan_time': 0.8,
            'last_sync': timezone.now().strftime('%H:%M:%S'),
        }
    })


@require_http_methods(["POST"])
def api_record_attendance(request):
    """
    API để plugin OpenCV gọi khi nhận diện được khuôn mặt
    
    Expected POST data:
    {
        "student_id": "SV001",
        "confidence": 98.5,
        "camera_id": "CAM01"
    }
    """
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        confidence = data.get('confidence', 0)
        camera_id = data.get('camera_id', '')
        
        # Tìm sinh viên
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Student not found'
            }, status=404)
        
        # Tạo bản ghi điểm danh
        today = timezone.now().date()
        current_time = timezone.now().time()
        
        record, created = AttendanceRecord.objects.get_or_create(
            student=student,
            date=today,
            defaults={
                'time_in': current_time,
                'status': 'present',
                'confidence': confidence,
                'camera_id': camera_id,
            }
        )
        
        if not created:
            # Đã điểm danh rồi, cập nhật time_out
            record.time_out = current_time
            record.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Attendance recorded',
            'data': {
                'student_name': student.full_name,
                'student_id': student.student_id,
                'time': current_time.strftime('%H:%M:%S'),
                'status': record.status,
                'created': created
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def api_students(request):
    """API lấy danh sách sinh viên"""
    students = Student.objects.all().values(
        'student_id', 'full_name', 'class_name', 'is_registered'
    )
    return JsonResponse({
        'success': True,
        'data': list(students)
    })


@require_http_methods(["GET"])
def api_attendance_today(request):
    """API lấy danh sách điểm danh hôm nay"""
    today = timezone.now().date()
    records = AttendanceRecord.objects.filter(date=today).select_related('student')
    
    data = [{
        'student_id': r.student.student_id,
        'student_name': r.student.full_name,
        'time_in': r.time_in.strftime('%H:%M:%S') if r.time_in else None,
        'status': r.status,
        'confidence': r.confidence,
    } for r in records]
    
    return JsonResponse({
        'success': True,
        'date': str(today),
        'data': data
    })
