from app.libs.redprint import RedPrint
from app import db
# from app import
#http://127.0.0.1/api/v1/user/center
api = RedPrint('user',description='用户模块')
@api.route('/center')
def center():

    # app.logger.error('这是第一个error log')
    # app.logger.warning('这是第一个warning log')
    # app.logger.info('这是第一个info log')
    # app.logger.debug('这是第一个debug log')
    # user= User.query.get(1)
    #
    # user.name = 'xxx'
    #
    # db.session.add()
    #
    return 'center'
