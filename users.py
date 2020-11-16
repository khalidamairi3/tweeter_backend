import dbcreds
import secrets
import json
from flask import  Response, request
import mariadb
def get_users():
    result = None
    params = request.args
    user_id = params.get("userId")
    conn = None
    cursor = None
    result = None
    if user_id:
        
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?",[user_id,])
            result = cursor.fetchall()
        except mariadb.OperationalError as e:
            message = "connection error" 
        except:
            message ="somthing went wrong, probably bad params " 
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
    else:
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
        except mariadb.OperationalError as e:
            message = "connection error" 
        except:
            message ="somthing went wrong" 
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
    if result or result ==[]:
        users=[]
        for item in result:
            user = {
                "userId":item[4],
                "email":item[1],
                "username":item[0],
                "bio":item[3],
                "birthdate":item[5]
                }
            users.append(user)
        return Response(json.dumps(users,default=str) ,mimetype="application/json",status=200)
    else:
        return Response(message ,mimetype="application/json",status=400)


def post_user():
    data = request.json
    conn = None
    cursor = None
    result = None
    user=None
    email=data.get("email")
    username = data.get("username")
    password = data.get("password")
    bio = data.get("bio")
    birthdate = data.get("birthdate")
    
    if email and username and password and bio and birthdate: 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username,email,password,bio,birthday) VALUES (?, ?, ?, ?, ?)", [ data["username"], data["email"] , data["password"] , data["bio"] , data["birthdate"]])
            conn.commit()
            userId = cursor.lastrowid
            print(user)
            loginToken=secrets.token_urlsafe(16)
            cursor.execute("INSERT INTO `session` (user_id, login_token) VALUES (?,?)",[userId,loginToken,])
            conn.commit()
            result = cursor.rowcount
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
                user = {

                    "userId":userId,    
                    "email":data["email"],
                    "username":data["username"],
                    "bio":data["bio"],
                    "birthdate":data["birthdate"],
                    "loginToken":loginToken
                        
                    }
                return Response(json.dumps(user,default=str),mimetype="application/json",status=201)
            return Response(message ,mimetype="text/html",status=400)
    else:
        return Response("There is missing data" ,mimetype="text/html",status=400)

def patch_user():
    data = request.json
    conn = None
    cursor = None
    result = None
    email=data.get("email")
    username = data.get("username")
    password = data.get("password")
    bio = data.get("bio")
    birthdate = data.get("birthdate")
    loginToken=data.get("loginToken")
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if email !="" and email !=None and loginToken !="" and loginToken !=None :
            cursor.execute("UPDATE users SET email= ?  WHERE id = ( SELECT user_id FROM users inner join `session` s on users.id = s.user_id WHERE login_token = ? )",[email,loginToken,])
        if username !="" and username !=None and loginToken !="" and loginToken !=None :
            cursor.execute("UPDATE users SET username= ?  WHERE id = ( SELECT user_id FROM users inner join `session` s on users.id = s.user_id WHERE login_token = ?)",[username,loginToken,])
        if password !="" and password !=None and loginToken !="" and loginToken !=None :
            cursor.execute("UPDATE users SET password= ?  WHERE id = ( SELECT user_id FROM users inner join `session` s on users.id = s.user_id WHERE login_token = ?)",[password,loginToken,])
        if bio !="" and bio !=None and loginToken !="" and loginToken !=None :
            cursor.execute("UPDATE users SET bio= ?  WHERE id = ( SELECT user_id FROM users inner join `session` s on users.id = s.user_id WHERE login_token = ?)",[bio,loginToken,])
        if birthdate !="" and birthdate !=None and loginToken !="" and loginToken !=None :
            cursor.execute("UPDATE users SET birthday= ?  WHERE id = ( SELECT user_id FROM users inner join `session` s on users.id = s.user_id WHERE login_token = ?)",[birthdate,loginToken,])
        conn.commit()
        result= cursor.rowcount
    except mariadb.OperationalError as e:
        message = "connection error or wrong entry"
    except mariadb.IntegrityError as e:
        message = "Something is wrong with your data. probably there is another user using the same username or the same email"
    except:
        message =  "somthing went wrong"
    finally:
        if cursor != None:
                cursor.close()
        if conn != None:
            conn.rollback()
            conn.close()
        if(result == 1):
            user=None
            conn=None
            cursor=None
            try:
                conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
                cursor = conn.cursor()
                cursor.execute("SELECT id, email, username, bio, birthday FROM users INNER JOIN `session` s1 ON id=s1.user_id WHERE s1.login_token =?" ,[loginToken,])
                user=cursor.fetchone()
            except mariadb.OperationalError as e:
                message = "connection error or wrong entry"
            except:
                message =  "somthing went wrong"
            finally:
                if cursor != None:
                    cursor.close()
                if conn != None:
                    conn.rollback()
                    conn.close()
                if(user):
                    res = {
                        "userId":user[0],
                        "email":user[1],
                        "username":user[2],
                        "bio":user[3],
                        "birthdate":user[4]

                    }
                    return Response(json.dumps(res,default=str),mimetype="application/json",status=200)
                else:
                    return Response(message ,mimetype="text/html",status=400)
        else:
            return Response(message ,mimetype="text/html",status=400)



                                      
         
def delete_user():
    data=request.json
    password = data.get("password")
    loginToken = data.get("loginToken")
    print(password)
    print(loginToken)
    rows=None
    try:
        conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT id,password FROM users INNER JOIN `session` s1 ON id=s1.user_id WHERE s1.login_token =?" ,[loginToken,])
        user=cursor.fetchone()
        print(user)
        if user:
            if user[1]==password:
                cursor.execute("DELETE FROM `session` WHERE user_id = ?",[user[0],])
                cursor.execute("DELETE FROM comment_likes WHERE user_id = ?",[user[0],])
                cursor.execute("DELETE FROM comment_likes WHERE comment_id = (SELECT id FROM comment WHERE user_id=?)",[user[0],])
                cursor.execute("DELETE FROM comment WHERE user_id = ?",[user[0],])
                cursor.execute("DELETE FROM tweet_likes WHERE user_id = ?",[user[0],])
                cursor.execute("DELETE FROM tweet_likes WHERE tweet_id = (SELECT id FROM tweet WHERE user_id=?)",[user[0],])
                cursor.execute("DELETE FROM tweet WHERE user_id = ?",[user[0],])
                cursor.execute("DELETE FROM user_follows WHERE user_id = ? or followId = ?",[user[0],user[0]])
                cursor.execute("DELETE FROM users WHERE id = ?",[user[0],])
                conn.commit()
                rows=cursor.rowcount
    except mariadb.OperationalError as e:
        message = "connection error or wrong entry"
    except mariadb.IntegrityError as e:
        message = "Something is wrong with your data. probably there is another user using the same username or the same email"
    except:
        message =  "somthing went wrong"
    finally:
        if cursor != None:
            cursor.close()
        if conn != None:
            conn.rollback()
            conn.close()
        if rows == 1 :
            return Response("Delete Succecs",mimetype="text/html",status=204)
        else:
            return Response(message,mimetype="text/html",status=400)
