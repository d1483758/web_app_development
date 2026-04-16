from . import db
from datetime import datetime

class Step(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data):
        """
        新增一筆步記錄
        data: 包含 recipe_id, step_number, instruction 的字典
        """
        try:
            step = cls(**data)
            db.session.add(step)
            db.session.commit()
            return step
        except Exception as e:
            db.session.rollback()
            print(f"[Step.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有步驟記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"[Step.get_all] Error: {e}")
            return []

    @classmethod
    def get_by_id(cls, record_id):
        """取得單筆步驟記錄"""
        try:
            return cls.query.get(record_id)
        except Exception as e:
            print(f"[Step.get_by_id] Error: {e}")
            return None

    @classmethod
    def update(cls, record_id, data):
        """更新特定步驟記錄"""
        try:
            step = cls.query.get(record_id)
            if step:
                for key, value in data.items():
                    setattr(step, key, value)
                db.session.commit()
                return step
            return None
        except Exception as e:
            db.session.rollback()
            print(f"[Step.update] Error: {e}")
            return None

    @classmethod
    def delete(cls, record_id):
        """刪除特定步驟記錄"""
        try:
            step = cls.query.get(record_id)
            if step:
                db.session.delete(step)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"[Step.delete] Error: {e}")
            return False
