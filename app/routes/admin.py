from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    """
    HTTP GET /admin: (需最高管理權限)
    顯示所有圖表或管理專屬用的儀表板(`admin.html`)。
    """
    pass

@admin_bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def admin_delete_recipe(recipe_id):
    """
    HTTP POST /admin/recipe/<id>/delete: (需管理權限)
    強制下架任一筆違規食譜。
    """
    pass

@admin_bp.route('/user/<int:user_id>/ban', methods=['POST'])
def ban_user(user_id):
    """
    HTTP POST /admin/user/<id>/ban: (需管理權限)
    將任一不良會員停權無法登入。
    """
    pass
