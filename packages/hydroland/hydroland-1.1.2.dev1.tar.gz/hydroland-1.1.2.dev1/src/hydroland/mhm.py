#!/usr/bin/env python3
import argparse
import os
import logging
import shutil
import subprocess
import sys
from typing import List, Optional

from hydroland.data_preparation import prepare_data
from hydroland.mhm_setup import update_mhm_nml


# Initialize logging
logger = logging.getLogger(__name__)


def symlink_force(src: str, dest: str) -> None:
    """
    Create a symlink at `dest` pointing to `src`, removing any existing file or link.

    Parameters
    ----------
    src : str
        Source file path to link from.
    dest : str
        Destination path where the symlink will be created.
    """
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.islink(dest) or os.path.exists(dest):
            os.remove(dest)
        os.symlink(src, dest)
    except OSError as e:
        logger.error(f"Error creating symlink {dest} -> {src}: {e}")
        sys.exit(1)


def move_force(src: str, dest: str) -> None:
    """
    Move `src` to `dest`, creating parent directories if needed and overwriting existing files.

    Parameters
    ----------
    src : str
        Source file path to move.
    dest : str
        Destination path where the file will be moved.
    """
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(dest):
            os.remove(dest)
        shutil.move(src, dest)
    except Exception as e:
        logger.error(f"Error moving {src} to {dest}: {e}")
        sys.exit(1)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parses command-line arguments for the mHM run script.

    Parameters
    ----------
    argv : Optional[List[str]]
        List of command-line arguments to parse (defaults to None, which uses sys.argv).

    Returns
    -------
    argparse.Namespace
        Parsed arguments namespace with all required options.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Configure and execute mHM."
        )
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
        "--current_mhm_dir",
        required=True,
        help="Directory for current mHM run inputs and outputs.",
    )
    parser.add_argument(
        "--forcings_dir",
        required=True,
        help="Directory containing mHM forcing files.",
    )
    parser.add_argument(
        "--mhm_log_dir",
        required=True,
        help="Directory for mHM log files.",
    )
    parser.add_argument(
        "--mhm_fluxes_dir",
        required=True,
        help="Directory to save processed mHM flux outputs.",
    )
    parser.add_argument(
        "--mhm_restart_dir",
        required=True,
        help="Directory for mHM restart files.",
    )
    parser.add_argument(
        "--hydroland_opa",
        required=True,
        help="Path to Hydroland OPA output directory.",
    )
    parser.add_argument(
        "--pre",
        required=True,
        help="Variable name for precipitation data.",
    )
    parser.add_argument(
        "--stat_freq",
        required=True,
        choices=["daily", "hourly"],
        help="Statistical frequency (daily or hourly).",
    )
    parser.add_argument(
        "--mhm_out_file",
        required=True,
        help="Output filename for processed mHM flux data.",
    )
    parser.add_argument(
        "--executable_mhm",
        default="mhm",
        help="Path to the mHM executable (default: 'mhm').",
    )

    return parser.parse_args(argv)


def execute_mhm(
    ini_date: str,
    end_date: str,
    next_date: str,
    current_mhm_dir: str,
    forcings_dir: str,
    mhm_log_dir: str,
    mhm_fluxes_dir: str,
    mhm_restart_dir: str,
    hydroland_opa: str,
    pre: str,
    stat_freq: str,
    mhm_out_file: str,
    executable_mhm: str,
) -> None:
    """
    Executes mHM including setup, execution, restart handling, and data preparation for next mHM execution.
    """
    # Update the mHM namelist
    logger.debug(f"Updating mhm name list.")
    update_mhm_nml(
        start_date=ini_date,
        end_date=end_date,
        next_date=next_date,
        mhm_nml=os.path.join(current_mhm_dir, "mhm.nml"),
    )

    # Use high thread count
    os.environ["OMP_NUM_THREADS"] = "640"

    # Link meteorological forcings
    for var in ("pre", "tavg", "pet"):
        src = os.path.join(forcings_dir, f"mHM_{ini_date}_to_{end_date}_{var}.nc")
        dest = os.path.join(current_mhm_dir, "input", "meteo", f"{var}.nc")
        symlink_force(src, dest)

    # Execute mHM and capture logs
    logger.debug(f"Executing mHM.")
    log_file = os.path.join(mhm_log_dir, f"mhm_{ini_date}_to_{end_date}.log")
    with open(log_file, "w") as lf:
        ret = subprocess.run(
            [executable_mhm, current_mhm_dir], stdout=lf, stderr=subprocess.STDOUT
        )
    if ret.returncode != 0:
        logger.error(f"mhm failed (see {log_file}) with exit code {ret.returncode}")
        sys.exit(1)

    # Move and link restart file for next run
    src_restart = os.path.join(current_mhm_dir, "output", f"{next_date}_mHM_restart.nc")
    dst_restart = os.path.join(mhm_restart_dir, f"{next_date}_mHM_restart.nc")
    move_force(src_restart, dst_restart)

    next_input = os.path.join(
        current_mhm_dir, "input", "restart", f"{next_date}_mHM_restart.nc"
    )
    symlink_force(dst_restart, next_input)

    # Prepare final flux outputs with DGOV data
    prepare_data(
        in_dir=hydroland_opa,
        out_dir=mhm_fluxes_dir,
        out_file=mhm_out_file,
        stat_freq=stat_freq,
        var=pre,
        add_DGOV_data=True,
        current_ini_date=ini_date,
        current_end_date=end_date,
        in_hydroland_dir=os.path.join(current_mhm_dir, "output"),
    )
