import sqlite3


class DB:
    def __init__(self):
        self.con =sqlite3.connect('flask.db', check_same_thread=False) 
        self.c = self.con.cursor() 
        
    def create(self):
        self.c.execute(""" CREATE TABLE IF NOT EXISTS  users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL 
            
        ) """)
        self.con.commit() 
        
    def insert(self, *args):
        self.c.execute("INSERT INTO users VALUES(?,?)", args)
        self.con.commit()
            
    def get_user_cred(self, *args):
        try:
            self.c.execute("SELECT * FROM users WHERE username=? AND password=?", args)
            user = self.c.fetchone()
            return user
        except:
            self.c.execute("SELECT * FROM users WHERE username=?", args)
            return self.c.fetchone()
    
            
        