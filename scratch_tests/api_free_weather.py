#######################################
#
# Created: 04/08/2020
# Author: Medad Newman
#
########################################

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
