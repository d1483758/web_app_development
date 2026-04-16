from . import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data):
        """
        新增一筆收藏記錄
        data: 包含 user_id, recipe_id 的字典
        """
        try:
            favorite = cls(**data)
            db.session.add(favorite)
            db.session.commit()
            return favorite
        except Exception as e:
            db.session.rollback()
            print(f"[Favorite.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有收藏記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"[Favorite.get_all] Error: {e}")
            return []

    @classmethod
    def get_by_id(cls, record_id):
        """取得單筆收藏記錄"""
        try:
            return cls.query.get(record_id)
        except Exception as e:
            print(f"[Favorite.get_by_id] Error: {e}")
            return None

    @classmethod
    def update(cls, record_id, data):
        """更新特定收藏記錄"""
        try:
            favorite = cls.query.get(record_id)
            if favorite:
                for key, value in data.items():
                    setattr(favorite, key, value)
                db.session.commit()
                return favorite
            return None
        except Exception as e:
            db.session.rollback()
            print(f"[Favorite.update] Error: {e}")
            return None

    @classmethod
    def delete(cls, record_id):
        """刪除特定收藏記錄"""
        try:
            favorite = cls.query.get(record_id)
            if favorite:
                db.session.delete(favorite)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"[Favorite.delete] Error: {e}")
            return False
