# Flask To-Do List

## 1. Thông tin sinh viên
- **Họ và tên**: Hồ Minh Luân  
- **MSSV**: 22644751  

## 2. Mô tả dự án
Flask To-Do List là một ứng dụng web giúp người dùng quản lý danh sách công việc của mình một cách dễ dàng.  
Ứng dụng hỗ trợ:
- Tạo, chỉnh sửa, xóa và đánh dấu công việc đã hoàn thành.
- Đăng nhập, đăng ký tài khoản và quản lý người dùng.
- Phân quyền người dùng (admin, user).
- Sinh dữ liệu ngẫu nhiên để kiểm thử.

## 3. Công nghệ sử dụng
- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login  
- **Database**: SQLite / PostgreSQL  
- **Frontend**: HTML, CSS, JavaScript  
- **Triển khai**: Docker  

## 4. Hướng dẫn cài đặt và chạy ứng dụng
### Bước 1: Clone repository
```bash
git clone https://github.com/LuanSky0911/flask-tiny-app.git
cd flask-tiny-app
```

### Bước 2: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng
```bash
python app.py
```

### Bước 4: Tạo tài khoản người dùng

### Bước 5: Kích hoạt quyền admin
Chạy file `set_admin.py` để cấp hoặc hủy quyền admin cho tài khoản.

### Bước 6: Tạo dữ liệu mẫu
Chạy file `random_data.py` để sinh dữ liệu ngẫu nhiên.  
(**Lưu ý**: Cần thay đổi email để tạo dữ liệu cho user khác.)

## 5. Triển khai ứng dụng
Ứng dụng được triển khai tại địa chỉ:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)