from flask import Flask,request
import dbcreds
import users

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
    
        

    