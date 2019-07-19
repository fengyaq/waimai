# 做url路径拼接用
from flask import current_app

class UrlService():
    @staticmethod
    def BuildStaticUrl(url):
        full_url=current_app.config.get('DOMAIN')+'/static/'+url
        return full_url
