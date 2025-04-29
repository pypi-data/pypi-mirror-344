from datetime import datetime, timezone
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


def get_pet(
    stat_freq: str,
    in_dir: str,
    out_dir: str,
    in_file: str,
    out_file: str,
    lon_number: int,
) -> None:
    """
    Main routine to calculate PET and save to a NetCDF file.
    """
    # Construct the input file path
    input_file_path = f"{in_dir}/{in_file}"

    # Load the NetCDF dataset from in_file
    dataset = xr.open_dataset(input_file_path)
    tavg = dataset.tavg  # temp units: degC
    lat = dataset.lat  # lat units: degrees
    lon = dataset.lon  # lon units: degrees
    time = dataset.time  # time given in days

    # Convert latitude array to radians & prepare for computation
    lat_array = np.radians(lat.data)
    lat_array = np.repeat(lat_array[:, np.newaxis], lon_number, axis=1)
    lat_array = lat_array[np.newaxis, :, :]

    pet = np.empty(tavg.shape)

    for date, data in enumerate(tavg):
        # Getting date time & converting to datetime
        np_time = data.time.values
        current_time = datetime.fromtimestamp(int(np_time) / 1e9, tz=timezone.utc)

        # Getting data for each date as an array
        tavg_array = tavg.values[date : date + 1, :, :]

        # Calculating PET
        pet_data = pet_calculator(tavg_array, lat_array, current_time, stat_freq)

        # Add the data to PET
        pet[date] = pet_data

    # Set attributes for the PET DataArray
    pet_attrs = {"units": "mm", "missing_value": -9999.0, "_FillValue": -9999.0}

    # Create PET DataArray
    pet = xr.DataArray(
        pet,
        coords=[time, lat, lon],
        dims=["time", "lat", "lon"],
        attrs=pet_attrs,
    )

    # Save the PET dataset to out_file
    output_file_path = f"{out_dir}/{out_file}"
    pet_dataset = xr.Dataset({"pet": pet})
    pet_dataset.to_netcdf(output_file_path)


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
