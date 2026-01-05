import pandas as pd

from calc_results import (
    gsee_input_data,
    calc_pv_feed_in_ts,
)


class weather:

    def __init__(self,args):
        self.year = args["year"]
        self.args = args


        df_raw = pd.read_csv(
            args["weather_data"],
            sep=";",
            engine="python",  # tolerant for weird separators
            encoding="utf-8",
        )

        # force numeric int for time columns (no data changes outside these columns)
        for c in ["month", "day", "hour"]:
            df_raw[c] = pd.to_numeric(df_raw[c], errors="raise").astype(int)

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

        # --- take data from 5th column onward (index 4) ---
        df_data = df_raw.iloc[:, 4:].copy()
        df_data.index = dt
        df_data.index.name = "time"

        self.data = df_data

    # add functions

    calc_pv_feed_in_ts = calc_pv_feed_in_ts
