import dbcreds
import json
from flask import  Response, request
import mariadb
def get():
    params=request.args
    userId= params.get("userId")
    conn = None
    cursor = None
    result = None
    if userId:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users INNER JOIN  user_follows uf ON id=uf.user_id WHERE uf.followId =?" ,[userId,])
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