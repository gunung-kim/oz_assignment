from flask import Flask,request,jsonify
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker,base
import os

app=Flask(__name__)

# # 임시저장소
#  todos = {
#     1:" study",
#     2:"sleep"
# }

#############################
#        db 설정
#########################
# # instance 폴더을 만들고
# engine = create_engine("sqlite:///instance/todos.db",scho=True)

# 자동으로 instance 만들기
#os를 import한 이유
# 대문자로 하는 이유는 이 값은 바뀌지 않느다
BASE_DIR = os.path.dirname(__file__) # 현재 파이썬을 실행하는 파일의 위치를 반환
#instance 폴더의 경로와 현재 실행되는 폴더의 경로를 합친다
INSTANCE_DIR = os.path.join(BASE_DIR,"instance")
# exist_ok 는 만일 같은 폴더가 있을때는 생성되지 않도록
os.makedirs(INSTANCE_DIR,exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(INSTANCE_DIR,"Todos.db")}"

engine = create_engine(DATABASE_URL,scho=True)

sessionLocal = sessionmaker(bind=engine)

#############################
#        모델 정의
#########################

Base = declarative_base()

class Todo(Base):
    __tanlename__ = "todos"

    id = Column(Integer, primary_key=True,index=True)
    task = Column(String,nullable=False)

    def __repr__(self):
        return "<Todo id={self.id}),task='{self.task}'>"

Base.metadata.create_all(bind=engine)


##################################################################################


# READ : 전체항목조회
@app.route('/todos',methods=['GET']) #methods인 이유는 리스트가 들어가기 때문
def get_todos():
    db = sessionLocal()
    todos=db.query(Todo).all()
    db.close()
    return jsonify([{"id":t.id,"task":t.task} for t in todos])

# READ : 특성 항복 조회
@app.route('/todos/<int:todo_id>',methods=['GET'])
def get_todo(todo_id):
    db = sessionLocal()

    # todos=db.query(Todo).filter(Todo.id == todo.id)
    #  index 활용
    task = db.query(Todo).get(todo_id)
    data = request.get_json()
    db.close()
    todo = Todo(task=data["task"])
    if not task:
        return jsonify({"error":"해당 할 일이 없습니다"}),404
    return jsonify({"id":todo.id,"task":todo.task})

# CREATE :새로운 항목 추가
@app.route('/todos',methods=['POST'])
def create_todo():
    # 특정바디의 데이터 가져오기
    data = request.get_json()
    
    db = sessionLocal()
    todo = Todo(task=data["task"])
    db.add(todo)
    db.commit()
    db.refresh(todo)   #->>>>>>>>commit 후 자동 생성된 id 불러오기
    db.close() # 데이터베이스에 저장은 되지만 추가한 거만 따로 반환할려면 따로 가져와야한다
    
    # 실제 민간데이터는 추가가 완료되었다고만 한다
    return jsonify({"id":todo.id,"task":[todo.id]})

# UPDATE : 특정 항목 수정
@app.route('/todos/<int:todo_id>',methods=['PUT'])
def update_todo(todo_id):
    db = sessionLocal()
    todo = db.query(Todo).get(todo_id)
    if not todo:
        db.close()
        return jsonify({"error":"not found"}),404
    data = request.get_json     
    todo.task = data["task"]   
    db.commit()
    updated = {"id":todo.id,"task":todo.task}
    db.close()
    return jsonify({"id":todo.id,"task":todo.task})

# DELETE : 특정 항복 삭제
@app.route('/todos/<todo_id>',methods={'DELETE'})
def delete_todo(todo_id):
    db = sessionLocal()
    todo = db.query(Todo).get(todo_id)
    if not todo:
        db.close()
        return jsonify({"error":"not found"}),404
    db.delete(todo) 
    db.commit()
    db.close()
    return jsonify({"deleted" : todo_id})

if __name__=="__main__":
    app.run(debug=True)

