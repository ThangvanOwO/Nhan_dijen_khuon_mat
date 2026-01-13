from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register_face, name='register'),
    
    # Scan camera - Placeholder cho plugin OpenCV
    # Anh có thể thay đổi URL này hoặc tạo app riêng cho plugin OpenCV
    path('scan/camera/', views.scan_camera, name='scan_camera'),
    
    # API Endpoints
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/record-attendance/', views.api_record_attendance, name='api_record_attendance'),
    path('api/students/', views.api_students, name='api_students'),
    path('api/attendance/today/', views.api_attendance_today, name='api_attendance_today'),
]
