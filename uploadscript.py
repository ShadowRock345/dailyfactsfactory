from database import Database
from logger import Logger
import schedule
import time as pytime
import threading
from logger import Config
import datetime
import numpy as np
from discord_webhook import DiscordWebhook

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
    printmsg =  'starting upload timecheck'
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
    webhook = DiscordWebhook(url='https://canary.discord.com/api/webhooks/1122554218520264714/PW8FGYZyJRJQ0Y8YBGnYBI1b_Wxh2RaV9SJHzhooVgPhWh_E0zRfJ3xG6TEjnrr8FHnf', content='I am uploading a Video. {realtime()}')
    response = webhook.execute()
    return 0

def main():
    values = readvalues()
    
def calculate_interval():
    # Anzahl der Videos
    num_videos = int(config.getvalue('count'))

    # Tageslänge in Sekunden
    seconds_in_day = 24 * 60 * 60

    # Zeitintervall basierend auf der Anzahl der Videos berechnen
    interval = seconds_in_day / num_videos

    return interval

def schedule_readvalues():
    interval = calculate_interval()

    # Funktion `readvalues()` entsprechend dem berechneten Zeitintervall in der Schedule einplanen
    schedule.every(interval).seconds.do(readvalues)

config = Config('UPLOAD')
module = str(config.getvalue('module'))
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))

configloader()

schedule_readvalues()

errorlevel = 0

threadstarter()
main()