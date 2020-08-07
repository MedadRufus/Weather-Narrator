########################################################################################################################
#
# Created: 04/08/2020
# Author: Medad Newman
#
# This app pipes the tone of the weather
# every hour. It marks the passing of time
# with a chime that corresponds to the weather.
# e.g. when there is thunder, it plays thunder sounds
#
# Use case: You are deep inside a building. And you rarely go out. You need to get an idea
# of the weather. This program will wake up and chime the weather, letting you know
# what the weather outside is like!
########################################################################################################################


from logging_utils import setup_logging

# inbuilt dependencies
from datetime import datetime
import time
import os
import sys
import logging

# External dependentcies
from playsound import playsound
import pyttsx3
import schedule
import requests




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


    def check_weather(self):
        conn = requests.get("https://www.metaweather.com/api/location/44418/").json()
        # print(conn)
        # print(conn["consolidated_weather"][0]["weather_state_name"])
        # print(conn["consolidated_weather"][1]["weather_state_name"])
        # print(conn["consolidated_weather"][2]["weather_state_name"])
        # print(conn["consolidated_weather"][3]["weather_state_name"])
        # print(conn["consolidated_weather"][4]["weather_state_name"])

        logging.debug("The weather is :"+conn["consolidated_weather"][0]["weather_state_name"])


        self.play_weather_chime(conn["consolidated_weather"][0]["weather_state_name"])


    def play_weather_chime(self,weather_state_name:str):

        self.speak_text("The time is {} and the weather is {}".format(self.get_time(),weather_state_name))

        if self.play_tunes == True:
            #todo: map the consolidated weather to an audio file.
            if weather_state_name == "Snow":
                self.play_sound("Wind-Mark_DiAngelo-1940285615.mp3") # http://soundbible.com/1810-Wind.html
            elif weather_state_name == "Sleet":
                self.play_sound("Rain_Inside_House-Mark_DiAngelo-323934112.mp3") # http://soundbible.com/2065-Rain-Inside-House.html by Mark DiAngelo
            elif weather_state_name == "Hail":
                self.play_sound("Hailstorm-Mike_Koenig-447872762.mp3") # http://soundbible.com/1718-Hailstorm.html
            elif weather_state_name == "Thunderstorm":
                self.play_sound("thunder_strike_2-Mike_Koenig-2099467696.mp3") # http://soundbible.com/2016-Thunder-Strike-2.html
            elif weather_state_name == "Heavy Rain":
                self.play_sound("heavy-rain-daniel_simon.mp3") # http://soundbible.com/2217-Heavy-Rain-Wind.html by Daniel Simion
            elif weather_state_name == "Light Rain":
                self.play_sound("Rain_Inside_House-Mark_DiAngelo-323934112.mp3") # http://soundbible.com/2065-Rain-Inside-House.html by Mark DiAngelo
            elif weather_state_name == "Showers":
                self.play_sound("Rain_Inside_House-Mark_DiAngelo-323934112.mp3") # http://soundbible.com/2065-Rain-Inside-House.html by Mark DiAngelo
            elif weather_state_name == "Heavy Cloud":
                self.play_sound("Cargo Plane Ambiance-SoundBible.com-1150109206.mp3")  # http://soundbible.com/490-Cargo-Plane-Ambiance.html
            elif weather_state_name == "Light Cloud":
                self.play_sound("Cargo Plane Ambiance-SoundBible.com-1150109206.mp3")  # http://soundbible.com/490-Cargo-Plane-Ambiance.html
            elif weather_state_name == "Clear":
                self.play_sound("Sunny Day-SoundBible.com-2064222612.mp3") # http://soundbible.com/1661-Sunny-Day.html



    def play_sound(self,file:str):
        playsound('audio_files/{}'.format(file))


    def speak_text(self,text:str):
        """
        Use the narrator tool to convert text to audio
        :param text:
        :return:
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

if __name__  == "__main__":
    wa = WeatherApp()

    # chime once at the beginning
    wa.check_weather()

    # create job for the scheduler
    def job():
        wa.check_weather()

    # chime on the 15th minute of each hour
    schedule.every().hour.at(":00").do(job)
    schedule.every().hour.at(":15").do(job)
    schedule.every().hour.at(":30").do(job)
    schedule.every().hour.at(":45").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


