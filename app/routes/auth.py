from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    HTTP GET /register: 顯示註冊註冊表單 (`auth.html`)。
    HTTP POST /register: 接收表單並將資料以 hashed password 新增至 User 表。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('所有欄位皆為必填。', 'danger')
            return render_template('auth.html', is_register=True)
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('此 Email 已經被註冊過！', 'danger')
            return render_template('auth.html', is_register=True)
            
        hashed_pw = generate_password_hash(password)
        new_user = User.create({
            'username': username,
            'email': email,
            'password_hash': hashed_pw,
            'is_admin': False
        })
        
        if new_user:
            flash('註冊成功！請直接登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('系統發生錯誤，請稍後再試。', 'danger')
            
    return render_template('auth.html', is_register=True)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    HTTP GET /login: 顯示登入表單 (`auth.html`)。
    HTTP POST /login: 校準帳密，若正確則於 Session 寫入 `user_id`。
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('請填寫信箱與密碼。', 'warning')
            return render_template('auth.html')
            
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # 發放登入成功狀態到 Session 裡面
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash(f'歡迎回來，{user.username}！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('信箱或密碼錯誤。', 'danger')
            
    return render_template('auth.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    清除使用者的登入 Session，並重導回來首頁。
    """
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('您已經成功登出。', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
def profile():
    """
    展示該登入會員的自創食譜列表，以及其按下最愛的收藏夾。
    """
    if 'user_id' not in session:
        flash('請先登入才能查看個人檔案', 'warning')
        return redirect(url_for('auth.login'))
        
    user = User.get_by_id(session['user_id'])
    return render_template('profile.html', user=user)
