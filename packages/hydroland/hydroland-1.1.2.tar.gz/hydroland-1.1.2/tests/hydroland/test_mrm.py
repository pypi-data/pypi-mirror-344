import os
import stat
import shutil
import subprocess
import pytest
from types import SimpleNamespace
from hydroland import mrm

# --- Tests for parse_args ---
def test_parse_args_minimal_systemexit():
    # resolution is defined as int but choices are floats: should error on parsing
    argv = [
        '--current_mhm_dir', '/mhm',
        '--current_mrm_dir', '/mrm',
        '--mrm_restart_dir', '/restart',
        '--mrm_log_dir', '/logs',
        '--ini_date', '20210101',
        '--end_date', '20210102',
        '--next_date', '20210103',
        '--stat_freq', 'daily',
        '--init_files', '/init',
        '--forcings_dir', '/forcings',
        '--mhm_fluxes_dir', '/mhm_fluxes',
        '--mrm_fluxes_dir', '/mrm_fluxes',
        '--mhm_out_file', 'outmhm.nc',
        '--mrm_out_file', 'outmrm.nc',
        '--hydroland_opa', '/opa',
        '--pre', 'tp',
        '--resolution', '0.1',
    ]
    with pytest.raises(SystemExit):
        mrm.parse_args(argv)

# --- Test execute_mrm workflow ---
@pytest.fixture
def setup_dirs(tmp_path):
    # Create directories and dummy files
    base = tmp_path
    dirs = {
        'current_mrm_dir': str(base/'cur_mrm'),
        'mrm_restart_dir': str(base/'restart'),
        'mrm_log_dir': str(base/'logs'),
        'init_files': str(base/'init'),
        'forcings_dir': str(base/'forc'),
        'mhm_fluxes_dir': str(base/'mhm_flux'),
        'mrm_fluxes_dir': str(base/'mrm_flux'),
        'hydroland_opa': str(base/'opa'),
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    # create dummy run_parallel_mrm.sh
    script = os.path.join(dirs['current_mrm_dir'], 'run_parallel_mrm.sh')
    with open(script, 'w') as f:
        f.write('#!/bin/bash\necho ok')
    return dirs

class DummyPRun:
    def __init__(self):
        self.ran = False
    def run(self):
        self.ran = True

@pytest.mark.parametrize('return_prepare,return_merge', [(True, True)])
def test_execute_mrm_flow(monkeypatch, setup_dirs, return_prepare, return_merge):
    dirs = setup_dirs

    # patch generate_mrm_arg_list
    monkeypatch.setattr(mrm, 'generate_mrm_arg_list', lambda path: ['1 0 "' + path + '/1.day" 0'])
    # patch prepare_data
    calls = {'prep1': False, 'prep2': False, 'merge': False}
    def fake_prepare_data(**kwargs):
        if not calls['prep1']:
            calls['prep1'] = True
        else:
            calls['prep2'] = True
        return None
    monkeypatch.setattr(mrm, 'prepare_data', fake_prepare_data)

    # patch write_run_parallel_mrm
    monkeypatch.setattr(mrm, 'write_run_parallel_mrm', lambda *args, **kwargs: None)
    # patch chmod
    monkeypatch.setattr(os, 'chmod', lambda path, mode: None)
    # patch ParallelRun
    dummy_pr = DummyPRun()
    monkeypatch.setattr(mrm, 'ParallelRun', lambda **kwargs: dummy_pr)
    # patch mrm_fluxes_merge
    monkeypatch.setattr(mrm, 'mrm_fluxes_merge', lambda **kwargs: calls.update({'merge': True}))
    # patch shutil.move to avoid missing file errors
    monkeypatch.setattr(shutil, 'move', lambda src, dst: None)
    monkeypatch.setenv('OMP_NUM_THREADS', '1')

    params = {
        'current_mrm_dir': dirs['current_mrm_dir'],
        'mrm_restart_dir': dirs['mrm_restart_dir'],
        'mrm_log_dir': dirs['mrm_log_dir'],
        'ini_date': '2021_01_01',
        'end_date': '2021_01_02',
        'next_date': '2021_01_03',
        'stat_freq': 'daily',
        'init_files': dirs['init_files'],
        'forcings_dir': dirs['forcings_dir'],
        'mhm_fluxes_dir': dirs['mhm_fluxes_dir'],
        'mrm_fluxes_dir': dirs['mrm_fluxes_dir'],
        'mhm_out_file': 'mhm.nc',
        'mrm_out_file': 'mrm.nc',
        'hydroland_opa': dirs['hydroland_opa'],
        'pre': 'tp',
        'resolution': '0.1',
        'executable_mrm': 'mrm',
        'omp_num_threads': '1',
    }

    # should not throw
    mrm.execute_mrm(**params)

    assert calls['prep1'] and calls['prep2'], "Both prepare_data calls should be made"
    assert dummy_pr.ran, "ParallelRun.run should have been invoked"
    assert calls['merge'], "mrm_fluxes_merge should have been called"
