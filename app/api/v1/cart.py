from app.libs.redprint import RedPrint
from flask import request,jsonify,current_app,g
from app import db
# 导入food模型类
from app.models.food import Food,Category
from app.models.address import MemberAddress
from app.models.cart import MemberCart
from app.service import memberService,url_service

# 添加拼接路径是一个静态方法 用来做url路径拼接用
from app.utils.common import BuildStaticUrl
import requests
api = RedPrint('cart',description='购物车视图')



@api.route('/add',methods=['POST'])
def add():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:
        member = g.member
        if not member:
            res['code'] = -1
            res['msg'] = '用户不存在'
            return jsonify(res)

        id = request.form.get('id') # 食品id
        num = request.form.get('num')
        fromtype = request.form.get('fromtype')
        if not all([id,num]):
            res['code'] = -1
            res['msg'] = '缺少参数'
            return jsonify(res)

        id = int(id)
        num = int(num)
        fromtype = int(fromtype)
        if id <= 0:
            res['code'] = -1
            res['msg'] = 'id错误'
            return jsonify(res)

        # 参数检验
        food = Food.query.get(id)

        if not food:
            res['code'] = -1
            res['msg'] = '商品不存在'
            return jsonify(res)

        if food.status != 1:
            res['code'] = -1
            res['msg'] = '商品已下架'
            return jsonify(res)

        # if num < 1:
        #     res['code'] = -1
        #     res['msg'] = '商品数量不对'
        #     return jsonify(res)

        if num > food.stock:
            res['code'] = -1
            res['msg'] = '库存不足'
            return jsonify(res)
        if fromtype == 0:  # 从加入购物车过来
            if num <= 0:
                res['code'] = -1
                res['msg'] = '参数错误'
                return jsonify(res)
        else:  # 从加减号过来
            if num != 1 and num != -1:
                res['code'] = -1
                res['msg'] = '参数错误'
                return jsonify(res)


        # 查自己购物车是否存在这个商品
        membercart = MemberCart.query.filter_by(member_id=member.id,food_id=id).first()
        if not membercart:
            membercart = MemberCart()
            membercart.food_id = id
            membercart.member_id = member.id
            membercart.quantity = num
        else:
            membercart.quantity += num
        db.session.add(membercart)
        db.session.commit()
        # 购物车 若存在，就数量累积，若不存在就创建
        res['msg'] = '添加成功'
        return jsonify(res)


    except Exception as e:
        res['code'] = -1
        res['msg'] = '参数错误'
        return jsonify(res)


@api.route('/list')
def list():
    res = {'code':1,'msg':'成功','data':{}}
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)

    membercart = MemberCart.query.filter_by(member_id=member.id).all()
    list = []
    totalPrice = 0
    for mc in membercart:
        temp_food = {}
        food = Food.query.get(mc.food_id)
        if not food or food.status != 1:
            continue

        temp_food['id'] = mc.id
        temp_food['food_id'] = mc.food_id
        temp_food['pic_url'] = url_service.UrlService.BuildStaticUrl(food.main_image)
        temp_food['name'] = food.name
        temp_food['price'] = str(food.price)
        temp_food['active'] = 'true'
        temp_food['number'] = mc.quantity

        totalPrice += mc.quantity * food.price
        list.append(temp_food)

    res['data']['list'] = list
    res['data']['totalPrice'] = str(totalPrice)
    return jsonify(res)


import json
@api.route('/delete',methods=['POST'])
def delete():
    res = {'code': 1, 'msg': '成功', 'data': {}}

    ids = request.form.get('ids')
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)

    # 变列表
    ids = json.loads(ids)

    for id in ids:
        membercat = MemberCart.query.get(id)
        # if not membercat:
        #     continue
        db.session.delete(membercat)
        db.session.commit()

    return jsonify(res)
