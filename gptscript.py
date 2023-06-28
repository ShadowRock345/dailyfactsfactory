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
import json
from discord_logger import Discord_logger

global module,errorlevel,videocount,openaiorganizationm,openaiapi_key,factcount,testmode


def configloader():
    global testmode
    if testmode == True:
        printmsg = '!using testmode!'
        logger.success(printmsg)
        discord_logger.success(printmsg,module)
    realtimevalue = realtime()
    printmsg = 'loading configs: ' + str(module) + '|' + str(time) + '|' + str(testmode) + '|' + str(factcount)
    logger.success(printmsg)
    discord_logger.success(printmsg,module)

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

def readvalues():
    global module
    errorlevel = 0
    values = 0 # zuerst auf null setzten
    while values == 0:
        database.connect() #GPT Database öffnen
        values = database.getvalues()  #GPT Database Daten auslesen
        realtimevalue = realtime()
        database.close() #GPT Database schließen
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
    fact_list = []
    openai.organization = str(openaiorganization)
    openai.api_key = openaiapi_key
    for element in zuverwendendezeilen:
        topic = sorted_gptarray[element,1]
        prompt = 'Generate ' + str(factcount) + ' short facts to the topic "'+ str(topic) + '" . They should be formated in a list for python.'
        i = 0
        while i == 0:
            try:
                response = openai.Completion.create(model="text-davinci-003",prompt=prompt,temperature=0.2,max_tokens=80)
                printmsg = 'generated ' + str(factcount) + 'facts for the topic: ' + str(topic)
                logger.success(printmsg)
                discord_logger.success(printmsg,module)
                i = 1
            except:
                printmsg = 'error generating ' + str(factcount) + ' facts for the topic: ' + str(topic) + ' | error code: ' + str(response.status_code)
                logger.error(printmsg,errorlevel)
                if errorlevel < 3:
                    errorlevel += 1
                else:
                    discord_logger.error(printmsg,module)
                    time.sleep(600)
                time.sleep(30)
        response_json = json.loads(str(response))
        facts = response_json["choices"][0]["text"]
        short_fact_list = facts.strip().split("\n")
        fact_list.append(topic)
        fact_list.append(short_fact_list)
    return fact_list

def writetomaindatabase(fact_list):
    errorvalue = 0
    x = 0
    length_fact_list = len(fact_list)
    while x < length_fact_list:
        fact_topic = fact_list[x]
        x += 1
        facts = fact_list[x]
        x += 1
        i = 0
        while i == 0:
            #try:
                database.connect()
                string_fact_topic = str(fact_topic)
                string_facts = str(facts)
                #Status, Fakt, Titel, Hashtag, Performance, VideoID, Laenge, MusikID, Url
                valuestowrite = ['fact_generated',string_facts,string_fact_topic,None,None,None,None,None,None]
                databasestatus = database.write(valuestowrite,'main')
                database.close()
                if databasestatus == 1:
                    printmsg = 'facts for: ' + str(fact_topic) + ' were added to the main database'
                    logger.success(printmsg)
                    discord_logger.success(printmsg,module)
                    i = 1
                else:
                    pytime.sleep(10)
            # except Exception as e:
            #     printmsg = 'error writing to main database, errorcode: ' + str(errorvalue) + ' Exception: ' + str(e)
            #     logger.error(printmsg,errorvalue)
            #     if errorvalue < 3:
            #         errorvalue += 1
            #     else:
            #       discord_logger.error(printmsg,module)
            #     pytime.sleep(15)

def main():
    values = readvalues()
    zuverwendendezeilen,sorted_gptarray = converttoarray(values)
    if testmode == True:
        fact_list = [54, ['1. Jazz is a genre of music that originated in the late 19th and early 20th centuries in African American communities.', '2. Rock music is a genre of popular music that originated as "rock and roll" in the United States in the 1950s.', '3. Hip hop is a genre of music that originated in the late 1970s in the Bronx, New York City.'], 55, ['1. International relations is a field of study that examines the interactions between countries.', '2. It is a multidisciplinary field that combines elements of political science, economics, history, and law.', '3. International relations is concerned with the causes of war, the maintenance of peace, and the promotion of cooperation between states.'], 18, ['1. Psychiatry is a branch of medicine that focuses on the diagnosis, treatment, and prevention of mental health disorders.', '', '2. Psychiatrists are medical doctors who specialize in mental health and can prescribe medications.', '', '3. Psychotherapy is a form of treatment used in psychiatry that involves talking with a mental health professional to help identify and manage mental health issues.'], 7, ['["Social media is used by over 3 billion people worldwide.",', '"Facebook is the most popular social media platform with over 2.5 billion users.",', '"Twitter has over 330 million active users every month."]'], 24, ["['The first human civilization appeared in Mesopotamia around 3500 BC.',", " 'The Roman Empire was one of the largest and most influential empires in world history.',", " 'The Industrial Revolution began in the late 18th century and changed the way people lived and worked.']"]]
    else:
        fact_list = getfacts(zuverwendendezeilen,sorted_gptarray)
    writetomaindatabase(fact_list)



config = Config('GPT')
module = str(config.getvalue('module'))
time = str(config.getvalue('time'))
videocount = int(config.getothervalue('UPLOAD', 'count'))
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
discord_logger = Discord_logger()
openaiorganization = str(config.getvalue('openaiorganization'))
openaiapi_key = str(config.getvalue('openaiapi_key'))
factcount = str(config.getvalue('factcount'))
testmode = bool(config.getvalue('testmode'))


configloader()

schedule.every().day.at(time).do(main)

#threadstarter() #zum test ausgeblendet
main()
