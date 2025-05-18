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

    def get_db(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
            self.local.cursor = self.local.conn.cursor()
        return self.local.cursor, self.local.conn
    
    def adddata(self,tablename:str,resources:dict):
        cursor, conn = self.get_db()
        if tablename=="user":
            resources['password']=generate_password_hash(resources['password'])
            query = f"""INSERT INTO user 
                (Userid, First_Name, Last_Name, Status, Email, Password,Fine) 
                VALUES (?, ?, ?, ?, ?, ?, ?)"""
            values = (
            f'U{self.i}', 
            resources['fname'], 
            resources['lname'],
            0, 
            resources['email'], 
            resources['password'],
            0
            )
            self.i=self.i+1
            cursor.execute(query, values)
        elif tablename=="borrow":
            from datetime import date,datetime
            today = date.today()
            mon=today.month
            pas=today.day
            pas=pas+7
            if(mon%2==0):
                if(pas>31):
                    pas=pas-31
                else:
                    pas=pas-30
            date_string = f"{today.year}-{today.month}-{pas}"
            date_format = "%Y-%m-%d"
            date_object = datetime.strptime(date_string, date_format).date()
            query = f"""INSERT INTO user 
                (BorrowID,UserID,BookID,BorrowDate,DueDate) 
                VALUES (?, ?, ?, ?, ?)"""
            values = (
            f'BW{self.k}', 
            self.uid,
            self.bid,
            today, 
            date_object, 
            0
            )
            cursor.execute(query, values)
        conn.commit()
        conn.close()

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
                self.uid=userid
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
        if row:
            self.bid=row[0]
            print(self.bid)
            return row
        else:
            return False

