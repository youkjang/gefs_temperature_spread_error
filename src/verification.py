"""
Verification utilities for spread-error analysis.
"""

import numpy as np
import xarray as xr


def stack_members(member_arrays):
    """
    Combine a list of member DataArrays into one DataArray with dimension 'member'.
    """
    ens = xr.concat(member_arrays, dim="member")
    ens = ens.assign_coords(member=np.arange(1, len(member_arrays) + 1))

    return ens


def ensemble_mean(ens: xr.DataArray) -> xr.DataArray:
    """
    Compute ensemble mean.
    """
    return ens.mean(dim="member")


def ensemble_spread(ens: xr.DataArray) -> xr.DataArray:
    """
    Compute ensemble spread as standard deviation across members.
    """
    return ens.std(dim="member")


def forecast_error(
    forecast: xr.DataArray,
    analysis: xr.DataArray,
) -> xr.DataArray:
    """
    Compute forecast error.

    Error = ensemble mean forecast - analysis
    """
    forecast, analysis = xr.align(forecast, analysis, join="inner")

    return forecast - analysis


def rmse(error: xr.DataArray) -> float:
    """
    Compute domain-mean RMSE.
    """
    return float(np.sqrt((error ** 2).mean(skipna=True)))


def mean_absolute_error(error: xr.DataArray) -> float:
    """
    Compute domain-mean absolute error.
    """
    return float(np.abs(error).mean(skipna=True))


def domain_mean(da: xr.DataArray) -> float:
    """
    Compute simple spatial mean over available grid points.
    """
    return float(da.mean(skipna=True))


def kelvin_to_celsius(da: xr.DataArray) -> xr.DataArray:
    """
    Convert Kelvin to Celsius.
    """
    out = da - 273.15
    out.attrs["units"] = "degC"

    return out
