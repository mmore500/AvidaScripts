import typing

import pandas as pd


def extract_dominant_taxon(
    population_df: pd.DataFrame,
    role: typing.Literal["host", "parasite"],
) -> dict:

    domidx = population_df[
        population_df["role"] == role
    ]["Number of currently living organisms"].idxmax()
    return population_df.loc[domidx].to_dict()
