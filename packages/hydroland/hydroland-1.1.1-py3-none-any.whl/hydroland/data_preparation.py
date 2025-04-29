from datetime import datetime, timezone
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Optional, Union
import logging
import sys
import numpy as np
import pandas as pd
import xarray as xr


# Initialize logging
logger = logging.getLogger(__name__)


def pet_calculator(
    tavg: np.ndarray,
    lat: np.ndarray,
    time: datetime,
    stat_freq: str,
    l_heat: float = 2.26,
    w_density: float = 977.0,
) -> np.ndarray:
    """
    Calculate potential evapotranspiration (PET) based on Hargreaves & Samani equation (1985).
    """
    e_rad = e_rad_calculator(time, lat)
    pet = (e_rad / (l_heat * w_density)) * ((tavg + 5) / 100)
    pet = pet * 1000
    pet[tavg < -5] = 0
    return pet if stat_freq == "daily" else pet / 24


def e_rad_calculator(time: datetime, lat: np.ndarray) -> np.ndarray:
    """
    Calculate extraterrestrial radiation (MJ/m²/day) for a given day and latitude.
    """
    doy = pd.Timestamp(time).day_of_year - 1
    dist = 1 + (0.033 * np.cos(((2 * np.pi * doy) / 365)))
    dec = np.radians(-23.44 * np.cos(np.radians((360 / 365) * (doy + 10))))
    ang = np.arccos(np.clip(-np.tan(lat) * np.tan(dec), -1, 1))
    e_rad = (ang * np.sin(lat) * np.sin(dec)) + (
        np.cos(lat) * np.cos(dec) * np.sin(ang)
    )
    return 37.5 * dist * e_rad

def _compute_pet(args):
    """
    Worker helper to calculate PET for a single time slice.
    args: tuple(tavg_array, lat_array, time_val, stat_freq)
    """
    tavg_slice, lat_array, time_val, stat_freq = args
    return pet_calculator(tavg_slice, lat_array, time_val, stat_freq)

def get_pet(
    stat_freq: str,
    in_dir: str,
    out_dir: str,
    in_file: str,
    out_file: str,
    lon_number: int,
    max_workers: int = None,
) -> None:
    """
    Calculate PET in parallel across time dimension and save to NetCDF.
    """
    # Load dataset
    ds = xr.open_dataset(f"{in_dir}/{in_file}")
    tavg = ds.tavg  # (time, lat, lon)
    lat = ds.lat
    times = ds.time.values

    # Prepare latitude broadcast
    lat_rad = np.radians(lat.data)
    lat2d = np.repeat(lat_rad[:, np.newaxis], lon_number, axis=1)
    lat3d = lat2d[np.newaxis, :, :]

    # Build arguments for each time slice
    tasks = []
    for idx, t in enumerate(times):
        # convert timestamp to datetime
        current_time = datetime.fromtimestamp(int(t) / 1e9, tz=timezone.utc)
        tarr = tavg.isel(time=idx).values[np.newaxis, :, :]
        tasks.append((tarr, lat3d, current_time, stat_freq))

    # Compute PET in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(_compute_pet, tasks))

    # Stack results into array
    pet_data = np.vstack(results)
    pet_data = pet_data.astype(np.float32)

    # Wrap into DataArray
    pet_da = xr.DataArray(
        pet_data,
        coords=[ds.time, ds.lat, ds.lon],
        dims=["time", "lat", "lon"],
        attrs={"units": "mm", "missing_value": -9999.0, "_FillValue": -9999.0},
    )
    pet_ds = xr.Dataset({"pet": pet_da})

    # Output
    pet_ds.to_netcdf(f"{out_dir}/{out_file}")

    ds.close()


def clone_day(ds: xr.Dataset) -> xr.Dataset:
    """
    Shift the time by one day and concatenate to double the time axis.
    """
    shift = np.timedelta64(1, "D")
    ds_shifted = ds.copy()
    ds_shifted["time"] = ds["time"] + shift
    ds = xr.concat([ds, ds_shifted], dim="time")
    return ds


def set_days_to_zero(ds: xr.Dataset) -> xr.Dataset:
    """
    Reset all timestamps to midnight daily for a daily-frequency dataset.
    """
    start_date = pd.Timestamp(ds.time.values[0]).normalize()
    time_zeros = pd.date_range(start=start_date, periods=ds.time.size, freq="D")
    ds["time"] = time_zeros
    return ds


def convert_units(ds: xr.Dataset, var: str, freq: str) -> xr.Dataset:
    """
    Rename and convert units for the specified variable.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset containing `var`.
    var : str
        One of "2t", "tp", "tprate", or "avg_tprate".
    freq : str
        Either "daily" or "hourly", affects rate conversion.

    Returns
    -------
    xr.Dataset
        Dataset with renamed variable and updated units.
    """
    if var == "2t":
        new_var = "tavg"
        ds = ds.rename({var: new_var})
        ds[new_var] = ds[new_var] - 273.15
        ds[new_var].attrs["units"] = "degC"
    elif var == "tp":
        new_var = "pre"
        ds = ds.rename({var: new_var})
        ds[new_var] = ds[new_var] * 1000
        ds[new_var].attrs["units"] = "mm"
    elif var in {"tprate", "avg_tprate"}:
        new_var = "pre"
        ds = ds.rename({var: new_var})
        factor = 86400 if freq == "daily" else 3600 if freq == "hourly" else 1
        ds[new_var] = ds[new_var] * factor
        ds[new_var].attrs["units"] = "mm"
    else:
        raise ValueError(f"Invalid Hydroland variable: {var}.")

    # Set missing value attributes.
    missing_value = -9999.0
    ds[new_var].attrs["_FillValue"] = missing_value
    ds[new_var].attrs["missing_value"] = missing_value

    return ds


def str2bool(value: Union[str, bool]) -> bool:
    """
    Convert a string or bool to a boolean. Raises if not a valid boolean string.
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        logger.error(f"{value=}. Boolean value expected.")
        sys.exit(1)


def ensure_lat_lon_order(ds: xr.Dataset) -> xr.Dataset:
    """
    Ensure latitude is descending and longitude is ascending in the dataset.
    """
    # Check for the latitude variable.
    if "lat" in ds:
        lat_name = "lat"
    elif "latitude" in ds:
        lat_name = "latitude"
    else:
        logger.error("Latitude variable ('lat' or 'latitude') not found in the dataset.")
        sys.exit(1)

    # Check for the longitude variable.
    if "lon" in ds:
        lon_name = "lon"
    elif "longitude" in ds:
        lon_name = "longitude"
    else:
        logger.error("Longitude variable ('lon' or 'longitude') not found in the dataset.")
        sys.exit(1)

    # Get latitude and longitude values.
    lat_values = ds[lat_name].values
    lon_values = ds[lon_name].values

    # Ensure latitude is descending.
    if not (lat_values[1:] < lat_values[:-1]).all():
        ds = ds.sortby(lat_name, ascending=False)

    # Ensure longitude is ascending.
    if not (lon_values[1:] > lon_values[:-1]).all():
        ds = ds.sortby(lon_name, ascending=True)
    return ds


def main_mhm(
    in_dir: str, in_file: str, out_dir: str, out_file: str, var: str, stat_freq: str
) -> None:
    """
    Process an mHM file: clone single-day data, zero out timestamps,
    convert units, reorder lat/lon, and write out.
    """
    input_path = Path(in_dir, in_file)
    ds = xr.open_dataset(input_path)

    # Check the number of time steps.
    ntime = ds.time.size

    # Clone day if necessary.
    if ntime == 1:
        ds = clone_day(ds)

    # Set days to zero if frequency is daily.
    if stat_freq == "daily":
        ds = set_days_to_zero(ds)

    # Convert units.
    ds = convert_units(ds, var, stat_freq)

    # Ensure latitude is descending and longitude is ascending.
    ds = ensure_lat_lon_order(ds)

    # Save the processed file.
    output_path = Path(out_dir, out_file)
    ds.to_netcdf(output_path)


def main_mrm(
    in_dir: str, in_file: str, out_dir: str, out_file: str, stat_freq: str
) -> bool:
    """
    Process an mRM file similarly to mHM, but only write if daily.

    Returns
    -------
    bool
        True if a daily file was written; False otherwise.
    """
    input_path = Path(in_dir, in_file)
    ds = xr.open_dataset(input_path)

    # Check the number of time steps.
    ntime = ds.time.size

    # Clone day if necessary.
    if ntime == 1:
        ds = clone_day(ds)

    # Set days to zero if frequency is daily.
    if stat_freq == "daily":
        ds = set_days_to_zero(ds)
        output_path = Path(out_dir, out_file)
        ds.to_netcdf(output_path)
        return True
    else:
        return False


def pass_DGOV_attrs(
    opa_data: xr.DataArray, hydroland_ds: xr.Dataset, out_dir: str, out_file: str
) -> None:
    """
    Copy DGOV attributes from an OPA  into a Hydroland and save the result.
    """
    attributes_to_copy = [
        "activity",
        "dataset",
        "experiment",
        "generation",
        "type",
        "levtype",
        "model",
        "class",
        "realization",
        "stream",
        "resolution",
        "expver",
    ]

    for attr in attributes_to_copy:
        if attr in opa_data.attrs:
            hydroland_ds.attrs[attr] = opa_data.attrs[attr]

    hydroland_ds.attrs["application"] = "Hydroland"

    output_path = Path(out_dir) / out_file
    hydroland_ds.to_netcdf(output_path)


def DGOV_data(
    stat_freq: str,
    in_dir: str,
    in_hydroland_dir: str,
    current_ini_date: str,
    current_end_date: str,
    var: str,
    mRM: bool,
    out_dir: str,
    out_file: str,
) -> None:
    """
    Find matching OPA and Hydroland files, copy DGOV attributes, and save a new Hydroland file.
    """

    # Build wildcard patterns for OPA
    if stat_freq == "hourly":
        opa_pattern = (
            f"{current_ini_date}_T00_00_to_{current_end_date}_T23_00_{var}_*.nc"
        )
    else:
        opa_pattern = f"{current_ini_date}*{var}*.nc"

    # Build Hydroland pattern
    if mRM:
        if stat_freq == "hourly":
            hydroland_pattern = f"{current_ini_date}_T00_00_to_{current_end_date}_T23_00_mRM_Fluxes_States.nc"
        else:
            hydroland_pattern = f"{current_ini_date}_mRM_Fluxes_States.nc"
    else:
        hydroland_pattern = "mHM_Fluxes_States.nc"

    # Get OPA file
    opa_paths = list(Path(in_dir).glob(opa_pattern))
    if not opa_paths:
        logger.error(f"No OPA file found matching {opa_pattern} in {in_dir}")
        sys.exit(1)
    opa_path = opa_paths[0]
    opa_ds = xr.open_dataset(opa_path)

    # Get Hydroland file by exact filename
    hydroland_path = Path(in_hydroland_dir) / hydroland_pattern
    if not hydroland_path.exists():
        logger.error(f"No Hydroland file found at {hydroland_path}")
        sys.exit(1)
    hydroland_ds = xr.open_dataset(hydroland_path)

    # Copy attrs and save
    pass_DGOV_attrs(
        opa_data=opa_ds[var],
        hydroland_ds=hydroland_ds,
        out_dir=out_dir,
        out_file=out_file,
    )


def prepare_data(
    in_dir: str,
    out_dir: str,
    out_file: str,
    stat_freq: str,
    in_file: Optional[str] = None,
    var: Optional[str] = None,
    mRM: bool = False,
    add_DGOV_data: bool = False,
    current_ini_date: Optional[str] = None,
    current_end_date: Optional[str] = None,
    in_hydroland_dir: Optional[str] = None,
) -> None:
    """
    Dispatch to the appropriate data preparation: DGOV, mRM or mHM.
    """

    if add_DGOV_data:
        logger.debug(f"Adding DGOV data to {out_file=}")
        DGOV_data(
            stat_freq=stat_freq,
            in_dir=in_dir,
            in_hydroland_dir=in_hydroland_dir,
            current_ini_date=current_ini_date,
            current_end_date=current_end_date,
            var=var,
            mRM=mRM,
            out_dir=out_dir,
            out_file=out_file,
        )
    elif mRM:
        logger.debug(f"Generating mRM {out_file=}")
        main_mrm(
            in_dir=in_dir,
            in_file=in_file,
            out_dir=out_dir,
            out_file=out_file,
            stat_freq=stat_freq,
        )
    else:
        logger.debug(f"Generating mHM {out_file=}")
        main_mhm(
            in_dir=in_dir,
            in_file=in_file,
            out_dir=out_dir,
            out_file=out_file,
            var=var,
            stat_freq=stat_freq,
        )
