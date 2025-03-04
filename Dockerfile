# Sử dụng Python 3.10 làm base image
FROM python:3.10

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả file vào container
COPY . /app

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Mở cổng 5000
EXPOSE 5000

# Khởi chạy Flask sau khi container khởi động
CMD ["sh", "-c", "flask db upgrade || python -c 'from app import db, app; with app.app_context(): db.create_all()' && flask run --host=0.0.0.0 --port=5000"]
