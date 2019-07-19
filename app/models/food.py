from app import db
from .baseModel import BaseModel


# 分类表
class Category(BaseModel, db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False, default='')
    weight = db.Column(db.Integer, nullable=False, default=0)  # 权重
    status = db.Column(db.Integer, nullable=False, default=1)  # 状态 1：有效 0：无效
    food = db.relationship('Food', backref='category')

    @property
    def status_desc(self):
        return self.status

    def __repr__(self):
        return self.name


# 食品表
class Food(BaseModel, db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, default='')  # 名称
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)  # 售卖价格
    main_image = db.Column(db.String(100), nullable=False, default='')  # 主图
    summary = db.Column(db.String(2000), nullable=False, default='')  # 描述
    stock = db.Column(db.Integer, nullable=False, default='')  # 库存量
    tags = db.Column(db.String(200), nullable=False, default='')  # tag关键字，以,逗号分割,
    status = db.Column(db.Integer, nullable=False, default=1)  # 状态 1：有效 0：无效
    month_count = db.Column(db.Integer, nullable=False, default=0)  # 月销售量
    total_count = db.Column(db.Integer, nullable=False, default=0)  # 总销售量
    view_count = db.Column(db.Integer, nullable=False, default=0)  # 浏览次数
    comment_count = db.Column(db.Integer, nullable=False, default=0)  # 总评论量

    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
