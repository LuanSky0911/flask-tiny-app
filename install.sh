#!/bin/bash

echo "🚀 Bắt đầu cài đặt ứng dụng Flask To-Do List..."

# Cập nhật hệ thống
echo "🔄 Cập nhật hệ thống..."
sudo apt update && sudo apt upgrade -y

# Cài đặt Python và pip nếu chưa có
echo "🐍 Cài đặt Python và pip..."
sudo apt install python3 python3-pip python3-venv -y

# Tạo môi trường ảo
echo "🛠 Tạo virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Cài đặt các thư viện cần thiết
echo "📦 Cài đặt dependencies..."
pip install -r requirements.txt

# Khởi tạo cơ sở dữ liệu
echo "📊 Khởi tạo database..."
python -c "from app import db, app; with app.app_context(): db.create_all()"

# Thêm dữ liệu mẫu
echo "📝 Thêm dữ liệu giả lập..."
python random_data.py

# Thiết lập tài khoản admin
echo "🔐 Cấp quyền admin..."
python set_admin.py

# Chạy ứng dụng Flask
echo "🚀 Khởi động ứng dụng..."
flask run --host=0.0.0.0 --port=5000
