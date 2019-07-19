from wtforms import fields, validators
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = fields.StringField(label='管理员账号', validators=[validators.required()])
    password = fields.PasswordField(label='密码', validators=[validators.required()])

    remember_me = fields.BooleanField('记住我')
    submit = fields.SubmitField('登陆')