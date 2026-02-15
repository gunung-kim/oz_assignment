# python 라이브러리
from flask import Flask , render_template
from flask_smorest import Api
from flask_migrate import Migrate
import os

# 로컬 모듈
from db import db
from jwt_utiles import jwt
from routes.auth import auth_bp
from routes.todo import todo_bp
from models import User,Todos


app=Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['JWT_SECRET_KEY'] = 'My_secret_key'

app.config['API_TITLE'] = "My Api"
app.config['API_VERSION'] = "v1"
app.config['OPENAPI_VERSION'] = "3.1.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

db.init_app(app)
migrate = Migrate(app,db)
jwt.init_app(app)

api = Api(app)

api.register_blueprint(auth_bp)
api.register_blueprint(todo_bp)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


if __name__=="__main__":
    with app.app_context():
        print("디비 생성 시작")
        db.create_all()
        print('디비 생성 끝')
    app.run(debug=True)