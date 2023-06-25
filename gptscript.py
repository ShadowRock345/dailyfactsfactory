from database import Database
from logger import Logger
import schedule
import time as pytime
import threading
from logger import Config
import datetime
import numpy as np

global module,errorlevel

def configloader():
    realtimevalue = realtime()
    printmsg = 'loading configs: ' + str(module) + '|' + str(time) + '|' + str(database) + '|' + str(logger)
    #print('[' + module + ']' + str(realtimevalue) + '|' + printmsg)
    logger.success(printmsg)

def threadstarter():
    threadstarter = 0
    while threadstarter == 0:
        try:
            thread = threading.Thread(target=timecheck) #timecheck Funktion startet als erstes in eigenem Thread
            thread.start()
            threadstarter = 1
        except:
            pytime.sleep(2)
            printmsg = 'failed to start thread'
            logger.error(printmsg,errorlevel)
            #print('[' + str(module) + ']' + str(realtimevalue) + '|' + str(errorlevel) + '|' + printmsg)
            if errorlog < 3:
                errorlevel += 1
            else:
                pytime.sleep(120)

def timecheck():
    global module
    realtimevalue = realtime()
    printmsg =  'starting gpt timecheck'
    realtimevalue = realtime()
    #print('[' + str(module) + ']' + str(realtimevalue) + '|' + printmsg)
    logger.success(printmsg)
    while True:
        schedule.run_pending()
        pytime.sleep(1)

def realtime():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def readvalues():
    global module,errorlevel
    values = 'null' # zuerst auf null setzten
    while values == 'null':
        database.connect() #GPT Database öffnen
        values = database.getvalues()  #GBT Database Daten auslesen
        realtimevalue = realtime()
        #print('[' + str(module) + ']' + str(realtimevalue) + '|' + printmsg)
        database.close() #GPT Database schließen
        if values == 'null':
            printmsg = 'failed to open ' + module + ' database'
            logger.error(printmsg,errorlevel)
            realtimevalue = realtime()
            #print('[' + str(module) + ']' + str(realtimevalue) + '|' + str(errorlevel) + '|' + str(printmsg))
            if errorlevel < 3:
                errorlevel += 1
            else:
                pytime.sleep(120)
        printmsg = 'opening ' + str(module) + ' database, values:' + str(values)
        logger.success(printmsg)
    return values

def converttoarray(values):
    gptarray = np.array(values)
    third_column = gptarray[:, 2]
    sorted_indices = np.argsort(third_column)[::-1]
    sorted_gptarray = gptarray[sorted_indices]
    zeile = 0
    print(sorted_gptarray)
    num_rows = sorted_gptarray.shape[0]
    #while zeile <= num_rows:
    #    performancenumber1 = sorted_gptarray[zeile,2]

def main():
    values = readvalues()
    gptarray = converttoarray(values)




config = Config('GPT')
module = str(config.getvalue('module'))
time = str(config.getvalue('time'))
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))

configloader()

schedule.every().day.at(time).do(main)
errorlevel = 0

#threadstarter() #zum test ausgeblendet
main()
