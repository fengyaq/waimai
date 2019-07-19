from app import db
from .baseModel import BaseModel

class MemberAddress(db.Model):
    __tablename__ = 'member_address'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    nickname = db.Column(db.String(20), nullable=False, default='')
    mobile = db.Column(db.String(11), nullable=False,default='')
    province_id = db.Column(db.Integer, nullable=False, default=0)
    province_str = db.Column(db.String(50), nullable=False, default='')
    city_id = db.Column(db.Integer, nullable=False, default=0)
    city_str = db.Column(db.String(50), nullable=False, default='')
    area_id = db.Column(db.Integer, nullable=False, default=0)
    area_str = db.Column(db.String(50), nullable=False, default='')
    address = db.Column(db.String(100), nullable=False, default='')
    status = db.Column(db.Integer, nullable=False, default=1)
    is_default = db.Column(db.Integer, nullable=False)

    def showAddress(self):
        return self.province_str+self.city_str+self.area_str+self.address
