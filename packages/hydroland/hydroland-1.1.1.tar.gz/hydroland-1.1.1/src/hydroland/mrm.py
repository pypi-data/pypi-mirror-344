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
    parser = argparse.ArgumentParser(description="Hydroland mRM main script")
    parser.add_argument(
        "--current_mhm_dir",
        help="Directory containing current MHM outputs",
        required=True,
    )
    parser.add_argument(
        "--current_mrm_dir",
        help="Directory to store MRM inputs and outputs",
        required=True,
    )
    parser.add_argument(
        "--mrm_restart_dir", help="Directory for MRM restart files", required=True
    )
    parser.add_argument(
        "--mrm_log_dir", help="Directory for MRM log files", required=True
    )
    parser.add_argument("--ini_date", help="Initial date (YYYY_MM_DD)", required=True)
    parser.add_argument("--end_date", help="End date (YYYY_MM_DD)", required=True)
    parser.add_argument("--next_date", help="Next date (YYYY_MM_DD)", required=True)
    parser.add_argument(
        "--stat_freq",
        choices=["daily", "hourly"],
        help="Statistic frequency",
        required=True,
    )
    parser.add_argument(
        "--init_files", help="Base directory for initial files", required=True
    )
    parser.add_argument(
        "--forcings_dir", help="Directory for forcing files", required=True
    )
    parser.add_argument(
        "--mhm_fluxes_dir", help="Directory of MHM flux outputs", required=True
    )
    parser.add_argument(
        "--mrm_fluxes_dir", help="Directory of MRM flux outputs", required=True
    )
    parser.add_argument(
        "--mhm_out_file", help="Filename of MHM output flux file", required=True
    )
    parser.add_argument(
        "--mrm_out_file", help="Filename of MRM output flux file", required=True
    )
    parser.add_argument(
        "--hydroland_opa",
        help="OPA directory for Hydroland post-processing",
        required=True,
    )
    parser.add_argument(
        "--pre", help="Prefix/variable name for data preparation", required=True
    )
    parser.add_argument(
        "--resolution", help="Routing resolution identifier", required=True
    )
    parser.add_argument(
        "--executable_mrm",
        required=False,
        default="mhm",
        help="Filename and path of the mRM executable (e.g. /path/to/mhm).",
    )
    parser.add_argument(
        "--omp_num_threads",
        required=False,
        default="53",
        help="number of mrm subdomains to be calculated in parallel.",
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


if __name__ == "__main__":
    args = parse_args()
    execute_mrm(
        args.current_mrm_dir,
        args.mrm_restart_dir,
        args.mrm_log_dir,
        args.ini_date,
        args.end_date,
        args.next_date,
        args.stat_freq,
        args.init_files,
        args.forcings_dir,
        args.mhm_fluxes_dir,
        args.mrm_fluxes_dir,
        args.mhm_out_file,
        args.mrm_out_file,
        args.hydroland_opa,
        args.pre,
        args.resolution,
        args.executable_mrm,
    )
