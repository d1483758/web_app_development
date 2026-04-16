from flask import Blueprint

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/<int:recipe_id>')
def view_recipe(recipe_id):
    """
    HTTP GET /recipe/<recipe_id>
    從 DB 顯示單篇完整食譜資訊，包含多對多的關聯材料與步驟 (`recipe.html`)。
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new_recipe():
    """
    HTTP GET /recipe/new: 給予一張可以新增食譜標題與數個材料、步驟的動態表單 (`edit_recipe.html`)。
    HTTP POST /recipe/new: (需登入) 接收表單寫入 Recipe, Ingredient, Step 返回該篇展示頁。
    """
    pass

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    HTTP GET /recipe/<recipe_id>/edit: (需所有權) 將舊有的資料塞置表單 (`edit_recipe.html`) 回饋。
    HTTP POST /recipe/<recipe_id>/edit: (需所有權) 將資料內容修改後提交更新。
    """
    pass

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    HTTP POST /recipe/<recipe_id>/delete: (需所有權)
    直接從 DB 硬刪去並透過 cascade 拿掉所有關連子檔案，回傳並 redirect 回 /profile。
    """
    pass

@recipe_bp.route('/<int:recipe_id>/favorite', methods=['POST'])
def toggle_favorite(recipe_id):
    """
    HTTP POST /recipe/<recipe_id>/favorite: (需登入)
    根據當前 user 對此食譜狀態切換 Favorite；若有就取消，無則加入，回調刷新畫面。
    """
    pass
