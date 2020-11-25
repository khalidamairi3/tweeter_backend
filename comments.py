import dbcreds
import json
from flask import  Response, request
import mariadb
import datetime



def get():
    params=request.args
    tweetId= params.get("tweetId")
    commentId = params.get("commentId")
    conn = None
    cursor = None
    result = None
    if tweetId:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT c.id, c.tweet_id, u.id , u.username , c.content , c.created_at FROM users u  INNER JOIN comment c ON u.id = c.user_id WHERE c.tweet_id=? AND c.comment_id IS NULL" ,[tweetId,])
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
                comments=[]
                for row in result:
                    comment = {
                    "commentId":row[0],
                    "tweetId":row[1],
                    "userId":row[2],    
                    "username":row[3],
                    "content":row[4],
                    "createdAt":row[5],   
                    }
                    comments.append(comment)
                return Response(json.dumps(comments,default=str),mimetype="application/json",status=200)
            else:
                return Response("failed",mimetype="text/html",status=400)
    elif commentId:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT c.id, c.comment_id, u.id , u.username , c.content , c.created_at FROM users u  INNER JOIN comment c ON u.id = c.user_id WHERE c.comment_id=?" ,[commentId,])
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
                comments=[]
                for row in result:
                    comment = {
                    "commentCommentId":row[0],
                    "commentId":row[1],
                    "userId":row[2],    
                    "username":row[3],
                    "content":row[4],
                    "createdAt":row[5],   
                    }
                    comments.append(comment)
                return Response(json.dumps(comments,default=str),mimetype="application/json",status=200)
            else:
                return Response("failed",mimetype="text/html",status=400)
    else:
        return Response("failed",mimetype="text/html",status=400)

def post():
    data = request.json
    conn = None
    cursor = None
    result = None
    tweet=None
    loginToken=data.get("loginToken")
    content = data.get("content")
    tweetId = data.get("tweetId")
    commentId = data.get("commentId")
    
    if content and content!="" and loginToken and loginToken !="" and tweetId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT u.id, u.username FROM users u INNER JOIN `session` s ON u.id=s.user_id  WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            createdAt=datetime.datetime.now()
            cursor.execute("INSERT INTO comment(tweet_id,content, created_at, user_id)VALUES(?,?, ?, ?)", [ tweetId,content, createdAt , user[0] ,])
            conn.commit()
            result = cursor.rowcount
            commentId = cursor.lastrowid
        except mariadb.OperationalError as e:
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data. probably there is another user using the same username or the same email"
        except Error as e:
            message = e
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()

            if result == 1 :
                comment = {
                    "commentId":commentId,
                    "tweetId": tweetId,
                    "userId": user[0],
                    "username": user[1],
                    "content": content,
                    "createdAt": createdAt
                        
                    }
                return Response(json.dumps(comment,default=str),mimetype="application/json",status=201)
            return Response(message ,mimetype="text/html",status=400)
    elif content and content!="" and loginToken and loginToken !="" and commentId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT u.id, u.username FROM users u INNER JOIN `session` s ON u.id=s.user_id  WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("SELECT tweet_id FROM comment where id=?",[commentId,])
            tweetId = cursor.fetchone()
            if tweetId and tweetId[0]!=None:
                createdAt=datetime.datetime.now()
                cursor.execute("INSERT INTO comment(comment_id,content, created_at, user_id)VALUES(?,?, ?, ?)", [ commentId ,content, createdAt , user[0] ,])
                conn.commit()
                result = cursor.rowcount
                commentid = cursor.lastrowid
        except mariadb.OperationalError as e:
            print(e)
            message = "connection error or wrong entry"
        except mariadb.IntegrityError as e:
            message = "Something is wrong with your data. probably there is another user using the same username or the same email"
        except Exception as e:
            print(e)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()

            if result == 1 :
                comment = {
                    "commentCommentId":commentid,
                    "commentId":commentId,
                    "userId": user[0],
                    "username": user[1],
                    "content": content,
                    "createdAt": createdAt
                        
                    }
                return Response(json.dumps(comment,default=str),mimetype="application/json",status=201)
            return Response("failed" ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)



def patch():
    data = request.json
    conn = None
    cursor = None
    result = None
    loginToken=data.get("loginToken")
    content = data.get("content")
    commentId = data.get("commentId")
    if content and content!="" and loginToken and loginToken !="" and commentId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT u.id, u.username FROM users u INNER JOIN `session` s ON u.id=s.user_id  WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("SELECT user_id, tweet_id, created_at  FROM comment WHERE id=?",[commentId,])
            comment =cursor.fetchone()
            if user[0]==comment[0]:
                cursor.execute("UPDATE comment SET content=? WHERE id=?", [ content, commentId])
                conn.commit()
                result = cursor.rowcount
            else:
                message = "not authorized"
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

            if result == 1 :
                comment = {
                    "commentId":commentId,
                    "tweetId": comment[1],
                    "userId": user[0],
                    "username": user[1],
                    "content": content,
                    "createdAt": comment[2]
                        
                    }
                return Response(json.dumps(comment,default=str),mimetype="application/json",status=201)
            return Response(message,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)

def delete():
    data = request.json
    conn = None
    cursor = None
    result = None
    loginToken=data.get("loginToken")
    commentId = data.get("commentId")
    
    if loginToken!="" and loginToken !=None and commentId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT s.user_id FROM `session` s WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("SELECT user_id FROM comment WHERE id=?",[commentId,])
            commentUser =cursor.fetchone()
            if user[0]==commentUser[0]:
                cursor.execute("DELETE FROM comment_likes WHERE comment_id=?", [commentId,])
                cursor.execute("DELETE FROM comment WHERE id = ?",[commentId,])
                conn.commit()
                result = cursor.rowcount
            else:
                message = "not authorized"
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

            if result == 1 :
                return Response("SUCCES" ,mimetype="text/html",status=204)
            return Response(message ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)

