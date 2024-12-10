from database import Database
from logger import Logger
import schedule
import time as pytime
import threading
from logger import Config
import datetime
import numpy as np
from discord_webhook import DiscordWebhook
import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import pickle
from discord_logger import Discord_logger
import requests

#uploading on different platforms

TOKEN_PATH = 'credentials.pickle'

# Berechtigungsbereiche für die YouTube Data API
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# # Überprüfen, ob Anmeldeinformationen bereits vorhanden sind
# if os.path.exists(TOKEN_PATH):
#     with open(TOKEN_PATH, 'rb') as token:
#         credentials = pickle.load(token)
# else:
#     # Erstellen Sie eine neue Instanz des InstalledAppFlow-Objekts
#     flow = InstalledAppFlow.from_client_secrets_file('secret.json', SCOPES)
#
#     # Führen Sie den Autorisierungsfluss durch
#     credentials = flow.run_local_server(port=0)
#
#     # Speichern Sie die Anmeldeinformationen in der Datei
#     with open(TOKEN_PATH, 'wb') as token:
#         pickle.dump(credentials, token)

# Verwenden Sie die Anmeldeinformationen, um die YouTube API zu initialisieren und Aktionen auszuführen
youtube = build('youtube', 'v3', credentials=credentials)

global module,errorlevel,videos

graph_url = 'https://graph.facebook.com/v17.0'

def upoloadyoutube(video_path, title, description, tags, categoryID, privacy):
    #tags should be a list
    #privacy: public, unlisted, private
    video_path = video_path

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secret.json"

    scopes = ["https://ww.googleapis.com/auth/youtube.upload"]
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)

    youtube = build(api_service_name, api_version, credentials=credentials)

    video_metadata = {
        "snippet": {
            "title": str(title),
            "description": str(description),
            "tags": (tags),
            "categoryId": int(categoryID)
        },
        "status": {
            "privacyStatus": str(privacy)
        }
    }

    request_body = {
        "media_body": MediaFileUpload(video_path),
        "part": "snippet,status"
    }

    response = youtube.videos().insert(body=video_metadata,**request_body).execute()

    video_url = "https://www.youtube.com/shorts/" + response["id"]

    return video_url

def uploadinstagramm(caption='', media_type='', share_to_feed='', thumb_offset='',video_url='',access_token = '',instagram_account_id):
    url = graph_url + instagram_account_id + '/media'
    param = dict()
    param['access_token'] = access_token
    param['caption'] = caption
    param['media_type'] = media_type
    param['share_to_feed'] = share_to_feed
    param['thumb_offset'] = thumb_offset
    param['video_url'] = video_url
    response = requests.post(url,params=param)
    #log response
    reponse = response.json()
    logger.info(str(response))
    discord_logger.success(str(response),"UPLOAD")
    return response

def uploadinstagramm(ig_container_id = '', access_token=''):
    url = graph.url + ig_container_id
    param = {}
    param['access_token'] = access_token
    param['fields'] = 'status_code'
    response = requests.get(url,param=param)
    reponse = response.json()
    logger.info(str(response))
    discord_logger.success(str(response),"UPLOAD")
    return response

def publish_container(creation_id = '',access_token = '',instagram_account_id=''):
    url = graph_url + instagram_account_id + '/media_publish'
    param = dict()
    param['access_token'] = access_token
    param['creation_id'] = creation_id
    response = requests.post(url,params=param)
    response = response.json()
    logger.info(str(response))
    discord_logger.success(str(response),"UPLOAD")
    return response

#1.uploadinstagramm
#2.uploadinstagramm (solange warten bis "status_code": "FINISHED" in antwort, auslesen
#3.publish_container

def configloader():
    realtimevalue = realtime()
    printmsg = 'loading configs: ' + str(module) + '|' + str(count) + '|' + str(database) + '|' + str(logger)
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
    global module,errorlevel,videos
    #path = str("videos/") + str(videos[0]) + str(".mp4")
    #vurl = upoload(path, str(videos[0]), str(videos[0]), ["#shorts","cool"], 21, "unlisted")
    #webhook = DiscordWebhook(url='https://canary.discord.com/api/webhooks/1122554218520264714/PW8FGYZyJRJQ0Y8YBGnYBI1b_Wxh2RaV9SJHzhooVgPhWh_E0zRfJ3xG6TEjnrr8FHnf', content='I am uploading a Video. {realtime()}, {vurl}')
    #response = webhook.execute()
    #videos.pop(0)
    return 0

def main():
    values = readvalues()
    
def calculate_interval():
    # Anzahl der Videos
    num_videos = int(config.getvalue('count'))

    # Tageslaenge in Sekunden
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
count = int(config.getvalue('count'))
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
discord_logger = Discord_logger()

videos = [1,2,3,4,5]

configloader()

schedule_readvalues()

errorlevel = 0

threadstarter()
main()