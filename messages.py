import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb


def post():
    loginToken = request.json.get("loginToken")
    chatId= request.json.get("chatId")
    message = request.json.get("message")
    conn = None
    cursor = None
    result = None
    messageId =None
    
    if loginToken != "" and loginToken != None and chatId != None and message !="" and message != None: 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM `session` WHERE login_token = ?" , [loginToken,])
            user_id = cursor.fetchone()[0]
            cursor.execute("SELECT c.user_id, c.masseger_id FROM chat c WHERE c.id=?", [ chatId,])
            originalUsers = cursor.fetchone()
            if user_id == originalUsers[0] or user_id == originalUsers[1]:
                cursor.execute("INSERT INTO messages (user_id,chat_id,message) VALUES (?,?,?)",[user_id,chatId,message])
                result = cursor.rowcount
                messageId = cursor.lastrowid
                conn.commit()
                cursor.execute("SELECT * FROM messages WHERE id =?",[messageId])
                userMessage = cursor.fetchone()

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
                chat_message= {

                    "messageId":messageId,    
                    "message":userMessage[0],
                    "userId":userMessage[2],
                    "chatId":chatId,
                    "date":userMessage[4],
                        
                    }
                return Response(json.dumps(chat_message,default=str),mimetype="application/json",status=201)
            return Response("failed" ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)

def get():
    loginToken = request.headers.get("loginToken")
    chatId= request.args.get("chatId")
    conn = None
    cursor = None
    result = None
    
    if loginToken != "" and loginToken != None and chatId != None: 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM `session` WHERE login_token = ?" , [loginToken,])
            user_id = cursor.fetchone()[0]
            cursor.execute("SELECT c.user_id, c.masseger_id FROM chat c WHERE c.id=?", [ chatId,])
            originalUsers = cursor.fetchone()
            if user_id == originalUsers[0] or user_id == originalUsers[1]:
                cursor.execute("SELECT * FROM messages WHERE chat_id =?",[chatId,])
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

            if result == [] or result !=None :
                messages=[]
                for row in result:

                    chat_message= {

                        "messageId":row[1],    
                        "message":row[0],
                        "userId":row[2],
                        "chatId":chatId,
                        "date":row[4],
                            
                        }
                    messages.append(chat_message)
                return Response(json.dumps(messages,default=str),mimetype="application/json",status=201)
            return Response(message ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)
