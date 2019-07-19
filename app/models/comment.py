from app.models.baseModel import BaseModel
from app import db


class MemberComments(BaseModel, db.Model):
    __tablename__ = 'member_comments'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    pay_order_id = db.Column(db.Integer, db.ForeignKey('pay_order.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=1)
    content = db.Column(db.String(200), nullable=False, default='')

    @property
    def score_desc(self):
        score_map = {
            "10": "好评",
            "6": "中评",
            "0": "差评",
        }
        return score_map[str(self.score)]
