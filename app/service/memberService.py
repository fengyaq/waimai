import random
import string
import hashlib
from flask import current_app
import requests
class memberService():

    @staticmethod
    def geneAuthCode(member=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member.id, member.salt, member.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    # app_id=current_app['APP_ID']
    #     app_secert = current_app['APP_SECERT']
    #     # 前端调用wx.login()获取临时登陆凭证code 并且回传给开发者服务器
    #     # 调用auth.code2session()拿到open_id<用户的唯一标识>会话密钥session_key
    #     # 在项目config文件下存入密钥信息
    #     #     APP_SECERT=''
    #     #     APP_ID=
    #     # GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
    #
    # url='https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'\
    #         .format(app_id,app_secert,res['data'])
    #     print(url)
    #     response=request.get(url)
    #     content=request.json()
    #     open_id=content.get('openid')
    #     print(response)
    def getOpenid(code):
        app_id = current_app.config.get('APP_ID')
        app_secret = current_app.config.get('APP_SECRET')
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(app_id, app_secret, code)
        response = requests.get(url)
        content = response.json()
        print(content)
        open_id = content.get('openid')
        return open_id

    @staticmethod
    def getSalt(len=16):
        str = [random.choice(string.ascii_letters + string.digits) for _ in range(1, len + 1)]

        ran_str = "".join(str)

        return ran_str

