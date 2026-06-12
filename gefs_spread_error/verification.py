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
    

def rmse(error: xr.DataArray, weighted: bool = True) -> float:
    """
    Compute spatial RMSE.
    """
    squared_error = error ** 2

    if weighted:
        mse = area_weighted_mean(squared_error)
    else:
        mse = domain_mean(squared_error)

    return float(np.sqrt(mse))


def mean_absolute_error(error: xr.DataArray, weighted: bool = True) -> float:
    """
    Compute spatial mean absolute error.
    """
    abs_error = np.abs(error)

    if weighted:
        return area_weighted_mean(abs_error)

    return domain_mean(abs_error)


def domain_mean(da: xr.DataArray) -> float:
    """
    Compute the simple spatial mean over available grid points.
    """
    return float(da.mean(skipna=True))


def kelvin_to_celsius(da: xr.DataArray) -> xr.DataArray:
    """
    Convert Kelvin to Celsius.
    """
    out = da - 273.15
    out.attrs["units"] = "degC"

    return out

def area_weighted_mean(da: xr.DataArray) -> float:
    """
    Compute latitude-weighted spatial mean.

    This is better than a simple average for lat-lon gridded data.
    """
    weights = np.cos(np.deg2rad(da.latitude))

    mean_value = da.weighted(weights).mean(
        ("latitude", "longitude"),
        skipna=True,
    )

    return float(mean_value)

def bias(error: xr.DataArray, weighted: bool = True) -> float:
    """
    Compute spatial mean bias.

    Bias = mean(forecast - analysis)
    """
    if weighted:
        return area_weighted_mean(error)

    return domain_mean(error)

def spread_skill_ratio(spread_mean: float, rmse_value: float) -> float:
    """
    Compute the spread-skill ratio.

    ratio < 1: ensemble spread is smaller than RMSE
    ratio ≈ 1: spread and RMSE are well matched
    ratio > 1: ensemble spread is larger than RMSE
    """
    if rmse_value == 0:
        return np.nan

    return float(spread_mean / rmse_value)
