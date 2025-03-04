from app import db, User, app

with app.app_context():
    user = User.query.filter_by(email="luanminhho2018@gmail.com").first()
    if user:
        user.is_admin = True # Quyền admin
      # user.is_admin = False  # Hủy quyền admin
        db.session.commit()
        print(f"Tài khoản {user.username} đã được cấp quyền admin!")
    else:
        print("Tài khoản không tồn tại!")