import sqlite3
import threading

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
            from werkzeug.security import generate_password_hash
            resources['password']=generate_password_hash(resources['password'])
            query = f"""INSERT INTO {tablename} 
                (Userid, First_Name, Last_Name, Email, Password) 
                VALUES (?, ?, ?, ?, ?)"""
            values = (
            f'U{self.i}', 
            resources['fname'], 
            resources['lname'], 
            resources['email'], 
            resources['password']
            )
            cursor.execute(query, values)
            conn.commit()

    def check(self,email:str,password:str):
        cursor, conn = self.get_db()
        from werkzeug.security import generate_password_hash
        password=generate_password_hash(password)
        cursor.execute("""
        SELECT 1 FROM your_table 
        WHERE email = ? AND password = ?
        """, (email, password))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False