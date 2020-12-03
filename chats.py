import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb

def get():
    headers = request.headers
    loginToken = headers.get("loginToken")
    result=None
    conn= None 
    cursor = None
    if loginToken != None:

        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM `session` WHERE login_token = ?" , [loginToken,])
            user_id = cursor.fetchone()[0]
            cursor.execute("SELECT c.id, u1.id, u1.username, u2.id, u2.username FROM users u1 INNER JOIN chat c INNER JOIN users u2 ON u1.id = c.user_id AND u2.id = c.masseger_id WHERE c.user_id = ? OR c.masseger_id = ?",[user_id,user_id])
            result = cursor.fetchall()
        except mariadb.OperationalError as e:
            print (e)
            message = "connection error" 
        except Exception as e:
            print(e)
            message ="somthing went wrong, probably bad params " 
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if (result !=None or result ==[]):
                chats=[]
                for row in result :
                    chat = {
                        "chatId":row[0],
                        "userId":row[1],
                        "username":row[2],
                        "messagerId":row[3],
                        "messager_username":row[4],
                        }
                    chats.append(chat)
                return Response(json.dumps(chats,default=str) ,mimetype="application/json",status=200)
            else:
                return Response(message ,mimetype="application/json",status=400)
    else:
        return Response("invalid data" ,mimetype="application/json",status=400)
    



def post():
    data = request.json
    loginToken = data.get("loginToken")
    messagerId =data.get("messagerId")
    result=None
    rows=None
    conn= None 
    cursor = None
    if loginToken != "" and loginToken !=None and messagerId != None:

        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM `session` WHERE login_token = ?" , [loginToken,])
            user_id = cursor.fetchone()[0]
            cursor.execute("SELECT username FROM users WHERE id = ? OR id = ?",[user_id,messagerId])
            result = cursor.fetchall()
            cursor.execute("INSERT INTO chat(user_id,masseger_id) VALUES (?,?)",[user_id,messagerId])
            chatId = cursor.lastrowid
            conn.commit()
            rows=cursor.rowcount
        except mariadb.OperationalError as e:
            print (e)
            message = "connection error" 
        except Exception as e:
            print(e)
            message ="somthing went wrong, probably bad params " 
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if (result !=None or result ==[]) and rows ==1:
                chat = {
                    "chatId":chatId,
                    "userId":user_id,
                    "username":result[0][0],
                    "messagerId":messagerId,
                    "messager_username":result[1][0],
                    }
                return Response(json.dumps(chat,default=str) ,mimetype="application/json",status=200)
            else:
                return Response(message ,mimetype="application/json",status=400)
    else:
        return Response("invalid data" ,mimetype="application/json",status=400)