from app.models.baseModel import  BaseModel
from app import db
from datetime import datetime
class PayOrder(BaseModel, db.Model):
    __tablename__ = 'pay_order'

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(40), nullable=False, unique=True, default='') # 随机签名
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)# 总价
    yun_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)# 运费
    pay_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)# 实付总价
    pay_sn = db.Column(db.String(128), nullable=False, default='')# 第三方流水号
    prepay_id = db.Column(db.String(128), nullable=False, default='') # 第三方预付id
    note = db.Column(db.Text, nullable=False,default='') # 备注
    status = db.Column(db.Integer, nullable=False, default=-8) # 1：支付完成 0 无效 -1 申请退款 -2 退款中 -9 退款成功  -8 待支付  -7 完成支付待确认
    express_status = db.Column(db.Integer, nullable=False, default=-8)# 快递状态，-8 待发货  -7 已发货
    express_address_id = db.Column(db.Integer, nullable=False, default=0)# 快递地址id
    express_info = db.Column(db.String(100), nullable=False, default='')#快递信息
    comment_status = db.Column(db.Integer, nullable=False, default=-8)#评论状态 -8 未评级 -7已评级
    pay_time = db.Column(db.DateTime, nullable=False,default=datetime.now())#付款到账时间
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)# 会员id


    @property
    def status_desc(self):
        if self.status == -8:
            return '待付款'
        elif self.status == -7:
            return '待发货'
        elif self.status == -6:
            return '待收货'
        elif self.status == -5:
            return '待评价'
        elif self.status == 1:
            return '已完成'
        elif self.status == 0:
            return '已关闭'


class PayOrderItem(BaseModel,db.Model):
    __tablename__ = 'pay_order_item'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0) #数量
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)# 价格
    note = db.Column(db.Text, nullable=False)# 备注
    status = db.Column(db.Integer, nullable=False, default=1)#1：成功 0 失败
    pay_order_id = db.Column(db.Integer, db.ForeignKey('pay_order.id'), nullable=False)# 订单id
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)# 会员表
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)# 美食表-