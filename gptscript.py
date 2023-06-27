from database import Database
from logger import Logger
from logger import Config
import schedule
import time as pytime
import threading
import datetime
import numpy as np
import random
import os
import openai

global module,errorlevel,videocount,openaiorganizationm,openaiapi_key,factcount


def configloader():
    realtimevalue = realtime()
    printmsg = 'loading configs: ' + str(module) + '|' + str(time) + '|' + str(database) + '|' + str(logger)
    #print('[' + module + ']' + str(realtimevalue) + '|' + printmsg)
    logger.success(printmsg)

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
            #print('[' + str(module) + ']' + str(realtimevalue) + '|' + str(errorlevel) + '|' + printmsg)
            if errorlevel < 3:
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
    global module
    errorlevel = 0
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
    global videocount
    gptarray = np.array(values)
    third_column = gptarray[:, 2]
    sorted_indices = np.argsort(third_column)[::-1]
    sorted_gptarray = gptarray[sorted_indices]
    zeile = videocount
    num_rows = sorted_gptarray.shape[0] - 1
    while zeile < num_rows:
        performancenumber1 = sorted_gptarray[zeile,2]
        zeile += 1
        performancenumber2 = sorted_gptarray[zeile,2]
        if performancenumber1 != performancenumber2:
            allrowstoinclude = zeile
            zeile = num_rows + 10
        else:
            allrowstoinclude = zeile
    if allrowstoinclude != videocount:
        zuverwendendezeilen = random.sample(range(0, allrowstoinclude), videocount)
    else:
        zuverwendendezeilen = []
        i = 0
        while i <= videocount:
            zuverwendendezeieln.append(i)
            i += 1
    return zuverwendendezeilen,sorted_gptarray

def getfacts(zuverwendendezeilen,sorted_gptarray):
    global openaiapi_key,openaiorganization,factcount
    errorlevel = 0
    openai.organization = str(openaiorganization)
    openai.api_key = openaiapi_key
    print(openaiapi_key)
    for element in zuverwendendezeilen:
        topic = sorted_gptarray[element,1]
        prompt = 'Generate ' + str(factcount) + ' short facts to the topic "'+ str(topic) + '" . They should be formated in a list for python.'
        print(prompt +'\n')
        input('continue?\n')
        i = 0
        while i == 0:
            response = openai.Completion.create(model="text-davinci-003",prompt=prompt,temperature=0.2,max_tokens=80)
            if response.status_code == 200:
                printmsg = 'generated ' + str(factcount) + 'facts for the topic: ' + str(topic)
                logger.success(printmsg)
                i = 1
            else:
                printmsg = 'error generating ' + str(factcount) + 'facts for the topic: ' + str(topic) + ' | error code: ' + str(response.status_code)
                logger.error(printmsg,errorlevel)
                if errorlevel < 3:
                    errorlevel += 1
                time.sleep(30)
            print(str(response))


def main():
    values = readvalues()
    zuverwendendezeilen,sorted_gptarray = converttoarray(values)
    factlist = getfacts(zuverwendendezeilen,sorted_gptarray)




config = Config('GPT')
module = str(config.getvalue('module'))
time = str(config.getvalue('time'))
videocount = int(config.getothervalue('UPLOAD', 'count'))
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
openaiorganization = str(config.getvalue('openaiorganization'))
openaiapi_key = str(config.getvalue('openaiapi_key'))
factcount = str(config.getvalue('factcount'))


configloader()

schedule.every().day.at(time).do(main)

#threadstarter() #zum test ausgeblendet
main()
