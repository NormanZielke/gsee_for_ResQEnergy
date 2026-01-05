from pathlib import Path
import gsee.pv
import pandas as pd


def gsee_input_data(self):
    """
    Prepare input DataFrame for gsee.pv.run_model().

    Expected columns in `self.data`
    ------------------------------
    - radiation_downwelling : global horizontal irradiance [W/m²]
    - radiation_diffuse     : diffuse irradiance component [W/m²]
    - air_temperature_mean  : ambient temperature [°C] (used by GSEE if provided)

    Returns
    -------
    pandas.DataFrame
        DataFrame indexed by time with columns:
        - global_horizontal
        - diffuse_fraction
        - temperature
    """
    df_data = self.data

    df_data_pv = pd.DataFrame(
        index=df_data.index
    )

    # global horizontal irradiance [W/m²]
    df_data_pv["global_horizontal"] = df_data["radiation_downwelling"]

    # diffuse fraction (raw)
    df_data_pv["diffuse_fraction"] = (
            df_data["radiation_diffuse"] / df_data["radiation_downwelling"]
    )

    # project to physically admissible domain if diffuse_fraction < 0
    df_data_pv.loc[df_data_pv["diffuse_fraction"] < 0, "diffuse_fraction"] = 0.0

    # optional: ambient temperature [°C]
    df_data_pv["temperature"] = df_data["air_temperature_mean"]

    # set diffuse_fraction = 0 where global_horizontal == 0
    mask_zero_ghi = df_data_pv["global_horizontal"] == 0

    df_data_pv.loc[mask_zero_ghi, "diffuse_fraction"] = 0.0

    self.pv_data_gsee = df_data_pv

    return self.pv_data_gsee


def calc_pv_feed_in_ts(self):
    """
    Calculate PV feed-in time series for multiple azimuth angles using GSEE.

    Uses configuration keys from `self.args`:
    - coords (lat, lon)
    - tilt (deg)
    - azimut (list[int]): azimuth angles passed to GSEE as `azim`
    - capacity (float): installed capacity (passed to GSEE, units follow GSEE conventions)
    - output_base_dir (str): base directory for CSV output
    - year (int): used for output filename only

    Returns
    -------
    pandas.DataFrame
        DataFrame with one column per azimuth (string column names),
        indexed by time. Values are PV feed-in from GSEE.
    """
    args = self.args

    pv_data_gsee = gsee_input_data(self)

    series_list = []

    for azim in args["azimut"]:
        # Run GSEE PV model for each azimuth.
        pv_feed_ts = gsee.pv.run_model(
            data=pv_data_gsee,
            coords=args["coords"],
            tilt=args["tilt"],
            azim=azim,
            tracking=0,
            capacity=args["capacity"],  # W (i.e., 1 kWp)
        )

        pv_feed_ts.name = str(azimut)
        series_list.append(pv_feed_ts)

    df_pv_feed_in_ts = pd.concat(series_list, axis=1)

    # save to CSV
    out_dir = Path(args["output_base_dir"]) / "pv_feed_in"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"pv_feed_in_ts_{args['year']}.csv"
    df_pv_feed_in_ts.to_csv(csv_path)

    print(f"df_pv_feed_in_ts successfully saved to: {csv_path}")

    return df_pv_feed_in_ts
