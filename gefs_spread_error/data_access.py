"""
Data access utilities for GEFS and GFS GRIB2 files on public NOAA S3.

This version is designed for Google Colab and portfolio demonstration.
It downloads small GRIB2 files locally before opening with cfgrib, because cfgrib
is more reliable with local file paths than anonymous S3 file-like objects.
"""

from pathlib import Path
from datetime import datetime, timedelta

import fsspec
import xarray as xr


def gefs_s3_path(init_date: str, init_hour: str, member: str, fhr: int) -> str:
    """
    Return the NOAA GEFS public S3 path for one member and forecast hour.

    Example:
    s3://noaa-gefs-pds/gefs.20240115/00/atmos/pgrb2sp25/gep01.t00z.pgrb2s.0p25.f024
    """
    return (
        f"s3://noaa-gefs-pds/gefs.{init_date}/{init_hour}/atmos/pgrb2sp25/"
        f"{member}.t{init_hour}z.pgrb2s.0p25.f{fhr:03d}"
    )


def gfs_analysis_s3_path(valid_date: str, valid_hour: str) -> str:
    """
    Return the NOAA GFS public S3 path for a GFS analysis file.

    Example:
    s3://noaa-gfs-bdp-pds/gfs.20240116/00/atmos/gfs.t00z.pgrb2.0p25.f000
    """
    return (
        f"s3://noaa-gfs-bdp-pds/gfs.{valid_date}/{valid_hour}/atmos/"
        f"gfs.t{valid_hour}z.pgrb2.0p25.f000"
    )


def valid_datetime(init_date: str, init_hour: str, fhr: int):
    """
    Return valid datetime for an initialization time plus forecast hour.
    """
    init_dt = datetime.strptime(init_date + init_hour, "%Y%m%d%H")
    return init_dt + timedelta(hours=fhr)


def download_s3_file(s3_path: str, local_path: str, overwrite: bool = False) -> str:
    """
    Download a public S3 file to a local path.
    """
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    if local_path.exists() and not overwrite:
        return str(local_path)

    fs = fsspec.filesystem("s3", anon=True)
    fs.get(s3_path, str(local_path))

    return str(local_path)


def open_t2m_grib(local_file: str, variable: str = "t2m") -> xr.DataArray:
    """
    Open 2-m temperature from a local GRIB2 file using cfgrib.

    Returns
    -------
    xarray.DataArray
        2-m temperature in Kelvin.
    """
    ds = xr.open_dataset(
        local_file,
        engine="cfgrib",
        backend_kwargs={
            "filter_by_keys": {
                "typeOfLevel": "heightAboveGround",
                "level": 2,
            },
            "indexpath": "",
        },
    )

    if variable not in ds:
        raise KeyError(
            f"{variable} not found. Available variables: {list(ds.data_vars)}"
        )

    return ds[variable]


def subset_conus(
    da: xr.DataArray,
    lon_min: float,
    lon_max: float,
    lat_min: float,
    lat_max: float,
) -> xr.DataArray:
    """
    Subset to an approximate CONUS domain.

    GEFS/GFS longitude is usually 0-360.
    Latitude may be descending, so this handles both cases.
    """
    lat = da["latitude"]

    if float(lat[0]) > float(lat[-1]):
        da = da.sel(latitude=slice(lat_max, lat_min))
    else:
        da = da.sel(latitude=slice(lat_min, lat_max))

    da = da.sel(longitude=slice(lon_min, lon_max))

    return da


def load_gefs_member_t2m(
    config,
    member: str,
    fhr: int,
    init_date: str | None = None,
    init_hour: str | None = None,
    cache_dir: str = "data/gefs",
) -> xr.DataArray:
    """
    Download and open one GEFS member 2-m temperature forecast.
    """
    s3_path = gefs_s3_path(
# replaced with init_date,init_hour for multi Initial dates
#        config.init_date,
#        config.init_hour,
        init_date,
        init_hour,
        member,
        fhr,
    )

    local_file = (
        Path(cache_dir)
# replaced with init_date,init_hour for multi Initial dates
#      / config.init_date,
#      /  config.init_hour,
        / init_date
        / init_hour
        / f"{member}_f{fhr:03d}.grib2"
    )

    downloaded = download_s3_file(s3_path, local_file)

    da = open_t2m_grib(downloaded, variable=config.variable)

    da = subset_conus(
        da,
        config.lon_min,
        config.lon_max,
        config.lat_min,
        config.lat_max,
    )

    return da


def load_gfs_analysis_t2m(
    config,
    fhr: int,
    init_date: str | None = None,
    init_hour: str | None = None,
    cache_dir: str = "data/gfs",
) -> xr.DataArray:
    """
    Download and open GFS analysis 2-m temperature valid at GEFS forecast time.
    """

# replaced with init_date,init_hour for multi Initial dates
    
    #vdt = valid_datetime(config.init_date, config.init_hour, fhr)
    vdt = valid_datetime(init_date, init_hour, fhr)

    valid_date = vdt.strftime("%Y%m%d")
    valid_hour = vdt.strftime("%H")

    s3_path = gfs_analysis_s3_path(valid_date, valid_hour)

    local_file = (
        Path(cache_dir)
        / valid_date
        / valid_hour
        / "gfs_analysis_f000.grib2"
    )

    downloaded = download_s3_file(s3_path, local_file)

    da = open_t2m_grib(downloaded, variable=config.variable)

    da = subset_conus(
        da,
        config.lon_min,
        config.lon_max,
        config.lat_min,
        config.lat_max,
    )

    return da
