from app.interceptor.apiInterceptor import *

# 注册蓝图
from app.api.v1 import createBluePrint
app.register_blueprint(createBluePrint(), url_prefix='/api/v1')

# 注册管理后台
from app.admin import admin_page
app.register_blueprint(admin_page,url_prefix='/admin')