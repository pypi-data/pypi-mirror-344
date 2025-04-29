# Hydroland

**Hydroland** is an open-source, component-based model coupling framework for environmental simulations.

---

## Overview

This guide explains how to run the Hydroland application within the Autosubmit workflow. It does *not* cover:

- Creating an experiment with Autosubmit
- Accessing the Virtual Machine (VM)

For those topics, please see:

- [Workflow - Getting Started](https://earth.bsc.es/gitlab/digital-twins/de_340-2/workflow/-/tree/main#documentation)
- [How to Access the VM](https://wiki.eduuni.fi/display/cscRDIcollaboration/Autosubmit+Virtual+Machine)

---

## Running Hydroland

In this example, we run Hydroland on [LUMI HPC](https://docs.lumi-supercomputer.eu) using historical IFS-NEMO data (see [Coupling NEMO and IFS](https://www.ecmwf.int/en/elibrary/75709-coupling-nemo-and-ifs-models-single-executable)). After creating your experiment with minimal configuration, edit the files in `/appl/AS/AUTOSUBMIT_DATA/${exp_id}/conf`:

1. **`main.yml`** — Configure a one-month run starting on 1991-01-01:
   ```yaml
   RUN:
     WORKFLOW: apps
     ENVIRONMENT: cray
     PROCESSOR_UNIT: cpu
     TYPE: production
   APP:
     NAMES: [HYDROLAND]
     READ_FROM_DATABRIDGE: "true"
   EXPERIMENT:
     DATELIST: 19910101  # Start date (YYYYMMDD)
     MEMBERS: fc0
     CHUNKSIZEUNIT: day
     SPLITSIZEUNIT: day
     CHUNKSIZE: 1
     NUMCHUNKS: 3
     CALENDAR: standard
   PLATFORMS:
     LUMI:
       TYPE: slurm
       APP_PARTITION: debug
       CUSTOM_DIRECTIVES: ['#SBATCH --time=00:15:00']
   ```

2. **`request.yml`** — Select the Climate DT data (IFS-NEMO Historic high resolution):
   ```yaml
   REQUEST:
     EXPERIMENT: hist
     ACTIVITY: baseline
     RESOLUTION: high
     REALIZATION: 1
     GENERATION: 2
     MODEL: ifs-fesom
   ```

By default, Hydroland:

- Uses daily timesteps
- Requests variables `tp` and `2t` at `0.1°` resolution
- Does **not** apply bias adjustment

To customize these settings, edit `proj/git_project/conf/mother_request.yml` under the `HYDROLAND:` section. For example:

```yaml
HYDROLAND:
  1:
    GSVREQUEST:
      param: "2t"
      grid: "0.1/0.1"
      method: nn
    OPAREQUEST:
      variable: "2t"
      stat: "raw"
      bias_adjustment: none
      stat_freq: "hourly"
  2:
    GSVREQUEST:
      param: "tp"
      grid: "0.1/0.1"
      method: nn
    OPAREQUEST:
      variable: "tp"
      stat: "raw"
      bias_adjustment: none
      stat_freq: "hourly"
```

After editing, create and run your experiment as described in the [Getting Started guide](https://earth.bsc.es/gitlab/digital-twins/de_340-2/workflow/-/tree/main#documentation). You can monitor all experiments on the Climate DT [visualization site](https://climatedt-wf.csc.fi).

For more details, see the [workflow wiki](https://earth.bsc.es/gitlab/digital-twins/de_340-2/workflow/-/wikis/home).

---

## Hydroland Output Structure

All final results are stored in `${OUT_PATH}` (e.g., on LUMI: `/scratch/project_465000454/tmp/${exp_id}`). The Hydroland output directory looks like:

```
${OUT_PATH}/
├── forcings/
└── hydroland/
    ├── mhm/
    │   ├── log_files/
    │   ├── restart_files/
    │   ├── current_run/   # removed after execution
    │   │   ├── input/
    │   │   │   ├── meteo/
    │   │   │   └── restart/
    │   │   └── output/
    │   └── fluxes/
    └── mrm/
        ├── log_files/
        │   ├── subdomain_1/
        │   └── ...
        ├── restart_files/
        │   ├── subdomain_1/
        │   └── ...
        ├── current_run/   # removed after execution
        └── fluxes/
```

- **Restart files** (≈3 GB per timestep) store initial data.
- **Log and forcing files** are created each timestep.

Hydroland retains only one set of monthly files plus the current and previous timesteps to minimize storage and support restart capability. On LUMI, Hydroland stores restart/forcing files under `/project/project_465000454/applications/hydroland` (on MN5: `/gpfs/projects/ehpc01/applications/hydroland`).

When timestep *n* completes successfully, files for *n–1* are deleted—except the first and last day of the month—ensuring at least two restart points per month. This allows resuming or restarting from any completed month. For example, if a run fails on 2020-03-27, you can restart from 2020-03-26 or 2020-03-01.

---

## instalation
```
pip install git+https://git.ufz.de/destine_cats/hydroland.git

```

## License

Hydroland is licensed under **LGPLv3**.  
© 2025–2030 Hydroland developers, Helmholtz-Zentrum für Umweltforschung GmbH – UFZ. All rights reserved.

