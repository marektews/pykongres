from flask import Blueprint, redirect, request
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
from sql import Zbory, Users
from uuid import uuid4
from hashlib import sha256

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
    """
    Logowanie za pomocą nazwy i numeru zboru
    """
    _login = request.json['login']
    _passwd = request.json['passwd']
    res = Zbory.query.filter_by(name=_login, number=_passwd).all()
    if len(res) == 1:
        if login_user(User(uid=uuid4().hex)):
            return "", 200  # OK
        else:
            return "", 403  # Forbidden
    else:
        return "", 401  # Unauthorized


@login_api.route('/admin', methods=['POST'])
def login_admin():
    """
    Logowanie na poziom moderatora
    """
    _login = request.json['login']
    _passwd = request.json['password']
    h = sha256(_passwd.encode('utf8'))
    _hash = h.hexdigest()
    users = Users.query.filter_by(login=_login, hash=_hash).all()
    if len(users) == 1:
        if login_user(User(uid=_hash)):
            res = {
                "id": users[0].id,
                "fn": users[0].fn,
                "ln": users[0].ln,
                "permissions": {
                    "is_sra": users[0].is_sra,
                    "is_srp": users[0].is_srp,
                    "is_pk": users[0].is_pk,
                    "is_rja": users[0].is_rja,
                    "is_monitoring": users[0].is_monitoring,
                    "is_users": users[0].is_users
                },
            }
            return res, 200  # OK
        else:
            return {}, 403  # Forbidden
    else:
        return {}, 401  # Unauthorized


@login_api.route('/permissions', methods=['POST'])
def login_permissions():
    user_id = request.json['user_id']
    user = Users.query.filter_by(id=user_id).one()
    res = {
        "is_sra": user.is_sra,
        "is_srp": user.is_srp,
        "is_pk": user.is_pk,
        "is_rja": user.is_rja,
        "is_monitoring": user.is_monitoring,
        "is_users": user.is_users
    }
    return res, 200


@login_required
@login_api.route('/logout')
def logout():
    """Anulowanie logowania"""
    logout_user()
    return redirect('http://jw.org')
