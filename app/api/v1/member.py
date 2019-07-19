from app.libs.redprint import RedPrint
from flask import request,jsonify,current_app,g
from app.models.member import Member,OauthMemberBind
from app.service.memberService import memberService
from app.utils.common import BuildStaticUrl
from app import db
# 导入food模型类
from app.models.food import Food
import requests
api = RedPrint('member',description='会员模块')


"""授权登陆"""
@api.route('/login',methods=['POST'])
def login():
    res = {'code':1,'msg':'成功','data':{}}
    nickname = request.form.get('nickname')
    avataUrl = request.form.get('avataUrl')
    gender = request.form.get('gender')
    code = request.form.get('code')
    print(nickname,avataUrl,gender,code)
    if len(code) < 1:
        res['code'] = -1
        res['msg'] = 'code有误'
        return jsonify(res)
    if not all([nickname,avataUrl,gender,code]):
        res['code'] = -1
        res['msg'] = '参数有误'
        return jsonify(res)
    open_id = memberService.getOpenid(code)
    print(open_id,'---------------------')
    if not open_id:
        res['code'] = -1
        res['msg'] = '获取openid出错'
        return jsonify(res)
    oauthmemberbind = OauthMemberBind.query.filter_by(openid=open_id).first()

    if not oauthmemberbind:
        member = Member()
        member.nickname = nickname
        member.avatar = avataUrl
        member.gender = gender
        member.salt = memberService.getSalt()

        db.session.add(member)
        db.session.commit()

        oauthmemberbind = OauthMemberBind()
        oauthmemberbind.openid = open_id
        oauthmemberbind.client_type = 'wx'
        oauthmemberbind.type = 1
        oauthmemberbind.member_id = member.id

        db.session.add(oauthmemberbind)
        db.session.commit()

    member = Member.query.get(oauthmemberbind.member_id)
    token = "%s#%s"%(memberService.geneAuthCode(member),member.id)
    res['data']['token'] = token
    return jsonify(res)

"""授权登陆后跳转首页视图"""
@api.route('/cklogin',methods = ['POST'])
def cklogin():
    res = {'code':1,'msg':'成功','data':{}}
    code = request.form.get('code')
    if len(code) < 1:
        res['code'] = -1
        res['msg'] = 'code有误'
        return jsonify(res)
    open_id = memberService.getOpenid(code)
    if not open_id:
        res['code'] = -1
        res['msg'] = '获取openid出错'
        return jsonify(res)
    oauthmemberbind = OauthMemberBind.query.filter_by(openid=open_id).first()

    if not oauthmemberbind:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)
    member = Member.query.get(oauthmemberbind.member_id)
    token = "%s#%s"%(memberService.geneAuthCode(member),member.id)
    res['data']['token'] = token
    return jsonify(res)

@api.route('/info',methods=['POST'])
def info():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    # 验证登陆
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '请登陆'
        return jsonify(res)


    # member_n = request.form.get(member.id)

    user_info = {}
    user_info['nickname'] = member.nickname
    user_info['avataUrl'] = member.avatar


    res['data']['user_info'] = user_info

    return jsonify(res)

