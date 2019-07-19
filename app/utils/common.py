import logging
from flask import current_app
ALLOWED_file_EXTENSIONS = set(['md', 'MD', 'word', 'txt', 'py', 'java', 'c', 'c++', 'xlsx'])
ALLOWED_photo_EXTENSIONS = set(['png', 'jpg', 'xls', 'JPG', 'PNG', 'gif', 'GIF'])

import hashlib


# md5 32位加密
def md5(strs):
    m2 = hashlib.md5()
    m2.update(strs.encode('utf8'))
    return m2.hexdigest()


def verifyMd5(strs, hash_strs):
    if md5(strs) == hash_strs:
        return True
    else:
        return False


# 生成随机数量
from random import Random


def random_str(randomlength=5):
    _str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        _str += chars[random.randint(0, length)]
    return _str


def allowed_photo(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_photo_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_file_EXTENSIONS


# 截取字符串
def getstrsplit(beginint, strs):
    lens = len(strs)
    return strs[beginint:lens]


def trueReturn(data, msg='success'):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg='fail'):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }


# 判断是不是数字
def isNum(arg):
    try:
        int(arg)
        return True
    except Exception as e:
        return False
    # if isinstance(arg, int):
    #     return True
    #
    # if not isinstance(arg, str):
    #     return False
    #
    # if arg.isdigit():
    #     return True
# 构造静态图片绝对路径
def BuildStaticUrl(url):
    static_id = current_app.config.get('STATIC_ID') + url
    return static_id

# def buildPicUrl(url):
#     static_d = current_app.config.get('STATIC_D')
#     return static_d + url
