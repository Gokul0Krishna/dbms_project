import sqlite3
import threading
from werkzeug.security import generate_password_hash, check_password_hash

class Tableaction:
    def __init__(self):
        self.local = threading.local()    
        self.i=0
        self.j=0

    def get_db(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
            self.local.cursor = self.local.conn.cursor()
        return self.local.cursor, self.local.conn
    
    def adddata(self,tablename:str,resources:dict):
        cursor, conn = self.get_db()
        if tablename=="user":
            resources['password']=generate_password_hash(resources['password'])
            query = f"""INSERT INTO {tablename} 
                (Userid, First_Name, Last_Name, Status, Email, Password) 
                VALUES (?, ?, ?, ?, ?, ?)"""
            values = (
            f'U{self.i}', 
            resources['fname'], 
            resources['lname'],
            0, 
            resources['email'], 
            resources['password']
            )
            cursor.execute(query, values)
            conn.commit()
            conn.close()

    def check(self,email:str,password:str):
        cursor, conn = self.get_db()
        # cursor, _ = self.get_db()
        cursor.execute("SELECT password FROM user WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            stored_hash = result[0]
            return check_password_hash(stored_hash, password)
        else:
            return False
    
    def fetchdata(self,bookname:str):
        cursor, conn = self.get_db()
        cursor.execute("SELECT password FROM book WHERE Title = ?", (bookname))
        result = cursor.fetchone()