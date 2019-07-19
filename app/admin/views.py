from . import admin_page
from .forms import LoginForm
from app.models.admin import User
from flask_login import login_user, logout_user
from flask import redirect, request, url_for, render_template, flash


@admin_page.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is not None:
            flag = User.verity_password(form.password.data, user.password_hash)
            if flag:
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for("admin.index"))
        flash('无效的用户名或者密码')

    return render_template("admin/login.html", form=form)


@admin_page.route("/logout")
def logout():
    logout_user()
    flash("退出成功！")
    return redirect(url_for('admin.login'))
