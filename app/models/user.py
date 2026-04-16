from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    recipes = db.relationship('Recipe', backref='author', lazy=True, cascade="all, delete-orphan")
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, data):
        """
        新增一筆使用者記錄
        data: 包含 username, email, password_hash, is_admin 的字典
        """
        try:
            user = cls(**data)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"[User.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有使用者記錄
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"[User.get_all] Error: {e}")
            return []

    @classmethod
    def get_by_id(cls, record_id):
        """
        取得單筆使用者記錄
        """
        try:
            return cls.query.get(record_id)
        except Exception as e:
            print(f"[User.get_by_id] Error: {e}")
            return None

    @classmethod
    def update(cls, record_id, data):
        """
        更新特定使用者記錄
        data: 需要更新的欄位與值 dict
        """
        try:
            user = cls.query.get(record_id)
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                db.session.commit()
                return user
            return None
        except Exception as e:
            db.session.rollback()
            print(f"[User.update] Error: {e}")
            return None

    @classmethod
    def delete(cls, record_id):
        """
        刪除特定使用者記錄
        """
        try:
            user = cls.query.get(record_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"[User.delete] Error: {e}")
            return False
