from app import db

from datetime import datetime
from flask_login import UserMixin
from .baseModel import BaseModel


# # 用户表
class User(UserMixin, BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    role = db.Column(db.String(64), nullable=True)
    password_hash = db.Column(db.String(128))
    head_img = db.Column(db.String(1024), unique=False, nullable=True)

    from app import login_manager
    @login_manager.user_loader
    def load_user(userid):
        user = User.query.filter_by(id=userid).first()
        return user

    def verity_password(originPassword, password):
        from app.utils import common
        newpassword = common.md5(originPassword)
        return password == newpassword

    def __repr__(self):
        return '<User %r>' % self.username
