from app import db
from app.models.baseModel import BaseModel

class Member(BaseModel, db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, default='')
    mobile = db.Column(db.String(11), nullable=False, default='')
    gender = db.Column(db.Integer, nullable=False, default=0)
    avatar = db.Column(db.String(200), nullable=False, default='')
    salt = db.Column(db.String(32), nullable=False, default='')
    reg_ip = db.Column(db.String(100), nullable=False, default='')
    status = db.Column(db.Integer, nullable=False, default=1)  # 1有效  0无效

    @property
    def status_desc(self):
        return self.status

    @property
    def sex_desc(self):
        sex_mapping = {
            "0": "未知",
            "1": "男",
            "2": "女"
        }
        return sex_mapping[str(self.gender)]


class OauthMemberBind(BaseModel, db.Model):
    __tablename__ = 'oauth_member_bind'

    id = db.Column(db.Integer, primary_key=True)
    client_type = db.Column(db.String(20), nullable=False, default='')  # 客户端来源类型。qq,weibo,weixin
    type = db.Column(db.Integer, nullable=False, default=0)  # 类型 type 1:wechat ,
    openid = db.Column(db.String(80), nullable=False, default='')  # 第三方id
    unionid = db.Column(db.String(100), nullable=False, default='')
    extra = db.Column(db.Text, nullable=False, default='')  # 额外字段
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)


# {
#     'a':1
#     'b':1
#     'c':1
# }