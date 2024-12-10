from logger import Config
from discord_webhook import DiscordWebhook
from logger import Logger
import datetime

#logging on discord for review of videos

config = Config('DISCORD')
discord_error_webhook = str(config.getvalue('discord_error_webhook'))
discord_success_webhook = str(config.getvalue('discord_success_webhook'))
discord_new_video_webhook = str(config.getvalue('discord_new_video_webhook'))
discord_analytic_webhook = str(config.getvalue('discord_analytic_webhook'))

class Discord_logger():
    def __init__(self):
        self.errorlevel = 0
        self.logger = Logger("discord_logger")

    def realtime(self):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')

    def error(self, data, script):
        try:
            webhook = DiscordWebhook(url=discord_error_webhook, content=f'{self.realtime()}|' + str(script) + '| ' + str(data))
            response = webhook.execute()
        except:
            self.logger.error('failed sending discord error webhook',self.errorlevel)

    def success(self, data, script):
        try:
            webhook = DiscordWebhook(url=discord_success_webhook, content=f'{self.realtime()} |' + str(script) + '| ' + str(data))
            response = webhook.execute()
        except:
            self.logger.error('failed sending discord success webhook',self.errorlevel)

    def new_video(self, data, script):
        try:
            webhook = DiscordWebhook(url=discord_new_video_webhook, content=f'{self.realtime()} |' + str(script) + '| ' + str(data))
            response = webhook.execute()
        except:
            self.logger.error('failed sending discord new_video webhook',self.errorlevel)

    def analytic(self, data, script):
        try:
            webhook = DiscordWebhook(url=discord_analytic_webhook, content=f'{self.realtime()} |' + str(script) + '| ' + str(data))
            response = webhook.execute()
        except:
            self.logger.error('failed sending discord analytic webhook',self.errorlevel)