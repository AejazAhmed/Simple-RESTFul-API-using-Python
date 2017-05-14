import time
from random import randint
import json




def sign_up(db_connection,data):
    try:
        if 'token' in data:
            del data['token']
        c = db_connection.cursor()
        _id = int(time.time())+randint(0,100000)
        values = "%d,'%s','%s','%s'" % (_id,data['username'],data['password'],str(_id))
        c.execute("INSERT INTO user(id,username,password,token) VALUES("+values+")")
        db_connection.commit()
        return {"success":"user with username "+data['username']+" created successfully. please login with given to gain access"}
    except Exception as e:
        if "UNIQUE" in str(e):
            return {"error":"user name already exists please select different username"}
        else:
            return {"error":str(e)}

def login(db_connection,data):
    import uuid
    try:
        c = db_connection.cursor()
        c.execute( "SELECT * FROM user where username = "+"'"+data['username']+"' and password="+"'"+data['password']+"'" )
        fetch =c.fetchall()
        if fetch:
            token =  str(uuid.uuid4())
            token = data['username']+"--"+token
            c.execute("UPDATE user SET token="+"'"+str(token)+"' WHERE username = "+"'"+data['username']+"' and password="+"'"+data['password']+"'")
            db_connection.commit()
            return {"token":str(token)}
        else:
            return {"error":"Invalid Username or password"}
    except Exception as e:
        return {"error":str(e)}

# def logout(db_connection,data):
#     import uuid
#     try:
#         c = db_connection.cursor()
#         c.execute( "SELECT * FROM user where username = "+"'"+data['username']+"' and password="+"'"+data['password']+"'" )
#         fetch =c.fetchall()
#         if fetch:
#             token =  str(uuid.uuid4())
#             # token = data['username']+"--"+token
#             c.execute("UPDATE user SET token="+"'"+str(token)+"' WHERE username = "+"'"+data['username']+"' and password="+"'"+data['password']+"'")
#             db_connection.commit()
#             return {"token":str(token)}
#         else:
#             return {"error":"Invalid Username or password"}
#     except Exception as e:
#         return {"error":str(e)}

def authenticate(db_connection,data):
    try:
        c = db_connection.cursor()
        c.execute( "SELECT * FROM user where token ="+"'"+data+"'" )
        # c.execute( "SELECT * FROM user where token ="+"'"+data['token']+"' and username="+"'"+data['username']+"'" )
        token = c.fetchall()
        if token:
            print "auth", token
            return True
        else:
            return False
    except Exception as e:
        return False
