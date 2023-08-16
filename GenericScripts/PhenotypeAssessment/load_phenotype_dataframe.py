import numpy as np
import pandas as pd

from .count_environment_tasks import count_environment_tasks
from .iter_environment_tasks import iter_environment_tasks


def load_phenotype_dataframe(
    phenotype_path: str,
    environment_content: str,
) -> pd.DataFrame:
    """Deserialze a spop file as Pandas DataFrame.

    Generates additional columns with convenience statistics.
    """

    num_tasks = count_environment_tasks(environment_content)
    assert (
        num_tasks + 2
        == len(
            pd.read_csv(
                phenotype_path,
                comment="#",
                index_col=False,
                nrows=1,
                sep=" ",
            )
            .dropna(axis=1, how="all")  # because trailing space -> empty col
            .columns,
        )
    )

    res = pd.read_csv(
        phenotype_path,
        comment="#",
        index_col=False,
        sep=" ",
        names=[
            "Genome Sequence",  # column 1
            "Viable",  # column 2
        ]
        + [f"Trait {i}" for i in range(num_tasks)],
    ).dropna(  # because trailing space -> empty col
        axis=1, how="all"
    )
    for i, task in enumerate(iter_environment_tasks(environment_content)):
        res[f"Task {task}"] = res[f"Trait {i}"]
    res["Phenotype"] = [
        "inviable"
        if not row["Viable"]
        else "".join(
            str(int(value)) for col, value in row.items() if col.startswith("Trait ")
        )
        for __, row in res.iterrows()
    ]
    res["Num Traits"] = [
        sum(
            int(value)
            for col, value in row.items()
            if col.startswith("Trait ")  # noqa fmt
        )
        for __, row in res.iterrows()
    ]

    return res
