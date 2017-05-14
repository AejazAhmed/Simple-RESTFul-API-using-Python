import sqlite3


def run_database():
    conn = sqlite3.connect('wingify.db')
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM user""")
        c.execute("""SELECT * FROM product""")
        print "No changes found"
        return True
    except Exception as e:
        c.execute(""" CREATE TABLE product (id INT PRIMARY KEY NOT NULL ,
        product_name CHAR(50) NOT NULL,
        product_discription TEXT,
        price DECIMAL)
        """)
        c.execute(""" CREATE TABLE user (id INT PRIMARY KEY NOT NULL ,
        username CHAR(50) NOT NULL UNIQUE,
        password CHAR(100) NOT NULL,
        token CHAR(150))
        """)
        conn.commit()
        print "user Table is Created\n"
        print "product Table is Created\n"
        conn.close()
        return True
