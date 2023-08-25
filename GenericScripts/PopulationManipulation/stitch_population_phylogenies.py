from collections import Counter
import copy
import typing
import warnings

import pandas as pd
from hstrat import _auxiliary_lib as hstrat_auxlib


def _check_population_dfs(population_dfs: typing.List[pd.DataFrame]) -> None:
    # all ID's must be unique
    assert all(  # noqa fmt
        population_df["ID"].is_unique for population_df in population_dfs
    )
    # must be asexual: each has only one parent
    assert not any(
        population_df["Parent ID(s)"].str.contains(",").any()
        for population_df in population_dfs
    )

    # parent role must equal child role
    for population_df in population_dfs:
        id_roles = dict(
            zip(
                population_df["ID"],
                population_df["role"],
            ),
        )
        for parent_id, child_role in zip(
            population_df["Parent ID(s)"],
            population_df["role"],
        ):
            if parent_id in id_roles:
                assert id_roles["parent_id"] == child_role


def _setup_calculated_cols(population_dfs: typing.List[pd.DataFrame]) -> None:
    for epoch, population_df in enumerate(population_dfs):
        geneses_mask = population_df["Parent ID(s)"].str.contains(
            "(none)",
            regex=False,
        )
        assert not (population_df["ID"] == -1).any()
        population_df.loc[geneses_mask, "Parent ID(s)"] = "-1"

        population_df["id"] = population_df["ID"].astype(int)
        population_df["ancestor_id"] = population_df["Parent ID(s)"].astype(int)

        # loose ends are taxa with ancestors outside records
        loose_ends = ~population_df["ancestor_id"].isin({*population_df["id"]})
        # should have some loose ends
        assert loose_ends.any() or len(population_df) == 0
        population_df["is loose end"] = loose_ends

        # point loose end (genesis) taxa ancestor ids to themselves
        population_df.loc[loose_ends, "ancestor_id"] = population_df.loc[
            loose_ends, "id"
        ]

        # setup alifestd ancestor_list
        population_df[
            "ancestor_list"  # noqa fmt
        ] = hstrat_auxlib.alifestd_make_ancestor_list_col(
            population_df["id"],
            population_df["ancestor_id"],
        )
        population_df["epoch"] = epoch
        population_df.drop(["ID", "Parent ID(s)"], axis=1, inplace=True)


def stitch_population_phylogenies(
    population_df_sequence: typing.Iterable[pd.DataFrame],
    mutate: bool = False,
) -> pd.DataFrame:
    """Join phylogeny data of spop archives from sequential evolutionary epochs
    based on common genetic sequenes.

    Parameters
    ----------
    population_df_sequence : Iterable[pd.DataFrame]
        Deserialized spop data from `load_population_dataframe`, sequenced
        chronologically.
    mutate : bool, default False
        Are side effects on the input dataframes allowed?

    Returns
    -------
    pandas.DataFrame
        Stitched phylogeny in alife standard format.
    """
    apply = (lambda x: x) if mutate else copy.deepcopy
    population_dfs = [*map(apply, population_df_sequence)]

    # safetcy check data...
    _check_population_dfs(population_dfs)

    # create alias columns...
    _setup_calculated_cols(population_dfs)

    agg_df = hstrat_auxlib.alifestd_aggregate_phylogenies(population_dfs)
    assert hstrat_auxlib.alifestd_validate(agg_df)

    # find all entries to stich together across epochs
    stitches = {}  # map stitch from ids to stitch to ids
    for leading_epoch, following_epoch in hstrat_auxlib.pairwise(
        range(len(population_dfs)),
    ):
        leading_df = agg_df[agg_df["epoch"] == leading_epoch]
        following_df = agg_df[agg_df["epoch"] == following_epoch]

        # check for ambiguities and sort for best bet in ambiguous cases
        extant_seq_counts = Counter(
            leading_df.loc[
                leading_df["Number of currently living organisms"] > 0,
                "Genome Sequence",
            ],
        )
        loose_ends_mask = following_df["is loose end"]
        num_redundancies = sum(
            extant_seq_counts[loose_seq] - 1
            for loose_seq in following_df.loc[
                loose_ends_mask,
                "Genome Sequence",
            ]
            if loose_seq in extant_seq_counts
        )
        if num_redundancies:
            warnings.warn(
                f"epoch {leading_epoch} has "
                f"{num_redundancies} ambiguous redundant sequences",
            )
            # dict construction ensures latest take precedent
            leading_df = leading_df.sort_values(
                "Number of currently living organisms",
                ascending=False,
            )

        # record stitches
        leading_seq2id_lookup = dict(
            zip(leading_df["Genome Sequence"], leading_df["id"]),
        )
        loose_ends_mask = following_df["is loose end"]
        for idx, loose_row in following_df[loose_ends_mask].iterrows():
            loose_id = loose_row["id"]
            loose_seq = loose_row["Genome Sequence"]
            if loose_seq in leading_seq2id_lookup:
                stitch_to_id = leading_seq2id_lookup[loose_seq]
                stitches[loose_id] = stitch_to_id

    # check that all loose ends are marked as geneses (ancestry points to self)
    stitch_rows_mask = agg_df["id"].isin(stitches)
    assert (
        agg_df[stitch_rows_mask]["ancestor_id"]  # noqa fmt
        == agg_df[stitch_rows_mask]["id"]
    ).all()

    # perform stitching
    agg_df.loc[stitch_rows_mask, "ancestor_id"] = (
        # this way because inplace option of replace doesn't work here
        agg_df.loc[stitch_rows_mask, "ancestor_id"].replace(stitches)
    )
    # then update ancestor_list to match
    agg_df["ancestor_list"] = hstrat_auxlib.alifestd_make_ancestor_list_col(
        agg_df["id"],
        agg_df["ancestor_id"],
    )

    # warn if any unstitched
    headless_mask = agg_df["epoch"] > 0
    geneses_mask = agg_df["id"] == agg_df["ancestor_id"]
    num_unstitched = (headless_mask & geneses_mask).sum()
    if num_unstitched:
        warnings.warn(
            f"{num_unstitched} unstitched entries "
            f"({len(stitches)} stitched entries)"
        )

    return agg_df
