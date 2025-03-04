from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # 🔹 Thêm phương thức đổi mật khẩu
    def change_password(self, old_password, new_password):
        if self.check_password(old_password):  # Kiểm tra mật khẩu cũ có đúng không
            self.set_password(new_password)   # Cập nhật mật khẩu mới
            db.session.commit()
            return True
        return False

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date, nullable=True)  # YYYY-MM-DD
    priority = db.Column(db.String(10), nullable=True)  # LOW, MEDIUM, HIGH
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))