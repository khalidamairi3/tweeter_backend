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
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if userId:
            cursor.execute("SELECT * FROM notifications n INNER JOIN users u on n.user_id = u.id WHERE n.notified_id =?" ,[userId,])
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
            notifications=[]
            for row in result:
                notification = {
                "notificationId":row[0],
                "userId":row[1],    
                "username":row[5],
                "message":row[3],
                "viewStaus":row[4],   
                }
                notifications.append(notification)
            return Response(json.dumps(notifications,default=str),mimetype="application/json",status=200)
        else:
            return Response("failed",mimetype="text/html",status=400)
def patch():
    data=request.json
    notificationId= data.get("notificationId")
    conn = None
    cursor = None
    result = None
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if notificationId:
            cursor.execute("UPDATE notifications SET view_status = ? WHERE id =?" ,[ 1 , notificationId])
        conn.commit()
        result=cursor.rowcount
    except mariadb.OperationalError as e:
        message = "connection error or wrong entry"
    except Exception as e:
        print(e)
        message =  "somthing went wrong"
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if result == 1:
            
            notification = {
            "notificationId":notificationId,
            "viewStaus": 1,   
            }
                
            return Response(json.dumps(notification,default=str),mimetype="application/json",status=200)
        else:
            return Response("failed",mimetype="text/html",status=400)
    