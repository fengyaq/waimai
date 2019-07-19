from app.libs.redprint import RedPrint
from flask import request,jsonify,g
from app.models.cart import MemberCart
from app.models.food import Food
from app.models.address import MemberAddress
from app.utils.common import BuildStaticUrl
from app.models.order import PayOrder,PayOrderItem
import json
from app import db
api = RedPrint('order',description='订单视图')

# @api.route('/commit',methods=['POST'])
# def commit():
#     res = {'code': 1, 'msg': '成功', 'data': {}}
#     ids = request.form.get('ids')  # 商品id
#
#     ids = json.loads(ids) # 转列表
#
#     member = g.member
#     if not member:
#         res['code'] = -1
#         res['msg'] = '用户不存在'
#         return jsonify(res)
#
#
#     """
#      goods_list: [
#             // {
#             //     id:22,
#             //     name: "小鸡炖蘑菇",
#             //     price: "85.00",
#             //     pic_url: "/images/food.jpg",
#             //     number: 1,
#             // },
#             // {
#             //     id:22,
#             //     name: "小鸡炖蘑菇",
#             //     price: "85.00",
#             //     pic_url: "/images/food.jpg",
#             //     number: 1,
#             // }
#         ],
#         default_address: {
#             name: "编程浪子",
#             mobile: "12345678901",
#             detail: "上海市浦东新区XX",
#         },
#         yun_price: "1.00",
#         pay_price: "85.00",
#         total_price: "86.00",
#         params: null,
#     """
#
#
#
#
#     goods_list = []
#     yun_price = 0
#     total_price = 0
#     default_address ={}
#     # 大写改小写ctrl + shift + u
#
#     for id in ids:
#         temp_data = {}
#         membercart = MemberCart.query.filter_by(food_id=id,member_id=member.id).first()
#         food = Food.query.get(id)
#         temp_data['id'] = id
#         temp_data['name'] = food.name
#         temp_data['price'] = str(food.price)
#         temp_data['pic_url'] = BuildStaticUrl(food.main_image)
#         temp_data['number'] = membercart.quantity
#
#         goods_list.append(temp_data)
#         total_price = membercart.quantity * food.price
#
#     # 查询此会员的默认地址
#         address = MemberAddress.query.filter_by(member_id=member.id,is_default=1).first()
#
#         default_address['id'] = address.id
#         default_address['name'] = address.nickname
#         default_address['mobile'] = address.mobile
#         default_address['detail'] = str(address.province_str + address.city_str + address.area_str)
#
#
#     # 计算总价
#
#     res['data']['goods_list'] = goods_list
#     res['data']['default_address'] = default_address
#     # res['data']['yun_price'] = str(yun_price)
#     # res['data']['pay_price'] = str(pay_price)
#     res['data']['total_price'] = total_price
#
#
#     return jsonify(res)


@api.route('/commit', methods=['POST'])
def commit():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    ids = request.form.get('ids')
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '该用户不存在'
        return jsonify(res)
    ids = json.loads(ids)

    '''
    id:22,
                name: "小鸡炖蘑菇",
                price: "85.00",
                pic_url: "/images/food.jpg",
                number: 1,

                yun_price: "1.00",
                pay_price: "85.00",
                total_price: "86.00",
                params: null
    '''
    goods_list = []
    yun_price= 0
    pay_price=0
    for id in ids:
        temp_data = {}
        membercart = MemberCart.query.filter_by(member_id=member.id,food_id=id).first()

        food = Food.query.get(id)


        temp_data['id'] = id
        temp_data['name'] = food.name
        temp_data['price'] = str(food.price)
        temp_data['pic_url'] = BuildStaticUrl(food.main_image)
        temp_data['number'] = membercart.quantity
        goods_list.append(temp_data)
        # print(temp_data)
        pay_price += membercart.quantity * food.price

    memberaddress = MemberAddress.query.filter_by(member_id=member.id,is_default=1).first()

    # 地址
    default_address = {}
    default_address['id'] = memberaddress.id
    default_address['name'] = memberaddress.nickname
    default_address['mobile'] = memberaddress.mobile
    default_address['address'] = str(memberaddress.province_str + memberaddress.city_str + memberaddress.area_str+memberaddress.address)

    total_price =yun_price + pay_price

    res['data']['goods_list'] = goods_list
    res['data']['default_address'] = default_address
    res['data']['total_price'] = str(total_price)
    res['data']['yun_price'] = str(yun_price)
    res['data']['pay_price'] = str(pay_price)
    return jsonify(res)



@api.route('/create', methods=['POST'])
def create():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:
        member = g.member
        if not member:
            res['code'] = -1
            res['msg'] = '该用户不存在'
            return jsonify(res)

        ids = request.form.get('ids')
        address_id = request.form.get('address_id')
        note = request.form.get('note')

        pay_price = 0
        yun_price = 0
        ids = json.loads(ids)
        # 根据ids查购物车
        for id in ids:
            membercart = MemberCart.query.filter_by(member_id=member.id,food_id=id).first()
            if not membercart:
                continue

            food =Food.query.get(id)

            if not food or food.status != 1:
                continue

            pay_price += food.price * membercart.quantity

        memberaddress = MemberAddress.query.get(address_id)

        if not memberaddress:
            res['code'] = -1
            res['msg'] = '地址不存在'
            return jsonify(res)

        #  1生成订单
        payorder = PayOrder()
        payorder.order_sn =geneOrderSn()  # 唯一
        payorder.total_price = yun_price + pay_price
        payorder.yun_price = yun_price
        payorder.pay_price = pay_price
        payorder.note = note
        payorder.status = -8  # 待付款
        payorder.express_status = -1 # 待发货
        payorder.express_address_id = address_id
        payorder.express_info = memberaddress.showAddress()
        payorder.comment_status = -1 # 待评论
        payorder.member_id = member.id

        db.session.add(payorder)

        # 2扣库存
        foods = db.session.query(Food).filter(Food.id.in_(ids)).with_for_update().all()
        temp_stock ={} # 临时库存

        for food in foods:
            temp_stock[food.id] = food.stock

        for id in ids:
            membercart = MemberCart.query.filter_by(member_id=member.id, food_id=id).first()

            if membercart.quantity > temp_stock[id]:
                res['code'] = -1
                res['msg'] = '库存不足'
                return jsonify(res)
            # 更新库存
            food = db.session.query(Food).filter(Food.id == id).update({
                'stock':temp_stock[id]-membercart.quantity
            })
            if not food:
                raise  Exception('更新失败')

            food = Food.query.get(id)

            # 3 生成订单的商品从表
            payorderitem = PayOrderItem()
            payorderitem.quantity = membercart.quantity
            payorderitem.price = food.price
            payorderitem.note = note
            payorderitem.status = 1
            payorderitem.pay_order_id = payorder.id
            payorderitem.member_id = member.id
            payorderitem.food_id = id

            db.session.add(payorderitem)

            # 4清空购物车
            db.session.delete(membercart) # 删除已经下单的购物车

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        res['code'] = -1
        res['msg'] = '出现异常'
        return jsonify(res)

    return jsonify(res)



import hashlib
import random
import time
def geneOrderSn():
    m = hashlib.md5()
    sn = None
    while True:
        str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
        m.update(str.encode("utf-8"))
        sn = m.hexdigest()
        if not PayOrder.query.filter_by(order_sn=sn).first():
            break
    return sn


@api.route('/list')
def list():
    res = {'code': 1, 'msg': '成功', 'data': {}}

    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '该用户不存在'
        return jsonify(res)

    # // ["待付款", "待发货", "待收货", "待评价", "已完成", "已关闭"]
    # // ["-8", "-7", "-6", "-5", "1", "0"]

    status = request.args.get('status')
    print(status,'----------------------------')

    order_list = []
    payorders = PayOrder.query.filter_by(member_id=member.id,status=status).all()
    for payorder in payorders:
        temp_data = {}
        temp_data['status'] = payorder.status
        temp_data['status_desc'] = payorder.status_desc
        temp_data['date'] = payorder.create_time.strftime('%Y-%m-%d %H:%M:%S')
        temp_data['note'] = payorder.note
        temp_data['order_sn'] = payorder.order_sn
        temp_data['total_price'] = str(payorder.total_price)
        temp_data['order_number'] = payorder.create_time.strftime('%Y%m%d%H%M%S')+str(payorder.id).zfill(5)
        goods_list = []

        # 查订单商品
        payorderitems = PayOrderItem.query.filter_by(pay_order_id=payorder.id).all()
        for payorderitem in payorderitems:
            food = Food.query.get(payorderitem.food_id)
            temp_food = {}
            temp_food['pic_url'] = BuildStaticUrl(food.main_image)

            goods_list.append(temp_food)

        temp_data['goods_list'] = goods_list
        order_list.append(temp_data)

    res['data']['order_list'] = order_list
    return jsonify(res)


# # 从商品详情页立即购买提交订单
# @api.route('/nowbuy', methods=['GET', 'POST'])
# def nowbuy():
#         res = {'code': 1, 'msg': 'successful', 'data': {}}
#
#         id = request.form.get('id')  # 商品id
#         num = request.form.get('num')
#
#         if not num:
#             res['code'] = -1
#             res['msg'] = '参数不全'
#             return jsonify(res)
#
#         if not id:
#             res['code'] = -1
#             res['msg'] = '参数不全 '
#             return jsonify(res)
#
#         member = g.member
#
#         if not member:
#             res['code'] = -1
#             res['msg'] = '验证失败'
#             return jsonify(res)
#
#         id = int(id)
#         num = int(num)
#         goods_list = []  # 商品
#         yun_price = 0  # 运费
#         pay_price = 0  # 商品金额
#
#         food = Food.query.get(id)
#
#         if not food or food.status != 1:
#             res['code'] = -1
#             res['msg'] = '商品不存在'
#             return jsonify(res)
#
#         temp_food = {}
#         temp_food['id'] = food.id
#         temp_food['name'] = food.name
#         temp_food['price'] = str(food.price)
#         temp_food['pic_url'] = BuildStaticUrl(food.main_image)
#         temp_food['number'] = num
#
#         pay_price = num * food.price
#         goods_list.append(temp_food)
#
#         address = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()
#
#         default_address = {
#             'id': address.id,
#             'name': address.nickname,
#             'mobile': address.mobile,
#             'detail': address.province_str + address.city_str + address.area_str + address.address,
#         }
#
#         res['data']['goods_list'] = goods_list
#         res['data']['default_address'] = default_address
#         res['data']['yun_price'] = str(yun_price)
#         res['data']['pay_price'] = str(pay_price)
#         res['data']['total_price'] = str(pay_price + yun_price)
#
#         return jsonify(res)


#立即购买
@api.route('/info', methods=['POST'])
def info():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    id = request.values.get('id')#商品id
    num = request.values.get('num')  # 商品数量
    id = int(id)
    num = int(num)
    if not id:
        res['code'] = -1
        res['msg'] = 'id不存在'
        return jsonify(res)
    if not num:
        res['code'] = -1
        res['msg'] = 'num不存在'
        return jsonify(res)
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '该用户不存在'
        return jsonify(res)
    goods_list = []
    yun_price = 0
    pay_price = 0
    food = Food.query.get(id)
    if not food:
        res['code'] = -1
        res['msg'] = '商品不存在'
        return jsonify(res)
    temp_data = {}
    temp_data['id'] = id
    temp_data['name'] = food.name
    temp_data['price'] = str(food.price)
    temp_data['pic_url'] = BuildStaticUrl(food.main_image)
    temp_data['number'] = num
    goods_list.append(temp_data)

    pay_price += num * food.price

    address = MemberAddress.query.filter_by(member_id = member.id,is_default = 1).first()
    default_address = {}
    default_address['id'] = address.id
    default_address['name'] = address.nickname
    default_address['mobile'] = address.mobile
    default_address['address'] = address.showAddress()

    total_price = yun_price + pay_price
    res['data']['goods_list'] = goods_list
    res['data']['default_address'] = default_address
    res['data']['total_price'] = str(total_price)
    res['data']['yun_price'] = str(yun_price)
    res['data']['pay_price'] = str(pay_price)
    return jsonify(res)








