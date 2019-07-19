from app.libs.redprint import RedPrint
from flask import request, jsonify, g
from app.models.address import MemberAddress
from app.models.order import PayOrder
from app.models.comment import MemberComments
from app import db

api = RedPrint(name='comment', description='评价视图')


@api.route('/add', methods=['POST'])
def add():
    res = {'code': 1, 'msg': '成功', 'data': {}}

    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '验证失败'
        return jsonify(res)

    order_sn = request.form.get('order_sn')
    content = request.form.get('content')
    score = request.form.get('score')

    if not all([order_sn, content, score]):
        res['code'] = -1
        res['msg'] = '参数不全'
        return jsonify(res)

    if score not in ['10', '6', '0']:
        res['code'] = -1
        res['msg'] = '分数不对'
        return jsonify(res)

    payorder = PayOrder.query.filter_by(order_sn=order_sn).first()

    if not payorder:
        res['code'] = -1
        res['msg'] = '订单不存在'
        return jsonify(res)

    membercomments = MemberComments()
    membercomments.pay_order_id = payorder.id
    membercomments.member_id = member.id
    membercomments.score = score
    membercomments.content = content

    db.session.add(membercomments)

    payorder.status = 1
    db.session.add(payorder)
    db.session.commit()

    return jsonify(res)


@api.route('/list1')
def list1():
    resp = {'code': 1, 'msg': '成功', 'data': {}}

    member = g.member

    if not member:
        resp['code'] = -1
        resp['msg'] = '验证失败'
        return jsonify(resp)

    membercomments = MemberComments.query.filter_by(member_id=member.id).all()
    '''
    list: [
            {
                date: "2018-07-01 22:30:23",
                order_number: "20180701223023001",
                content: "记得周六发货",
            },
            {
                date: "2018-07-01 22:30:23",
                order_number: "20180701223023001",
                content: "记得周六发货",
            }
        ]

   '''
    list = []
    for mc in membercomments:
        temp_mc = {}
        temp_mc['date'] = mc.create_time.strftime('%Y-%m-%d')
        temp_mc['order_number'] = mc.pay_order_id
        temp_mc['content'] = mc.content
        list.append(temp_mc)
    resp['data']['list'] = list

    return jsonify(resp)