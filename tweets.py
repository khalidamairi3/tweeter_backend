import dbcreds
import json
from flask import  Response, request
import mariadb
import datetime


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
            cursor.execute("SELECT * FROM tweet t INNER JOIN users u on t.user_id = u.id WHERE t.user_id =?" ,[userId,])
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
                tweets=[]
                for row in result:
                    tweet = {
                    "tweetId":row[0],
                    "userId":row[3],    
                    "username":row[4],
                    "content":row[1],
                    "createdAt":row[2],   
                    }
                    tweets.append(tweet)
                return Response(json.dumps(tweets,default=str),mimetype="application/json",status=200)
            else:
                return Response("failed",mimetype="text/html",status=400)
    else:
        return Response("somthing went wrong",mimetype="text/html",status=400)

def post():
    data = request.json
    conn = None
    cursor = None
    result = None
    tweet=None
    loginToken=data.get("loginToken")
    content = data.get("content")
    
    if content and content!="" and loginToken and loginToken !=None : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT u.id, u.username FROM users u INNER JOIN `session` s ON u.id=s.user_id  WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            createdAt=datetime.datetime.now()
            cursor.execute("INSERT INTO tweet(content, created_at, user_id)VALUES(?, ?, ?);", [ content, createdAt , user[0] ,])
            conn.commit()
            result = cursor.rowcount
            tweetId = cursor.lastrowid
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
                tweet = {

                    "tweetId": tweetId,
                    "userId": user[0],
                    "username": user[1],
                    "content": content,
                    "createdAt": createdAt
                        
                    }
                return Response(json.dumps(tweet,default=str),mimetype="application/json",status=201)
            return Response(message ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)
def patch():
    data = request.json
    conn = None
    cursor = None
    result = None
    loginToken=data.get("loginToken")
    content = data.get("content")
    tweetId = data.get("tweetId")
    
    if content and content!="" and loginToken and loginToken !=None and tweetId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT s.user_id FROM `session` s WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("SELECT user_id FROM tweet WHERE id=?",[tweetId,])
            tweetUser =cursor.fetchone()
            if user[0]==tweetUser[0]:
                cursor.execute("UPDATE tweet SET content=? WHERE id=?", [ content, tweetId])
                conn.commit()
                result = cursor.rowcount
            else:
                message="not authorized"
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
                tweet = {

                    "tweetId": tweetId,
                    "content": content,

                        
                    }
                return Response(json.dumps(tweet,default=str),mimetype="application/json",status=201)
            return Response(message ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)

def delete():
    data = request.json
    conn = None
    cursor = None
    result = None
    loginToken=data.get("loginToken")
    tweetId = data.get("tweetId")
    
    if loginToken and loginToken !=None and tweetId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT s.user_id FROM `session` s WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("SELECT user_id FROM tweet WHERE id=?",[tweetId,])
            tweetUser =cursor.fetchone()
            if user[0]==tweetUser[0]:
                cursor.execute("DELETE FROM comment_likes WHERE comment_id=(SELECT c.id FROM comment c WHERE tweet_id = ?)", [tweetId,])
                cursor.execute("DELETE FROM comment WHERE tweet_id = ?",[tweetId,])
                cursor.execute("DELETE FROM tweet_likes WHERE tweet_id = ?",[tweetId,])
                cursor.execute("DELETE FROM tweet WHERE id = ?",[tweetId,])
                conn.commit()
                result = cursor.rowcount
            else:
                message="not authorized"
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
                return Response("SUCCESS" ,mimetype="text/html",status=204)
            return Response(message ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)

