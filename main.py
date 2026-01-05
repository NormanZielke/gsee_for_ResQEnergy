from weather import weather



args = {
    "weather_data" : "input/try_mean_rcp85.p3.txt", # filepath of artificial or measured input weather data
    "year" : 2050,                                  # year of feed_in_timeseries
    "coords": (52.43, 13.54),                       # coords of pv plant (52.43, 13.54) => Adlershof (Berlin)
    "tilt": 30,                                     # 30 degrees tilt angle
    "azimut" : [90,135,180,225,270],                # chosen azimut values to generate pv feed_in_timeseries [E,SE,S,SW,W]
    "capacity" : 1,                                 # installed pv capacity
    "output_base_dir" : "output",                   # base output dir
}



if __name__ == "__main__":

    weather = weather(args)

    weather.calc_pv_feed_in_ts()
