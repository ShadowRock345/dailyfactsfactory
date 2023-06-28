from database import Database
from logger import Logger
from logger import Config
from discord_logger import Discord_logger
import schedule
import tts
import os
import time as pytime

global module,voice

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
    global module
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
            printmsg = 'opening ' + str(module) + ' database'
            logger.success(printmsg)
            discord_logger.success(printmsg,module)
    return values

def checkaudiofile(filename):
    folder = "/textaudios"
    
    file_path = os.path.join(folder,filename)
    
    if os.path.exists(file_path):
        return 1
    else:
        return 0

def createaudio(text,filename):
    global voice
    tts.tts(text,voice,filename)
    

def main():
    values = read_main()
    


discord_logger = Discord_logger()
config = Config('TEXTAUDIO')
module = str(config.getvalue('module'))
schedule.every(5).minutes.do(main)
database = database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
voice = Logger(str(config.getvalue('voice')))

#threadstarter() #zum test ausgeblendet
main()

