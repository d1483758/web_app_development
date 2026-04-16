from . import db
from datetime import datetime

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data):
        """
        新增一筆材料記錄
        data: 包含 recipe_id, name, amount 的字典
        """
        try:
            ingredient = cls(**data)
            db.session.add(ingredient)
            db.session.commit()
            return ingredient
        except Exception as e:
            db.session.rollback()
            print(f"[Ingredient.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有材料記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"[Ingredient.get_all] Error: {e}")
            return []

    @classmethod
    def get_by_id(cls, record_id):
        """取得單筆材料記錄"""
        try:
            return cls.query.get(record_id)
        except Exception as e:
            print(f"[Ingredient.get_by_id] Error: {e}")
            return None

    @classmethod
    def update(cls, record_id, data):
        """更新特定材料記錄"""
        try:
            ingredient = cls.query.get(record_id)
            if ingredient:
                for key, value in data.items():
                    setattr(ingredient, key, value)
                db.session.commit()
                return ingredient
            return None
        except Exception as e:
            db.session.rollback()
            print(f"[Ingredient.update] Error: {e}")
            return None

    @classmethod
    def delete(cls, record_id):
        """刪除特定材料記錄"""
        try:
            ingredient = cls.query.get(record_id)
            if ingredient:
                db.session.delete(ingredient)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"[Ingredient.delete] Error: {e}")
            return False
