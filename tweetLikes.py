import dbcreds
import json
from flask import  Response, request
import mariadb


def get():
    params = request.args
    tweetId=params.get("tweetId")
    conn = None
    cursor = None
    result = None
    if tweetId:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT tl.tweet_id, u.id, u.username FROM users u INNER JOIN tweet_likes tl ON u.id=tl.user_id  WHERE tl.tweet_id=?",[tweetId,])
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

            if result:
                likes = []
                for row in result:

                    like = {

                    "tweetId": row[0],
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
            cursor.execute("SELECT tl.tweet_id, u.id, u.username FROM users u INNER JOIN tweet_likes tl ON u.id=tl.user_id ")
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

            if result:
                likes = []
                for row in result:

                    like = {

                    "tweetId": row[0],
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
    tweetId = data.get("tweetId")
    
    if loginToken !="" and loginToken !=None and tweetId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM `session` WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("INSERT INTO tweet_likes (tweet_id,user_id)VALUES(?,?)", [tweetId,user[0] ,])
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
    tweetId = data.get("tweetId")
    
    if loginToken !="" and loginToken !=None and tweetId : 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM `session` WHERE login_token=?",[loginToken,])
            user = cursor.fetchone()
            cursor.execute("DELETE FROM tweet_likes WHERE tweet_id =? AND user_id=?", [tweetId,user[0] ,])
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