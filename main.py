########################################################################################################################
#
# Created: 04/08/2020
# Author: Medad Newman
#
# Use case: You are deep inside a building. And you rarely go out. You need to get an idea
# of the weather. This program will wake up and chime the weather, letting you know
# what the weather outside is like! Also tells you the time
########################################################################################################################


import json
import logging
import os
import sys
import time
from configparser import ConfigParser
# inbuilt dependencies
from datetime import datetime

import pyttsx3
import requests
import schedule
# External dependentcies
from playsound import playsound

from logging_utils import setup_logging


class WeatherApp:

    def __init__(self):
        # Setup logging
        script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        if (not setup_logging(console_log_output="stdout", console_log_level="info", console_log_color=True,
                              logfile_file=script_name + ".log", logfile_log_level="info", logfile_log_color=False,
                              log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
            print("Failed to setup logging, aborting.")

        # setup text to speech engine
        self.engine = pyttsx3.init()
        self.play_tunes = False
        self.city = None
        self.temperature = None

        # now begin the program
        self.run_everything()

    def run_everything(self):
        # read the config file
        parser = ConfigParser()
        parser.read('app_config.conf')
        times = json.loads(parser.get("Times", "minute"))

        # chime once at the beginning
        self.check_weather()

        # create job for the scheduler
        def job():
            self.check_weather()

        # schedule the times
        for minute in times:
            # TODO:assert if time is within 0 to 60
            # chime on the nth minute of each hour
            time_str = ":{:02d}".format(minute)
            logging.info("Time sheduled for " + time_str)
            schedule.every().hour.at(time_str).do(job)

        # sleep wait
        while True:
            schedule.run_pending()
            time.sleep(1)

    def check_weather(self):
        """
        Get weather in London from BBC weather and read it out
        :return:  None
        """
        conn = requests.get("https://www.metaweather.com/api/location/44418/").json()
        print(conn)
        bbc_weather = conn["consolidated_weather"][0]["weather_state_name"]
        temp = conn["consolidated_weather"][0]["the_temp"]
        logging.debug("The weather is :" + bbc_weather)

        self.play_weather_chime(bbc_weather,temp)

    def play_weather_chime(self, weather_state_name: str, temperature):
        """
        Read out weather
        :param weather_state_name:
        :return: None
        """

        self.speak_text("The time is {}, temperature is {:.1f} degrees celcius and the weather is {}".format(self.get_time(),temperature, weather_state_name))

    def play_sound(self, file: str):
        playsound('audio_files/{}'.format(file))

    def speak_text(self, text: str):
        """
        Use the narrator tool to convert text to audio
        :param text:
        :return: None
        """
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()

    def get_time(self):
        """
        Just get the time
        :return: time as aa:bb cc where aa is hour is 12 hour format, bb in minutes, cc is am or pm
        """
        now = datetime.now()
        time_format = '%I:%M %p'
        current_time = now.strftime(time_format)

        logging.info("The current time is {}".format(current_time))
        return current_time


if __name__ == "__main__":
    wa = WeatherApp()
