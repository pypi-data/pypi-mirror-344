import numpy as np
import pandas as pd
import xarray as xr
import pytest
from datetime import datetime, timezone

from hydroland.data_preparation import (
    pet_calculator,
    e_rad_calculator,
    _compute_pet,
    clone_day,
    set_days_to_zero,
    convert_units,
    str2bool,
    ensure_lat_lon_order,
)


def test_e_rad_monotonic_latitude():
    # At spring equinox, extraterrestrial radiation should decrease with latitude
    time = datetime(2021, 3, 20, tzinfo=timezone.utc)  # Approximate equinox
    lats = np.array([0.0, np.pi / 4])  # Equator vs 45 degrees
    e_rad = e_rad_calculator(time, lats)
    assert e_rad.shape == (2,)
    assert e_rad[0] > e_rad[1], "E_rad at equator should exceed at 45 degrees during equinox"


def test_pet_below_threshold_zero():
    # PET should be zero when tavg < -5°C
    tavg = np.full((1, 2, 2), -10.0)
    lat = np.zeros((1, 2, 2))
    time = datetime(2021, 1, 1, tzinfo=timezone.utc)
    pet = pet_calculator(tavg, lat, time, stat_freq="daily")
    assert np.all(pet == 0), "PET must be zero for temperatures below -5°C"


def test_pet_and_compute_wrapper_agree():
    # _compute_pet should yield same as pet_calculator
    tavg = np.full((1, 1, 1), 10.0)
    lat = np.zeros((1, 1, 1))
    time = datetime(2021, 3, 1, tzinfo=timezone.utc)
    freq = "daily"
    direct = pet_calculator(tavg, lat, time, freq)
    wrapped = _compute_pet((tavg, lat, time, freq))
    assert np.allclose(direct, wrapped)


def test_clone_day_and_concat():
    # clone_day should double time axis by shifting one day
    times = pd.date_range("2020-01-01", periods=2, freq="D")
    ds = xr.Dataset({"a": ("time", [1, 2])}, coords={"time": times})
    out = clone_day(ds)
    assert out.time.size == 4
    # Check the second half is exactly +1 day
    expected = times + np.timedelta64(1, "D")
    assert np.array_equal(out.time.values[2:], expected)


def test_set_days_to_zero_normalize():
    # set_days_to_zero should normalize all times to midnight with daily freq
    times = [np.datetime64("2020-01-01T06:30"), np.datetime64("2020-01-02T12:45")]
    ds = xr.Dataset({"a": ("time", [1, 2])}, coords={"time": times})
    out = set_days_to_zero(ds)
    assert all(t.astype("datetime64[h]").astype(int) % 24 == 0 for t in out.time.values)
    # Should start at 2020-01-01
    assert out.time.values[0] == np.datetime64("2020-01-01T00:00")


def test_convert_units_2t_and_tp_and_rates():
    # Prepare sample values
    kelvin = 300.0
    precip_rate = 0.001  # m/s or m/day
    for var, freq, expected_unit in [
        ("2t", "daily", "degC"),
        ("tp", "daily", "mm"),
        ("tprate", "daily", "mm"),
        ("avg_tprate", "hourly", "mm"),
    ]:
        data = np.array([kelvin]) if var == "2t" else np.array([precip_rate])
        ds = xr.Dataset({var: ("x", data)})
        out = convert_units(ds, var, freq)
        # Check rename
        assert "tavg" in out or "pre" in out
        # Check units attribute
        name = "tavg" if var == "2t" else "pre"
        assert out[name].attrs.get("units") == expected_unit
        # Check missing value attrs
        assert out[name].attrs.get("_FillValue") == -9999.0
        assert out[name].attrs.get("missing_value") == -9999.0
    # Invalid var raises ValueError
    ds_bad = xr.Dataset({"badvar": ("x", [1])})
    with pytest.raises(ValueError):
        convert_units(ds_bad, "badvar", "daily")


def test_str2bool_true_and_false_and_invalid(capsys):
    # True values
    for true_str in ["yes", "True", "T", "1", "y"]:
        assert str2bool(true_str) is True
    # False values
    for false_str in ["no", "false", "F", "0", "n"]:
        assert str2bool(false_str) is False
    # Boolean input
    assert str2bool(True) is True
    assert str2bool(False) is False
    # Invalid triggers sys.exit
    with pytest.raises(SystemExit):
        str2bool("notabool")


def test_ensure_lat_lon_order_and_missing():
    # Create dataset with lat ascending and lon descending
    lat = np.array([0, 1])
    lon = np.array([10, 0])
    ds = xr.Dataset(coords={"lat": lat, "lon": lon})
    out = ensure_lat_lon_order(ds)
    # lat should now be descending
    assert (out.lat.values[0] > out.lat.values[-1])
    # lon should be ascending
    assert (out.lon.values[0] < out.lon.values[-1])
    # Test missing lat raises SystemExit
    ds_no_lat = xr.Dataset(coords={"lon": lon})
    with pytest.raises(SystemExit):
        ensure_lat_lon_order(ds_no_lat)
    # Test 'latitude' and 'longitude' names
    ds_alt = xr.Dataset(coords={"latitude": np.array([1, 0]), "longitude": np.array([0, 5])})
    out2 = ensure_lat_lon_order(ds_alt)
    assert (out2.latitude.values[0] > out2.latitude.values[-1])
    assert (out2.longitude.values[0] < out2.longitude.values[-1])
