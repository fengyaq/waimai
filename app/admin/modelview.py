from flask import url_for, redirect, request
from flask_login.utils import current_user
from jinja2 import Markup
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
import os.path as op

file_path = op.join(op.dirname(__file__), '../static')  # 文件上传路径


class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin.login', next=request.url))


class UModelview(MyModelView):
    column_labels = {
        'id': '序号',
        'email': '邮件',
        'username': '用户名',
        'role': '角色',
        'password_hash': '密码',
        'head_img': '头像',
        'create_time': '创建时间',
        'update_time': '更新时间'
    }
    column_exclude_list = ['password_hash', ]

    def _list_thumbnail(view, context, model, name):
        if not model.head_img:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.head_img)))

    column_formatters = {
        'head_img': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'head_img': form.ImageUploadField('Image',
                                          base_path=file_path,
                                          relative_path="uploadfile/",
                                          thumbnail_size=(100, 100, True))
    }


class FModelview(MyModelView):
    column_labels = {
        'id': '序号',
        'summary': '描述',
        'stock': '库存量',
        'category': '分类',
    }

    def get_img(view, context, model, name):
        if not model.main_image:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=model.main_image))

    column_formatters = {
        'main_image': get_img
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'main_image': form.ImageUploadField('Image',
                                            base_path=file_path,
                                            relative_path="uploadfile/")
    }
