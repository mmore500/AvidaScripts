import pandas as pd


def couple_colocal_taxa(
    phylogeny_df: pd.DataFrame,
    mutate: bool = False,
) -> pd.DataFrame:
    """Filter for taxa with known snapshot location between epochs and group
    taxa sharing same cell together.

    Colocal taxa are assigned the same "colocal_uid".

    Parameters
    ----------
    phylogeny_df : pd.DataFrame
        Deserialized spop data from `load_population_dataframe` or
        `stitch_population_phylogenies`.
    mutate : bool, default False
        Are side effects on the input dataframes allowed?

    Returns
    -------
    pandas.DataFrame
        Stitched phylogeny in alife standard format.
    """

    if not mutate:
        phylogeny_df = phylogeny_df.copy()

    if "epoch" not in phylogeny_df:
        phylogeny_df["epoch"] = 0

    # drop taxa that weren't alive for epoch-to-epoch transitions
    drop_mask = phylogeny_df["Number of currently living organisms"] == 0
    extant_df = phylogeny_df.loc[~drop_mask].drop(
        ["ancestor_id", "ancestor_list"], axis="columns", errors="ignore"
    )

    # ensure cell ids work as expected
    assert (
        extant_df["Occupied Cell IDs"].str.count(",")
        == extant_df["Number of currently living organisms"] - 1
    ).all()

    extant_df["site"] = extant_df["Occupied Cell IDs"].str.split(",")

    bysite_df = extant_df.explode("site", ignore_index=True).drop(
        "Occupied Cell IDs", axis="columns"
    )
    bysite_df["colocal_uid"] = bysite_df.groupby(["site", "epoch"]).ngroup()

    # check that two taxa with same role aren't occupying same site
    if "role" in bysite_df:
        assert (bysite_df.groupby(["colocal_uid", "role"]).size() == 1).all()

    return bysite_df
