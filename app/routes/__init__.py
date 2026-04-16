from flask import Blueprint

# 註冊 Blueprints 到主要 Flask instance 時使用的函式
def init_routes(app):
    from .main import main_bp
    from .auth import auth_bp
    from .recipe import recipe_bp
    from .admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp, url_prefix='/recipe')
    app.register_blueprint(admin_bp, url_prefix='/admin')
