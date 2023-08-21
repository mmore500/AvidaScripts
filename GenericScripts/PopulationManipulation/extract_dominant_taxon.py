import typing

import pandas as pd


def extract_dominant_taxon(
    population_df: pd.DataFrame,
    role: typing.Literal["host", "parasite"],
) -> dict:
    """Extract taxon entry in spop dataframe with most currently living
    organisms.

    Parameters
    ----------
    population_df : pd.DataFrame
        Deserialized spop file, from `load_population_dataframe`.
    role : {'host', 'parasite'}
        Should the taxon dominant among hosts or parasites be loaded?

    Returns
    -------
    dict
        Dictionary of data for the dominant taxon of the specified role.
    """

    domidx = population_df[population_df["role"] == role][
        "Number of currently living organisms"
    ].idxmax()
    return population_df.loc[domidx].to_dict()
