#!/usr/bin/env python3
import argparse
import glob
import logging
import sys
import os
from typing import List, Optional

from data_preparation import get_pet, prepare_data


# Initialize logging
logger = logging.getLogger(__name__)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parses command-line arguments for the script.

    Parameters
    ----------
    argv : Optional[List[str]], optional
        List of arguments. Defaults to None for sys.argv.

    Returns
    -------
    argparse.Namespace
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Hydroland → mHM pre‐processing driver"
    )
    parser.add_argument("ini_date", help="Start date (YYYYMMDD)")
    parser.add_argument("end_date", help="End date (YYYYMMDD)")
    parser.add_argument(
        "stat_freq",
        choices=["hourly", "daily"],
        help="Statistic frequency of input data",
    )
    parser.add_argument("temp_var", help="Temperature variable name suffix")
    parser.add_argument("pre_var", help="Precipitation variable name suffix")
    parser.add_argument("forcings_dir", help="Output directory for mHM forcings")
    parser.add_argument(
        "lon_number", type=int, help="Longitude index for PET calculation"
    )
    parser.add_argument("hydroland_opa", help="Directory with raw OPA NetCDF files")

    return parser.parse_args(argv)


def find_file(directory: str, pattern: str) -> Optional[str]:
    """Return the first file matching the glob pattern in directory"""
    full_pattern = os.path.join(directory, pattern)
    matches = glob.glob(full_pattern)
    if not matches:
        return None
    return matches[0]


def preprocess_forcings(
    ini_date: str,
    end_date: str,
    stat_freq: str,
    temp_var: str,
    pre_var: str,
    forcings_dir: str,
    lon_number: int,
    hydroland_opa: str,
) -> None:
    """
    Creates the needed NetCDF forcing files to execute Hydroland
    """
    # build filename patterns for precipitation and temperature
    if stat_freq == "hourly":
        pre_pat = f"{ini_date}_T00*to_{end_date}_T23*{pre_var}_*.nc"
        tavg_pat = f"{ini_date}_T00*to_{end_date}_T23*{temp_var}_*.nc"
    else:
        pre_pat = f"{ini_date}_{pre_var}_timestep_60_daily_*.nc"
        tavg_pat = f"{ini_date}_{temp_var}_timestep_60_daily_*.nc"

    pre_file = find_file(hydroland_opa, pre_pat)
    tavg_file = find_file(hydroland_opa, tavg_pat)
    if pre_file is None:
        logger.error(f"No precipitation file matching {pre_pat}")
        sys.exit(1)
    if tavg_file is None:
        logger.error(f"No temperature file matching {tavg_pat}")
        sys.exit(1)

    out_tavg = f"mHM_{ini_date}_to_{end_date}_tavg.nc"
    out_pre = f"mHM_{ini_date}_to_{end_date}_pre.nc"
    # prepare precipitation and temperature data
    logger.debug("Creating Hydroland precipitation and temperature forcing files.")
    prepare_data(
        in_dir=hydroland_opa,
        in_file=tavg_file,
        out_dir=forcings_dir,
        out_file=out_tavg,
        var=temp_var,
        stat_freq=stat_freq,
    )
    prepare_data(
        in_dir=hydroland_opa,
        in_file=pre_file,
        out_dir=forcings_dir,
        out_file=out_pre,
        var=pre_var,
        stat_freq=stat_freq,
    )

    # estimate Potential Evapotranspiration
    logger.debug("Estimating Hydroland Evapotranspiration forcing file.")
    out_pet = f"mHM_{ini_date}_to_{end_date}_pet.nc"
    get_pet(
        stat_freq=stat_freq,
        in_dir=forcings_dir,
        out_dir=forcings_dir,
        in_file=out_tavg,
        out_file=out_pet,
        lon_number=lon_number,
    )


if __name__ == "__main__":
    args = parse_args()
    preprocess_forcings(
        args.hydroland_dir,
        args.ini_date,
        args.end_date,
        args.stat_freq,
        args.temp_var,
        args.pre_var,
        args.forcings_dir,
        args.lon_number,
        args.hydroland_opa,
    )
