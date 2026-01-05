from pathlib import Path
import gsee.pv
import pandas as pd


def gsee_input_data(self):
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
    args = self.args

    pv_data_gsee = gsee_input_data(self)

    series_list = []

    for azimut in args["azimut"]:

        pv_feed_ts = gsee.pv.run_model(
            data=pv_data_gsee,
            coords=args["coords"],
            tilt=args["tilt"],
            azim=azimut,
            tracking=0,
            capacity=args["capacity"],  # W (i.e., 1 kWp)
        )

        pv_feed_ts.name = str(azimut)

        series_list.append(pv_feed_ts)

    df_pv_feed_in_ts = pd.concat(series_list, axis=1)

    out_dir = Path(args["output_base_dir"]) / "pv_feed_in"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"pv_feed_in_ts_{args['year']}.csv"
    df_pv_feed_in_ts.to_csv(csv_path)


    return df_pv_feed_in_ts
