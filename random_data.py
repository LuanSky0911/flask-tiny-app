from app import db, Task, User, app  
from datetime import datetime, timedelta
import random

task_contents = ["Đi chợ", "Nấu ăn", "Học Python", "Đọc sách", "Luyện tập thể thao", "Viết báo cáo", "Họp nhóm", "Mua đồ", "Dọn dẹp nhà cửa", "Lập kế hoạch tuần mới"]
priorities = ["LOW", "MEDIUM", "HIGH"]

user_email = "luanminh@gmail.com"  # Thay email của user cần test

with app.app_context():
    user = User.query.filter_by(email=user_email).first()  
    
    if user:  
        for i in range(50):
            new_task = Task(
                content=random.choice(task_contents),
                due_date=datetime.now() + timedelta(days=random.randint(1, 30)),
                priority=random.choice(priorities),
                user_id=user.id  
            )
            db.session.add(new_task)

        db.session.commit()
        print(f"Đã thêm dữ liệu giả lập cho user {user.email} (ID: {user.id}) thành công!")
    else:
        print(f"Không tìm thấy user với email: {user_email}")
