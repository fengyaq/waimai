from app.libs.redprint import RedPrint
from flask import request,jsonify,current_app
from app import db
# 导入food模型类
from app.models.food import Food,Category
from app.models.cart import MemberCart
# 添加拼接路径是一个静态方法 用来做url路径拼接用
from app.utils.common import BuildStaticUrl
import requests
api = RedPrint('food',description='食品视图')

"""
banners: [
                {
                    "id": 1,
                    "pic_url": "/images/food.jpg"
                },
                {
                    "id": 2,
                    "pic_url": "/images/food.jpg"
                },
                {
                    "id": 3,
                    "pic_url": "/images/food.jpg"
                }
            ],
            categories: [
                {id: 0, name: "全部"},
                {id: 1, name: "川菜"},
                {id: 2, name: "东北菜"},
            ],
"""

@api.route('/search')
def search():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    foods = Food.query.filter_by(status=1).limit(3).all()
    # 轮播图
    banners = []
    for food in foods:
        temp_food = {}
        temp_food['id'] = food.id
        temp_food['pic_url'] = BuildStaticUrl(food.main_image)

        banners.append(temp_food)

    # 分类
    categorys = Category.query.filter_by(status=1).all()
    categories = []
    # 假数据
    categories.append({
        'id':0,'name':'全部'
    })
    for category in categorys:
        temp_category = {}
        temp_category['id'] = category.id
        temp_category['name'] = category.name
        categories.append(temp_category)

    res['data']['banners'] = banners
    res['data']['categories'] = categories
    return jsonify(res)



@api.route('/all')
def all():
    res = {'code':1,'msg':'成功','data':{}}
    try:
        cid = request.args.get('cid')
        page = request.args.get('page')
        if not cid:
            cid = '0'

        if not page:
            page = '1'
        cid = int(cid)
        page = int(page)

        """每页一个"""
        pagesize = 1                   #---
        # 公式，记住   分页                  |
        offset = (page-1)*pagesize     #---

        goods = []
        query = Food.query.filter_by(status=1)
        if cid == 0:
            foods = query.offset(offset).limit(pagesize).all()
        else:
            foods = query.filter_by(cat_id=cid).offset(offset).limit(pagesize).all()

        for food in foods:
            temp_data = {}
            temp_data['id'] = food.id
            temp_data['name'] = food.name
            temp_data['min_price'] = str(food.price)
            temp_data['price'] = str(food.price)
            temp_data['pic_url'] = BuildStaticUrl(food.main_image)
            goods.append(temp_data)

        res['data']['goods'] = goods
        if len(foods) < pagesize:
            res['data']['ismore'] = 0
        else:
            res['data']['ismore'] = 1
        return jsonify(res)
    except Exception as e:
        res['code'] = -1
        res['msg'] = '参数错误'
        return jsonify(res)




@api.route('/info')
def info():
    res = {'code':1,'msg':'成功','data':{}}
    try:
        id = request.args.get('id')
        if not id:
            res['code'] = -1
            res['msg'] = '参数不能为空'
            return jsonify(res)
        id =int(id)
        if id <= 0:
            res['code'] = -1
            res['msg'] = '参数有误'
            return jsonify(res)

        food = Food.query.get(id)
        info={}
        info['id'] = food.id
        info['name'] = food.name
        info['summary'] = food.summary
        info['total_count'] = food.total_count
        info['comment_count'] = food.comment_count
        info['stock'] = food.stock
        info['price'] = str(food.price)
        info['main_image'] = BuildStaticUrl(food.main_image)
        info['pics'] = [BuildStaticUrl(food.main_image),BuildStaticUrl(food.main_image),BuildStaticUrl(food.main_image)]
        res['data']['info'] = info

        return jsonify(res)
    except Exception as e:
        res['code'] = -1
        res['msg'] = '参数有误'
        return jsonify(res)
