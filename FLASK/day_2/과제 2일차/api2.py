from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema

book_blp = Blueprint("book","book",url_prefix="/book",description="book API")
books=[]

#전체 책 
@book_blp.route('/') # Blueprint로 인해 / = /book과 같음 prefix로 설정
class Books(MethodView):
    @book_blp.response(200,BookSchema(many=True)) # response를 many=True로 지정하여 리스트 형식으로 반환
    def get(self):
        return books # 전체 항목 조회
    
    @book_blp.arguments(BookSchema(many=True)) # 입력받을 인자값이 리스트 형식으로 Bookschema로 역직렬화되어 들어옴
    @book_blp.response(201,BookSchema(many=True)) # 보낼 response를 직렬화하여 json형태로 반환 response code는 201 (기존에 없던 데이터가 추가되었다)
    def post(self,new_datas): # new_data를 postman body에 입력
        for new_data in new_datas:
            new_data['id'] = len(books)+1 # new_data에 id 부여
            books.append(new_data) #리스트에 추가
        return new_datas # 추가한 데이터 반환

#특정 책 
@book_blp.route('/<int:book_id>') #사용자가 따로 주소창에 입력해야하는 book_id
class Books(MethodView):

    @book_blp.arguments(BookSchema) # many=True 이걸 하는 순간 mod_data는 리스트형식으로 가져옴, postman body에 입력되는 값이 있을때만 입력
    @book_blp.response(200,BookSchema) # 서버에서 응답 response를 보낼때 Bookschema에 맞춰서 보낸다
    def get(self,book_id):
        for ids in books:
            if book_id == ids['id']:
                return ids
        return abort(404,message="book_id not found")
    
    @book_blp.arguments(BookSchema) # many=True 이걸 하는 순간 mod_data는 리스트형식으로 가져옴, postman body에 입력되는 값이 있을때만 입력
    @book_blp.response(200,BookSchema) # 서버에서 응답 response를 보낼때 Bookschema에 맞춰서 보낸다
    def put(self,mod_data,book_id): # 함수 인자값으로는 mod_data는 postman body에 book_id는 주소창에입력
        for book in books: # 아이디가 있는지 찾아야하니 먼저 books 객체 하나씩 꺼내기
            if book_id == book['id']:   # book_id와 books안의 객체 하나씩 id값과 비교
                book.update(mod_data) #있으면 mod_data로 기존 data 수정
                return book # 수정된 book만 return
        return abort(404,message="book_id not found") #일치하는 book_id가 없을떄 abort return 
    
    #postman body에 입력할 필요 없으니 book_blp.arguments를 추가할 필요가 없다
    @book_blp.response(200,BookSchema(many=True)) #response를 Bookschema를 거져서 pytohn을 json으로 직렬화, books를 반환해야하니 many=True 추가
    def delete(self,book_id):
        global books # 주소창에 book_id를 입력받아야하므로 함수 인자값으로 book_id 
        for ids in books: # books 리스트에서 id값 찾기위해 for문으로 객체 하나씩 꺼내기
            if book_id == ids['id']: # 꺼낸 객체 하나씩 인자값으로 입력한 book_id와 같은지 검사
                books.remove(ids) # 아이디가 같을때 해당 객체 삭제
                return books # 삭제된 리스트 반환   -> 여기서 빈 리스트가 반환되는데 이유를 모르겠음
        return abort(404,message="book_id not found") # book_id와 같은 값이 없을때 abort 반환