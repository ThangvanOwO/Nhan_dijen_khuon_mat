from django.contrib import admin
from .models import Class, Student, Session, Attendance, Camera, SystemStats


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_id', 'name', 'teacher', 'room', 'is_active', 'get_student_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['class_id', 'name', 'teacher']
    ordering = ['class_id']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'class_obj', 'is_registered', 'created_at']
    list_filter = ['is_registered', 'class_obj', 'created_at']
    search_fields = ['student_id', 'full_name', 'email']
    ordering = ['student_id']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'class_obj', 'date', 'start_time', 'status', 'get_attendance_count', 'get_attendance_rate']
    list_filter = ['status', 'class_obj', 'date']
    search_fields = ['session_id', 'topic']
    date_hierarchy = 'date'
    ordering = ['-date', '-start_time']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status', 'check_in_time', 'confidence']
    list_filter = ['status', 'session__date', 'session__class_obj']
    search_fields = ['student__student_id', 'student__full_name']
    ordering = ['-session__date', 'student__student_id']


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['camera_id', 'name', 'location', 'status', 'last_active']
    list_filter = ['status']
    search_fields = ['camera_id', 'name', 'location']


@admin.register(SystemStats)
class SystemStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_students', 'attendance_rate', 'total_scans']
    date_hierarchy = 'date'
    ordering = ['-date']
