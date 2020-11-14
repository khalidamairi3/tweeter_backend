import dbcreds
import json
from flask import  Response, request
import mariadb


def get():
    params=request.args
    userId= params.get("userId")
    print(userId)
    conn = None
    cursor = None
    result = None
    if userId:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users INNER JOIN  user_follows uf ON id=uf.followId WHERE uf.user_id =?" ,[userId,])
            result=cursor.fetchall()
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except:
            message =  "somthing went wrong"
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if result or result==[]:
                users=[]
                for row in result:
                    user = {

                    "userId":row[4],    
                    "email":row[1],
                    "username":row[0],
                    "bio":row[2],
                    "birthdate":row[5],   
                    }
                    users.append(user)
                return Response(json.dumps(users,default=str),mimetype="application/json",status=200)
            else:
                return Response("failed",mimetype="text/html",status=400)
    else:
        return Response("somthing wen wrong",mimetype="text/html",status=400)

            

def post():
    conn = None
    cursor=None
    rows=None
    data=request.json
    loginToken = data.get("loginToken")
    followId = data.get("followId")
    if loginToken !="" and loginToken and followId:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id from `session` WHERE login_token =?" ,[loginToken,])
            userId = cursor.fetchone()
            cursor.execute("INSERT INTO user_follows (user_id, followId) VALUES (?,?)",[userId[0],followId,])
            conn.commit()
            rows=cursor.rowcount
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data."
        except:
            message =  "somthing went wrong"
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if rows ==1:
                return Response("succes" ,mimetype="text/html",status=204)
            else:
                return Response(message ,mimetype="text/html",status=400)
def delete():
    conn = None
    cursor=None
    rows=None
    data=request.json
    loginToken = data.get("loginToken")
    followId = data.get("followId")
    if loginToken !="" and loginToken and followId:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id from `session` WHERE login_token =?" ,[loginToken,])
            userId = cursor.fetchone()
            cursor.execute("DELETE FROM user_follows WHERE user_id=? AND followId=?",[userId[0],followId,])
            conn.commit()
            rows=cursor.rowcount
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data."
        except:
            message =  "somthing went wrong"
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if rows ==1:
                return Response("succes" ,mimetype="text/html",status=204)
            else:
                return Response(message ,mimetype="text/html",status=400)

