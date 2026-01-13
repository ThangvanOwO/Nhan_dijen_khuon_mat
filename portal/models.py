from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """Model lưu thông tin sinh viên"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Mã sinh viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(blank=True, verbose_name="Email")
    class_name = models.CharField(max_length=50, blank=True, verbose_name="Lớp")
    face_encoding = models.BinaryField(null=True, blank=True, verbose_name="Face Encoding Data")
    face_image = models.ImageField(upload_to='faces/', null=True, blank=True, verbose_name="Ảnh khuôn mặt")
    is_registered = models.BooleanField(default=False, verbose_name="Đã đăng ký khuôn mặt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sinh viên"
        verbose_name_plural = "Danh sách sinh viên"
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class AttendanceRecord(models.Model):
    """Model lưu lịch sử điểm danh"""
    STATUS_CHOICES = [
        ('present', 'Có mặt'),
        ('late', 'Đi muộn'),
        ('absent', 'Vắng mặt'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(verbose_name="Ngày")
    time_in = models.TimeField(null=True, blank=True, verbose_name="Giờ vào")
    time_out = models.TimeField(null=True, blank=True, verbose_name="Giờ ra")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present', verbose_name="Trạng thái")
    confidence = models.FloatField(default=0.0, verbose_name="Độ tin cậy nhận diện (%)")
    camera_id = models.CharField(max_length=50, blank=True, verbose_name="ID Camera")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bản ghi điểm danh"
        verbose_name_plural = "Lịch sử điểm danh"
        ordering = ['-date', '-time_in']
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.get_status_display()}"


class Camera(models.Model):
    """Model quản lý camera"""
    STATUS_CHOICES = [
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('maintenance', 'Bảo trì'),
    ]

    camera_id = models.CharField(max_length=50, unique=True, verbose_name="ID Camera")
    name = models.CharField(max_length=100, verbose_name="Tên camera")
    location = models.CharField(max_length=200, verbose_name="Vị trí")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Địa chỉ IP")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Trạng thái")
    last_active = models.DateTimeField(null=True, blank=True, verbose_name="Hoạt động lần cuối")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Danh sách camera"

    def __str__(self):
        return f"{self.name} ({self.camera_id})"


class SystemStats(models.Model):
    """Model lưu thống kê hệ thống"""
    date = models.DateField(unique=True, verbose_name="Ngày")
    total_students = models.IntegerField(default=0, verbose_name="Tổng số sinh viên")
    attendance_rate = models.FloatField(default=0.0, verbose_name="Tỷ lệ điểm danh (%)")
    avg_scan_time = models.FloatField(default=0.0, verbose_name="Thời gian scan trung bình (s)")
    total_scans = models.IntegerField(default=0, verbose_name="Tổng số lần scan")

    class Meta:
        verbose_name = "Thống kê hệ thống"
        verbose_name_plural = "Thống kê hệ thống"
        ordering = ['-date']

    def __str__(self):
        return f"Stats - {self.date}"
