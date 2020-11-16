import dbcreds
import json
from flask import  Response, request
import mariadb


def get():
    params = request.args
    commentId=params.get("commentId")
    conn = None
    cursor = None
    result = None
    if commentId:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT cl.comment_id, u.id, u.username FROM users u INNER JOIN comment_likes cl ON u.id=cl.user_id  WHERE cl.comment_id=?",[commentId,])
            result = cursor.fetchall()
            print(result)
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data. probably there is another user using the same username or the same email"
        except:
            message =  "somthing went wrong" 
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()

            if result or result ==[]:
                likes = []
                for row in result:

                    like = {

                    "commentId": row[0],
                    "userId": row[1],
                    "username": row[2]
                        
                    }
                    likes.append(like)
                return Response(json.dumps(likes,default=str),mimetype="application/json",status=201)
            return Response(message ,mimetype="text/html",status=400)
    else:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT cl.comment_id, u.id, u.username FROM users u INNER JOIN comment_likes cl ON u.id=cl.user_id ")
            result = cursor.fetchall()
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data. probably there is another user using the same username or the same email"
        except:
            message =  "somthing went wrong" 
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()

            if result or result ==[]:
                likes = []
                for row in result:

                    like = {

                    "commentId": row[0],
                    "userId": row[1],
                    "username": row[2]
                        
                    }
                    likes.append(like)
                return Response(json.dumps(likes,default=str),mimetype="application/json",status=201)
            return Response(message ,mimetype="text/html",status=400)
def post():
    data = request.json
    conn = None
    cursor = None
    result = None
    loginToken=data.get("loginToken")
    commentId = data.get("commentId")
    
    if loginToken !="" and loginToken !=None and commentId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM `session` WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("INSERT INTO comment_likes (comment_id,user_id)VALUES(?,?)", [commentId,user[0] ,])
            conn.commit()
            result = cursor.rowcount
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data. probably there is another user using the same username or the same email"
        except Exception  as e:
            message = e
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()

            if result == 1 :
                return Response("SUCCESS",mimetype="text/html",status=201)
            return Response(message ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)


def delete():
    data = request.json
    conn = None
    cursor = None
    result = None
    loginToken=data.get("loginToken")
    commentId = data.get("commentId")
    
    if loginToken !="" and loginToken !=None and commentId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM `session` WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("DELETE FROM comment_likes WHERE comment_id =? AND user_id=?", [commentId,user[0] ,])
            conn.commit()
            result = cursor.rowcount
            print(result)
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data. probably there is another user using the same username or the same email"
        except Exception  as e:
            message = e
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()

            if result == 1 :
                return Response("SUCCESS",mimetype="text/html",status=201)
            return Response("something is wrong" ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)