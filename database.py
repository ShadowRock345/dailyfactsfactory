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
                return 0

        elif self.typ == "stockvideo":
            try:
                query = "SELECT * FROM stockvideo"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 0

        elif self.typ == "music":
            try:
                query = "SELECT * FROM music"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 0

        elif self.typ == "gpt":
            try:
                query = "SELECT * FROM gpt"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 0
        else:
            try:
                query = "SELECT * FROM main"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            except mysql.connector.Error as error:
                return 0

    def write(self, data, writetype):
        if writetype == "main":
            if len(data) == self.main:
                try:
                    placeholders = '(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    querplaceholders = data
                    query = f'INSERT INTO video (Status, Fakt, Titel, Hashtags, Performance, VideoID, Laenge, MusikID, Url) VALUES {placeholders}'
                    db2 = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="maindatabase")
                    cursor2 = db2.cursor()
                    cursor2.execute(query, querplaceholders)
                    db2.commit()
                    cursor2.close()
                    db2.close()
                    self.logger.info("Data inserted into the " + writetype + " database successfully.")
                    return 1
                except mysql.connector.Error as error:
                    self.logger.error("Error writing to " + writetype + " database: " + str(error), 3)
                    return 0
            else:
                self.logger.error("Data length does not match the expected count for the " + writetype + " database.", 3)
                return 0

        elif writetype == "stockvideo":
            if len(data) == self.stockvideo:
                try:
                    placeholders = '(%s, %s, %s)'
                    querplaceholders = data
                    query = f'INSERT INTO video (Tags, Usecount, Laenge) VALUES {placeholders}'
                    db2 = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="stockvideodatabase")
                    cursor2 = db2.cursor()
                    cursor2.execute(query, querplaceholders)
                    db2.commit()
                    cursor2.close()
                    db2.close()
                    self.logger.info("Data inserted into the " + writetype + " database successfully.")
                    return 1
                except mysql.connector.Error as error:
                    self.logger.error("Error writing to " + writetype + " database: " + error, 3)
                    return 0
            else:
                self.logger.error("Data length does not match the expected count for the " + writetype + " database.", 3)
                return 0

        elif writetype == "music":
            if len(data) == self.music:
                try:
                    placeholders = '(%s, %s, %s)'
                    querplaceholders = data
                    query = f'INSERT INTO video (Tags, Usecount, Laenge) VALUES {placeholders}'
                    db2 = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="stockmusicdatabase")
                    cursor2 = db2.cursor()
                    cursor2.execute(query, querplaceholders)
                    db2.commit()
                    cursor2.close()
                    db2.close()
                    self.logger.info("Data inserted into the " + writetype + " database successfully.")
                    return 1
                except mysql.connector.Error as error:
                    self.logger.error("Error writing to " + writetype + " database: " + error, 3)
                    return 0
            else:
                self.logger.error("Data length does not match the expected count for the " + writetype + " database.", 3)
                return 0

        elif writetype == "gpt":
            if len(data) == self.gpt:
                try:
                    placeholders = '(%s, %s, %s)'
                    querplaceholders = data
                    query = f'INSERT INTO video (Thema, Score, Uhrzeit) VALUES {placeholders}'
                    db2 = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="gptdatabase")
                    cursor2 = db2.cursor()
                    cursor2.execute(query, querplaceholders)
                    db2.commit()
                    cursor2.close()
                    db2.close()
                    self.logger.info("Data inserted into the " + writetype + " database successfully.")
                    return 1
                except mysql.connector.Error as error:
                    self.logger.error("Error writing to " + writetype + " database: " + error, 3)
                    return 0
            else:
                self.logger.error("Data length does not match the expected count for the " + writetype + " database.", 3)
                return 0

        else:
            self.logger.error("Invalid database type.")
            return 0
        return 0

    def update(self, writetype, update_columns, update_values, identification_column, identification_value):
        if writetype == "main":
            try:
                db2 = mysql.connector.connect(host="localhost",user="admin",password="FactsFactoryBotDatabase",database="maindatabase")
                cursor2 = db2.cursor()
                set_clause = ", ".join(f"{column} = %s" for column in update_columns)

                query = f"UPDATE video SET {set_clause} WHERE {identification_column} = %s"

                update_values.append(identification_value)

                cursor2.execute(query, update_values)

                db2.commit()

                cursor2.close()
                db2.close()
                return 1
            except mysql.connector.Error as error:
                self.logger.error("Failed updating " + writetype + " database: " + str(error), 3)
                return 0

    def close(self):
        self.cursor.close()
        self.db.close()