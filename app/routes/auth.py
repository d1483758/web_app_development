from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    HTTP GET /register: 顯示註冊註冊表單 (`auth.html`)。
    HTTP POST /register: 接收表單並將資料以 hashed password 新增至 User 表。重導向至登入。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    HTTP GET /login: 顯示登入表單 (`auth.html`)。
    HTTP POST /login: 校準帳密，若正確則於 Session 寫入 `user_id`。重導向至首頁。
    """
    pass

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    HTTP GET/POST /logout: 清除使用者的登入 Session，並重導回來首頁。
    """
    pass

@auth_bp.route('/profile')
def profile():
    """
    HTTP GET /profile: (需登入)
    展示該登入會員的自創食譜列表，以及其按下最愛的收藏夾。(`profile.html`)
    """
    pass
