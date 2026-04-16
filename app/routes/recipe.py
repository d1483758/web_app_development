from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.step import Step
from app.models.favorite import Favorite
from app.models import db

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/<int:recipe_id>')
def view_recipe(recipe_id):
    """
    HTTP GET /recipe/<recipe_id>
    從 DB 顯示單篇完整食譜資訊，包含多對多的關聯材料與步驟 (`recipe.html`)。
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該篇食譜', 'danger')
        return redirect(url_for('main.index'))
    return render_template('recipe.html', recipe=recipe)

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new_recipe():
    """
    HTTP GET /recipe/new: 顯示空白表單 (`edit_recipe.html`)。
    HTTP POST /recipe/new: 接收表單並寫入 Recipe, Ingredient, Step 返回該篇展示頁。
    """
    if 'user_id' not in session:
        flash('請先登入後才能建立食譜', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        image_url = request.form.get('image_url', '')

        if not title or not description or not category:
            flash('請填妥所有必填欄位！', 'danger')
            return render_template('edit_recipe.html')

        recipe_data = {
            'title': title,
            'description': description,
            'category': category,
            'image_url': image_url,
            'user_id': session['user_id']
        }
        
        new_rec = Recipe.create(recipe_data)
        if new_rec:
            # 接收動態材料表單 (這需要前端有相同的陣列名稱支援)
            ing_names = request.form.getlist('ingredient_name[]')
            ing_amounts = request.form.getlist('ingredient_amount[]')
            for i in range(len(ing_names)):
                if ing_names[i] and ing_amounts[i]:
                    Ingredient.create({
                        'recipe_id': new_rec.id,
                        'name': ing_names[i],
                        'amount': ing_amounts[i]
                    })
                    
            # 接收動態步驟表單
            step_instructions = request.form.getlist('step_instruction[]')
            for i in range(len(step_instructions)):
                if step_instructions[i]:
                    Step.create({
                        'recipe_id': new_rec.id,
                        'step_number': i + 1,
                        'instruction': step_instructions[i]
                    })

            flash('成功新增食譜！', 'success')
            return redirect(url_for('recipe.view_recipe', recipe_id=new_rec.id))
        else:
            flash('新增失敗，請稍後再試。', 'danger')

    return render_template('edit_recipe.html')

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    HTTP GET /recipe/<recipe_id>/edit: 將舊有的資料塞入表單預設。
    HTTP POST /recipe/<recipe_id>/edit: 將資料內容修改後提交更新。
    """
    if 'user_id' not in session:
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))

    recipe = Recipe.get_by_id(recipe_id)
    if not recipe or recipe.user_id != session['user_id']:
        flash('您無權限編輯此食譜', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        image_url = request.form.get('image_url', recipe.image_url)

        if not title or not description or not category:
            flash('請填妥所有必填欄位！', 'danger')
            return render_template('edit_recipe.html', recipe=recipe)
            
        update_data = {
            'title': title,
            'description': description,
            'category': category,
            'image_url': image_url
        }
        if Recipe.update(recipe_id, update_data):
            # 若實務上允許更動 ingredients 與 steps，需要在此處先刪除關聯舊的，再次重新寫入
            # MVP 中這邊僅實作更新食譜標題與本文的邏輯。
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))
        else:
            flash('更新失敗，請稍後再試。', 'danger')

    return render_template('edit_recipe.html', recipe=recipe)

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    HTTP POST /recipe/<recipe_id>/delete:
    直接從 DB 硬刪去並透過 cascade 拿掉所有關連子檔案，回傳並 redirect 回 /profile。
    """
    if 'user_id' not in session:
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))

    recipe = Recipe.get_by_id(recipe_id)
    is_admin = session.get('is_admin', False)
    if not recipe or (recipe.user_id != session['user_id'] and not is_admin):
        flash('您無權限刪除此食譜', 'danger')
        return redirect(url_for('main.index'))
    
    if Recipe.delete(recipe_id):
        flash('已成功刪除食譜。', 'success')
    else:
        flash('刪除失敗。', 'danger')
    return redirect(url_for('auth.profile'))

@recipe_bp.route('/<int:recipe_id>/favorite', methods=['POST'])
def toggle_favorite(recipe_id):
    """
    HTTP POST /recipe/<recipe_id>/favorite:
    切換收藏狀態，若以存在則取消，否則加入。
    """
    if 'user_id' not in session:
        flash('請先登入以使用收藏功能', 'warning')
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('食譜不存在', 'danger')
        return redirect(url_for('main.index'))
        
    existing_fav = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if existing_fav:
        Favorite.delete(existing_fav.id)
        flash('已取消收藏', 'info')
    else:
        Favorite.create({'user_id': user_id, 'recipe_id': recipe_id})
        flash('成功加入收藏！', 'success')
        
    # 可選回到原食譜或是 user profile 頁面
    return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))
