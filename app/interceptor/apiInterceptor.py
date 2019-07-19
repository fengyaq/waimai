from app import app
from flask import request,jsonify,g,current_app
from app.models.member import Member
from app.service.memberService import memberService



@app.before_request
def before_request():
    # 前端api接口忽略
    ignore_urls = current_app.config.get('IGNORE_URLS')
    if request.path in ignore_urls:
        return

    # 管理后台和静态文件
    if '/api' not in request.url or '/static' in request.url:
        return

    print('before_requestbefore_requestbefore_requestbefore_requestbefore_request')
    resp = {'code': 1, 'msg': '成功', 'data': {}}
    # f19f1e60450b2341fc69a2a9122eb33c#3     取到token

    g.member = None
    token = request.headers.get('token')

    if not token:
        resp['code'] = -1
        resp['msg'] = '必须登录'
        return jsonify(resp)
    # (f19f1e60450b2341fc69a2a9122eb331,3)
    tuple_token = token.split('#')

    if len(tuple_token) != 2:
        resp['code'] = -1
        resp['msg'] = 'token错误'
        return jsonify(resp)

    # 查会员
    member = Member.query.get(tuple_token[1])

    # 如果查不到会员
    if not member:
        resp['code'] = -1
        resp['msg'] = '没有找到该用户'
        return jsonify(resp)

    # 根据查到会员 生成token
    c_token = memberService.geneAuthCode(member)

    # 根据生成的token跟取到token
    if c_token != tuple_token[0]:
        resp['code'] = -1
        resp['msg'] = 'token错误'
        return jsonify(resp)

    g.member = member

