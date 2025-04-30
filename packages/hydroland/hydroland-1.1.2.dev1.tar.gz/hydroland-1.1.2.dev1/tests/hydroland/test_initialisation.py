import os
import shutil
import glob
import pytest
import hydroland.initialisation as init

# --- parse_args tests ---
def test_parse_args_minimal():
    argv = [
        '--ini_date', '20210101',
        '--end_date', '20210110',
        '--init_files', '/init',
        '--app_outpath', '/app',
        '--resolution', '0.1',
        '--current_mhm_dir', '/mhm_current',
        '--forcings_dir', '/forcings',
        '--mhm_restart_dir', '/mhm_restart',
        '--current_mrm_dir', '/mrm_current',
        '--mrm_restart_dir', '/mrm_restart',
    ]
    # Given mismatched int type and float choices, parse_args should exit
    with pytest.raises(SystemExit):
        init.parse_args(argv)

# --- ensure_removed tests ---
@pytest.mark.parametrize('path,is_link,is_file,is_dir,removed', [
    ('/file', True, False, False, 'file'),
    ('/file2', False, True, False, 'file'),
    ('/dir', False, False, True, 'dir'),
])
def test_ensure_removed(monkeypatch, path, is_link, is_file, is_dir, removed):
    calls = []
    monkeypatch.setattr(os.path, 'islink', lambda p: is_link)
    monkeypatch.setattr(os.path, 'isfile', lambda p: is_file)
    monkeypatch.setattr(os.path, 'isdir', lambda p: is_dir)
    monkeypatch.setattr(os, 'remove', lambda p: calls.append(('remove', p)))
    monkeypatch.setattr(shutil, 'rmtree', lambda p: calls.append(('rmtree', p)))
    init.ensure_removed(path)
    if removed == 'file':
        assert calls == [('remove', path)]
    else:
        assert calls == [('rmtree', path)]

# --- link_force tests ---
def test_link_force(monkeypatch):
    calls = []
    monkeypatch.setattr(init, 'ensure_removed', lambda dst: calls.append(('ensure_removed', dst)))
    monkeypatch.setattr(os, 'symlink', lambda src, dst: calls.append(('symlink', src, dst)))
    init.link_force('/src/path', '/dst/path')
    assert calls == [
        ('ensure_removed', '/dst/path'),
        ('symlink', '/src/path', '/dst/path')
    ]

# --- remove_matching_files tests ---
def test_remove_matching_files(monkeypatch, tmp_path, caplog):
    caplog.set_level('DEBUG')
    # Create fake files and dirs
    file1 = tmp_path / 'a.nc'
    dir1 = tmp_path / 'sub'
    file1.write_text('x')
    dir1.mkdir()
    monkeypatch.setattr(glob, 'iglob', lambda pat, recursive: [str(file1), str(dir1)])
    calls = []
    monkeypatch.setattr(os.path, 'islink', lambda p: False)
    monkeypatch.setattr(os.path, 'isfile', lambda p: p == str(file1))
    monkeypatch.setattr(os.path, 'isdir', lambda p: p == str(dir1))
    monkeypatch.setattr(os, 'remove', lambda p: calls.append(('remove', p)))
    monkeypatch.setattr(shutil, 'rmtree', lambda p: calls.append(('rmtree', p)))
    init.remove_matching_files([str(tmp_path/'*')])
    assert ('remove', str(file1)) in calls
    assert ('rmtree', str(dir1)) in calls
    assert 'Removed' in caplog.text

# --- start_initialisation tests ---
@pytest.fixture
def no_fs(monkeypatch):
    # Prevent real filesystem operations for initialization
    monkeypatch.setattr(init, 'remove_matching_files', lambda pats: None)
    monkeypatch.setattr(init, 'create_header', lambda out_dir, resolution: None)
    monkeypatch.setattr(init, 'create_parameter_nml', lambda out_dir: None)
    monkeypatch.setattr(init, 'create_output_nml', lambda out_dir: None)
    monkeypatch.setattr(init, 'create_nml', lambda out_dir: None)
    monkeypatch.setattr(shutil, 'copy', lambda src, dst: None)

def test_start_initialisation_cold(monkeypatch, tmp_path, no_fs):
    base = tmp_path
    dirs = {
        'current_mhm_dir': str(base/'mhm'),
        'current_mrm_dir': str(base/'mrm'),
        'mhm_restart_dir': str(base/'mhm_restart'),
    }
    # No previous restart exists
    monkeypatch.setattr(os.path, 'exists', lambda p: False)
    # Capture link_force calls
    calls = []
    monkeypatch.setattr(init, 'link_force', lambda src, dst: calls.append(('link', src, dst)))
    init.start_initialisation(
        ini_date='20210101',
        end_date='20210105',
        previous_date='20201231',
        stat_freq='daily',
        init_files=str(base/'init'),
        app_outpath=str(base/'app'),
        resolution=1,
        current_mhm_dir=dirs['current_mhm_dir'],
        forcings_dir=str(base/'forcings'),
        mhm_restart_dir=dirs['mhm_restart_dir'],
        current_mrm_dir=dirs['current_mrm_dir'],
        mrm_restart_dir=str(base/'mrm_restart'),
    )
    assert any(c[0]=='link' and 'mHM_restart' in c[1] for c in calls)
    assert any(c[0]=='link' and 'mRM_restart' in c[1] for c in calls)

def test_start_initialisation_warm(monkeypatch, tmp_path, no_fs):
    monkeypatch.setattr(os.path, 'exists', lambda p: True)
    calls = []
    monkeypatch.setattr(init, 'link_force', lambda src, dst: calls.append(('link', src, dst)))
    init.start_initialisation(
        ini_date='20210101',
        end_date='20210105',
        previous_date='20201231',
        stat_freq='daily',
        init_files=str(tmp_path/'init'),
        app_outpath=str(tmp_path/'app'),
        resolution=1,
        current_mhm_dir=str(tmp_path/'mhm'),
        forcings_dir=str(tmp_path/'forcings'),
        mhm_restart_dir=str(tmp_path/'mhm_restart'),
        current_mrm_dir=str(tmp_path/'mrm'),
        mrm_restart_dir=str(tmp_path/'mrm_restart'),
    )
    expected = (
        'link',
        os.path.join(str(tmp_path/'mhm_restart'), '20210101_mHM_restart.nc'),
        os.path.join(str(tmp_path/'mhm'), 'input', 'restart', '20210101_mHM_restart.nc')
    )
    assert calls == [expected]
