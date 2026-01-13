from django.db import models
from django.contrib.auth.models import User


class Class(models.Model):
    """Model quản lý lớp học"""
    class_id = models.CharField(max_length=20, unique=True, verbose_name="Mã lớp")
    name = models.CharField(max_length=100, verbose_name="Tên lớp")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    teacher = models.CharField(max_length=100, blank=True, verbose_name="Giảng viên")
    room = models.CharField(max_length=50, blank=True, verbose_name="Phòng học")
    schedule = models.CharField(max_length=200, blank=True, verbose_name="Lịch học")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lớp học"
        verbose_name_plural = "Danh sách lớp học"
        ordering = ['class_id']

    def __str__(self):
        return f"{self.class_id} - {self.name}"
    
    def get_student_count(self):
        return self.students.count()


class Student(models.Model):
    """Model lưu thông tin học viên"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Mã học viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    
    # Liên kết với lớp học
    class_obj = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='students', verbose_name="Lớp học")
    
    # Dữ liệu khuôn mặt
    face_data = models.CharField(max_length=500, blank=True, verbose_name="Đường dẫn ảnh/vector đặc trưng")
    face_encoding = models.BinaryField(null=True, blank=True, verbose_name="Face Encoding Data")
    face_image = models.ImageField(upload_to='faces/', null=True, blank=True, verbose_name="Ảnh khuôn mặt")
    
    is_registered = models.BooleanField(default=False, verbose_name="Đã đăng ký khuôn mặt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Học viên"
        verbose_name_plural = "Danh sách học viên"
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class Session(models.Model):
    """Model định nghĩa buổi học"""
    STATUS_CHOICES = [
        ('scheduled', 'Đã lên lịch'),
        ('ongoing', 'Đang diễn ra'),
        ('completed', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]
    
    SESSION_TYPE_CHOICES = [
        ('morning', 'Sáng'),
        ('afternoon', 'Chiều'),
        ('evening', 'Tối'),
    ]
    
    session_id = models.CharField(max_length=50, unique=True, verbose_name="Mã buổi học")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sessions', 
                                   verbose_name="Lớp học")
    session_number = models.IntegerField(default=1, verbose_name="Buổi thứ mấy")
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='morning',
                                     verbose_name="Loại buổi (sáng/chiều/tối)")
    date = models.DateField(verbose_name="Ngày học")
    start_time = models.TimeField(verbose_name="Giờ bắt đầu")
    end_time = models.TimeField(verbose_name="Giờ kết thúc")
    topic = models.CharField(max_length=200, blank=True, verbose_name="Chủ đề buổi học")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', 
                              verbose_name="Trạng thái")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Buổi học"
        verbose_name_plural = "Danh sách buổi học"
        ordering = ['-date', '-start_time']
        unique_together = ['class_obj', 'date', 'start_time']

    def __str__(self):
        return f"{self.session_id} - {self.class_obj.name} - {self.date}"
    
    def get_attendance_count(self):
        return self.attendances.filter(status='present').count()
    
    def get_attendance_rate(self):
        total = self.class_obj.students.count()
        if total == 0:
            return 0
        present = self.get_attendance_count()
        return round((present / total) * 100, 1)
    
    def get_students_present(self):
        """Trả về danh sách học sinh có mặt trong buổi học này"""
        return Student.objects.filter(
            attendances__session=self,
            attendances__status__in=['present', 'late']
        ).distinct()
    
    def get_student_count(self):
        """Số lượng học sinh có mặt trong buổi học này"""
        return self.get_students_present().count()
    
    def get_session_type_display_vi(self):
        """Hiển thị loại buổi bằng tiếng Việt"""
        type_map = {
            'morning': 'Sáng',
            'afternoon': 'Chiều', 
            'evening': 'Tối',
        }
        return type_map.get(self.session_type, self.session_type)


class Attendance(models.Model):
    """Model điểm danh - bảng cầu nối giữa Session và Student"""
    STATUS_CHOICES = [
        ('present', 'Có mặt'),
        ('late', 'Đi muộn'),
        ('absent', 'Vắng mặt'),
        ('excused', 'Có phép'),
    ]
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances',
                                 verbose_name="Buổi học")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances',
                                 verbose_name="Học viên")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent', 
                              verbose_name="Trạng thái")
    check_in_time = models.TimeField(null=True, blank=True, verbose_name="Giờ check-in")
    check_out_time = models.TimeField(null=True, blank=True, verbose_name="Giờ check-out")
    confidence = models.FloatField(default=0.0, verbose_name="Độ tin cậy nhận diện (%)")
    camera_id = models.CharField(max_length=50, blank=True, verbose_name="ID Camera")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Điểm danh"
        verbose_name_plural = "Lịch sử điểm danh"
        ordering = ['-session__date', 'student__student_id']
        unique_together = ['session', 'student']

    def __str__(self):
        return f"{self.student.full_name} - {self.session.date} - {self.get_status_display()}"


# =====================================================
# Models phụ trợ (giữ lại)
# =====================================================

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
