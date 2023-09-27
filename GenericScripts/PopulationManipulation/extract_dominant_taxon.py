import typing

import pandas as pd


def extract_dominant_taxon(
    population_df: pd.DataFrame,
    role: typing.Literal["host", "parasite"],
    exclude_monolithic: bool = True,
) -> dict:
    """Extract taxon entry in spop dataframe with most currently living
    organisms.

    Excludes genome sequences consisting of only one character (instruction
    type).

    Parameters
    ----------
    population_df : pd.DataFrame
        Deserialized spop file, from `load_population_dataframe`.
    role : {'host', 'parasite'}
        Should the taxon dominant among hosts or parasites be loaded?
    exclude_monolithic : bool, default True
        Should taxa with only one instruction type (i.e., character) in
        sequence be excluded?

        Excludes genomes that have been disabled by complete nopout.

    Returns
    -------
    dict
        Dictionary of data for the dominant taxon of the specified role.
    """

    def test_seq_for_inclusion(seq: str) -> bool:
        if exclude_monolithic:
            return len(set(seq)) > 1
        else:
            return True

    role_mask = population_df["role"] == role
    monolith_mask = population_df["Genome Sequence"].apply(
        test_seq_for_inclusion,
    )
    mask = role_mask & monolith_mask
    if not any(mask):
        raise ValueError(
            f"no eligible population members in {mask=} for {role=} "
            f"in {population_df=} from {role_mask=} and {monolith_mask=}",
        )

    domidx = population_df[mask][
        "Number of currently living organisms"  # noqa: fmt
    ].idxmax()
    return population_df.loc[domidx].to_dict()
