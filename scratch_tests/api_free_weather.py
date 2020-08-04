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

import json
import requests
from timers import RepeatedTimer, RepeatTimer

def check_weather():
    conn = requests.get("https://www.metaweather.com/api/location/44418/").json()
    print(conn)
    print(conn["consolidated_weather"][0]["weather_state_name"])
    print(conn["consolidated_weather"][1]["weather_state_name"])
    print(conn["consolidated_weather"][2]["weather_state_name"])
    print(conn["consolidated_weather"][3]["weather_state_name"])
    print(conn["consolidated_weather"][4]["weather_state_name"])


if __name__  == "__main__":
    t = RepeatedTimer(3.0, check_weather,daemon=False) # check weather every 60 seconds
    t.start()
