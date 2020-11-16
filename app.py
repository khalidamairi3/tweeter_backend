from flask import Flask,request
import dbcreds
import users
import user_login
import follows
import followers
import tweets
import comments
app = Flask(__name__)

@app.route("/api/users",methods=["GET","POST","PATCH","DELETE"])
def getUsers():
    if request.method == "GET":
        return users.get_users()
    elif request.method=="POST":
        return users.post_user()
    elif request.method=="PATCH":
        return users.patch_user()
    elif request.method=="DELETE":
        return users.delete_user()
    else :
        Response("not supported", mimetype="text/html", status=500)

@app.route("/api/login",methods=["POST","DELETE"])
def login():
    if request.method == "POST":
        return user_login.post()
    elif request.method=="DELETE":
        return user_login.delete()
    else :
        Response("not supported", mimetype="text/html", status=500)

@app.route("/api/follows",methods=["GET","POST","DELETE"])
def follows_api():
    if request.method == "GET":
        return follows.get()
    elif request.method == "POST":
        return follows.post()
    elif request.method=="DELETE":
        return follows.delete()
    else :
        Response("not supported", mimetype="text/html", status=500)

@app.route("/api/followers",methods=["GET"])
def followers_api():
    if request.method == "GET":
        return followers.get()    
    else :
        Response("not supported", mimetype="text/html", status=500) 

@app.route("/api/tweets",methods=["GET","POST","PATCH","DELETE"])
def tweet():
    if request.method == "GET":
        return tweets.get()
    elif request.method=="POST":
        return tweets.post()
    elif request.method=="PATCH":
        return tweets.patch()
    elif request.method=="DELETE":
        return tweets.delete()
    else :
        Response("not supported", mimetype="text/html", status=500)

@app.route("/api/comments",methods=["GET","POST","PATCH","DELETE"])
def comment():
    if request.method == "GET":
        return comments.get()
    elif request.method=="POST":
        return comments.post()
    elif request.method=="PATCH":
        return comments.patch()
    elif request.method=="DELETE":
        return comments.delete()
    else :
        Response("not supported", mimetype="text/html", status=500)
   