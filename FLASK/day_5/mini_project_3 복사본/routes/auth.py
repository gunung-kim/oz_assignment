# python 라이브러리
from flask_jwt_extended import get_jwt_identity,create_access_token
from flask import request
from flask_smorest import Blueprint,abort
from flask.views import MethodView

# 로컬 모듈
from db import db
from schemas import UserSchema
from models import User

auth_bp = Blueprint("auth",__name__,url_prefix='/')

@auth_bp.route('/login')
class Login(MethodView):
    @auth_bp.arguments(UserSchema)
    def post(self,data):    
        user = User.query.filter_by(name=data['name']).first()
        if not user:
            abort(401,message='something wrong')
        if not user.verify_password(data['password']):
            abort(401,message='something wrong')
        access_token = create_access_token(identity=str(user.id))
        return {
            'msg':'login success',
            "access_token":access_token
        }

# user token check
def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        abort(401,message='something wrong')
    user = User.query.filter_by(id=int(user_id)).first()
    if not user:
        abort(401,message='something wrong')
    return user
