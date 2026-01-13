#!/usr/bin/env python3
"""
Script tự động tạo MySQL database và user cho hệ thống điểm danh
Chạy: python setup_mysql.py
"""
import subprocess
import sys
import os

# Cấu hình database
DB_NAME = 'attendance_db'
DB_USER = 'django'
DB_PASSWORD = '123456'
DB_HOST = 'localhost'

def run_mysql_command(command, use_root=True):
    """Chạy lệnh MySQL"""
    if use_root:
        # Thử với sudo mysql (không cần password trên nhiều hệ thống Linux)
        cmd = ['sudo', 'mysql', '-e', command]
    else:
        cmd = ['mysql', '-u', DB_USER, f'-p{DB_PASSWORD}', '-e', command]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, '', str(e)

def check_mysql_installed():
    """Kiểm tra MySQL đã cài đặt chưa"""
    try:
        result = subprocess.run(['which', 'mysql'], capture_output=True)
        return result.returncode == 0
    except:
        return False

def check_mysql_running():
    """Kiểm tra MySQL đang chạy không"""
    try:
        result = subprocess.run(['systemctl', 'is-active', 'mariadb'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        result = subprocess.run(['systemctl', 'is-active', 'mysql'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def create_database():
    """Tạo database và user"""
    print(f"\n{'='*60}")
    print("  KHỞI TẠO MYSQL DATABASE CHO HỆ THỐNG ĐIỂM DANH")
    print(f"{'='*60}\n")
    
    # Kiểm tra MySQL
    if not check_mysql_installed():
        print("[!] MySQL/MariaDB chưa được cài đặt!")
        print("\nCài đặt trên Arch/CachyOS:")
        print("  sudo pacman -S mariadb")
        print("  sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql")
        print("  sudo systemctl start mariadb")
        print("  sudo systemctl enable mariadb")
        return False
    
    print("[✓] MySQL/MariaDB đã được cài đặt")
    
    # Kiểm tra MySQL đang chạy
    if not check_mysql_running():
        print("[!] MySQL/MariaDB chưa chạy!")
        print("\nKhởi động MySQL:")
        print("  sudo systemctl start mariadb")
        print("  # hoặc")
        print("  sudo systemctl start mysql")
        return False
    
    print("[✓] MySQL/MariaDB đang chạy")
    
    # Tạo database
    print(f"\n[INFO] Đang tạo database '{DB_NAME}'...")
    success, _, err = run_mysql_command(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    
    if not success:
        print(f"[!] Lỗi tạo database: {err}")
        print("\nThử chạy thủ công:")
        print(f"  sudo mysql -e \"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\"")
        return False
    
    print(f"[✓] Database '{DB_NAME}' đã được tạo")
    
    # Tạo user
    print(f"\n[INFO] Đang tạo user '{DB_USER}'...")
    commands = [
        f"CREATE USER IF NOT EXISTS '{DB_USER}'@'{DB_HOST}' IDENTIFIED BY '{DB_PASSWORD}';",
        f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{DB_USER}'@'{DB_HOST}';",
        f"FLUSH PRIVILEGES;"
    ]
    
    for cmd in commands:
        success, _, err = run_mysql_command(cmd)
        if not success:
            print(f"[!] Lỗi: {err}")
    
    print(f"[✓] User '{DB_USER}' đã được tạo với quyền truy cập database")
    
    # Thông tin kết nối
    print(f"\n{'='*60}")
    print("  THÔNG TIN KẾT NỐI DATABASE")
    print(f"{'='*60}")
    print(f"  Database: {DB_NAME}")
    print(f"  User:     {DB_USER}")
    print(f"  Password: {DB_PASSWORD}")
    print(f"  Host:     {DB_HOST}")
    print(f"{'='*60}\n")
    
    return True

def run_migrations():
    """Chạy Django migrations"""
    print("[INFO] Đang chạy Django migrations...")
    
    # Chuyển sang thư mục project
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Chạy migrations
    venv_python = os.path.join(project_dir, 'venv', 'bin', 'python')
    if not os.path.exists(venv_python):
        venv_python = 'python'
    
    try:
        result = subprocess.run([venv_python, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("[✓] Migrations thành công!")
            return True
        else:
            print(f"[!] Lỗi migrations: {result.stderr}")
            return False
    except Exception as e:
        print(f"[!] Lỗi: {e}")
        return False

if __name__ == '__main__':
    if create_database():
        print("\n[INFO] Database đã sẵn sàng!")
        print("\nBước tiếp theo:")
        print("  1. Chạy migrations: python manage.py migrate")
        print("  2. Khởi động server: python manage.py runserver")
    else:
        print("\n[!] Có lỗi xảy ra. Vui lòng kiểm tra lại.")
        sys.exit(1)
