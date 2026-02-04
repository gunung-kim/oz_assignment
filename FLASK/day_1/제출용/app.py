from flask import Flask, render_template,request
app = Flask(__name__)

users =[
    {"username" : "traveler","name" : "Alex"},
    {"username" : "photographer","name" : "Sam"},
    {"username" : "gourmet","name" : "Chris"}
]

@app.route("/")
def home():
    return render_template("home.html",users=users)

@app.route("/user")
def user():
    s_name= request.args.get("name")
    find_list = None
    for n in range(3):
        if s_name == users[n]['name']:
            find_list = users[n]
            break
        else :
            pass
    return render_template("index.html",find_list=find_list)

if __name__=="__main__":
    app.run(debug=True)