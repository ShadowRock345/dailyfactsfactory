from logger import Logger
from database import Database
from logger import Config
from discord_logger import Discord_logger
from moviepy.editor import *
import time as pytime
import os
import ast
import datetime
import random
from pydub import AudioSegment
import numpy as np
from mutagen.mp3 import MP3
import glob
from pydub import AudioSegment

global codecr, font_path, video_info_parsed, stockvideo, stockmusic, channelname, video_infos,tts_path,module,video_pause_time, fact_count

def realtime():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def get_mp3_length(file_path):
    audio = MP3(file_path)
    return audio.info.length

def all_matching_tts_files(tts_path,id):
    pattern = tts_path + '/' + str(id) + '_*'
    files = glob.glob(pattern)
    files.sort()
    return files

def get_audio_length():
    global video_info_parsed,tts_path,module,video_pause_time
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
        music.append(video_pause_time)
        music_files_sorted.append(intro)
        music_files_sorted.append('FILLER')

        if intro in matching_files:
            matching_files.remove(intro)

        for file in matching_files:
            factlength = get_mp3_length(file)
            music.append(factlength)
            music.append(video_pause_time)
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

def create_complete_sound():
    global video_infos, video_info_parsed, stockmusic

    audio_files = video_infos[1]
    timings = video_infos[0]

    if os.path.exists("createdaudio/" +  str(video_info_parsed[0]) + "_99.mp3"):
        os.remove("createdaudio/" +  str(video_info_parsed[0]) + "_99.mp3")

    timings_array = np.array(timings) * 1000
    stock_music = AudioSegment.from_file(str(stockmusic))
    final_audio = AudioSegment.empty()
    start_times = []
    start_times.append(0)
    i = 0
    times_added_up = 0
    while i < len(timings):

        times_added_up = times_added_up + timings_array[i]
        start_times.append(times_added_up)
        i += 1
    #print(start_times)
    final_audio = AudioSegment.empty()

    start_times_array = np.array(start_times)
    audio_files_array = np.array(audio_files)

    x = 0
    while x < len(audio_files):
        audiofile = audio_files_array[x]
        if audiofile != 'FILLER':
            audio = AudioSegment.from_file(audiofile)
            start_time = int(start_times_array[x]/1000)
            print('start time: ' + str(start_time))
            audio = audio[start_time:]
            final_audio += audio
        else:
            break_duration = timings_array[x]
            print('pause, duration: ' + str(break_duration))
            silent_segment = AudioSegment.silent(duration=break_duration)
            final_audio += silent_segment
        x += 1

    final_audio_duration = len(final_audio)
    stock_music_cut = stock_music[:final_audio_duration]
    stock_music_cut = stock_music_cut.fade_in(2000).fade_out(4000)
    final_audio_with_music = final_audio.overlay(stock_music_cut - 20)
    output_filename = "createdaudio/" +  str(video_info_parsed[0]) + "_99.mp3"
    final_audio_with_music.export(output_filename, format="mp3")
    total_length = len(final_audio_with_music) / 1000
    video_infos.append(total_length)

def render():
    global codecr, font_path, video_info_parsed, stockvideo, stockmusic, channelname, fact_count

    stock_video_path = str(stockvideo)
    stock_music_path = str(stockmusic)

    create_complete_sound()

    video_clip = VideoFileClip(stock_video_path).set_duration(video_infos[3])
    try:
        audio_clip = AudioFileClip("createdaudio/" + str(video_info_parsed[0]) + "_99.mp3").set_duration(video_infos[3])
    except:
        audio_clip = AudioFileClip(stock_music_path).set_duration(video_infos[2])

    target_width = video_clip.h * 9 // 16
    video_clip = video_clip.crop(x1=(video_clip.w - target_width) / 2, x2=(video_clip.w + target_width) / 2)
    video_clip = video_clip.resize(height=1080)

    channel_name = "@" + str(channelname)
    title = str(fact_count).capitalize() + " Facts \n about " + str(video_info_parsed[2])
    facts = video_info_parsed[1]
    timings = video_infos[0]

    clips = []

    timings_array = np.array(timings) * 1000
    start_times = []
    #start_times.append(0)
    i = 0
    times_added_up = 0
    while i < len(timings):

        times_added_up = times_added_up + timings_array[i]
        start_times.append(times_added_up)
        i += 1
    #print(start_times)

    all_file_names = np.array(video_infos[1])
    start_times_without_pause = []
    x = 0
    while x < len(video_infos[1]):
        file_name = all_file_names[x]
        if file_name != 'FILLER':
            start_times_without_pause.append(start_times[x])
        x += 1

    #print(start_times_without_pause)
    #pytime.sleep(10000000)
    start_times_array = np.array(start_times)

    print(start_times_without_pause)

    # Erstellung der Textclips für die Fakten
    for i in range(len(facts)):
        print(facts[i])
        fact = facts[i]
        start_time = int(start_times_without_pause[i]/1000)
        end_time = int(start_times_without_pause[i + 1]/1000) if i + 1 < len(start_times_without_pause) else video_clip.duration

        break_duration = 1.0

        fact_text = (
            TextClip(fact, fontsize=40, color='white', font=font_path, method='caption', align='center',
                     size=(video_clip.w, None))
            .set_start(start_time)
            .set_end(end_time + break_duration)
            .set_position(('center','center'))
        )

        clips.append(fact_text)

    start_times_without_pause.insert(0,0)

    # Erstellung des Textclips für den Channelnamen und den Titel
    channel_text = TextClip(channel_name, fontsize=20, color='white', font=font_path, method='caption',
                            align='center', size=(video_clip.w, None)).set_duration(video_clip.duration)
    title_text = TextClip(title, fontsize=70, color='white', font=font_path, method='caption', align='center',
                          size=(video_clip.w, None)).set_duration((start_times_without_pause[1]/1000)-1).set_start(0)

    # Erstellung der Hintergrundboxen für den Titel und den Fakt

    title_text = title_text.set_position(('center','center'))

    #title_box = ColorClip(size=(video_clip.w, title_text.h + 100), color=(0, 0, 0), duration=start_times_without_pause[0]).set_position(('center', 'center')).set_start(0).set_end((start_times_without_pause[1]/1000)+3)



    # Positionierung der Textclips in den Hintergrundboxen
    #channel_text = channel_text.set_position(('center', 'center'))
    vertical_offset = 150  
    channel_text = channel_text.set_position(('center', video_clip.h/2 + vertical_offset))

    # Overlay der Textclips und Hintergrundboxen auf dem Video
    video_with_text = CompositeVideoClip([video_clip, channel_text, title_text] + clips)

    # Repeat the video clip in an endless loop with a smooth transition
    loop_duration = video_clip.duration + 1.0  # Add 1 second for smooth transition
    looped_video = concatenate_videoclips([video_with_text.crossfadein(0.5).crossfadeout(1)])

    final_video = looped_video.set_audio(audio_clip)  # Stockmusik mit geringer Lautstärke: .volumex(0.2)

    final_video.write_videofile("videos/" + str(video_info_parsed[0]) + ".mp4", codec=codecr, fps=24)

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
video_pause_time = float(config.getvalue('video_pause_time'))
fact_count = str(config.getothervalue('GPT','factcount'))

main()