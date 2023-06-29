from logger import logger
from database import Database
from database import Config
from moviepy.editor import *
import time
import os
import datetime
import random
from pydub import AudioSegment

global font_path, video_info_parsed, stockvideo, stockmusic

def realtime():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def get_audio_length(file_path):
    audio = AudioSegment.from_file(file_path)
    length_in_seconds = len(audio) / 1000 #Umrechnung von Millisekunden in Sekunden
    return length_in_seconds

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

def parse_new_video(values):
    video_infos = []
    array = np.array(values)
    if len(array) == 0:
        logger.error('main database is empty',errorlevel = 3)
        discord_logger.error('main database is empty',module)
    else:
        seccond_column = array[:, 1]
        i = 0
        for status in seccond_column:
            if status == 'tts_generated':
                id = array[i,0]
                facts = array[i,2]
                topic = array[i,3]
                videoid = array[i,6]
                musicid = array[i,8]
                video_infos.append(id)
                video_infos.append(facts)
                video_infos.append(topic)
                video_infos.append(videoid)
                video_infos.append(musicid)
            i += 1
    return video_infos

def findvideo(videotag:str) -> list[str]:
    database_video = Database("stockvideo")
    errorlevel = 0
    values = 0 # zuerst auf null setzten
    while values == 0:
        database_video.connect() #video Database öffnen
        values = database_video.getvalues()  #video Database Daten auslesen
        realtimevalue = realtime()
        database_video.close() #video Database schließen
        if values == 0:
            printmsg = 'failed to open ' + 'video' + ' database'
            logger.error(printmsg,errorlevel)
            realtimevalue = realtime()
            if errorlevel < 3:
                errorlevel += 1
            else:
                pytime.sleep(120)
                discord_logger.error(printmsg,module)
        else:
            printmsg = 'opening video database'
            logger.success(printmsg)
            discord_logger.success(printmsg,module)
    results = []
    for row in values:
        if videotag in row[1]:
            result = ",".join(map(str, row))
            results.append(result)
    return results

def findmusic(musictag:str) -> list[str]:
    database_video = Database("music")
    errorlevel = 0
    values = 0 # zuerst auf null setzten
    while values == 0:
        database_video.connect() #music Database öffnen
        values = database_video.getvalues()  #music Database Daten auslesen
        realtimevalue = realtime()
        database_video.close() #music Database schließen
        if values == 0:
            printmsg = 'failed to open ' + 'music' + ' database'
            logger.error(printmsg,errorlevel)
            realtimevalue = realtime()
            if errorlevel < 3:
                errorlevel += 1
            else:
                pytime.sleep(120)
                discord_logger.error(printmsg,module)
        else:
            printmsg = 'opening music database'
            logger.success(printmsg)
            discord_logger.success(printmsg,module)
    results = []
    for row in values:
        if musictag in row[1]:
            result = ",".join(map(str, row))
            results.append(result)
    return results

def render(stock_video_path, stock_music_path):
    global font_pathl, video_info_parsed

    
    columns_to_update = ['Laenge','Status']
    values_to_update = [3, 'video_generated']
    identifizierung = "ID"
    identifizierung_value = int(video_info_parsed[0])
    database.update("main", columns_to_update, values_to_update, identifizierung, identifizierung_value)
    pass

def main():
    global video_info_parsed, stockvideo, stockmusic

    values = read_main()
    video_info_parsed = parse_new_video()
    stockvideo = random.choice(findvideo(str(video_info_parsed[2])))
    stockmusic = random.choice(findmusic(str(video_info_parsed[2])))

    

config = Config('RENDER')
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
module = str(config.getvalue('module'))
codec = str(config.getvalue('codec'))
font_path = str(config.getvalue('font_path'))