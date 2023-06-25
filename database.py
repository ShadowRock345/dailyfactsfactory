import mysql.connector

class Database():
    def __init__(self, typ):
        self.typ = typ
        
    def connectdb(self):
        if (self.typ == "main"):
            db = mysql.connector.connect(host="localhost",user="",password="",database="maindatabase")
            cursor = db.cursor()
        elif (self.typ == "stockvideo"):
            db = mysql.connector.connect(host="localhost",user="",password="",database="stockvideodatabase")
            cursor = db.cursor()
        elif (self.typ == "music"):
            db = mysql.connector.connect(host="localhost",user="",password="",database="musicdatabase")
            cursor = db.cursor()
        elif (self.typ == "gpt"):
            db = mysql.connector.connect(host="localhost",user="",password="",database="gptdatabase")
            cursor = db.cursor()
        else:
            db = mysql.connector.connect(host="localhost",user="",password="",database="maindatabase")
            cursor = db.cursor()
            
    def writevalues(self, valueslist):
         if (self.typ == "main"):
           
        
            
        
    def close(self):
        db.close()