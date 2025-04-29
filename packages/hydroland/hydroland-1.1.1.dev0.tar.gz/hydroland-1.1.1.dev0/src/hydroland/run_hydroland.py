#!/usr/bin/env python3
import argparse
import os
import logging
import sys
from datetime import datetime, timedelta

from completion import cleanup_files
from data_preparation import str2bool
from initialisation import start_initialisation
from mhm import execute_mhm
from mrm import execute_mrm
from preprocessing import preprocess_forcings

# Initialize logging
logger = logging.getLogger(__name__)

# def str2bool(value):
#     """string to Boolean"""
#     if isinstance(value, bool):
#         return value
#     if value.lower() in ("yes", "true", "t", "y", "1"):
#         return True
#     elif value.lower() in ("no", "false", "f", "n", "0"):
#         return False
#     else:
#         logger.error(f"{value=}. Boolean value expected.")
#         sys.exit(1)


def parse_args(argv=None) -> argparse.Namespace:
    """
    Parses command-line arguments for the Hydroland pipeline.

    Parameters
    ----------
    argv : Optional[List[str]]
        List of arguments (defaults to sys.argv if None).

    Returns
    -------
    argparse.Namespace
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Run Hydroland mHM/mRM processing pipeline"
    )

    # Paths
    parser.add_argument(
        "--hydroland-opa", help="OPA directory for Hydroland post-processing"
    )
    parser.add_argument("--init-files", help="Base directory for initial files")
    parser.add_argument("--app-outpath", help="Application output base directory")

    # Date range
    parser.add_argument("--ini-year", help="Initialization year (YYYY)")
    parser.add_argument("--ini-month", help="Initialization month (MM)")
    parser.add_argument("--ini-day", help="Initialization day (DD)")
    parser.add_argument("--end-year", help="End year (YYYY)")
    parser.add_argument("--end-month", help="End month (MM)")
    parser.add_argument("--end-day", help="End day (DD)")

    # Processing options
    parser.add_argument(
        "--stat-freq", choices=["daily", "hourly"], help="Output frequency"
    )
    parser.add_argument("--pre", help="Precipitation variable")
    parser.add_argument("--temp", help="Temperature variable")
    parser.add_argument(
        "--grid", choices=["0.1/0.1", "0.05/0.05"], help="Spatial resolution"
    )
    parser.add_argument(
        "--splitsizeunit",
        choices=["day"],
        default="day",
        help="Split-unit for parallel runs (only 'day' supported)",
    )

    # Executables & threading
    parser.add_argument("--executable-mhm", default="mhm", help="Path to mHM binary")
    parser.add_argument("--executable-mrm", default="mrm", help="Path to mRM binary")
    parser.add_argument(
        "--omp-num-threads", default="53", help="Number of threads for mRM"
    )

    # Cleanup
    parser.add_argument(
        "--delete-files",
        type=str2bool,
        const=False,
        default=False,
        nargs="?",
        help="Whether to delete intermediate files",
    )

    args = parser.parse_args(argv)

    return args


def run_hydroland(
    hydroland_opa: str,
    init_files: str,
    app_outpath: str,
    ini_year: str,
    ini_month: str,
    ini_day: str,
    end_year: str,
    end_month: str,
    end_day: str,
    stat_freq: str,
    pre: str,
    temp: str,
    grid: str,
    splitsizeunit: str,
    executable_mhm: str,
    executable_mrm: str,
    omp_num_threads: str,
    delete_files: bool,
):
    """
    Executes the full Hydroland pipeline.
    """
    # Build out directories
    current_mhm_dir = os.path.join(app_outpath, "hydroland", "mhm", "current_run")
    mhm_log_dir = os.path.join(app_outpath, "hydroland", "mhm", "log_files")
    mhm_restart_dir = os.path.join(app_outpath, "hydroland", "mhm", "restart_files")
    mhm_fluxes_dir = os.path.join(app_outpath, "hydroland", "mhm", "fluxes")
    forcings_dir = os.path.join(app_outpath, "hydroland", "forcings")
    current_mrm_dir = os.path.join(app_outpath, "hydroland", "mrm", "current_run")
    mrm_log_dir = os.path.join(app_outpath, "hydroland", "mrm", "log_files")
    mrm_restart_dir = os.path.join(app_outpath, "hydroland", "mrm", "restart_files")
    mrm_fluxes_dir = os.path.join(app_outpath, "hydroland", "mrm", "fluxes")

    # Validate split unit
    if splitsizeunit != "day":
        logger.error(f"Error: Invalid SPLITSIZEUNIT '{splitsizeunit}'. Only 'day' supported.")
        sys.exit(1)

    # Parse grid
    if grid == "0.1/0.1":
        resolution = 0.1
        lon_number = 3600
    else:
        resolution = 0.05
        lon_number = 7200

    # Build dates
    ini_dt = datetime.strptime(f"{ini_year}-{ini_month}-{ini_day}", "%Y-%m-%d")
    end_dt = datetime.strptime(f"{end_year}-{end_month}-{end_day}", "%Y-%m-%d")

    ini_date = ini_dt.strftime("%Y_%m_%d")
    end_date = end_dt.strftime("%Y_%m_%d")
    previous_date = (ini_dt - timedelta(days=1)).strftime("%Y_%m_%d")
    next_date = (end_dt + timedelta(days=1)).strftime("%Y_%m_%d")

    # Output filenames
    if stat_freq == "hourly":
        mhm_out_file = f"{ini_date}_T00_00_to_{end_date}_T23_00_mHM_Fluxes_States.nc"
        mrm_out_file = f"{ini_date}_T00_00_to_{end_date}_T23_00_mRM_Fluxes_States.nc"
    else:
        mhm_out_file = f"{ini_date}_mHM_Fluxes_States.nc"
        mrm_out_file = f"{ini_date}_mRM_Fluxes_States.nc"

    # initialization
    logger.info("Starting Hydroland set-up files for current time-step.")
    start_initialisation(
        ini_date=ini_date,
        end_date=end_date,
        previous_date=previous_date,
        stat_freq=stat_freq,
        init_files=init_files,
        app_outpath=app_outpath,
        resolution=resolution,
        current_mhm_dir=current_mhm_dir,
        forcings_dir=forcings_dir,
        mhm_restart_dir=mhm_restart_dir,
        current_mrm_dir=current_mrm_dir,
        mrm_restart_dir=mrm_restart_dir,
    )

    # preprocess forcings
    logger.info("Processing Hydroland forcing files.")
    preprocess_forcings(
        ini_date=ini_date,
        end_date=end_date,
        stat_freq=stat_freq,
        temp_var=temp,
        pre_var=pre,
        forcings_dir=forcings_dir,
        lon_number=lon_number,
        hydroland_opa=hydroland_opa,
    )

    # run mHM
    logger.info("Executing mHM.")
    execute_mhm(
        ini_date=ini_date,
        end_date=end_date,
        next_date=next_date,
        current_mhm_dir=current_mhm_dir,
        forcings_dir=forcings_dir,
        mhm_log_dir=mhm_log_dir,
        mhm_fluxes_dir=mhm_fluxes_dir,
        mhm_restart_dir=mhm_restart_dir,
        hydroland_opa=hydroland_opa,
        pre=pre,
        stat_freq=stat_freq,
        mhm_out_file=mhm_out_file,
        executable_mhm=executable_mhm,
    )

    # run mRM
    logger.info("Executing mRM.")
    execute_mrm(
        current_mrm_dir=current_mrm_dir,
        mrm_restart_dir=mrm_restart_dir,
        mrm_log_dir=mrm_log_dir,
        ini_date=ini_date,
        end_date=end_date,
        next_date=next_date,
        stat_freq=stat_freq,
        init_files=init_files,
        forcings_dir=forcings_dir,
        mhm_fluxes_dir=mhm_fluxes_dir,
        mrm_fluxes_dir=mrm_fluxes_dir,
        mhm_out_file=mhm_out_file,
        mrm_out_file=mrm_out_file,
        hydroland_opa=hydroland_opa,
        pre=pre,
        resolution=resolution,
        executable_mrm=executable_mrm,
        omp_num_threads=omp_num_threads,
    )

    # cleanup
    logger.info("Cleaning up files and finishing Hydroland executing.")
    cleanup_files(
        ini_date=ini_date,
        previous_date=previous_date,
        forcings_dir=forcings_dir,
        mhm_restart_dir=mhm_restart_dir,
        mhm_log_dir=mhm_log_dir,
        mrm_restart_dir=mrm_restart_dir,
        mrm_log_dir=mrm_log_dir,
        hydroland_opa=hydroland_opa,
        delete_files=delete_files,
    )


if __name__ == "__main__":
    args = parse_args()
    run_hydroland(
        args.hydroland_opa,
        args.init_files,
        args.app_outpath,
        args.ini_year,
        args.ini_month,
        args.ini_day,
        args.end_year,
        args.end_month,
        args.end_day,
        args.stat_freq,
        args.pre,
        args.temp,
        args.grid,
        args.splitsizeunit,
        args.executable_mhm,
        args.executable_mrm,
        args.omp_num_threads,
        args.delete_files,
    )
