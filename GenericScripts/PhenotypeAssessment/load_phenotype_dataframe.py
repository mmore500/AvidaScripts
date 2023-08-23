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
    # check that num_tasks matches num cols in file
    try:
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
                .dropna(axis=1, how="all")  # b/c trailing space -> empty col
                .columns,
            )
            or len(
                pd.read_csv(
                    phenotype_path,
                    comment="#",
                    index_col=False,
                    sep=" ",
                )
            )
            == 0
        )
    except pd.errors.EmptyDataError:
        pass

    # load data from file
    names = [
        *["Genome Sequence", "Viable"],
        *[f"Trait {i}" for i in range(num_tasks)],
    ]
    res = pd.read_csv(
        phenotype_path,
        comment="#",
        index_col=False,
        names=names,
        sep=" ",
    ).fillna(
        {"Genome Sequence": ""},  # prevent empty genome seq from becoming nan
    )

    assert res["Viable"].astype(int).isin([0, 1]).all(), (
        phenotype_path,
        res[~res["Viable"].astype(int).isin([0, 1])]["Viable"].tolist()
    )

    for i in range(num_tasks):
        col = f"Trait {i}"
        assert res[col].astype(int).isin([0, 1]).all(), (
            phenotype_path,
            col,
            res[~res[col].astype(int).isin([0, 1])][col].tolist(),
        )  # noqa fmt

    if len(res):
        # because trailing space -> empty col
        res.dropna(axis=1, how="all", inplace=True)

    assert "Genome Sequence" in res.columns

    # postprocess to add calculated columns
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
