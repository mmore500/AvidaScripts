import typing

import pandas as pd

from .assess_phenotypes import assess_phenotypes


def assess_mutational_neighborhood_phenotypes(
    neighborhood_dict: typing.Dict[str, int],
    environment_content: str,
    instset_content: str,
) -> pd.DataFrame:

    phen_df = assess_phenotypes(
        neighborhood_dict.keys(),
        environment_content,
        instset_content,
    )
    if len(phen_df):
        phen_df["Mutational Distance"] = phen_df["Genome Sequence"].map(
            neighborhood_dict,
        )  # noqa fmt

    assert len(phen_df) == len(neighborhood_dict)

    return phen_df
