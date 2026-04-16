from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app.models.recipe import Recipe

admin_bp = Blueprint('admin', __name__)

def is_admin():
    return 'user_id' in session and session.get('is_admin', False)

@admin_bp.route('/')
def dashboard():
    """
    顯示所有圖表或管理專屬用的儀表板(`admin.html`)。
    """
    if not is_admin():
        flash('您未具備管理員權限', 'danger')
        return redirect(url_for('main.index'))
        
    users = User.get_all()
    recipes = Recipe.get_all()
    return render_template('admin.html', users=users, recipes=recipes)

@admin_bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def admin_delete_recipe(recipe_id):
    """
    強制下架任一筆違規食譜。
    """
    if not is_admin():
        flash('授權失敗！', 'danger')
        return redirect(url_for('main.index'))
        
    if Recipe.delete(recipe_id):
        flash('管理員：已成功下架該篇食譜。', 'success')
    else:
        flash('執行刪除失敗。', 'danger')
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/user/<int:user_id>/ban', methods=['POST'])
def ban_user(user_id):
    """
    將任一不良會員停權無法登入 (MVP 直接刪除)。
    """
    if not is_admin():
        flash('授權失敗！', 'danger')
        return redirect(url_for('main.index'))
        
    if User.delete(user_id):
        flash('管理員：已停權該會員所有服務與食譜', 'success')
    else:
        flash('停權操作失敗。', 'danger')
        
    return redirect(url_for('admin.dashboard'))
