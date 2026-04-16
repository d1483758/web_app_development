from . import db
from datetime import datetime

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade="all, delete-orphan")
    steps = db.relationship('Step', backref='recipe', lazy=True, cascade="all, delete-orphan")
    favorited_by = db.relationship('Favorite', backref='recipe', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, data):
        """
        新增一筆食譜記錄
        data: 包含 title, description, category, user_id, image_url 的字典
        """
        try:
            recipe = cls(**data)
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            print(f"[Recipe.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有食譜記錄
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"[Recipe.get_all] Error: {e}")
            return []

    @classmethod
    def get_by_id(cls, record_id):
        """
        取得單筆食譜記錄
        """
        try:
            return cls.query.get(record_id)
        except Exception as e:
            print(f"[Recipe.get_by_id] Error: {e}")
            return None

    @classmethod
    def update(cls, record_id, data):
        """
        更新特定食譜記錄
        data: 需要更新的欄位與值 dict
        """
        try:
            recipe = cls.query.get(record_id)
            if recipe:
                for key, value in data.items():
                    if key != 'updated_at':
                        setattr(recipe, key, value)
                recipe.updated_at = datetime.utcnow()
                db.session.commit()
                return recipe
            return None
        except Exception as e:
            db.session.rollback()
            print(f"[Recipe.update] Error: {e}")
            return None

    @classmethod
    def delete(cls, record_id):
        """
        刪除特定食譜記錄
        """
        try:
            recipe = cls.query.get(record_id)
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"[Recipe.delete] Error: {e}")
            return False
