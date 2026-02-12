from flask import request, jsonify
from flask_smorest import abort, Blueprint

def create_posts_blueprint(mysql):
    posts_blp = Blueprint(
        "posts",
        __name__,
        description='posts api',
        url_prefix="/posts"
        )
    
    @posts_blp.route("/",methods=['GET','POST'])
    def posts():
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            sql = "SELECT *FROM posts"
            cursor.execute(sql)

            posts = cursor.fetchall()
            cursor.close()
            
            post_list = []
            for post in posts:
                post_list.append({
                    "id":post[0],
                    "title":post[1],
                    "content":post[2]
                })
            return jsonify(post_list), 200 # jsonify는 해도되고 안해도 상관없음
        
        elif request.method == "POST":
            title = request.json.get("title")
            content = request.json.get("content")

            if not title or not title.strip() or not content or not content.strip():
                abort(400,message="title or content is empty")

            sql = "INSERT INTO posts(title,content)VALUES(%s,%s)"
            val = (title,content,)
            
            cursor.execute(sql,val)
            mysql.connection.commit()
            cursor.close()

            return jsonify({"msg":"success","title":title,"content":content}),201
 
    @posts_blp.route("/<int:id>",methods=["GET","PUT","DELETE"])
    def post(id):
        cursor = mysql.connection.cursor()
        if not id:
            abort(400,message="insert id")
        if request.method == "GET":
            sql = "SELECT * FROM posts WHERE id=%s"
            val = (id,)
            cursor.execute(sql,val)
            select_post = cursor.fetchone()
            cursor.close()
            if not select_post:
                abort(404,message="id not found")
            return jsonify({"id":select_post[0],"title":select_post[1],"content":select_post[2]}),200
        
        elif request.method == "PUT":
            title = request.json.get("title")
            content = request.json.get("content")

            if not title or not title.strip() or not content or not content.strip():
                abort(404,message="not found")
            
            # sql = f"UPDATE posts SET title={title},content={content} WHERE id={id}" 이건 보안적으로 취약하다
            sql = "UPDATE posts SET title=%s,content=%s WHERE id=%s"
            val = (title,content,id,)
            cursor.execute(sql,val)
            mysql.connection.commit()
            cursor.close()

            return jsonify({"msg":"success","title":title,"content":content})
        
        elif request.method == "DELETE":
            sql = "DELETE FROM posts WHERE id=%s"
            val = (id,)
            cursor.execute(sql,val)
            mysql.connection.commit()
            cursor.close()
            return jsonify({"msg":"success"})
        
        # 몰입 - 황문용 교수님
        # 생각에 관한

    return posts_blp