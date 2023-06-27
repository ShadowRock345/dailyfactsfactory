from logger import logger
from database import Database
from database import Config
from moviepy.editor import *
import time
import os

global font_path

def render(stock_video_path, stock_music_path):
    global font_path

    

    pass

def main():
    print("******Videorenderer******")

config = Config('RENDER')
database = Database(str(config.getvalue('database')))
logger = Logger(str(config.getvalue('logger')))
module = str(config.getvalue('module'))
codec = str(config.getvalue('codec'))
font_path = str(config.getvalue('font_path'))