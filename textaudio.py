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
    id_list = []
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
                id_list.append(id)
            i += 1
    return facts_to_generate, id_list

def checkaudiofile(file_name_list):
    global module
    files_not_found = []
    error_ids = []
    folder = "/textaudios"
    for file in file_name_list:
        file_path = os.path.join(folder,filename)
        if os.path.exists(file_path):
            printmsg = 'successfully generated tts: ' + str(file_path)
            logger.success(printmsg)
            discord_logger.success(printmsg,module)
        else:
            files_not_found.append(file)
    if len(files_not_found) != 0:
        for element in file_name_list:
            id = str(element)[0]
            printmsg = 'missing tts file: ' + str(element) + ' | id: ' + str(id)
            errorlevel = 3
            logger.error(printmsg,errorlevel)
            discord_logger.error(printmsg,module)
            error_ids.append(id)
    return error_ids

def createaudio(facts_to_generate, id_list):
    global voice
    length_facts_list = len(facts_to_generate)
    file_name_list = []
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
            if fact != '':
                filename = "textaudios/" + str(mainfilename) + '_' + str(x) + '.mp3'
                tts.tts(fact,voice,filename)
                x += 1
                file_name_list.append(filename)
                #print(fact)
                #print(filename)
        x = 0
        filename = "textaudios/" + str(mainfilename) + '_' + str(x) + '.mp3'
        text = 'Daily ' + str(topic) + ' facts!'
        tts.tts(text,voice,filename)
        file_name_list.append(filename)
        #print(text)
    return file_name_list

def write_new_status(error_ids, id_list):
    errorvalue = 0

    if error_ids != []:
        for id in error_ids:
            status = 'error_creating_tts'

            columns_to_update = ['Status']
            values_to_update = [status]
            identifizierung = "ID"
            identifizierung_value = int(id)
            database.update("main", columns_to_update, values_to_update, identifizierung, identifizierung_value)

        ids_in_only_one_list = list(set(id_list)-set(error_ids))

        for id in ids_in_only_one_list:
            status = 'tts_generated'

            columns_to_update = ['Status']
            values_to_update = [status]
            identifizierung = "ID"
            identifizierung_value = int(id)
            database.update("main", columns_to_update, values_to_update, identifizierung, identifizierung_value)

    else:
        status = 'tts_generated'

        columns_to_update = ['Status']
        values_to_update = [status]
        identifizierung = "ID"
        identifizierung_value = int(id)
        database.update("main", columns_to_update, values_to_update, identifizierung, identifizierung_value)


def main():
    values = read_main()
    facts_to_generate, id_list =  parse_new_facts(values)
    if facts_to_generate != []:
        file_name_list = createaudio(facts_to_generate)
        error_ids = checkaudiofile(file_name_list, id_list)
        write_new_status(error_ids, id_list)

discord_logger = Discord_logger()
config = Config('TEXTAUDIO')
module = str(config.getvalue('module'))
schedule.every(5).minutes.do(main)
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
voice = str(config.getvalue('voice'))

#threadstarter() #zum test ausgeblendet
main()

