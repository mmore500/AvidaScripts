import glob
import logging
from pathlib import Path
import subprocess
import tempfile
import typing

from keyname import keyname as kn
import pandas as pd

from ..get_avida import get_avida_executable_path
from .count_environment_tasks import count_environment_tasks
from .iter_environment_tasks import iter_environment_tasks
from .load_grid_task_dataframe import load_grid_task_dataframe


def _write_events_file(sequences: typing.List[str], run_dir: str) -> None:
    with open(f"{run_dir}/events.cfg", "w") as fp:
        fp.write("u begin InjectSequence aaa 0\n")
        fp.write("u begin InjectSequence aaa 1\n")
        num_updates_per_trial = 30
        for i, sequence in enumerate(sequences):
            begin_update = i * num_updates_per_trial
            end_update = (i + 1) * num_updates_per_trial
            fp.write(
                f"""
u {begin_update} KillRectangle 0 0 0 0
u {begin_update} InjectSequence aaa 0
u {begin_update} InjectParasiteSequence {sequence} 0
u {begin_update} KillRectangle 1 0 1 0
u {begin_update} InjectSequence aaa 1
u {end_update} DumpHostTaskGrid a=host_task_grid+order={i}+sequence={sequence}+ext=.dat
u {end_update} DumpParasiteTaskGrid a=parasite_task_grid+order={i}+sequence={sequence}+ext=.dat
"""
            )
        fp.write(f"u {len(sequences) * num_updates_per_trial} Exit\n")


def _write_avida_config(run_dir: str) -> None:
    Path(f"{run_dir}/avida.cfg").write_text(
        f"""
RANDOM_SEED 1
WORLD_X 2
WORLD_Y 1
COPY_MUT_PROB 0.0
DIVIDE_INS_PROB 0.0
DIVIDE_DEL_PROB 0.0
DEATH_METHOD 0  # disable age death
INFECTION_MECHANISM 0  # infections always succeed
PARASITE_NO_COPY_MUT 1

# What should happen to a parasite when it gives birth?
# 0 = Leave the parasite thread state untouched.
# 1 = Resets the state of the calling thread (for SMT parasites, this must be 1)
INJECT_METHOD 1

# Infection causes host steralization and takes all cpu cycles
# (setting this to 1 will override inject_virulence)
INJECT_IS_VIRULENT 0

# The probabalistic percentage of cpu cycles allocated to the parasite instead of the host.
# Ensure INJECT_IS_VIRULENT is set to 0.
# This only works for single infection at the moment.
# Note that this should be set to a default even if virulence is evolving.
PARASITE_VIRULENCE 0.85

# Maximum number of Threads a CPU can spawn
MAX_CPU_THREADS 2

#include INST_SET=instset.cfg
"""
    )


def assess_parasite_phenotypes(
    sequences: typing.Iterable[str],
    environment_content: str,
    instset_content: str,
) -> pd.DataFrame:
    """Calculate the phenotypes (i.e., task profiles) of given sequences.

    This function delegates to the Avida executable through a custom event '
    sequence.

    Parameters
    ----------
    sequences : typing.Iterable[str]
        Single-character-encoded instruction sequences to analyze.

    environment_content : str
        Avida environment configuration, specifying available tasks.

    instset_content : str
        Avida instruction set configuration, specifying available instructions.

    Returns
    -------
    pd.DataFrame
        Phenotype summaries, with rows corresponding to individual sequences.
    """

    sequences = [*sequences]
    if not sequences:
        return pd.DataFrame()

    phenotypes_outpath = tempfile.mktemp()
    Path(phenotypes_outpath).write_text("")

    with tempfile.TemporaryDirectory() as run_dir:
        Path(f"{run_dir}/environment.cfg").write_text(environment_content)
        Path(f"{run_dir}/instset.cfg").write_text(instset_content)
        _write_events_file(sequences, run_dir)
        _write_avida_config(run_dir)

        # Run avida
        avida_path = get_avida_executable_path()
        completed_process = subprocess.run(
            f"{avida_path}",
            capture_output=True,
            cwd=run_dir,
            shell=True,
            text=True,
        )
        completed_process.check_returncode()
        logging.info(completed_process.stdout)
        logging.info(completed_process.stderr)

        # safety check host grid data
        num_tasks = count_environment_tasks(environment_content)
        host_grid_paths = list(
            glob.glob(f"{run_dir}/data/a=host_task_grid+order=*+sequence=*+ext=.dat"),
        )
        assert len(host_grid_paths) == len(sequences)
        for host_grid_path in host_grid_paths:
            host_grid_df = load_grid_task_dataframe(host_grid_path, num_tasks)
            assert len(host_grid_df) == 2
            assert host_grid_df["Alive"].all()

        para_grid_paths = list(
            glob.glob(
                f"{run_dir}/data/a=parasite_task_grid+order=*+sequence=*+ext=.dat",
            ),
        )
        assert len(para_grid_paths) == len(sequences)
        para_grid_dfs = []
        for para_grid_path in para_grid_paths:
            para_grid_df = load_grid_task_dataframe(para_grid_path, num_tasks)
            assert len(para_grid_df) == 2

            path_attrs = kn.unpack(para_grid_path)
            para_grid_df["Genome Sequence"] = path_attrs["sequence"]
            para_grid_df["Order"] = int(path_attrs["order"])
            para_grid_dfs.append(para_grid_df)

    # concatenate all parasite grid dataframes
    concat_para_grid_df = pd.concat(para_grid_dfs)
    para_phen_df = (
        concat_para_grid_df[concat_para_grid_df["Site"] == 1]
        .drop(
            labels=["Site", "Row", "Col"],
            axis="columns",
        )
        .sort_values(
            by="Order",
        )
        .copy()
    )

    # postprocess to add columns for compat w/ load_phenotype_dataframe
    para_phen_df["Viable"] = para_phen_df["Alive"]

    for i, task in enumerate(iter_environment_tasks(environment_content)):
        para_phen_df[f"Task {task}"] = para_phen_df[f"Trait {i}"]

    para_phen_df["Phenotype"] = [
        "inviable"
        if not row["Viable"]
        else "".join(
            str(int(value)) for col, value in row.items() if col.startswith("Trait ")
        )
        for __, row in para_phen_df.iterrows()
    ]
    para_phen_df["Phenotype Traits"] = [
        "".join(
            str(int(value)) for col, value in row.items() if col.startswith("Trait ")
        )
        for __, row in para_phen_df.iterrows()
    ]
    para_phen_df["Num Traits"] = [
        sum(
            int(value)
            for col, value in row.items()
            if col.startswith("Trait ")  # noqa fmt
        )
        for __, row in para_phen_df.iterrows()
    ]

    return para_phen_df
