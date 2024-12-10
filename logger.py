#Logger class
import logging
import datetime

#Config class
import configparser

#simple logger written by shadowrock345

class Logger():
    def __init__(self, process):
        self.process = process
        self.logger = logging.getLogger(process)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        
        # Basic Logger
        file_handler = logging.FileHandler('log/FactsBot.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console Logger
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
    def warning(self, message, level):
        log_message = f'[{self.process}] [{self.get_current_time()}] | {message} , Level: {level}'
        self.logger.warning(log_message)
    
    def error(self, message, level):
        log_message = f'[{self.process}] [{self.get_current_time()}] | {message} , Level: {level}'
        self.logger.error(log_message)
    
    def info(self, message):
        log_message = f'[{self.process}] [{self.get_current_time()}] | {message}'
        self.logger.info(log_message)
    
    def success(self, message):
        log_message = f'[{self.process}] [{self.get_current_time()}] | {message}'
        self.logger.info(log_message)
        
    def get_current_time(self):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')

class Config():
    def __init__(self, module):
        self.module = module
        self.config = configparser.ConfigParser()
        self.logger = Logger('logger')
        self.config.read('config/config.ini')
        
    def getvalue(self, value):
        try:
            return self.config[str(self.module)][str(value)]
        except:
            return 'null'
        
    def getothervalue(self, name, value):
        try:
            return self.config[str(name)][str(value)]
        except:
            return 'null'

    def writevalue(self, value, valuetowrite):
        try:
            self.config[str(self.module)][str(value)] = valuetowrite
        except:
            self.logger.warning("Failed to write value to config file by " + str(self.module), 1)
        
        