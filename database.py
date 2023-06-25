import mysql.connector

class Database():
    def __init__(self, typ):
        self.typ = typ
        
    def connect(self):
        if (self.typ == "main"):
            self.db = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="maindatabase")
            self.cursor = self.db.cursor()
        elif (self.typ == "stockvideo"):
            self.db = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="stockvideodatabase")
            self.cursor = self.db.cursor()
        elif (self.typ == "music"):
            self.db = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="musicdatabase")
            self.cursor = self.db.cursor()
        elif (self.typ == "gpt"):
            self.db = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="gptdatabase")
            self.cursor = self.db.cursor()
        else:
            self.db = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="maindatabase")
            self.cursor = self.db.cursor()
            
    def getvalues(self):
        if (self.typ == "main"):
            try:
                query = f"SELECT * FROM video"
                self.cursor.execute(query)
                result = self.cursor.fetchall()

                return result

            except mysql.connector.Error as error:
                return 'null'

        elif (self.typ == "stockvideo"):
            try:
                query = f"SELECT * FROM stockvideo"
                self.cursor.execute(query)
                result = self.cursor.fetchall()

                return result

            except mysql.connector.Error as error:
                return 'null'

        elif (self.typ == "music"):
            try:
                query = f"SELECT * FROM music"
                self.cursor.execute(query)
                result = self.cursor.fetchall()

                return result

            except mysql.connector.Error as error:
                return 'null'

        elif (self.typ == "gpt"):
            try:
                query = f"SELECT * FROM gpt"
                self.cursor.execute(query)
                result = self.cursor.fetchall()

                return result

            except mysql.connector.Error as error:
                return 'null'
        else:
            try:
                query = f"SELECT * FROM main"
                self.cursor.execute(query)
                result = self.cursor.fetchall()

                return result

            except mysql.connector.Error as error:
                return 'null'

    def close(self):
        self.cursor.close()
        self.db.close()