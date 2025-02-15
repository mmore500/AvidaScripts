import logging
import os
from pathlib import Path
import subprocess
import tempfile
import typing

import pandas as pd

from ..get_avida import get_avida_executable_path
from ..GenomeManipulation import (
    GenomeManipulator,
    extend_instset_for_hostification,
    make_instset_path,
)
from .count_environment_tasks import count_environment_tasks
from .load_phenotype_dataframe import load_phenotype_dataframe


def assess_phenotypes(
    sequences: typing.Iterable[str],
    environment_content: str,
    instset_content: str,
    hostify_sequences: bool = False,
) -> pd.DataFrame:
    """Calculate the phenotypes (i.e., task profiles) of given sequences.

    This function delegates to Avida executable analyze mode.

    Parameters
    ----------
    sequences : typing.Iterable[str]
        Single-character-encoded instruction sequences to analyze.

    environment_content : str
        Avida environment configuration, specifying available tasks.

    instset_content : str
        Avida instruction set configuration, specifying available instructions.

    hostify_sequences : bool
        Should inject instructions be replaced with divide instructions?

        Makes parasite genomes compatible with Avida analysis mode,

    Returns
    -------
    pd.DataFrame
        Phenotype summaries, with rows corresponding to individual sequences.
    """

    sequences = [*sequences]

    gm = GenomeManipulator(make_instset_path(instset_content))
    if hostify_sequences:
        gm.extend_instset_for_hostification()
        # could also just do this above and not have to extend gm
        instset_content = extend_instset_for_hostification(instset_content)
        gwrap = lambda x: "".join(gm.hostify_parasite_sequence(x))
    else:
        gwrap = lambda x: x

    phenotypes_outpath = tempfile.mktemp()
    Path(phenotypes_outpath).write_text("")
    num_tasks = count_environment_tasks(environment_content)
    newline_char = "\n"  # no \'s allowed in fstring
    analyze_script = f"""PURGE_BATCH

{newline_char.join(f"LOAD_SEQUENCE {gwrap(genome)}" for genome in sequences)}

RECALC

DETAIL {phenotypes_outpath} sequence viable {
    " ".join(f"task.{i}" for i in range(num_tasks))
}
"""

    with tempfile.TemporaryDirectory() as run_dir:
        Path(f"{run_dir}/analyze.cfg").write_text(analyze_script)
        Path(f"{run_dir}/environment.cfg").write_text(environment_content)
        Path(f"{run_dir}/instset.cfg").write_text(instset_content)
        Path(f"{run_dir}/events.cfg").write_text("")

        avida_path = get_avida_executable_path()

        subprocess.run(
            f"{avida_path} --generate-config",
            capture_output=True,
            cwd=run_dir,
            shell=True,
        ).check_returncode()
        with open(f"{run_dir}/avida.cfg", "a") as fp:
            fp.write("\n#include INST_SET=instset.cfg\n")

        # Execute avida in analyze mode
        completed_process = subprocess.run(
            f"{avida_path} -set VERBOSITY 0 -set ANALYZE_FILE analyze.cfg -a",
            capture_output=True,
            cwd=run_dir,
            shell=True,
            text=True,
        )
        completed_process.check_returncode()
        logging.info(completed_process.stdout)
        logging.info(completed_process.stderr)

    res = load_phenotype_dataframe(phenotypes_outpath, environment_content)
    os.remove(phenotypes_outpath)
    # undo hostificaiton, if necessary
    if hostify_sequences:
        res["Genome Sequence"] = sequences
    return res
