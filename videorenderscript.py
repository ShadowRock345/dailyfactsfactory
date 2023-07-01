from logger import Logger
from database import Database
from logger import Config
from discord_logger import Discord_logger
from moviepy.editor import *
import time
import os
import ast
import datetime
import random
from pydub import AudioSegment
import numpy as np
from mutagen.mp3 import MP3
import glob

global codecr, font_path, video_info_parsed, stockvideo, stockmusic, channelname, video_infos,tts_path,module

def realtime():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def get_mp3_length(file_path):
    audio = MP3(file_path)
    return audio.info.length

def all_matching_tts_files(tts_path,id):
    pattern = tts_path + '/' + str(id) + '*'
    files = glob.glob(pattern)
    return files

def get_audio_length():
    global video_info_parsed,tts_path,module
    id = video_info_parsed[0]
    music = []
    music_files_sorted = []
    matching_files = all_matching_tts_files(tts_path,id)

    if matching_files == '':
        printmsg = 'no matching tts files were found'
        errorlevel = 3
        logger.error(printmsg,errorlevel)
        discord_logger.error(printmsg,module)
        final_video_lenght = []
    else:
        intro = str(tts_path) + '/' + str(id) + '_0.mp3'
        introlength = get_mp3_length(intro)
        music.append(introlength)
        music.append('0.3')
        music_files_sorted.append(intro)
        music_files_sorted.append('FILLER')

        if intro in matching_files:
            matching_files.remove(intro)

        for file in matching_files:
            factlength = get_mp3_length(file)
            music.append(factlength)
            music.append('0.3')
            music_files_sorted.append(file)
            music_files_sorted.append('FILLER')

        final_video_lenght = 0
        for element in music:
            final_video_lenght = final_video_lenght + float(element)

    return music,music_files_sorted,final_video_lenght

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
                facts_list = array[i,2]
                facts = ast.literal_eval(facts_list)
                topic = array[i,3]
                videoid = array[i,6]
                musicid = array[i,8]
                video_infos.append(id)
                video_infos.append(facts)
                video_infos.append(topic)
                video_infos.append(videoid)
                video_infos.append(musicid)
                return video_infos
            i += 1


def findvideo(videotag:str) -> list[str]:
    global video_infos
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
            if float(row[3]) >= float(video_infos[2]):
                #result = ",".join(map(str, row[0]))
                result = "stockvideo/" + (videotag) + ".mp4"
                results.append(result)
            else:
                result = "stockvideo/default.mp4"
                results.append(result)
    return results

def findmusic(musictag:str) -> list[str]:
    global video_infos
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
            if float(row[3]) >= float(video_infos[2]):
                #result = ",".join(map(str, row[0]))
                result = "stockmusic/" + str(musictag) + ".mp3"
                results.append(result)
            else:
                result = "stockmusic/default.mp3"
                results.append(result)
    return results

def render():
    global codecr, font_path, video_info_parsed, stockvideo, stockmusic, channelname

    stock_video_path = str(stockvideo)
    stock_music_path = str(stockmusic)

    video_clip = VideoFileClip(stock_video_path).set_duration(video_infos[2])
    audio_clip = AudioFileClip(stock_music_path).set_duration(video_infos[2])

    target_width = video_clip.h * 9 // 16
    video_clip = video_clip.crop(x1=(video_clip.w - target_width) / 2, x2=(video_clip.w + target_width) / 2)
    video_clip = video_clip.resize(height=1080)

    channel_name = "@" + str(channelname)
    title = "Fakt"
    fact = "Hier steht der Fakt"

    # Erstellung des Textclips für den Channelnamen und den Titel
    channel_text = TextClip(channel_name, fontsize=20, color='white', font=font_path, method='caption', align='center', size=(video_clip.w, None))
    title_text = TextClip(title, fontsize=70, color='white', font=font_path, method='caption', align='center', size=(video_clip.w, None))

    # Erstellung des Textclips für den Fakt
    fact_text = TextClip(fact, fontsize=40, color='white', font=font_path, method='caption', align='center', size=(video_clip.w, None)).set_duration(6).set_start(4)

    # Erstellung der Hintergrundboxen für den Titel und den Fakt
    title_box = ColorClip(size=(video_clip.w, title_text.h + 100), color=(0, 0, 0), duration=4).set_position(('center', 'center')).set_start(0).set_end(4)

    # Positionierung der Textclips in den Hintergrundboxen
    channel_text = channel_text.set_position(('center', 'center')).set_duration(video_clip.duration)
    title_text = title_text.set_position(('center', 'center')).set_duration(4).set_start(0)
    fact_text = fact_text.set_position(('center', 'bottom'))

    # Overlay der Textclips und Hintergrundboxen auf dem Video
    video_with_text = CompositeVideoClip([video_clip, channel_text, title_box, title_text, fact_text])
    final_video = video_with_text.set_audio(audio_clip.volumex(0.2))  # Stockmusik mit geringer Lautstärke

    for audio_file, timing in zip(video_infos[1], video_infos[0]):
        if audio_file != 'FILLER':
            audio = AudioFileClip(audio_file)
            if timing is not None:
                audio = audio.set_start(timing)
            final_video = final_video.set_audio(final_video.audio.set_duration(audio.duration))
            final_video = final_video.set_audio(audio)

    final_video.write_videofile("videos/"+str(video_info_parsed[0])+".mp4", codec=codecr, fps=24)

    #columns_to_update = ['Laenge','Status']
    #values_to_update = [3, 'video_generated']
    #identifizierung = "ID"
    #identifizierung_value = int(video_info_parsed[0])
    #database.update("main", columns_to_update, values_to_update, identifizierung, identifizierung_value)
    pass

def main():
    global video_info_parsed, stockvideo, stockmusic, video_infos
    video_infos = []
    values = read_main()
    video_info_parsed = parse_new_video(values)
    music,music_files_sorted,final_video_lenght = get_audio_length()
    video_infos.append(music)
    video_infos.append(music_files_sorted)
    video_infos.append(final_video_lenght)
    print(video_infos)
    stockvideo = random.choice(findvideo(str(video_info_parsed[2])))
    stockmusic = random.choice(findmusic(str(video_info_parsed[2])))

    render()

config = Config('RENDER')
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
module = str(config.getvalue('module'))
codecr = str(config.getvalue('codec'))
font_path = str(config.getvalue('font_path'))
discord_logger = Discord_logger()
channelname = str(config.getvalue('channelname'))
tts_path = str(config.getvalue('tts_path'))

main()