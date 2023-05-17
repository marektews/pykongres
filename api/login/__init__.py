from flask import Blueprint, redirect, request
from flask_login import LoginManager, login_user, logout_user, UserMixin
from sql import Zbory
from uuid import uuid4

login_api = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()


class User(UserMixin):
    def __init__(self, uid):
        self.id = uid


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_api.route('/login', methods=['POST'])
def login():
    _login = request.json['login']
    _passwd = request.json['passwd']
    res = Zbory.query.filter_by(name=_login, number=_passwd).all()
    if len(res) == 1:
        if login_user(User(uid=uuid4().hex)):
            return "", 200  # OK
        else:
            return "", 403  # Forbiden
    else:
        return "", 401  # Unauthorized


@login_api.route('/logout')
def logout():
    logout_user()
    return redirect('http://jw.org')