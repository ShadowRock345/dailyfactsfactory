from database import Database
from logger import Logger
from logger import Config
from discord_logger import Discord_logger
import schedule
import tts
import datetime
import os
import time as pytime
import numpy as np
import ast

global module,voice,database

def threadstarter():
    threadstarter = 0
    errorlevel = 0
    while threadstarter == 0:
        try:
            thread = threading.Thread(target=timecheck) #timecheck Funktion startet als erstes in eigenem Thread
            thread.start()
            threadstarter = 1
        except:
            pytime.sleep(2)
            printmsg = 'failed to start thread'
            logger.error(printmsg,errorlevel)
            if errorlevel < 3:
                errorlevel += 1
            else:
                discord_logger.error(printmsg,module)
                pytime.sleep(120)
                
def timecheck():
    global module
    realtimevalue = realtime()
    printmsg =  'starting gpt timecheck'
    realtimevalue = realtime()
    logger.success(printmsg)
    discord_logger.success(printmsg,module)
    while True:
        schedule.run_pending()
        pytime.sleep(1)
        
def realtime():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def read_main():
    global module,database
    errorlevel = 0
    values = 0 # zuerst auf null setzten
    while values == 0:
        database.connect() #main Database öffnen
        values = database.getvalues()  #main Database Daten auslesen
        realtimevalue = realtime()
        database.close() #main Database schließen
        if values == 0:
            printmsg = 'failed to open ' + module + ' database'
            logger.error(printmsg,errorlevel)
            realtimevalue = realtime()
            if errorlevel < 3:
                errorlevel += 1
            else:
                pytime.sleep(120)
                discord_logger.error(printmsg,module)
        else:
            printmsg = 'opening main database'
            logger.success(printmsg)
            discord_logger.success(printmsg,module)
    return values

def parse_new_facts(values):
    facts_to_generate = []
    array = np.array(values)
    if len(array) == 0:
        logger.error('main database is empty',errorlevel = 3)
        discord_logger.error('main database is empty',module)
    else:
        seccond_column = array[:, 1]
        i = 0
        for status in seccond_column:
            if status == 'fact_generated':
                id = array[i,0]
                facts = array[i,2]
                topic = array[i,3]
                facts_to_generate.append(id)
                facts_to_generate.append(facts)
                facts_to_generate.append(topic)
            i += 1
    return facts_to_generate

def checkaudiofile(filename):
    folder = "/textaudios"
    
    file_path = os.path.join(folder,filename)
    
    if os.path.exists(file_path):
        return 1
    else:
        return 0

def createaudio(facts_to_generate):
    global voice
    length_facts_list = len(facts_to_generate)
    i = 0
    while i < length_facts_list:
        mainfilename = facts_to_generate[i]
        i += 1
        facts_list = facts_to_generate[i]
        i += 1
        topic = facts_to_generate[i]
        i += 1
        x = 1
        facts = ast.literal_eval(facts_list)
        for fact in facts:
            filename = "textaudios/" + str(mainfilename) + '_' + str(x) + '.mp3'
            tts.tts(fact,voice,filename)
            x += 1
            #print(fact)
            #print(filename)
        x = 0
        filename = "textaudios/" + str(mainfilename) + '_' + str(x) + '.mp3'
        text = 'Daily ' + str(topic) + ' facts!'
        tts.tts(text,voice,filename)
        #print(text)
    
def main():
    values = read_main()
    facts_to_generate =  parse_new_facts(values)
    if facts_to_generate != []:
        createaudio(facts_to_generate)


discord_logger = Discord_logger()
config = Config('TEXTAUDIO')
module = str(config.getvalue('module'))
schedule.every(5).minutes.do(main)
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
voice = str(config.getvalue('voice'))

#threadstarter() #zum test ausgeblendet
main()

