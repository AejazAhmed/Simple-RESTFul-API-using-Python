import time
from random import randint
import json


def search_product(db_connection,search_query=None):
    try:
        response = []
        c = db_connection.cursor()
        if search_query:
            if 'price' in search_query:
                c.execute( "SELECT * FROM product where price="+search_query['price'])
                query_data = c.fetchall()
            elif 'product_name' in search_query:
                c.execute( "SELECT * FROM product where product_name LIKE "+"'"+str(search_query['product_name'])+"%'" )
                query_data = c.fetchall()
            else:
                c.execute(""" SELECT * FROM product  """)
                query_data = c.fetchall()
        else:
            c.execute(""" SELECT * FROM product  """)
            query_data = c.fetchall()
            print query_data
        if query_data:
            for data in query_data:
                qdict ={}
                qdict['id'] = data[0]
                qdict['product_name'] = data[1]
                qdict['product_discription'] = data[2]
                qdict['price'] = data[3]
                response.append(qdict)
        return response
    except Exception as e:
        return {"error":str(e)}

def add_product(db_connection,data):
    product_name= None
    product_discription = None
    price = None
    c = db_connection.cursor()
    _id = int(time.time())+randint(0,100000)
    data["id"] = _id
    if 'product_name' in data:
        product_name = str(data['product_name'])
    if 'product_discription' in data:
        description = data['description']
    if 'price' in data:
        price = data['price']
    try:
        if product_discription:
            values = "%d,%s,%s,%f" % (_id,product_name,product_discription,price)
        else:
            values = "%d,'%s','',%f" % (_id,product_name,price)

        print values
        c.execute("INSERT INTO product(id,product_name,product_discription,price) VALUES("+values+")")
        db_connection.commit()
        return data
    except Exception as e:
        return {"error":str(e)}

def update_product(db_connection,data):
    try:
        c = db_connection.cursor()
        query_set = ""
        if 'id' in data:
            for keys in data:
                if query_set:
                    query_set += ", "
                if data[keys]:
                    if str(data[keys]):
                        query_set += keys +"='"+str(data[keys])+"'"
                    else:
                        query_set += keys +"="+str(data[keys])
                else:
                    query_set += keys +"=''"
            if query_set:
                c.execute("SELECT * FROM product WHERE id="+str(data["id"]))
                query = c.fetchall()
                if query:
                    c.execute("UPDATE product SET "+query_set+" WHERE id ="+str(data["id"]))
                    db_connection.commit()
                    return {"success":"database updated"}
                else:
                    return {"error":"product with given id does not exists"}
            else:
                return {"key_error":"please provide data to updated data"}
        else:
            return {"key_error":"please provid Id to perform do the update operation"}
    except Exception as e:
        return {"error":str(e)}

def delete_product(db_connection,data):
    try:
        c = db_connection.cursor()
        if 'id' in data:
            c.execute("SELECT * FROM product WHERE id="+str(data["id"]))
            query = c.fetchall()
            if query:
                c.execute("DELETE FROM product WHERE id ="+str(data["id"]))
                db_connection.commit()
                return {"success":"successfully deleted"}
            else:
                return {"error":"product with given id does not exists"}
        else:
            return {"key_error":"please provid Id to perform the delete operation"}
    except Exception as e:
        print str(e)
        return {"error":str(e)}
