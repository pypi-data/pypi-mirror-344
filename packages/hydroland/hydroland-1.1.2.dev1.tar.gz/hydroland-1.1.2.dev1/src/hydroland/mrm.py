#!/usr/bin/env python3
"""
Hydroland mRM driver script translated from Bash to Python,
with dynamic generation of MRM argument list.
"""

import argparse
import os
import logging
import shutil
import stat
from typing import List, Optional

from hydroland.data_preparation import prepare_data
from hydroland.mrm_setup import (
    ParallelRun,
    generate_mrm_arg_list,
    mrm_fluxes_merge,
    write_run_parallel_mrm,
)


# Initialize logging
logger = logging.getLogger(__name__)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parses command-line arguments for the Hydroland MRM main script.

    Parameters
    ----------
    argv : Optional[List[str]]
        List of command-line arguments to parse (defaults to None, which uses sys.argv).

    Returns
    -------
    argparse.Namespace
        Namespace containing all parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Configure and run Hydroland mRM."
        )
    )
    parser.add_argument(
        "--current_mhm_dir",
        required=True,
        help="Directory containing current mHM outputs.",
    )
    parser.add_argument(
        "--current_mrm_dir",
        required=True,
        help="Directory for current mRM run inputs and outputs.",
    )
    parser.add_argument(
        "--mrm_restart_dir",
        required=True,
        help="Directory for mRM restart files.",
    )
    parser.add_argument(
        "--mrm_log_dir",
        required=True,
        help="Directory for mRM log files.",
    )
    parser.add_argument(
        "--ini_date",
        required=True,
        help="Initial date for the run (YYYY_MM_DD).",
    )
    parser.add_argument(
        "--end_date",
        required=True,
        help="End date for the run (YYYY_MM_DD).",
    )
    parser.add_argument(
        "--next_date",
        required=True,
        help="Next date for restart (YYYY_MM_DD).",
    )
    parser.add_argument(
        "--stat_freq",
        required=True,
        choices=["daily", "hourly"],
        help="Statistical frequency for outputs (daily or hourly).",
    )
    parser.add_argument(
        "--init_files",
        required=True,
        help="Base directory for initial files.",
    )
    parser.add_argument(
        "--forcings_dir",
        required=True,
        help="Directory for forcing files.",
    )
    parser.add_argument(
        "--mhm_fluxes_dir",
        required=True,
        help="Directory containing mHM flux outputs.",
    )
    parser.add_argument(
        "--mrm_fluxes_dir",
        required=True,
        help="Directory containing mRM flux outputs.",
    )
    parser.add_argument(
        "--mhm_out_file",
        required=True,
        help="Filename for the mHM output flux file.",
    )
    parser.add_argument(
        "--mrm_out_file",
        required=True,
        help="Filename for the mRM output flux file.",
    )
    parser.add_argument(
        "--hydroland_opa",
        required=True,
        help="Directory for Hydroland OPA post-processing outputs.",
    )
    parser.add_argument(
        "--pre",
        required=True,
        help="Prefix or variable name for data preparation.",
    )
    parser.add_argument(
        "--resolution",
        required=True,
        type=int,
        choices=[0.1, 0.05],
        help="Spatial resolution.",
    )
    parser.add_argument(
        "--executable_mrm",
        default="mrm",
        help="Path to the mRM executable (default: 'mrm').",
    )
    parser.add_argument(
        "--omp_num_threads",
        default=53,
        type=int,
        help="Number of OpenMP threads for parallel mRM subdomains.",
    )

    return parser.parse_args(argv)


def execute_mrm(
    current_mrm_dir: str,
    mrm_restart_dir: str,
    mrm_log_dir: str,
    ini_date: str,
    end_date: str,
    next_date: str,
    stat_freq: str,
    init_files: str,
    forcings_dir: str,
    mhm_fluxes_dir: str,
    mrm_fluxes_dir: str,
    mhm_out_file: str,
    mrm_out_file: str,
    hydroland_opa: str,
    pre: str,
    resolution: str,
    executable_mrm: Optional[str] = "mhm",
    omp_num_threads: Optional[str] = "53",
) -> None:
    """
    Main workflow for Hydroland mRM execution.
    """

    mrm_arg_path = os.path.join(init_files, "mrm", "grdc")
    mrm_network_dir = os.path.join(
        init_files, "mrm", f"subdomain_river_masks_{resolution}"
    )
    mrm_id_gauges_file = os.path.join(init_files, "mrm", "mrm_input")

    arg_list = generate_mrm_arg_list(mrm_arg_path)

    os.environ["OMP_NUM_THREADS"] = omp_num_threads

    # Prepare MHM fluxes
    prepare_data(
        in_dir=mhm_fluxes_dir,
        in_file=mhm_out_file,
        out_dir=current_mrm_dir,
        out_file=mhm_out_file,
        stat_freq=stat_freq,
        mRM=True,
    )

    # Determine MHM output path
    if stat_freq == "daily":
        mhm_outfile = os.path.join(current_mrm_dir, mhm_out_file)
    else:
        mhm_outfile = os.path.join(mhm_fluxes_dir, mhm_out_file)

    ini_year, ini_month, ini_day = ini_date.split("_")
    end_year, end_month, end_day = end_date.split("_")

    write_run_parallel_mrm(
        ini_year,
        ini_month,
        ini_day,
        end_year,
        end_month,
        end_day,
        current_mrm_dir,
        mrm_restart_dir,
        mhm_outfile,
        mrm_network_dir,
        mrm_id_gauges_file,
        stat_freq,
        forcings_dir,
        next_date,
        resolution,
        executable_mrm,
    )

    # making run_parallel_mrm.sh executable
    run_script = os.path.join(current_mrm_dir, "run_parallel_mrm.sh")
    os.chmod(run_script, os.stat(run_script).st_mode | stat.S_IEXEC)

    # executing mRM
    logger.info("Starting mRM parallel subdomain execution...")
    pRun = ParallelRun(
        exe=run_script,
        args_list=arg_list,
        output_dir=current_mrm_dir,
        global_threads=int(os.environ["OMP_NUM_THREADS"]),
        exe_threads="1",
    )
    pRun.run()

    # merge all mRM subdomains
    logger.info("Merging all mRM subdomains into one...")
    mrm_fluxes_merge(
        current_mrm_dir=current_mrm_dir,
        mrm_out_file=mrm_out_file,
    )

    logger.info("Adding DGOV data to mRH output file...")
    prepare_data(
        in_dir=hydroland_opa,
        out_dir=mrm_fluxes_dir,
        out_file=mrm_out_file,
        stat_freq=stat_freq,
        var=pre,
        add_DGOV_data=True,
        mRM=True,
        current_ini_date=ini_date,
        current_end_date=end_date,
        in_hydroland_dir=current_mrm_dir,
    )

    # Move restart files and logs
    for sub_id in range(1, len(arg_list) + 1):
        # --- restart files ---
        src_restart = os.path.join(
            current_mrm_dir, f"subdomain_{sub_id}/output/mRM_restart_{next_date}.nc"
        )
        dst_restart = os.path.join(
            mrm_restart_dir, f"subdomain_{sub_id}/{next_date}_mRM_restart.nc"
        )
        if os.path.exists(dst_restart):
            os.remove(dst_restart)
        shutil.move(src_restart, dst_restart)

        # --- log files ---
        src_log = os.path.join(
            current_mrm_dir, f"subdomain_{sub_id}/mrm_{ini_date}_to_{end_date}.log"
        )
        dst_log_dir = os.path.join(mrm_log_dir, f"subdomain_{sub_id}")
        dst_log_path = os.path.join(dst_log_dir, os.path.basename(src_log))
        # remove existing log if present
        if os.path.exists(dst_log_path):
            os.remove(dst_log_path)
        # now move (will rename into dst_log_dir)
        shutil.move(src_log, dst_log_path)
