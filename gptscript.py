#from database import database
import schedule
import time

def my_function():
    print("Test")

schedule.every().day.at("13:01").do(my_function)

while True:
    schedule.run_pending()
    time.sleep(1)