# GSEE_for_ResQEnergy

`GSEE_for_ResQEnergy` is a small helper repository to generate **normalized PV feed-in time series** from weather data
for the location **Berlin Adlershof**.

This repository is a thin wrapper around `GSEE` and focuses on reproducible data preparation, basic raw-data checks,
and standardized CSV outputs. All PV yield calculations are performed by `GSEE`.

Sources used in this repository:

- GSEE repository: https://github.com/renewables-ninja/gsee
- GSEE documentation: https://gsee.readthedocs.io/en/latest/


## Installation

`GSEE` requires **Python 3.7** in this project setup. Two installation options are supported.

### Option 1: Create a dedicated conda environment (recommended)

    conda create -n gsee37 -c conda-forge python=3.7
    conda activate gsee37
    conda install -c conda-forge gsee

### Option 2: Use the provided environment file

An `environment.yaml` is included in this repository. Create the environment via:

    conda env create -f environment.yaml
    conda activate gsee37


## Repository structure and functionality

This repository implements a simple workflow:

1) Read a semicolon-separated weather file and build a consistent time index for the chosen year.

2) Run raw-data sanity checks (e.g. detect `radiation_diffuse < 0`) and report:
   - all affected rows (limited to the radiation columns),
   - the number of affected timesteps,
   - the share of affected timesteps relative to the full time series.

3) Convert the weather data into the input format expected by `gsee.pv.run_model`
   (e.g. `global_horizontal`, `diffuse_fraction`, optional `temperature`).

4) Run `GSEE` PV simulations for predefined configuration parameters (tilt, multiple azimuth angles, capacity).

5) Export the resulting PV feed-in time series to CSV for downstream use.

### Input

The input is a semicolon-separated weather file. The workflow expects time information that can be used to build a
`DatetimeIndex` (month/day/hour) and radiation variables such as:

- `radiation_downwelling` (global horizontal irradiance)
- `radiation_direct`
- `radiation_diffuse`
- optional: `air_temperature_mean`

### Output

PV feed-in time series are written as CSV to:

    output/pv_feed_in/pv_feed_in_ts_<YEAR>.csv


## Documentation

Primary documentation for the underlying PV modeling is provided by GSEE:

- GSEE documentation: https://gsee.readthedocs.io/en/latest/
- GSEE repository: https://github.com/renewables-ninja/gsee


## Citation

GSEE, created by Stefan Pfenninger and Iain Staffell (2016). Long-term patterns of European PV output using 30 years of validated hourly
reanalysis and satellite data. *Energy* 114, pp. 1251-1265. doi: 10.1016/j.energy.2016.08.060
https://doi.org/10.1016/j.energy.2016.08.060


## License

BSD-3-Clause

