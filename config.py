class Config():
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'
    # 配置密钥
    SECRET_KEY='Ligvdbgfsa'

    # 设置连接数据库的URL
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/wx'

    # 数据库和模型类同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True

    APP_ID = 'wx9b225ee8f9e459ad'
    APP_SECRET = 'd3792849a690e5299424f1e28aa42865'

    STATIC_ID = 'http://127.0.0.1:5000/static/'
    DOMAIN = 'http://127.0.0.1:5000'
    IGNORE_URLS = ['/api/vi/user/login']

    IGNORE_URLS = ['/api/v1/member/login',
                   '/api/v1/member/cklogin',
                   '/api/v1/food/search',
                   '/api/v1/food/all',
                   '/api/v1/food/info']

# 线上环境
class ProductingConfig(Config):
    DEBUG = False


# 生产环境
class DevelopmentConfig(Config):
    DEBUG = True


mapping_config = {
    'pro': ProductingConfig,
    'dev': DevelopmentConfig,
}
