

"""
Configuration for the GEFS temperature spread-error project.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ProjectConfig:
    # Forecast initialization
    init_date: str = "20240115"   # YYYYMMDD
    init_hour: str = "00"         # HH

    # NEW: multiple initialization dates
    init_dates: List[str] = field(
        default_factory=lambda: [
            "20240105",
            "20240110",
            "20240115",
            "20240120",
            "20240125",
        ]
    )

    # Forecast lead times to verify
    forecast_hours: List[int] = None

    # GEFS perturbation members.
    # Start small in Colab; increase to range(1, 31) later.
    members: List[str] = None

    # CONUS domain
    lon_min: float = 230.0  # 0-360 longitude; 230E = 130W
    lon_max: float = 300.0  # 300E = 60W
    lat_min: float = 20.0
    lat_max: float = 55.0

    # Variable name used by cfgrib for 2-m temperature
    variable: str = "t2m"

    # S3 buckets
    gefs_bucket: str = "noaa-gefs-pds"
    gfs_bucket: str = "noaa-gfs-bdp-pds"

    def __post_init__(self):
        if self.forecast_hours is None:
            self.forecast_hours = [24, 48, 72, 96]

        if self.members is None:
            # For a fast first run, use 10 perturbation members.
            # Later, change to [f"gep{i:02d}" for i in range(1, 31)]
            self.members = [f"gep{i:02d}" for i in range(1, 11)]
