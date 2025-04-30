import os
import glob
import pytest
from concurrent.futures import ThreadPoolExecutor
from hydroland import preprocessing

# --- Tests for parse_args ---
def test_parse_args_valid():
    argv = ['20200101', '20200131', 'daily', 'tavg', 'pre', '/out', '144', '/opa']
    args = preprocessing.parse_args(argv)
    assert args.ini_date == '20200101'
    assert args.end_date == '20200131'
    assert args.stat_freq == 'daily'
    assert args.temp_var == 'tavg'
    assert args.pre_var == 'pre'
    assert args.forcings_dir == '/out'
    assert args.lon_number == 144
    assert args.hydroland_opa == '/opa'

# --- Tests for find_file ---
def test_find_file_found(tmp_path):
    # create two files
    d = tmp_path
    f1 = d / 'file1.nc'
    f2 = d / 'file2.nc'
    f1.write_text('x')
    f2.write_text('y')
    # should return first matching
    result = preprocessing.find_file(str(d), 'file*.nc')
    assert result in {str(f1), str(f2)}

def test_find_file_notfound(tmp_path):
    result = preprocessing.find_file(str(tmp_path), '*.nc')
    assert result is None

# --- Test preprocess_forcings workflow ---
@ pytest.fixture(autouse=True)
def use_threads(monkeypatch):
    # Force ProcessPoolExecutor to ThreadPoolExecutor
    monkeypatch.setattr(preprocessing, 'ProcessPoolExecutor', ThreadPoolExecutor)
    yield

@ pytest.fixture
def setup_forcing_dirs(tmp_path):
    base = tmp_path
    opa = base / 'opa'
    out = base / 'out'
    osa = base / 'opa'
    opa.mkdir()
    out.mkdir()
    # create dummy hourly files for temp and pre
    f_pre = opa / '20200101_pre_timestep_60_daily_XXX.nc'
    f_tavg = opa / '20200101_tavg_timestep_60_daily_YYY.nc'
    f_pre.write_text('p')
    f_tavg.write_text('t')
    return str(base), str(opa), str(out)

def test_preprocess_forcings_success(tmp_path, monkeypatch, setup_forcing_dirs):
    base, opa_dir, out_dir = setup_forcing_dirs
    # monkeypatch find_file to pick our files
    monkeypatch.setattr(preprocessing, 'find_file', lambda dir, pat: glob.glob(os.path.join(dir, pat))[0])
    # track calls
    calls = {'prep': [], 'pet': False}
    def fake_prepare_data(**kwargs):
        calls['prep'].append(kwargs['out_file'])
    monkeypatch.setattr(preprocessing, 'prepare_data', fake_prepare_data)
    def fake_get_pet(**kwargs):
        calls['pet'] = True
    monkeypatch.setattr(preprocessing, 'get_pet', fake_get_pet)

    # run
    preprocessing.preprocess_forcings(
        ini_date='20200101',
        end_date='20200131',
        stat_freq='daily',
        temp_var='tavg',
        pre_var='pre',
        forcings_dir=out_dir,
        lon_number=144,
        hydroland_opa=opa_dir
    )

    # two prepare_data calls: tavg and pre outputs
    assert 'mHM_20200101_to_20200131_tavg.nc' in calls['prep']
    assert 'mHM_20200101_to_20200131_pre.nc' in calls['prep']
    # get_pet should be invoked once
    assert calls['pet']

@ pytest.mark.parametrize('missing', ['pre', 'tavg'])
def test_preprocess_forcings_missing(missing, tmp_path, monkeypatch, setup_forcing_dirs):
    base, opa_dir, out_dir = setup_forcing_dirs
    # monkeypatch find_file to return None when missing pattern
    def fake_find(dir, pat):
        if missing in pat:
            return None
        # otherwise real file
        return glob.glob(os.path.join(dir, pat))[0]
    monkeypatch.setattr(preprocessing, 'find_file', fake_find)
    with pytest.raises(SystemExit):
        preprocessing.preprocess_forcings(
            ini_date='20200101',
            end_date='20200131',
            stat_freq='daily',
            temp_var='tavg',
            pre_var='pre',
            forcings_dir=out_dir,
            lon_number=144,
            hydroland_opa=opa_dir
        )
