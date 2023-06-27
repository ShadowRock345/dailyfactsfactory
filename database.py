import mysql.connector
from logger import Logger

class Database():
    def __init__(self, typ):
        self.typ = typ
        self.main = 9
        self.gpt = 3
        self.stockvideo = 3
        self.music = 3
        self.logger = Logger("Database")
        
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
        if self.typ == "main":
            try:
                query = "SELECT * FROM video"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 'null'

        elif self.typ == "stockvideo":
            try:
                query = "SELECT * FROM stockvideo"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 'null'

        elif self.typ == "music":
            try:
                query = "SELECT * FROM music"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 'null'

        elif self.typ == "gpt":
            try:
                query = "SELECT * FROM gpt"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 'null'
        else:
            try:
                query = "SELECT * FROM main"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 'null'

    def write(self, data):
        if self.typ == "main":
            if len(data) == self.main:
                try:
                    query = "INSERT INTO video (Status, Fakt, Titel, Hashtag, Performance, VideoID, Laenge, MusikID, Url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    self.cursor.executemany(query, data)
                    self.db.commit()
                    self.logger.info("Data inserted into the " + self.typ + " database successfully.")
                except mysql.connector.Error as error:
                    self.logger.error("Error writing to " + self.typ + " database: " + error)
            else:
                self.logger.error("Data length does not match the expected count for the " + self.typ + " database.")

        elif self.typ == "stockvideo":
            if len(data) == self.stockvideo:
                try:
                    query = "INSERT INTO video (Tags, Usecount, Laenge) VALUES (%s, %s, %s)"
                    self.cursor.executemany(query, data)
                    self.db.commit()
                    self.logger.info("Data inserted into the " + self.typ + " database successfully.")
                except mysql.connector.Error as error:
                    self.logger.error("Error writing to " + self.typ + " database: " + error)
            else:
                self.logger.error("Data length does not match the expected count for the " + self.typ + " database.")

        elif self.typ == "music":
            if len(data) == self.music:
                try:
                    query = "INSERT INTO video (Tags, Usecount, Laenge) VALUES (%s, %s, %s)"
                    self.cursor.executemany(query, data)
                    self.db.commit()
                    self.logger.info("Data inserted into the " + self.typ + " database successfully.")
                except mysql.connector.Error as error:
                    self.logger.error("Error writing to " + self.typ + " database: " + error)
            else:
                self.logger.error("Data length does not match the expected count for the " + self.typ + " database.")

        elif self.typ == "gpt":
            if len(data) == self.gpt:
                try:
                    query = "INSERT INTO video (Thema, Score, Uhrzeit) VALUES (%s, %s, %s)"
                    self.cursor.executemany(query, data)
                    self.db.commit()
                    self.logger.info("Data inserted into the " + self.typ + " database successfully.")
                except mysql.connector.Error as error:
                    self.logger.error("Error writing to " + self.typ + " database: " + error)
            else:
                self.logger.error("Data length does not match the expected count for the " + self.typ + " database.")

        else:
            self.logger.error("Invalid database type.")

    def close(self):
        self.cursor.close()
        self.db.close()