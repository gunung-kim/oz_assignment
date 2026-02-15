# python 라이브러리
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
# 로컬 모듈 
from db import db
from models import User,Todos
from schemas import UserSchema,TodoSchema
from routes.auth import get_current_user

todo_bp=Blueprint('todo',__name__,url_prefix="/todos")

@todo_bp.route('/')
class UserTodoList(MethodView):
    @jwt_required()
    @todo_bp.response(200,TodoSchema(many=True))
    def get(self):
        # check user's token
        user = get_current_user()
        user_todos = Todos.query.filter_by(user_id=user.id)
        if not user_todos:
            abort(404,)
        return user_todos
    
    @jwt_required()
    @todo_bp.arguments(TodoSchema)
    @todo_bp.response(201,TodoSchema)
    def post(self,data):
        user = get_current_user()
        new_todo = Todos(title=data['title'],content=data['content'],user_id=user.id)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo
    
@todo_bp.route('/<int:todo_id>')
class UserTodoOne(MethodView):
    @jwt_required()
    @todo_bp.arguments(TodoSchema)
    @todo_bp.response(200,TodoSchema)
    def put(self,data,todo_id):
        user = get_current_user()
        target_todo = Todos.query.filter_by(id=todo_id,user_id=user.id).first()
        if not target_todo:
            abort(401,message='something wrong')
        cols = ['title','content']
        for col in cols:
            if col in data:
                setattr(target_todo,col,data[col])
        db.session.commit()
        return target_todo
    
    @jwt_required()
    @todo_bp.response(200,TodoSchema)
    def delete(self,todo_id):
        user = get_current_user()
        target_todo = Todos.query.filter_by(id=todo_id,user_id = user.id).first()
        if not target_todo:
            abort(401,message='something wrong')
        db.session.delete(target_todo)
        db.session.commit()
        return ""


