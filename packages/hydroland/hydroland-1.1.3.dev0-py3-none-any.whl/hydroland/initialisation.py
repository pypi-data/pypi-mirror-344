#!/usr/bin/env python3
import argparse
import glob
import os
import logging
import sys
import shutil
from typing import List, Optional

from hydroland.mhm_setup import create_header, create_nml, create_output_nml, create_parameter_nml


# Initialize logging
logger = logging.getLogger(__name__)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parses command-line arguments for the Hydroland initialisation.

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
            "Cleanup previous outputs, prepare directories, generate configuration files, "
            "and link restart files for Hydroland MHM/MRM runs. "
            "If a restart file exists for --previous_date, the run resumes from that date; "
            "otherwise, initial files from --init_files are used."
        )
    )
    parser.add_argument(
        "--ini_date",
        help="Initialization date for restart files (YYYYMMDD)",
        required=True,
    )
    parser.add_argument(
        "--end_date",
        help="End date for output files (YYYYMMDD)",
        required=True,
    )
    parser.add_argument(
        "--previous_date",
        help="Date of previous run for restart lookup (YYYYMMDD)",
    )
    parser.add_argument(
        "--stat_freq",
        choices=["daily", "hourly"],
        help="Frequency of model output statistics",
        default="daily",
    )
    parser.add_argument(
        "--init_files",
        help="Directory containing initial restart files",
        required=True,
    )
    parser.add_argument(
        "--app_outpath",
        help="Base directory for application outputs",
        required=True,
    )
    parser.add_argument(
        "--resolution",
        required=True,
        type=int,
        choices=[0.1, 0.05],
        help="Spatial resolution.",
    )
    parser.add_argument(
        "--current_mhm_dir",
        help="Current run directory for MHM",
        required=True,
    )
    parser.add_argument(
        "--forcings_dir",
        help="Directory to store forcing files",
        required=True,
    )
    parser.add_argument(
        "--mhm_restart_dir",
        help="Directory for MHM restart files",
        required=True,
    )
    parser.add_argument(
        "--current_mrm_dir",
        help="Current run directory for MRM",
        required=True,
    )
    parser.add_argument(
        "--mrm_restart_dir",
        help="Directory for MRM restart files",
        required=True,
    )
    return parser.parse_args(argv)


def ensure_removed(path: str) -> None:
    """
    Ensure that the given path is removed, unlinking if it's a symlink or deleting if it's a file.

    Parameters
    ----------
    path : str
        File or symlink path to remove.
    """
    # Remove symlinks or regular files
    if os.path.islink(path) or os.path.isfile(path):
        os.remove(path)
    # Remove directories (with all their contents)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def link_force(src: str, dst: str) -> None:
    """
    Create or overwrite a symlink from src to dst.

    Parameters
    ----------
    src : str
        Source file path for the symlink.
    dst : str
        Destination path of the symlink.
    """
    ensure_removed(dst)
    os.symlink(src, dst)


def remove_matching_files(patterns: List[str]) -> None:
    """
    Remove all files or directories matching any of the given glob patterns.
    """
    for pattern in patterns:
        # iglob with recursive=True honors "**" in your patterns
        for filepath in glob.iglob(pattern, recursive=True):
            try:
                # if it's a file or symlink, remove it
                if os.path.islink(filepath) or os.path.isfile(filepath):
                    os.remove(filepath)
                # if it's a directory, remove it and all its contents
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                logger.debug(f"Removed {filepath}")
            except FileNotFoundError:
                # already gone
                continue
            except Exception as e:
                logger.error(f"Error removing {filepath}: {e}")
                sys.exit(1)


def start_initialisation(
    ini_date: str,
    end_date: str,
    previous_date: str,
    stat_freq: str,
    init_files: str,
    app_outpath: str,
    resolution: int,
    current_mhm_dir: str,
    forcings_dir: str,
    mhm_restart_dir: str,
    current_mrm_dir: str,
    mrm_restart_dir: str,
) -> None:
    """
    Main execution function for cleaning previous outputs, preparing directories,
    generating configuration files, and handling restart file linking for Hydroland runs.
    """
    # Always clear out previous-model outputs to avoid stale data
    common_patterns = [
        f"{current_mhm_dir}/*.nc",
        f"{current_mhm_dir}/output/*.nc",
        f"{current_mrm_dir}/*.nc",
        f"{current_mrm_dir}/run_parallel_mrm.sh",
        f"{current_mrm_dir}/parallel_mrm.py",
        f"{current_mrm_dir}/subdomain_*",
    ]
    remove_matching_files(common_patterns)

    previous_re_file = os.path.join(mhm_restart_dir, f"{previous_date}_mHM_restart.nc")
    current_re_file = os.path.join(
        current_mhm_dir, "input", "restart", f"{ini_date}_mHM_restart.nc"
    )

    if not os.path.exists(previous_re_file):
        logger.debug(f"No {previous_re_file=} found, runing Hydroland cold start.")
        # First time through: cold start
        cold_patterns = [
            os.path.join(forcings_dir, f"mHM_{ini_date}_to_{end_date}_*.nc"),
            os.path.join(current_mhm_dir, "input", "restart", "*.nc"),
        ]
        remove_matching_files(cold_patterns)

        for i in range(1, 54):
            rm = os.path.join(
                current_mrm_dir, f"subdomain_{i}", f"{ini_date}_mRM_restart.nc"
            )
            if os.path.exists(rm):
                os.remove(rm)

        # Create necessary directories for MHM/MRM
        sub_mrm_logs = [
            os.path.join(app_outpath, "hydroland", "mrm", "log_files", f"subdomain_{i}")
            for i in range(1, 54)
        ]
        sub_mrm_restarts = [
            os.path.join(
                app_outpath, "hydroland", "mrm", "restart_files", f"subdomain_{i}"
            )
            for i in range(1, 54)
        ]
        dirs = [
            forcings_dir,
            os.path.join(app_outpath, "hydroland", "mhm", "log_files"),
            os.path.join(app_outpath, "hydroland", "mhm", "restart_files"),
            os.path.join(
                app_outpath, "hydroland", "mhm", "current_run", "input", "meteo"
            ),
            os.path.join(
                app_outpath, "hydroland", "mhm", "current_run", "input", "restart"
            ),
            os.path.join(app_outpath, "hydroland", "mhm", "current_run", "output"),
            os.path.join(app_outpath, "hydroland", "mhm", "fluxes"),
            *sub_mrm_logs,
            *sub_mrm_restarts,
            os.path.join(app_outpath, "hydroland", "mrm", "current_run"),
            os.path.join(app_outpath, "hydroland", "mrm", "fluxes"),
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)

        # Generate configuration files via provided scripts
        header_dir = os.path.join(current_mhm_dir, "input", "meteo")
        create_header(out_dir=header_dir, resolution=resolution)
        create_parameter_nml(out_dir=current_mhm_dir)
        create_output_nml(out_dir=current_mhm_dir)
        create_nml(out_dir=current_mhm_dir)

        # Adjust STAT_FREQ if hourly
        if stat_freq == "hourly":
            nml_file = os.path.join(current_mhm_dir, "mhm_outputs.nml")
            with open(nml_file, "r+") as f:
                text = f.read().replace(
                    "timeStep_model_outputs = -1", "timeStep_model_outputs = 1"
                )
                f.seek(0)
                f.write(text)
                f.truncate()

        # Copy and link initial restart files for cold start
        init_mhm_src = os.path.join(
            init_files, "mhm", "restart_files", f"mHM_restart_{resolution}.nc"
        )
        first_restart_file = os.path.join(mhm_restart_dir, f"{ini_date}_mHM_restart.nc")
        shutil.copy(init_mhm_src, first_restart_file)
        link_force(first_restart_file, current_re_file)

        for i in range(1, 54):
            src = os.path.join(
                init_files,
                "mrm",
                "restart_files",
                f"subdomain_{i}",
                f"mRM_restart_{resolution}.nc",
            )
            dst = os.path.join(
                mrm_restart_dir, f"subdomain_{i}", f"{ini_date}_mRM_restart.nc"
            )
            link_force(src, dst)

    else:
        # Subsequent runs: warm start
        logger.debug(f"{previous_re_file=} found, runing Hydroland warm start.")
        link_force(
            os.path.join(mhm_restart_dir, f"{ini_date}_mHM_restart.nc"), current_re_file
        )
