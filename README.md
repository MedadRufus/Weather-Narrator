# Weather Narrator
 
Its a very busy day. The deadline is approaching. You need to keep track of time. 
You have not had time to leave the building. Time seems to fly and before you know it, evening happens. You had no idea
of what the weather was like outside. You lost track of time. It does not have to be that way!

Make your day better with the Weather Narrator!
At every 15 minutes( 0th, 15th, 30th, 45th minute of each hour), you get a simple notification of the time and weather 
read out to you. No need to switch screens or look it up anywhere.

Stay informed!

I have been using it for the last few hours and it is an interesting experience. While making this application.
The deadline is nearing and Weather Narrator is letting me know!

# How to run
First install any python3 installation in your computer. Note that the program is only tested on *Windows*
Operating System.

Clone the repo to your computer like so:
```bash
git clone https://github.com/MedadRufus/Weather_notifications.git
cd Weather_notifications
```

Then install the python dependencies.
```bash
pip install -r requirements.txt
```


Now to execute the program, run on command line.
```bash
python main.py
```


# Customisations

You can change when you receive notifications each hour. Simply edit `app_config.conf`.
It looks like this by default
```bash
[Times]
# Select which minutes of each hour you want a notification. The list can be
# expanded as required. e.g. [3,5,12,23,57]. Ensure that the values are 0-59 inclusive
minute: [0,15,30,45]

```

Just change the minutes list to the times you want it to chime each hour


# Acknowledgements

Thanks to [MetaWeather.com](MetaWeather.com) for the freely available data api for weather.

# TODO
make the weather location configurable. It is currently set to London,UK by default
