from flask import Blueprint, render_template, request, flash
from app.models.recipe import Recipe

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP GET /
    渲染首頁食譜列表 (`index.html`)。
    """
    recipes = Recipe.get_all()
    # 這裡實務上會依建立時間發出 order_by 與 limit 之類的條件，目前直接呈現所有資料。
    return render_template('index.html', recipes=recipes)

@main_bp.route('/search')
def search():
    """
    HTTP GET /search?q=keyword
    對食譜進行全站搜尋過濾，回傳名單至 (`index.html`)。
    """
    query = request.args.get('q', '').strip()
    if query:
        # 使用 SQLAlchemy 的 ilike 支援大小寫模糊查詢
        recipes = Recipe.query.filter(Recipe.title.ilike(f'%{query}%')).all()
        if not recipes:
             flash(f'找不到與「{query}」相關的食譜。', 'info')
    else:
        recipes = Recipe.get_all()
        
    return render_template('index.html', recipes=recipes, search_query=query)
