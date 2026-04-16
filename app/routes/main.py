from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP GET /
    渲染首頁食譜列表 (`index.html`)。
    """
    pass

@main_bp.route('/search')
def search():
    """
    HTTP GET /search?q=keyword
    對食譜進行全站搜尋過濾，回傳名單至 (`index.html`)。
    """
    pass
