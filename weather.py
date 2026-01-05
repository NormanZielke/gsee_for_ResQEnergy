import pandas as pd

from calc_results import (
    calc_pv_feed_in_ts,
)


class Weather:
    """
    Weather data container and helper methods.

    This class reads a semicolon-separated weather file (e.g. artificial or measured data),
    constructs a DatetimeIndex from month/day/hour columns, and stores the remaining columns
    as a time-indexed DataFrame in `self.data`.

    Parameters
    ----------
    args : dict
        Configuration dictionary. Required keys:
        - "weather_data" (str): path to the input weather file
        - "year" (int): year used to construct the DatetimeIndex

    Attributes
    ----------
    year : int
        The year used for the DatetimeIndex.
    args : dict
        Raw configuration dictionary.
    data : pandas.DataFrame
        Time-indexed weather data (columns from 5th column onward).
    """

    def __init__(self,args):
        self.year = args["year"]
        self.args = args

        # Read raw file. Using engine="python" for more tolerant parsing of "weird" separators.
        df_raw = pd.read_csv(
            args["weather_data"],
            sep=";",
            engine="python",  # tolerant for weird separators
            encoding="utf-8",
        )

        # Enforce integer time columns to avoid implicit float parsing or string artifacts.
        # If these columns contain invalid values, we want to fail loudly (errors="raise").
        for c in ["month", "day", "hour"]:
            df_raw[c] = pd.to_numeric(df_raw[c], errors="raise").astype(int)

        # Construct a full DatetimeIndex for the chosen year.
        year_series = pd.Series([self.year] * len(df_raw), index=df_raw.index, dtype="int64")

        dt = pd.to_datetime(
            {
                "year": year_series,
                "month": df_raw["month"],
                "day": df_raw["day"],
                "hour": df_raw["hour"],
            },
            errors="raise",
        )

        # Keep only data columns from the 5th column onward (index 4).
        # Assumption: columns 0..3 are meta/time-related; 4 ..end are actual weather variables.
        df_data = df_raw.iloc[:, 4:].copy()
        df_data.index = dt
        df_data.index.name = "time"

        self.data = df_data

    # add functions

    calc_pv_feed_in_ts = calc_pv_feed_in_ts
