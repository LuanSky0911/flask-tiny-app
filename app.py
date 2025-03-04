from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, User, Task, bcrypt
from forms import RegisterForm, LoginForm, TaskForm
from config import Config
from forms import RegisterForm, LoginForm, TaskForm, ChangePasswordForm
from flask_migrate import Migrate
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)  
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Vui lòng đăng nhập để truy cập trang này."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email đã tồn tại! Vui lòng sử dụng email khác.', 'danger')
            return redirect(url_for('register'))

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Tài khoản của bạn đã được tạo!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.is_blocked:  # Nếu tài khoản bị khóa
                flash('Tài khoản của bạn đã bị khóa!', 'danger')
                return redirect(url_for('login'))  # Quay lại trang login
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Sai thông tin đăng nhập!', 'danger')
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất!', 'info')
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = TaskForm()
    # Lấy số trang từ URL, mặc định là trang 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  
    # Truy vấn danh sách công việc của user hiện tại và phân trang
    pagination = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date.asc()).paginate(page=page, per_page=per_page, error_out=False)
    tasks = pagination.items  # Danh sách task của trang hiện tại

    return render_template('home.html', user=current_user, form=form, tasks=tasks, pagination=pagination)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('Bạn không có quyền truy cập!', 'danger')
        return redirect(url_for('home'))
    
    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/admin/users')
def user_management():
    users = db.session.query(User.id, User.username, User.email, User.status, User.is_admin).all()
    user_list = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "status": "Hoạt động" if u.status else "Bị khóa",
            "is_admin": "Admin" if u.is_admin else "User"
        }
        for u in users
    ]
    return render_template('admin_users.html', users=user_list)

@app.route('/block_user/<int:user_id>')
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền!', 'danger')
        return redirect(url_for('admin'))

    user = User.query.get(user_id)

    # Không cho phép khóa admin
    if user and user.is_admin:
        flash(f'Không thể khóa tài khoản admin: {user.username}!', 'danger')
        return redirect(url_for('admin'))

    if user:
        user.is_blocked = True
        db.session.commit()
        flash(f'Đã khóa tài khoản {user.username}!', 'warning')

    return redirect(url_for('admin'))


@app.route('/unblock_user/<int:user_id>')
@login_required
def unblock_user(user_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền!', 'danger')
        return redirect(url_for('admin'))

    user = User.query.get(user_id)
    if user:
        user.is_blocked = False
        db.session.commit()
        flash(f'Đã mở khóa tài khoản {user.username}!', 'success')
    return redirect(url_for('admin'))
@app.route('/reset_password/<int:user_id>')
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền!', 'danger')
        return redirect(url_for('admin'))

    user = User.query.get(user_id)
    if user:
        user.set_password('123456')  
        db.session.commit()
        flash(f"Mật khẩu của {user.username} đã được reset thành '123456'.", 'success')
    return redirect(url_for('admin'))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.change_password(form.old_password.data, form.new_password.data):
            flash('Đổi mật khẩu thành công!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Mật khẩu cũ không đúng!', 'danger')
    return render_template('change_password.html', form=form)
@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task_content = request.form.get('task')
    due_date_str = request.form.get('due_date')  
    priority = request.form.get('priority') 

    # Kiểm tra nếu người dùng không nhập nội dung công việc
    if not task_content:
        flash('Vui lòng nhập công việc!', 'danger')
        return redirect(url_for('home'))

    # Chuyển đổi định dạng ngày từ 'YYYY-MM-DD' sang kiểu datetime.date
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
    except ValueError:
        flash('Ngày không hợp lệ! Vui lòng chọn đúng định dạng.', 'danger')
        return redirect(url_for('home'))

    # Thêm task vào cơ sở dữ liệu
    new_task = Task(content=task_content, due_date=due_date, priority=priority, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    
    flash('Công việc đã được thêm!', 'success')
    return redirect(url_for('task_list'))
@app.route('/add_task_page', methods=['GET', 'POST'])
@login_required
def add_task_page():
    form = TaskForm()
    if form.validate_on_submit():
        return add_task()  
    return render_template('add_task.html', form=form)

@app.route('/task_list', methods=['GET'])
@login_required
def task_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date.asc()).paginate(page=page, per_page=per_page, error_out=False)
    tasks = pagination.items
    return render_template('task_list.html', tasks=tasks, pagination=pagination)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        task.priority = request.form['priority']
        db.session.commit()
        flash('Công việc đã được cập nhật thành công!', 'success')
        return redirect(url_for('task_list'))
    return render_template('edit_task.html', task=task)


@app.route('/delete_multiple_tasks', methods=['POST'])
def delete_multiple_tasks():
    selected_tasks = request.form.getlist('selected_tasks')  
    if selected_tasks:
        try:
            Task.query.filter(Task.id.in_(selected_tasks)).delete(synchronize_session=False)
            db.session.commit()
            flash("Các công việc đã được xóa!", "success")
        except Exception as e:
            flash(f"Lỗi khi xóa công việc: {str(e)}", "danger")
            db.session.rollback()
    else:
        flash("Không có công việc nào được chọn để xóa!", "danger")
    return redirect(url_for('task_list'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5000)
