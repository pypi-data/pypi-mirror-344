import os
import shutil
import subprocess
import pytest
import hydroland.mhm as mhm
from types import SimpleNamespace

# --- symlink_force ---
def test_symlink_force_creates_and_overwrites(monkeypatch, tmp_path):
    calls = []
    src = '/path/src.nc'
    dest = str(tmp_path / 'sub' / 'dest.nc')
    # Track makedirs, exists removal and symlink
    monkeypatch.setattr(os, 'makedirs', lambda p, exist_ok: calls.append(('makedirs', p)))
    monkeypatch.setattr(os.path, 'dirname', lambda p: os.path.split(p)[0])
    monkeypatch.setattr(os.path, 'islink', lambda p: True)
    monkeypatch.setattr(os.path, 'exists', lambda p: True)
    monkeypatch.setattr(os, 'remove', lambda p: calls.append(('remove', p)))
    monkeypatch.setattr(os, 'symlink', lambda s, d: calls.append(('symlink', s, d)))
    mhm.symlink_force(src, dest)
    assert ('makedirs', os.path.dirname(dest)) in calls
    assert ('remove', dest) in calls
    assert ('symlink', src, dest) in calls

def test_symlink_force_oserror(monkeypatch, tmp_path):
    # Simulate OSError to trigger sys.exit
    monkeypatch.setattr(os, 'makedirs', lambda p, exist_ok: None)
    monkeypatch.setenv('TMP', str(tmp_path))
    def bad_symlink(s, d): raise OSError("fail")
    monkeypatch.setattr(os.path, 'dirname', lambda p: os.path.split(p)[0])
    monkeypatch.setattr(os.path, 'islink', lambda p: False)
    monkeypatch.setattr(os.path, 'exists', lambda p: False)
    monkeypatch.setattr(os, 'symlink', bad_symlink)
    with pytest.raises(SystemExit):
        mhm.symlink_force('a', str(tmp_path/'b'))

# --- move_force ---
def test_move_force_success(monkeypatch, tmp_path):
    calls = []
    src = str(tmp_path / 'a.txt')
    dest = str(tmp_path / 'out' / 'b.txt')
    open(src, 'w').close()
    monkeypatch.setattr(os, 'makedirs', lambda p, exist_ok: calls.append(('makedirs', p)))
    monkeypatch.setattr(os.path, 'exists', lambda p: True)
    monkeypatch.setattr(os, 'remove', lambda p: calls.append(('remove', p)))
    monkeypatch.setattr(shutil, 'move', lambda s, d: calls.append(('move', s, d)))
    mhm.move_force(src, dest)
    assert ('makedirs', os.path.dirname(dest)) in calls
    assert ('remove', dest) in calls
    assert ('move', src, dest) in calls

def test_move_force_exception(monkeypatch):
    monkeypatch.setattr(os, 'makedirs', lambda p, exist_ok: None)
    monkeypatch.setattr(os.path, 'exists', lambda p: False)
    def bad_move(s, d): raise Exception("fail")
    monkeypatch.setattr(shutil, 'move', bad_move)
    with pytest.raises(SystemExit):
        mhm.move_force('a', 'b')

# --- parse_args ---
def test_parse_args_required():
    args = mhm.parse_args([
        '--ini_date', '2021_01_01',
        '--end_date', '2021_01_02',
        '--next_date', '2021_01_03',
        '--current_mhm_dir', '/cm',
        '--forcings_dir', '/f',
        '--mhm_log_dir', '/log',
        '--mhm_fluxes_dir', '/flux',
        '--mhm_restart_dir', '/r',
        '--hydroland_opa', '/opa',
        '--pre', 'tp',
        '--stat_freq', 'daily',
        '--mhm_out_file', 'out.nc'
    ])
    assert args.ini_date == '2021_01_01'
    assert args.stat_freq == 'daily'
    assert args.executable_mhm == 'mhm'

# --- execute_mhm ---
@ pytest.fixture
def setup_dirs(tmp_path):
    base = tmp_path
    dirs = {k: str(base / k) for k in (
        'current_mhm_dir', 'forcings_dir', 'mhm_log_dir',
        'mhm_fluxes_dir', 'mhm_restart_dir', 'hydroland_opa'
    )}
    for p in dirs.values(): os.makedirs(p, exist_ok=True)
    return dirs

@ pytest.mark.parametrize('returncode,expect_exit', [(0, False), (1, True)])
def test_execute_mhm_flow(monkeypatch, setup_dirs, tmp_path, returncode, expect_exit):
    dirs = setup_dirs
    # Monkeypatch dependencies
    monkeypatch.setenv('OMP_NUM_THREADS', '')
    monkeypatch.setattr(mhm, 'update_mhm_nml', lambda **kwargs: None)
    calls = {'symlink': [], 'move': [], 'prepare': False}
    monkeypatch.setattr(mhm, 'symlink_force', lambda s, d: calls['symlink'].append((s, d)))
    monkeypatch.setattr(subprocess, 'run', lambda cmd, stdout, stderr: SimpleNamespace(returncode=returncode))
    monkeypatch.setattr(mhm, 'move_force', lambda s, d: calls['move'].append((s, d)))
    monkeypatch.setattr(mhm, 'prepare_data', lambda **kwargs: calls.__setitem__('prepare', True))
    # Run
    params = {
        'ini_date': '20210101', 'end_date': '20210102', 'next_date': '20210103',
        'current_mhm_dir': dirs['current_mhm_dir'], 'forcings_dir': dirs['forcings_dir'],
        'mhm_log_dir': dirs['mhm_log_dir'], 'mhm_fluxes_dir': dirs['mhm_fluxes_dir'],
        'mhm_restart_dir': dirs['mhm_restart_dir'], 'hydroland_opa': dirs['hydroland_opa'],
        'pre': 'tp', 'stat_freq': 'daily', 'mhm_out_file': 'out.nc', 'executable_mhm': 'mhm'
    }
    if expect_exit:
        with pytest.raises(SystemExit):
            mhm.execute_mhm(**params)
    else:
        mhm.execute_mhm(**params)
        # Validate that symlink, move, and prepare_data were invoked
        assert calls['symlink'], "Expected symlink_force calls"
        assert calls['move'], "Expected move_force calls"
        # No exception on returncode 0
