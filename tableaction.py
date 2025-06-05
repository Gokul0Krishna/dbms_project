import sqlite3
import threading
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager
import random

class Tableaction:
    def __init__(self):
        self.local = threading.local()    
        self.i=0
        self.j=0
        self.k=0
        self.uid=''
        self.bid=''
        self.signedin=False

    @contextmanager
    def _get_connection(self):
        """Safe connection handler with automatic cleanup"""
        conn = None
        try:
            conn = sqlite3.connect('mydatabase.db', timeout=10)
            conn.execute("PRAGMA busy_timeout = 5000")  # 5 second timeout
            yield conn
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def adddatauser(self,resources:dict):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            resources['password']=generate_password_hash(resources['password'])
            self.i=self.i+1
            print(self.i)
            query = f"""INSERT INTO user 
                (Userid, First_Name, Last_Name, Status, Email, Password) 
                VALUES (?, ?, ?, ?, ?, ?)"""
            values = (
            self.i, 
            resources['fname'], 
            resources['lname'],
            0, 
            resources['email'], 
            resources['password'],
            )
            cursor.execute(query, values)
            self.signedin=True
            conn.commit()

    def adddataborrow(self):  
            from datetime import date,timedelta
            today = date.today()
            due=today+timedelta(7)
            with self._get_connection() as conn:
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
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT userid, password FROM user WHERE email = ?", (email,))
            result = cursor.fetchone()
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
       with self._get_connection() as conn:
            cursor = conn.cursor()
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
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT First_Name FROM user 
                WHERE Userid = ?
                """, (self.i,))
            name = cursor.fetchone() 
            return name
    
    def setstatus(self,data):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE book 
                SET Status = ? 
                WHERE Bookid = ?
            """, (data, self.bid))
            conn.commit()
       

    def getuid(self):
         with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT userid FROM user ORDER BY userid DESC LIMIT 1")
            result = cursor.fetchone()
            print(result)
            conn.close()
            if result:
                self.i=int(result[0])
                print(self.i)

    def Signedin(self):
        return self.signedin    
    
    def getdataborrow(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM borrow WHERE Userid = ?", (self.i,))
            data=cursor.fetchall()
            return data
    
    def getdatauser(self):
        # self.i=1#remove
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT First_name,Last_Name,Email FROM user WHERE Userid = ?", (self.i,))
            data=cursor.fetchall()
            return data
    
    def setstatus(self,value:int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE book 
                SET Status = {value}
                WHERE Bookid = ?
            """, (self.bid,))
            conn.commit()

    def getbookdata(self,bokid:int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Title , Img FROM book WHERE Bookid = ?", (bokid,))
            data=cursor.fetchone()
            return data
    
    def reset(self):
        with self._get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute("UPDATE book SET Status = 0")
            conn.commit()

    def fine(self,bokid:int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DueDate FROM borrow WHERE BookID = ?", (bokid,))
            data=cursor.fetchall()       
            from datetime import date,datetime
            today = date.today()
            for i in data:
                due_date_str = i[0]
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if due_date<today:
                    cursor.execute(f"UPDATE book SET Fine = {today-due_date} WHERE Bookid = ?",(bokid,))
                    cursor.execute(f"UPDATE book SET Status = 1 WHERE Bookid = ?",(bokid,))
                    conn.commit()

    def resetfine(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Fine FROM book WHERE Bookid = ?", (self.bid,))
            data=cursor.fetchone()
            if int(data[0])>0:
                return True
            else:
                cursor.execute("UPDATE book SET Status = 0 WHERE Bookid = ?", (self.bid,))
                conn.commit()
                cursor.execute("DELETE FROM borrow WHERE Bookid = ?", (self.bid,))
                conn.commit()

    def checkusid(self):
         with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 
                FROM borrow 
                WHERE UserID = ? AND BookID = ?
            """, (self.i, self.bid))
            return cursor.fetchone()
    
    def signout(self):
            self.i=0
            self.signedin=False

    def randX(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM book")
            val=random.randint(0,(cursor.fetchone()[0])-1)
            val=f"B{val}"
            cursor.execute("SELECT Title FROM book WHERE Bookid = ?", (val,))
            data=cursor.fetchone()
            return data[0]
        
    def checkbook(self):
        if self.bid !='':
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Title FROM book WHERE Bookid = ?", (self.bid,))
                data=cursor.fetchone()
                return data[0]
        else:
            return False
        
    def getauth(self):
        with self._get_connection() as conn:
                a=[]
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT Author FROM book")
                data=cursor.fetchall()
                for i in data:
                    i=i[0].replace("  "," ")
                    a.append(i)
                return a