from flask import Blueprint, request, current_app
from flask_login import login_required
from .Hints import _pk_hints_all
from .Login import _pk_login
from .Create import _pk_create
from .Find import _pk_find
from .Update import _pk_update
from .Delete import _pk_delete
from .Read import _pk_read


pk_api = Blueprint('pk', __name__, url_prefix='/pk')


@login_required
@pk_api.route('/hints', methods=['GET'])
def pk_hints_all():
    return _pk_hints_all()


@login_required
@pk_api.route('/login', methods=['POST'])
def pk_login():
    return _pk_login(request.json['login'], request.json['passwd'])


@login_required
@pk_api.route('/create', methods=['POST'])
def pk_create():
    return _pk_create(request.json)


@login_required
@pk_api.route('/find', methods=['POST'])
def pk_find():
    return _pk_find(request.json)


@login_required
@pk_api.route('/update', methods=['POST'])
def pk_update():
    return _pk_update(request.json)


@login_required
@pk_api.route('/delete/<pk_id>', methods=['GET'])
def srp_delete(pk_id):
    return _pk_delete(pk_id)


@login_required
@pk_api.route('/read/<pk_id>')
def pk_read(pk_id):
    return _pk_read(pk_id)

