#!/usr/bin/env python3
import argparse
import glob
import logging
import sys
import os
from typing import List, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed

from hydroland.data_preparation import get_pet, prepare_data

# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parses command-line arguments for the Hydroland mHM pre-processing driver.

    Parameters
    ----------
    argv : Optional[List[str]]
        List of command-line arguments to parse (defaults to None, which uses sys.argv).

    Returns
    -------
    argparse.Namespace
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Hydroland mHM pre-processing: perform parallel data preparation for mRM results, "
            " merging all 53 subdomains into one and generated final output file."
        )
    )
    parser.add_argument(
        "ini_date",
        type=str,
        help="Start date for preprocessing (YYYYMMDD).",
        metavar="YYYYMMDD",
    )
    parser.add_argument(
        "end_date",
        type=str,
        help="End date for preprocessing (YYYYMMDD).",
        metavar="YYYYMMDD",
    )
    parser.add_argument(
        "stat_freq",
        choices=["hourly", "daily"],
        help="Statistic frequency of input data (hourly or daily).",
    )
    parser.add_argument(
        "temp_var",
        help="Suffix for temperature variable names in NetCDF files.",
    )
    parser.add_argument(
        "pre_var",
        help="Suffix for precipitation variable names in NetCDF files.",
    )
    parser.add_argument(
        "forcings_dir",
        help="Output directory for generated mHM forcing files.",
    )
    parser.add_argument(
        "lon_number",
        type=int,
        help="Longitude number of cells for PET calculation file.",
    )
    parser.add_argument(
        "hydroland_opa",
        help="Directory containing raw Hydroland OPA NetCDF files.",
    )

    return parser.parse_args(argv)


def find_file(directory: str, pattern: str) -> Optional[str]:
    """Return the first file matching the glob pattern in directory"""
    full_pattern = os.path.join(directory, pattern)
    matches = glob.glob(full_pattern)
    return matches[0] if matches else None


def _prep_data_job(job_args: dict) -> None:
    """Worker wrapper to call prepare_data with a dict of arguments."""
    prepare_data(**job_args)


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
    Creates the needed NetCDF forcing files to execute Hydroland,
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

    # prepare precipitation and temperature data in parallel
    logger.info("Starting parallel preparation of precipitation and temperature data...")
    jobs = [
        {
            "in_dir": hydroland_opa,
            "in_file": tavg_file,
            "out_dir": forcings_dir,
            "out_file": out_tavg,
            "var": temp_var,
            "stat_freq": stat_freq,
        },
        {
            "in_dir": hydroland_opa,
            "in_file": pre_file,
            "out_dir": forcings_dir,
            "out_file": out_pre,
            "var": pre_var,
            "stat_freq": stat_freq,
        },
    ]

    # use two workers to process both jobs concurrently
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(_prep_data_job, j) for j in jobs]
        for f in as_completed(futures):
            try:
                f.result()
            except Exception as e:
                logger.error(f"Error in data preparation task: {e}")
                sys.exit(1)

    # estimate Potential Evapotranspiration
    logger.info("Estimating Hydroland Evapotranspiration forcing file...")
    out_pet = f"mHM_{ini_date}_to_{end_date}_pet.nc"
    get_pet(
        stat_freq=stat_freq,
        in_dir=forcings_dir,
        out_dir=forcings_dir,
        in_file=out_tavg,
        out_file=out_pet,
        lon_number=lon_number,
    )
