import logging
from pathlib import Path
import subprocess
import tempfile
import typing

import pandas as pd

from ..get_avida import get_avida_executable_path
from .count_environment_tasks import count_environment_tasks
from .load_phenotype_dataframe import load_phenotype_dataframe


def assess_phenotypes(
    sequences: typing.Iterable[str],
    environment_content: str,
    instset_content: str,
) -> pd.DataFrame:

    phenotypes_outpath = tempfile.mktemp()
    num_tasks = count_environment_tasks(environment_content)
    newline_char = "\n"  # no \'s allowed in fstring
    analyze_script = f"""PURGE_BATCH

{newline_char.join(f"LOAD_SEQUENCE {genome}" for genome in sequences)}

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

    return load_phenotype_dataframe(phenotypes_outpath, environment_content)
