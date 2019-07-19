from app import db
from datetime import datetime


class BaseModel(object):
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now())
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now(), onupdate=datetime.now())
