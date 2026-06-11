# GEFS Temperature Spread–Error Relationship

This project evaluates the relationship between **GEFS ensemble spread** and **forecast error** for 2-meter temperature over the contiguous United States (CONUS).

The main goal is to examine whether a larger ensemble spread corresponds to a larger forecast error as the forecast lead time increases.

## Project Motivation

Ensemble forecasting is widely used in operational weather prediction because it provides information about forecast uncertainty. However, ensemble spread does not automatically guarantee reliable uncertainty information.

This project provides a simple spread-error diagnostic by comparing:

- GEFS ensemble spread
- GEFS ensemble-mean forecast error
- RMSE against a verifying analysis
- Lead-time dependence of spread and error

This workflow is relevant to operational forecast verification, ensemble model evaluation, and NOAA-style post-processing work.

## Data

### Forecast Data

- Model: NOAA Global Ensemble Forecast System (GEFS)
- Variable: 2-meter temperature
- Ensemble members: GEFS perturbation members
- Forecast lead times: +24 h, +48 h, +72 h, +96 h
- Data source: NOAA public S3 archive

### Verification Data

- Verifying field: GFS analysis
- Variable: 2-meter temperature
- Valid time: matched to each GEFS forecast lead time


## Repository Structure
```text
gefs-temperature-spread-error/
├── README.md
├── pyproject.toml
├── setup.py
├── notebooks/
│   └── 01_gefs_temperature_spread_error.ipynb
├── gefs_spread_error/
│   ├── __init__.py
│   ├── config.py
│   ├── data_access.py
│   ├── verification.py
│   └── plotting.py
└── figures/
```


## AI Use Disclosure
AI assistance was used to help draft and organize portions of the Python workflow and documentation. Scientific choices, code review, testing, and final project decisions were performed by the author.
