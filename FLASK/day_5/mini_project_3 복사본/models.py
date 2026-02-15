# python 라이브러리
from werkzeug.security import generate_password_hash,check_password_hash
# 로컬 모듈 임포트
from db import db

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer,primary_key=True,index=True)
    name = db.Column(db.String(100),nullable=False)
    hash_pw = db.Column(db.String(128),nullable=False)
    todo = db.relationship('Todos',back_populates='author',lazy=True)

    @property
    # 함수를 객체처럼 다룰수 있게해주는 데코레이터
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 비밀번호가 입력될때 자동으로 해쉬화하는 함수
    @password.setter
    def password(self,password):
        self.hash_pw = generate_password_hash(password)

    # 유저가 입력한 비밀번호를 해쉬화한 비밀번호와 데이터베이스에 저장된 비밀번호를 비교
    def verify_password(self,password):
        return check_password_hash(self.hash_pw,password)
    
class Todos(db.Model):
    __tablename__="todo"
    id = db.Column(db.Integer,primary_key=True,index=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(255))
    is_completed = db.Column(db.Boolean, default=False,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    author = db.relationship('User',back_populates='todo')