import os
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor
import pytest
import numpy as np
from netCDF4 import Dataset
from hydroland.mrm_setup import (
    ParallelRun,
    mosaic_two_tiles,
    merge_pair_jobs,
    mrm_fluxes_merge,
    generate_mrm_arg_list,
)

import xarray as xr

def create_dummy_nc(path, varname='Qrouted', data=None, fill_value=-9999.0):
    if data is None:
        data = np.array([[1, fill_value], [fill_value, 2]])
    ds = xr.Dataset({varname: (('lat', 'lon'), data)}, coords={'lat': [0,1], 'lon': [0,1]})
    ds[varname].encoding = {'_FillValue': fill_value, 'missing_value': fill_value}
    ds.to_netcdf(path)
    return path

# --- Test ParallelRun.run_program ---
def test_parallel_run_program_success(tmp_path, monkeypatch, caplog):
    exe = 'echo'
    args_list = ['hello']
    pr = ParallelRun(exe, args_list, str(tmp_path/'outdir'), 1, 2)
    class DummyProc:
        def __init__(self): self.returncode = 0
        def communicate(self): return ('out', '')
    monkeypatch.setattr(subprocess, 'Popen', lambda *args, **kwargs: DummyProc())
    caplog.set_level(logging.DEBUG)
    pr.run_program('arg1')
    assert 'Starting program' in caplog.text
    assert os.path.isdir(pr.output_dir)

# --- Test mosaic_two_tiles ---
def test_mosaic_two_tiles(tmp_path):
    f1 = tmp_path / 'in1.nc'
    f2 = tmp_path / 'in2.nc'
    out = tmp_path / 'out.nc'
    create_dummy_nc(str(f1), data=np.array([[1, -9999], [-9999, 4]]))
    create_dummy_nc(str(f2), data=np.array([[-9999, 3], [2, -9999]]))
    # Run mosaic
    mosaic_two_tiles(str(f1), str(f2), str(out))
    # Read with netCDF4 to avoid xarray warnings
    with Dataset(str(out), 'r') as ds:
        arr = ds.variables['Qrouted'][:]
        assert arr[0,0] == 1
        assert arr[0,1] == 3
        assert arr[1,0] == 2
        assert arr[1,1] == 4
        fill = ds.variables['Qrouted']._FillValue
        assert fill == -9999.0

# --- Test merge_pair_jobs ---
def test_merge_pair_jobs(monkeypatch, tmp_path):
    # Use threads to avoid pickling lambda
    monkeypatch.setattr('hydroland.mrm_setup.ProcessPoolExecutor', ThreadPoolExecutor)
    cur = str(tmp_path)
    for i in range(1,5): open(os.path.join(cur, f'pfx_{i}.nc'), 'w').close()
    calls = []
    monkeypatch.setattr('hydroland.mrm_setup.mosaic_two_tiles', lambda a,b,c: calls.append((a,b,c)))
    merge_pair_jobs('pfx', 4, 'outp', 2, cur, max_workers=1)
    expected = [
        (os.path.join(cur,'pfx_1.nc'), os.path.join(cur,'pfx_2.nc'), os.path.join(cur,'outp_1.nc')),
        (os.path.join(cur,'pfx_3.nc'), os.path.join(cur,'pfx_4.nc'), os.path.join(cur,'outp_2.nc')),
    ]
    assert calls == expected

# --- Test generate_mrm_arg_list ---
def test_generate_mrm_arg_list():
    arg_list = generate_mrm_arg_list('/data')
    assert len(arg_list) == 53
    assert arg_list[0].startswith('1 ')
    assert arg_list[-1].startswith('53 ')

# --- Test mrm_fluxes_merge ---
def test_mrm_fluxes_merge(tmp_path, monkeypatch):
    # Use threads to avoid pickling issues
    monkeypatch.setattr('hydroland.mrm_setup.ProcessPoolExecutor', ThreadPoolExecutor)
    cur = str(tmp_path)
    # Setup subdomain files
    os.makedirs(tmp_path/'subdomain_53'/'output', exist_ok=True)
    open(tmp_path/'subdomain_53'/'output'/'mRM_Fluxes_States.nc', 'w').close()
    for i in range(1,53):
        d = tmp_path/f'subdomain_{i}'/'output'
        os.makedirs(d, exist_ok=True)
        open(d/'mRM_Fluxes_States.nc', 'w').close()
    # Patch mosaic_two_tiles to create merged files
    def fake_mosaic(a, b, c): open(c, 'w').close()
    monkeypatch.setattr('hydroland.mrm_setup.mosaic_two_tiles', fake_mosaic)
    # Run merge; fake_mosaic writes intermediate and final files
    mrm_fluxes_merge(cur, 'final.nc', max_workers=1)
    assert os.path.exists(tmp_path/'final.nc'), "final.nc should be created by mosaic_two_tiles"
