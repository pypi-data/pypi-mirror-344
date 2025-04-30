import glob
import os
import shutil
from datetime import datetime
import pytest

import hydroland.completion as comp

# Helpers for mocking filesystem
class DummyPath:
    def __init__(self, path, is_dir=False):
        self._path = path
        self._is_dir = is_dir
    def __str__(self):
        return self._path
    def __repr__(self):
        return f"DummyPath({self._path!r}, is_dir={self._is_dir})"

@pytest.mark.parametrize("date_str,expected", [
    ("2021_01_15", datetime(2021,1,15)),
    ("2021-12-05", datetime(2021,12,5)),
])
def test_parse_date_variants(date_str, expected):
    parsed = comp.parse_date(date_str)
    assert parsed.year == expected.year
    assert parsed.month == expected.month
    assert parsed.day == expected.day

def test_parse_args_defaults_and_flag():
    args = comp.parse_args([
        "2021-03-01",
        "/forcings",
        "/mhm_restart",
        "/mhm_log",
        "/mrm_restart",
        "/mrm_log",
        "/opa"
    ])
    assert args.previous_date == "2021-03-01"
    assert args.forcings_dir == "/forcings"
    assert not args.delete_files

    args2 = comp.parse_args([
        "2021-03-01",
        "/forcings",
        "/mhm_restart",
        "/mhm_log",
        "/mrm_restart",
        "/mrm_log",
        "/opa",
        "--delete-files"
    ])
    assert args2.delete_files

@pytest.fixture(autouse=True)
def no_real_fs(monkeypatch):
    # Prevent actual filesystem operations
    monkeypatch.setattr(glob, 'glob', lambda pat: [])
    monkeypatch.setattr(os, 'remove', lambda p: None)
    monkeypatch.setattr(shutil, 'rmtree', lambda p: None)

def test_remove_matching_skips_boundary(monkeypatch, tmp_path):
    # Prepare patterns and fake files
    patterns = [str(tmp_path / "2021_03_01_file"), str(tmp_path / "2021_03_15_file"), str(tmp_path / "2021_03_30_file")]
    monkeypatch.setattr(glob, 'glob', lambda pat: patterns)
    calls = []
    monkeypatch.setattr(os, 'remove', lambda p: calls.append(('file', p)))
    monkeypatch.setattr(shutil, 'rmtree', lambda p: calls.append(('dir', p)))
    # Create a dummy file name pattern matcher
    # Assume none are directories
    monkeypatch.setattr(os.path, 'basename', lambda p: os.path.split(p)[1])
    monkeypatch.setattr(os.path, 'isdir', lambda p: False)

    # Boundary days = {1,30,29}
    comp.remove_matching(patterns, boundary_days={1,30,29})
    # Only the day 15 file should be deleted for each input pattern
    assert calls, "Expected at least one removal call"
    assert all(c == ('file', patterns[1]) for c in calls), f"Unexpected calls: {calls}"
    assert len(calls) == len(patterns)

def test_cleanup_files_no_delete(caplog):
    caplog.set_level('DEBUG')
    # Should early exit without removing anything
    comp.cleanup_files(
        previous_date="2021_03_15",
        forcings_dir="/f",
        mhm_restart_dir="/mr",
        mhm_log_dir="/ml",
        mrm_restart_dir="/rr",
        mrm_log_dir="/rl",
        hydroland_opa="/opa",
        delete_files=False
    )
    assert "--delete-files not set" in caplog.text

def test_cleanup_files_on_last_day(monkeypatch):
    # Test that remove_matching is called for month-end
    calls = []
    monkeypatch.setattr(comp, 'remove_matching', lambda pats, bd: calls.append((pats, bd)))

    # Use March 31, 2021
    comp.cleanup_files(
        previous_date="2021_03_31",
        forcings_dir="/f",
        mhm_restart_dir="/mr",
        mhm_log_dir="/ml",
        mrm_restart_dir="/rr",
        mrm_log_dir="/rl",
        hydroland_opa="/opa",
        delete_files=True
    )
    # Should have at least 5 calls (mhm restart, mhm log, forcings, opa, mrm patterns)
    assert len(calls) >= 5
    # Check boundary_days for March (should include 1, 31, 30)
    pats, bd = calls[0]
    assert 1 in bd and 30 in bd and 31 in bd

def test_cleanup_files_not_last_day(monkeypatch, caplog):
    caplog.set_level('INFO')
    # If date not last day, nothing should happen
    # Monkeypatch remove_matching to error if called
    monkeypatch.setattr(comp, 'remove_matching', lambda pats, bd: (_ for _ in ()).throw(Exception("Should not be called")))
    comp.cleanup_files(
        previous_date="2021_03_15",
        forcings_dir="/f",
        mhm_restart_dir="/mr",
        mhm_log_dir="/ml",
        mrm_restart_dir="/rr",
        mrm_log_dir="/rl",
        hydroland_opa="/opa",
        delete_files=True
    )
    # No exception means remove_matching wasn't called
