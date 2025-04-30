import os
import sys
import re
import pytest
import hydroland.mhm_setup as ms

# --- extract_date_components ---
def test_extract_date_components_valid():
    yyyy, mm, dd = ms.extract_date_components('2021_12_05')
    assert (yyyy, mm, dd) == ('2021', '12', '05')

def test_extract_date_components_invalid(monkeypatch, caplog):
    caplog.set_level('ERROR')
    with pytest.raises(SystemExit):
        ms.extract_date_components('20211205')
    assert "Date must be in YYYY_MM_DD format" in caplog.text

# --- update_mhm_nml ---
@pytest.fixture
def sample_nml(tmp_path):
    content = (
        "eval_Per(1)%yStart = 2000\n"
        "eval_Per(1)%yEnd   = 2001\n"
        "eval_Per(1)%mStart = 01\n"
        "eval_Per(1)%mEnd   = 02\n"
        "eval_Per(1)%dStart = 03\n"
        "eval_Per(1)%dEnd   = 04\n"
        "mhm_file_RestartIn(1)     = \"input/restart/old_mHM_restart.nc\"\n"
        "mhm_file_RestartOut(1)    = \"output/old_mHM_restart.nc\"\n"
    )
    path = tmp_path / 'mhm.nml'
    path.write_text(content)
    return str(path)

@pytest.mark.parametrize('start,end,nextd', [
    ('2021_01_01', '2021_01_31', '2021_02_01'),
    ('1999_12_31', '2000_01_31', '2000_02_01'),
])
def test_update_mhm_nml(sample_nml, start, end, nextd):
    ms.update_mhm_nml(start, end, nextd, sample_nml)
    text = open(sample_nml).read()
    ystart, mstart, dstart = start.split('_')
    yend, mend, dend = end.split('_')
    assert re.search(rf"eval_Per\(1\)%yStart = {ystart}", text)
    assert re.search(rf"eval_Per\(1\)%mEnd   = {mend}", text)
    assert f"input/restart/{start}_mHM_restart.nc" in text
    assert f"output/{nextd}_mHM_restart.nc" in text

# --- create_header ---
def test_create_header_01(tmp_path):
    out = str(tmp_path)
    ms.create_header(out, 0.1)
    header = tmp_path / 'header.txt'
    assert header.exists()
    lines = header.read_text().splitlines()
    assert "ncols         3600" in lines[0]
    assert any("cellsize      0.1" in line for line in lines), \
        f"Expected cellsize line with 0.1, got: {lines}"

def test_create_header_005(tmp_path):
    out = str(tmp_path)
    ms.create_header(out, 0.05)
    header = tmp_path / 'header.txt'
    assert header.exists()
    lines = header.read_text().splitlines()
    assert "nrows         2800" in "\n".join(lines)
    assert any("cellsize      0.05" in line for line in lines), \
        f"Expected cellsize line with 0.05, got: {lines}"


def test_create_header_invalid():
    with pytest.raises(SystemExit):
        ms.create_header('dummy', 0.2)

# --- create_parameter_nml, create_output_nml, create_nml ---
@pytest.mark.parametrize('fn,attr', [
    ('create_parameter_nml', 'mhm_parameter.nml'),
    ('create_output_nml', 'mhm_outputs.nml'),
    ('create_nml', 'mhm.nml'),
])
def test_create_nml_variants(tmp_path, fn, attr):
    out = str(tmp_path)
    getattr(ms, fn)(out)
    filepath = tmp_path / attr
    assert filepath.exists(), f"{attr} should be created"
    content = filepath.read_text()
    assert len(content) > 0
