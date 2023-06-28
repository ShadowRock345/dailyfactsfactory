from logger import Config
from discord_webhook import DiscordWebhook
from logger import Logger
import datetime

config = Config('DISCORD')
discord_error_webhook = str(config.getvalue('discord_error_webhook'))
discord_success_webhook = str(config.getvalue('discord_success_webhook'))
discord_new_video_webhook = str(config.getvalue('discord_new_video_webhook'))
discord_analytic_webhook = str(config.getvalue('discord_analytic_webhook'))

class Discord_logger():
    def __ini_(self):
        self.errorlevel = 0

    def realtime():
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')

    def error(self, data):
        try:
            webhook = DiscordWebhook(url=discord_error_webhook, content=f'{self.realtime()}, ' + str(data))
            response = webhook.execute()
        except:
            logger.error(printmsg = 'failed sending discord error webhook',errorlevel)

    def success(self, data):
        try:
            webhook = DiscordWebhook(url=discord_success_webhook, content=f'{self.realtime()}, ' + str(data))
            response = webhook.execute()
        except:
            logger.error(printmsg = 'failed sending discord success webhook',errorlevel)

    def new_video(self, data):
        try:
            webhook = DiscordWebhook(url=discord_new_video_webhook, content=f'{self.realtime()}, ' + str(data))
            response = webhook.execute()
        except:
            logger.error(printmsg = 'failed sending discord new_video webhook',errorlevel)

    def analytic(self, data):
        try:
            webhook = DiscordWebhook(url=discord_analytic_webhook, content=f'{self.realtime()}, ' + str(data))
            response = webhook.execute()
        except:
            logger.error(printmsg = 'failed sending discord analytic webhook',errorlevel)