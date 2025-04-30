#!/usr/bin/env python3

import multiprocessing as mp
import os
import logging
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from subprocess import Popen, PIPE
from typing import Tuple, List

import xarray as xr


# Initialize logging
logger = logging.getLogger(__name__)


class ParallelRun:
    def __init__(self, exe, args_list, output_dir, global_threads, exe_threads):
        self.exe = exe
        self.args_list = args_list
        self.output_dir = output_dir
        self.global_threads = global_threads
        self.exe_threads = exe_threads

    def run_program(self, exe_args):
        logger.debug("Starting program %s with args: %s", self.exe, exe_args)
        os.makedirs(self.output_dir, exist_ok=True)

        # set up the env
        my_env = os.environ.copy()
        my_env["OMP_NUM_THREADS"] = str(self.exe_threads)

        # launch and capture stdout/stderr
        proc = Popen(
            f"{self.exe} {exe_args}",
            shell=True,
            env=my_env,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
        )
        out, err = proc.communicate()

        if out:
            logger.debug("Output from %s:\n%s", exe_args, out.strip())
        if err:
            logger.error("Error from %s:\n%s", exe_args, err.strip())

    def run(self):
        startup = """
        Starting parallel run of: {}
        with global n threads:    {}
        and threads per exe:      {}

        Runs will be issued for the following list:
        """
        for xx in self.args_list:
            startup += "{}\n".format(xx)
        pool = mp.Pool(processes=self.global_threads)
        pool.map(self.run_program, self.args_list)


def mosaic_two_tiles(
    file1: str,
    file2: str,
    outfile: str,
    varname: str = "Qrouted",
    fill_value: float = -9999.0,
) -> None:
    """
    Mosaic two tiles on the same lat/lon grid by taking non-missing data
    from file1 and filling with data from file2. Ensures a single consistent
    _FillValue for the output variable.
    """
    # open both datasets
    ds1 = xr.open_dataset(file1)
    ds2 = xr.open_dataset(file2)

    da1 = ds1[varname]
    da2 = ds2[varname]

    # turn the CDO fill_value into NaNs for processing
    da1_clean = da1.where(da1 != fill_value)
    da2_clean = da2.where(da2 != fill_value)

    # mosaic: wherever da1 is NaN, take da2
    merged = da1_clean.fillna(da2_clean)

    # carry over attrs & coords
    merged.attrs = da1.attrs
    out = xr.Dataset({varname: merged}, coords=ds1.coords)

    # preserve encoding but remove conflicting fill metadata
    out[varname].encoding.update(da1.encoding)
    out[varname].encoding.pop("_FillValue", None)
    out[varname].encoding.pop("missing_value", None)
    # set a single, consistent fill value
    out[varname].encoding["_FillValue"] = fill_value

    # drop any _FillValue or missing_value on coords
    for coord in ("lat", "lon"):
        out[coord].encoding.pop("_FillValue", None)
        out[coord].encoding.pop("missing_value", None)

    # write out to NetCDF
    out.to_netcdf(outfile)

    # clean up
    ds1.close()
    ds2.close()
    
    logger.debug(f"Mosaicked {file1} + {file2} → {outfile}")


def merge_pair_jobs(prefix_in: str,
                    num_in: int,
                    prefix_out: str,
                    num_pairs: int,
                    current_mrm_dir: str,
                    max_workers: int = None) -> None:
    """
    Merge files in pairs using the given prefixes, in parallel.
    For example, merges:
      {prefix_in}_1.nc & {prefix_in}_2.nc -> {prefix_out}_1.nc,
      {prefix_in}_3.nc & {prefix_in}_4.nc -> {prefix_out}_2.nc, etc.

    Parameters
    ----------
    prefix_in : str
        Prefix of input files in current_mrm_dir
    num_in : int
        Number of input files (so loops over 1..num_in)
    prefix_out : str
        Prefix of output files in current_mrm_dir
    num_pairs : int
        How many pairs to process
    current_mrm_dir : str
        Directory containing the .nc files
    max_workers : int, optional
        Number of parallel workers (defaults to cpu_count)
    """
    jobs: List[Tuple[str, str, str]] = []
    i, j, num = 1, 2, 1
    while num_pairs > 0:
        if j <= num_in:
            f1 = os.path.join(current_mrm_dir, f"{prefix_in}_{i}.nc")
            f2 = os.path.join(current_mrm_dir, f"{prefix_in}_{j}.nc")
            out = os.path.join(current_mrm_dir, f"{prefix_out}_{num}.nc")
            jobs.append((f1, f2, out))
        i += 2; j += 2; num += 1; num_pairs -= 1

    # run all merges in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(mosaic_two_tiles, a, b, c) for a, b, c in jobs]
        for f in as_completed(futures):
            # will raise if mosaic_two_tiles failed
            f.result()


def mrm_fluxes_merge(current_mrm_dir: str, mrm_out_file: str,
                     max_workers: int = None) -> None:
    """
    Merge all mRM fluxes states across subdomains into one file,
    parallelizing each merge loop with a ProcessPoolExecutor.
    """
    # Step 0: initial copy
    src = os.path.join(current_mrm_dir, "subdomain_53", "output", "mRM_Fluxes_States.nc")
    dst = os.path.join(current_mrm_dir, "temp_second_loop_14.nc")
    shutil.copy(src, dst)

    # Step 1: initial pair merging of subdomains 1..52
    initial_jobs: List[Tuple[str, str, str]] = []
    i, j, num = 1, 2, 1
    while j <= 52:
        in1 = os.path.join(current_mrm_dir, f"subdomain_{i}", "output", "mRM_Fluxes_States.nc")
        in2 = os.path.join(current_mrm_dir, f"subdomain_{j}", "output", "mRM_Fluxes_States.nc")
        out = os.path.join(current_mrm_dir, f"temp_first_loop_{num}.nc")
        initial_jobs.append((in1, in2, out))
        i += 2; j += 2; num += 1

    # parallel initial merges
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(mosaic_two_tiles, a, b, c) for a, b, c in initial_jobs]
        for f in as_completed(futures):
            f.result()

    # subsequent loops: parallelized via merge_pair_jobs
    merge_pair_jobs("temp_first_loop", 26, "temp_second_loop", 13, current_mrm_dir, max_workers)
    merge_pair_jobs("temp_second_loop", 14, "temp_third_loop", 7, current_mrm_dir, max_workers)

    # rename as in original script
    os.replace(
        os.path.join(current_mrm_dir, "temp_third_loop_7.nc"),
        os.path.join(current_mrm_dir, "temp_fourth_loop_4.nc")
    )

    merge_pair_jobs("temp_third_loop", 7, "temp_fourth_loop", 4, current_mrm_dir, max_workers)
    merge_pair_jobs("temp_fourth_loop", 4, "temp_fifth_loop", 2, current_mrm_dir, max_workers)

    # final merge of last two
    final_in1 = os.path.join(current_mrm_dir, "temp_fifth_loop_1.nc")
    final_in2 = os.path.join(current_mrm_dir, "temp_fifth_loop_2.nc")
    final_out = os.path.join(current_mrm_dir, mrm_out_file)
    mosaic_two_tiles(final_in1, final_in2, final_out)


def generate_mrm_arg_list(grdc_path: str) -> List[str]:
    """
    Generate list of argument strings for parallel_mrm.py invocation.
    Each entry: subdomain_id, number_of_gauges, paths, gauge_ids
    """
    specs = [
        (1, 3, ["1196100", "1259151", "1599100"]),
        (2, 0, []),
        (3, 0, []),
        (4, 0, []),
        (5, 0, []),
        (6, 0, []),
        (7, 3, ["1531100", "1531450", "1531550"]),
        (8, 0, []),
        (9, 1, ["1495700"]),
        (10, 0, []),
        (11, 1, ["2906300"]),
        (12, 0, []),
        (13, 3, ["2469120", "2569005", "2969101"]),
        (14, 0, []),
        (15, 1, ["2901201"]),
        (16, 0, []),
        (17, 3, ["2151100", "2260100", "2260500"]),
        (18, 1, ["5224500"]),
        (19, 0, []),
        (20, 4, ["2907400", "2908305", "2909150", "2909152"]),
        (21, 3, ["2910300", "2999200", "2999500"]),
        (22, 0, []),
        (23, 1, ["2917920"]),
        (24, 0, []),
        (25, 1, ["4362600"]),
        (
            26,
            11,
            [
                "6116200",
                "6123400",
                "6221100",
                "6242401",
                "6335020",
                "6335050",
                "6337515",
                "6421100",
                "6421500",
                "6545800",
                "6973300",
            ],
        ),
        (27, 1, ["6970100"]),
        (28, 0, []),
        (29, 0, []),
        (30, 0, []),
        (31, 0, []),
        (32, 0, []),
        (33, 4, ["6233201", "6233410", "6233502", "6731400"]),
        (34, 2, ["6854700", "6854702"]),
        (35, 0, []),
        (36, 1, ["4214051"]),
        (37, 0, []),
        (
            38,
            7,
            [
                "4102100",
                "4103200",
                "4103550",
                "4103800",
                "4203152",
                "4203201",
                "4203250",
            ],
        ),
        (
            39,
            8,
            [
                "4207310",
                "4207900",
                "4208005",
                "4208150",
                "4208270",
                "4208271",
                "4208280",
                "4208730",
            ],
        ),
        (40, 0, []),
        (41, 1, ["4214520"]),
        (42, 0, []),
        (43, 0, []),
        (
            44,
            8,
            [
                "4119300",
                "4123050",
                "4123202",
                "4123300",
                "4123301",
                "4125804",
                "4126800",
                "4127800",
            ],
        ),
        (45, 2, ["4115345", "4115346"]),
        (
            46,
            7,
            [
                "4147700",
                "4149401",
                "4149410",
                "4149413",
                "4149630",
                "4149631",
                "4149632",
            ],
        ),
        (
            47,
            6,
            [
                "5101200",
                "5101301",
                "5204103",
                "5204301",
                "5204302",
                "5204401",
            ],
        ),
        (48, 0, []),
        (49, 3, ["5109151", "5109200", "5608096"]),
        (50, 0, []),
        (51, 3, ["3663655", "3664160", "3669600"]),
        (
            52,
            30,
            [
                "3618051",
                "3618052",
                "3618053",
                "3618500",
                "3618950",
                "3618951",
                "3620000",
                "3621200",
                "3622400",
                "3623100",
                "3624120",
                "3624121",
                "3624300",
                "3625320",
                "3625340",
                "3625350",
                "3625360",
                "3625370",
                "3627030",
                "3627402",
                "3627551",
                "3627650",
                "3628201",
                "3629150",
                "3629770",
                "3629771",
                "3629790",
                "3630150",
                "3630200",
                "3631100",
            ],
        ),
        (53, 1, ["3649412"]),
    ]
    arg_list: List[str] = []
    for sub, num, gids in specs:
        if gids:
            files = ",".join(f"'{grdc_path}/{gid}.day'" for gid in gids)
            ids = ",".join(gids)
            arg_list.append(f'{sub} {num} "{files}" {ids}')
        else:
            arg_list.append(f"{sub} {num} \"'XXX'\" 0")
    return arg_list


def write_run_parallel_mrm(
    ini_year: str,
    ini_month: str,
    ini_day: str,
    end_year: str,
    end_month: str,
    end_day: str,
    current_mrm_dir: str,
    mrm_restart_dir: str,
    mhm_outfile: str,
    mrm_network_dir: str,
    mrm_id_gauges_file: str,
    stat_freq: str,
    forcings_dir: str,
    next_date: str,
    resolution: str,
    executable_mrm: str,
):
    ini_date = f"{ini_year}_{ini_month}_{ini_day}"
    end_date = f"{end_year}_{end_month}_{end_day}"

    if stat_freq == "daily":
        time_step = 24
        timestep_model_outputs_mrm = -1
    else:
        time_step = 1
        timestep_model_outputs_mrm = 1

    # if logger is in debug then measured time for mrm subdomain runs
    if logger.isEnabledFor(logging.DEBUG):
        get_runtime="time"
    else:
        get_runtime=""

    script_path = os.path.join(current_mrm_dir, "run_parallel_mrm.sh")

    with open(script_path, "w") as f:
        f.write(f"""#!/bin/bash
subdomain_id=${{1?The subdomain ID must be specified}}
n_gauges=${{2?The number of gauges must be specified}}
grdc_fpaths="${{3-:XXX}}"
grdc_ids="${{4-:0}}"

subdomain="subdomain_${{subdomain_id}}"
restartFile="{mrm_restart_dir}/${{subdomain}}/{ini_date}_mRM_restart.nc"
networkFile="{mrm_network_dir}/subdomain_river_network_${{subdomain_id}}.nc"

    #  -- make workdir subdomains ----------------------
    mkdir -p {current_mrm_dir}/${{subdomain}}

    #  -- link files -----------------------------------
    cd {current_mrm_dir}/${{subdomain}}

    #  -- total runoff file ----------------------------
    mkdir -p input
    target_mhm_outfile={mhm_outfile}
    ln -fs ${{target_mhm_outfile}} input/total_runoff.nc

    #  -- morph files --------------------------------
    mkdir -p input/morph
    ln -fs ${{networkFile}} input/morph/river_network.nc
    ln -fs {mrm_id_gauges_file}/idgauges.asc input/morph/idgauges.asc # required name

    #  -- meteo files --------------------------------
    mkdir -p input
    # linking input forcings
    ln -fs {forcings_dir}/mHM_{ini_date}_to_{end_date}_pre.nc input/pre.nc
    ln -fs {forcings_dir}/mHM_{ini_date}_to_{end_date}_pet.nc input/pet.nc
    mkdir -p input/restart
    cd input/restart
    ln -fs ${{restartFile}}
    cd -
    mkdir -p output

    #  -- set eval variables for namelist -------------
    ystart={ini_year}
    yend={end_year}
    mstart={ini_month}
    mend={end_month}
    dstart={ini_day}
    dend={end_day}

    #  -- make mrm nam -----------------------------
    cat > {current_mrm_dir}/${{subdomain}}/mrm.nml << MRMNML
&directories_general
    dir_lcover = '../data/input/test_domain/input/'
    dir_morpho = 'input/morph/river_network.nc'
    dir_out = 'output/'
    dircommonfiles = 'output/'
    dirconfigout = 'output/'
    file_latlon = '${{networkFile}}'
    mhm_file_restartout = 'output/mHM_restart_001.nc'
    mrm_file_restartout = 'output/mRM_restart_{next_date}.nc'
/

&directories_mrm
    dir_bankfull_runoff = 'test_basin/input/optional_data/'
    dir_gauges = ''
    dir_total_runoff = 'input/'
/

&evaluation_gauges
    gauge_filename(1,:) = ${{grdc_fpaths}}
    gauge_id(1,:) = ${{grdc_ids}}
    ngaugestotal = ${{n_gauges}}
    nogauges_domain = ${{n_gauges}}
/

&inflow_gauges
    inflowgauge_filename(1,:) = ''
    inflowgauge_headwater = .FALSE.
    inflowgauge_id = -9
    ninflowgaugestotal = 0
    noinflowgauges_domain = 0
/

&lcover
    lcoveryearend = 2100
    lcoveryearstart = 1900
    lcoverfname = 'XXX'
    nlcoverscene = 1
/

&mainconfig
    iflag_cordinate_sys = 1
    l0domain = 1
    ndomains = 1
    read_opt_domain_data = 0
    resolution_hydrology = 0.1
    write_restart = .TRUE.
/

&mainconfig_mhm_mrm
    mrm_file_restartin = 'input/restart/{ini_date}_mRM_restart.nc'
    opti_function = 3
    opti_method = 1
    optimize = .FALSE.
    optimize_restart = .FALSE.
    read_restart = True
    resolution_routing = {resolution}
    timestep = {time_step}
/

&mainconfig_mrm
    alma_convention = .FALSE.
    filenamepetrunoff = 'pet'
    filenameprerunoff = 'pre'
    filenametotalrunoff = 'total_runoff'
    gw_coupling = .FALSE.
    varnamepetrunoff = 'pet'
    varnameprerunoff = 'pre'
    varnametotalrunoff = 'Q'
/

&optimization
    dds_r = 0.2
    mcmc_error_params = 0.01,
                        0.6
    mcmc_opti = .FALSE.
    niterations = 7
    sa_temp = -9.0
    sce_ngs = 2
    sce_npg = -9
    sce_nps = -9
    seed = 1235876
/

&optional_data
    dir_evapotranspiration = 'test_basin/input/optional_data/'
    dir_neutrons = 'test_basin/input/optional_data/'
    dir_soil_moisture = 'test_basin/input/optional_data/'
    file_tws = 'test_basin/input/optional_data/tws_basin_1.txt'
    nsoilhorizons_sm_input = 1
    timestep_et_input = -2
    timestep_sm_input = -2
/

&processselection
    processcase = 1, 1,
                1, 1,
                0, 1,
                1, 2,
                1, 0
/

&project_description
    contact = 'Stephan Thober (email: stephan.thober@ufz.de'
    conventions = 'tbd'
    history = ''
    mhm_details = 'Helmholtz Center for Environmental Research - UFZ, Department Computational Hydrosystems'
    project_details = 'Climate DT project'
    setup_description = 'model run for Climate DT project'
    simulation_type = 'simulation'
/

&time_periods
    eval_per%dend = ${{dend}}
    eval_per%dstart = ${{dstart}}
    eval_per%mend = ${{mend}}
    eval_per%mstart = ${{mstart}}
    eval_per%yend = ${{yend}}
    eval_per%ystart = ${{ystart}}
    warming_days = 0
/
MRMNML

cat > {current_mrm_dir}/${{subdomain}}/mrm_outputs.nml << MRMOUTPUT
&nloutputresults
    outputflxstate_mrm = .True.
    timestep_model_outputs_mrm = {timestep_model_outputs_mrm}
/
MRMOUTPUT

cat > {current_mrm_dir}/${{subdomain}}/mrm_parameter.nml << MRMPARAMETER
&routing1
    muskingumattenuation_riverslope = 0.01, 0.5, 0.3, 1.0, 1.0
    muskingumtraveltime_constant = 0.31, 0.35, 0.325, 1.0, 1.0
    muskingumtraveltime_impervious = 0.09, 0.11, 0.1, 1.0, 1.0
    muskingumtraveltime_riverlength = 0.07, 0.08, 0.075, 1.0, 1.0
    muskingumtraveltime_riverslope = 1.95, 2.1, 2.0, 1.0, 1.0
/

&routing2
    streamflow_celerity = 0.1, 15.0, 1.5, 0.0, 1.0
/

&routing3
    g1 = 0.1, 100.0, 30.0, 0.0, 1.0
    g2 = 0.1, 0.9, 0.6, 0.0, 1.0
/
MRMPARAMETER

{get_runtime} {executable_mrm} > mrm_{ini_date}_to_{end_date}.log 2>&1
""")
