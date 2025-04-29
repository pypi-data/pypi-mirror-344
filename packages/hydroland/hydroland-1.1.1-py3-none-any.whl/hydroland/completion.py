#!/usr/bin/env python3
"""
Script to process dates and optionally delete files except on month boundaries.

Usage:
    cleanup_script.py [--delete-files] INI_DATE PREVIOUS_DATE FORCINGS_DIR MHM_RESTART_DIR MHM_LOG_DIR MRM_RESTART_DIR MRM_LOG_DIR HYDROLAND_OPA

Dates can be in YYYY_MM_DD or YYYY-MM-DD format.
"""

import argparse
import glob
import os
import logging
import re
import shutil
from datetime import datetime, timedelta
from typing import List, Optional, Set


# Initialize logging
logger = logging.getLogger(__name__)


def remove_matching(patterns: List[str], boundary_days: Set[int]) -> None:
    """Helper to glob and remove files/directories skipping boundary dates."""
    # Regex to extract date pattern YYYY_MM_DD
    date_re = re.compile(r"(\d{4})_(\d{2})_(\d{2})")
    for pat in patterns:
        for path in glob.glob(pat):
            basename = os.path.basename(path)
            m = date_re.search(basename)
            if m:
                day = int(m.group(3))
                if day in boundary_days:
                    continue
            # Remove file or directory
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parses command-line arguments for the script.

    Parameters
    ----------
    argv : Optional[List[str]], optional
        List of arguments. Defaults to None to use sys.argv.

    Returns
    -------
    argparse.Namespace
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Process dates and optionally delete files"
    )
    parser.add_argument("ini_date", help="Initial date (YYYY_MM_DD or YYYY-MM-DD)")
    parser.add_argument(
        "previous_date", help="Previous date (YYYY_MM_DD or YYYY-MM-DD)"
    )
    parser.add_argument("forcings_dir", help="Path to forcings directory")
    parser.add_argument("mhm_restart_dir", help="Path to MHM restart directory")
    parser.add_argument("mhm_log_dir", help="Path to MHM log directory")
    parser.add_argument("mrm_restart_dir", help="Path to MRM restart directory")
    parser.add_argument("mrm_log_dir", help="Path to MRM log directory")
    parser.add_argument("hydroland_opa", help="Path to Hydroland OPA directory")
    parser.add_argument(
        "--delete-files",
        action="store_true",
        help="If set, delete logs, restart, and forcing files except at month boundaries",
    )
    return parser.parse_args(argv)


def parse_date(date_str: str) -> datetime:
    """Convert a date string (YYYY_MM_DD or YYYY-MM-DD) to a datetime object."""
    normalized = date_str.replace("_", "-")
    return datetime.strptime(normalized, "%Y-%m-%d")


def cleanup_files(
    ini_date: str,
    previous_date: str,
    forcings_dir: str,
    mhm_restart_dir: str,
    mhm_log_dir: str,
    mrm_restart_dir: str,
    mrm_log_dir: str,
    hydroland_opa: str,
    delete_files: bool = False,
) -> None:
    """
    Perform optional cleanup of files based on date logic.
    """
    ini_dt = parse_date(ini_date)
    prev_dt = parse_date(previous_date)

    print(f"INI_DATE: {ini_dt:%Y-%m-%d}")
    print(f"PREVIOUS_DATE: {prev_dt:%Y-%m-%d}")

    if not delete_files:
        logger.debug("--delete-files not set; no files were removed.")
        return

    year, month, day = prev_dt.year, prev_dt.month, prev_dt.day
    month_str = f"{month:02d}"

    # Compute next month boundary days
    if month == 12:
        first_next = datetime(year + 1, 1, 1)
    else:
        first_next = datetime(year, month + 1, 1)
    last_day = (first_next - timedelta(days=1)).day
    second_last = (first_next - timedelta(days=2)).day
    boundary_days = {1, last_day, second_last}

    # Skip deletion if prev day is a boundary
    if day in boundary_days:
        logger.debug(f"Skipping deletion for boundary date: {prev_dt:%Y-%m-%d}")
        return

    # Build base patterns using prefix YYYY_MM
    prefix = f"{year}_{month_str}"

    # 1) MHM restart files
    patterns = [os.path.join(mhm_restart_dir, f"{prefix}*_mHM_restart.nc")]
    remove_matching(patterns, boundary_days)

    # 2) MHM log files
    patterns = [os.path.join(mhm_log_dir, f"mhm_{prefix}*.log")]
    remove_matching(patterns, boundary_days)

    # 3) Forcing files
    patterns = [os.path.join(forcings_dir, f"*{prefix}*.nc")]
    remove_matching(patterns, boundary_days)

    # 4) Hydroland OPA files/directories
    patterns = [os.path.join(hydroland_opa, f"*{prefix}*")]
    remove_matching(patterns, boundary_days)

    # 5) MRM per-subdomain restart and logs
    mrm_patterns = []
    for i in range(1, 54):
        sub = f"subdomain_{i}"
        mrm_patterns.append(
            os.path.join(mrm_restart_dir, sub, f"{prefix}*_mRM_restart.nc")
        )
        mrm_patterns.append(os.path.join(mrm_log_dir, sub, f"mrm_{prefix}*.log"))
    remove_matching(mrm_patterns, boundary_days)

    logger.info(f"Deleted files for month: {prefix} (excluding boundary days).")


if __name__ == "__main__":
    args = parse_args()
    cleanup_files(
        ini_date=args.ini_date,
        previous_date=args.previous_date,
        forcings_dir=args.forcings_dir,
        mhm_restart_dir=args.mhm_restart_dir,
        mhm_log_dir=args.mhm_log_dir,
        mrm_restart_dir=args.mrm_restart_dir,
        mrm_log_dir=args.mrm_log_dir,
        hydroland_opa=args.hydroland_opa,
        delete_files=args.delete_files,
    )
