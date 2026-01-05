
def check_data(self):
    """
    Basic sanity checks for raw radiation data.

    The function performs the following checks:
    - Identifies rows where radiation_diffuse < 0
    - Prints the number of affected rows
    - Prints the share of affected rows relative to the full time series [%]
    - Always limits output to the columns:
      ["radiation_downwelling", "radiation_direct", "radiation_diffuse"]

    Returns
    -------
    None
        Output is written to standard output for inspection/debugging.
    """

    df_data = self.data

    cols = [
        "radiation_downwelling",
        "radiation_direct",
        "radiation_diffuse",
    ]

    # --- basic consistency check ---
    mask_neg = df_data["radiation_diffuse"] < 0

    n_neg = mask_neg.sum()
    n_total = len(df_data)

    share_neg = 100.0 * n_neg / n_total if n_total > 0 else 0.0

    print("=== Radiation diffuse sanity check ===")
    print(f"Total number of timesteps        : {n_total}")
    print(f"radiation_diffuse < 0 timesteps : {n_neg}")
    print(f"Share of negative values        : {share_neg:.3f} %")

    if n_neg > 0:
        print("\nRows with radiation_diffuse < 0:")
        print(df_data.loc[mask_neg, cols])
    else:
        print("\nNo negative radiation_diffuse values found.")














"""
# --- debug check ---

print(df_data.loc[:,["radiation_downwelling","radiation_direct","radiation_diffuse"]].max())
print(df_data.loc[:,["radiation_downwelling","radiation_direct","radiation_diffuse"]].min())

#print(df_data.loc[:,["radiation_downwelling","radiation_direct","radiation_diffuse"]])

print(df_data.loc[df_data["radiation_diffuse"] == -170.9])
print(df_data.loc ["2050-05-03 06:00:00":"2050-05-03 13:00:00",["radiation_downwelling","radiation_direct","radiation_diffuse"]])
print(df_data.loc["2050-05-03 11:00:00",["radiation_downwelling","radiation_direct","radiation_diffuse"]])


cols = ["radiation_downwelling", "radiation_direct", "radiation_diffuse"]

mask_neg = df_data["radiation_diffuse"] < 0

print("Number of negative radiation_diffuse values:", mask_neg.sum())

print("\nRows with negative radiation_diffuse:")
print(df_data.loc[mask_neg, cols])

"""