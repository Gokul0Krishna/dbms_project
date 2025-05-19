import sqlite3
import threading
from werkzeug.security import generate_password_hash, check_password_hash

class Tableaction:
    def __init__(self):
        self.local = threading.local()    
        self.i=0
        self.j=0
        self.k=0
        self.uid=''
        self.bid=''
        self.signedin=False

    def get_db(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
            self.local.cursor = self.local.conn.cursor()
        return self.local.cursor, self.local.conn
    
    def adddatauser(self,resources:dict):
            cursor, conn = self.get_db()
            resources['password']=generate_password_hash(resources['password'])
            self.i=self.i+1
            query = f"""INSERT INTO user 
                (Userid, First_Name, Last_Name, Status, Email, Password,Fine) 
                VALUES (?, ?, ?, ?, ?, ?, ?)"""
            values = (
            self.i, 
            resources['fname'], 
            resources['lname'],
            0, 
            resources['email'], 
            resources['password'],
            0
            )
            cursor.execute(query, values)
            self.signedin=True
            conn.commit()
            conn.close()

    def adddataborrow(self):  
            from datetime import date,timedelta
            today = date.today()
            due=today+timedelta(7)
            with sqlite3.connect('mydatabase.db') as conn:
                cursor = conn.cursor()
                query = f"""INSERT INTO borrow 
                    (UserID,BookID,BorrowDate,DueDate) 
                    VALUES (?, ?, ?, ?)"""
                print(self.i)
                values = ( 
                self.i,
                self.bid,
                today, 
                due, 
                )
                cursor.execute(query, values)
                conn.commit()

    def check(self,email:str,password:str):
        cursor, conn = self.get_db()
        # cursor, _ = self.get_db()
        cursor.execute("SELECT userid, password FROM user WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            userid=result[0]
            stored_hash = result[1]
            if check_password_hash(stored_hash, password):
                self.i=userid
                self.signedin=True
                return True
        else:
            return False
    
    def fetchdata(self,bookname:str):
        cursor, conn = self.get_db()
        cursor.execute("""
        SELECT * FROM book 
        WHERE Title = ?
        """, (bookname,))
        row = cursor.fetchone()
        conn.close()
        if row:
            self.bid=row[0]
            print(self.bid)
            return row
        else:
            return False

    def findname(self):
        with sqlite3.connect('mydatabase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT First_Name FROM user 
                WHERE Userid = ?
                """, (self.i,))
            name = cursor.fetchone() 
            return name
    
    def setstatus(self,data):
        cursor, conn = self.get_db()
        cursor.execute("""
            UPDATE book 
            SET Status = ? 
            WHERE Bookid = ?
        """, (data, self.bid))
        conn.commit()
        conn.close() 

    def getuid(self):
        cursor, conn = self.get_db()
        cursor.execute("SELECT userid FROM user ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        self.i=int(result)
        print(self.i)

    def Signedin(self):
        return self.signedin    
    
    def getdataborrow(self):
        with sqlite3.connect('mydatabase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT userid FROM user ORDER BY id DESC LIMIT 1")