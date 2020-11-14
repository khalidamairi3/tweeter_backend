import secrets
import dbcreds
import json
from flask import  Response, request
import mariadb
def post():
    data=request.json
    email = data.get("email")
    password=data.get("password")
    conn = None
    cursor = None
    user = None
    rows=None
    if email!="" and email !=None and password !="" and password != None:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?",[email,])
            user= cursor.fetchone()
            if user :
                if user[2]==password:
                    loginToken = secrets.token_urlsafe(16) 
                    cursor.execute("INSERT INTO `session` (user_id, login_token) VALUES (?,?)",[user[4],loginToken,])
                    conn.commit()
                    rows=cursor.rowcount
                else:
                    message="invalid entry"
            else:
                message="Email doesn't exist"
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data"
        except:
            message =  "somthing went wrong" 
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if rows == 1 :
                res = {
                   "userId": user[4],
                    "email": user[1],
                    "username": user[0],
                    "bio": user[3],
                    "birthdate": user[5],
                    "loginToken": loginToken 
                }
                return Response(json.dumps(res,default=str),mimetype="application/json" , status =201)
            else:
                return Response(message,mimetype="text/html",status=400)
    else:
        return Response("wrong entry",mimetype="text/html",status=400)
            


def delete():
    data =request.json
    loginToken = data.get("loginToken")
    rows=None
    if loginToken!="" and loginToken !=None:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `session` WHERE login_token = ?",[loginToken,])
            conn.commit()
            rows=cursor.rowcount
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data"
        except:
            message =  "somthing went wrong"
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if rows==1:
            return  Response("Success",mimetype="text/html",status=204)
    return  Response("failed",mimetype="text/html",status=400)
