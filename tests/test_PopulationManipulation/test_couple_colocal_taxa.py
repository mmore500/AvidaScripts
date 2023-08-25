import os

from hstrat import _auxiliary_lib as hstrat_auxlib
import pytest

from AvidaScripts.GenericScripts.PopulationManipulation import (
    couple_colocal_taxa,
    load_population_dataframe,
    stitch_population_phylogenies,
)


@pytest.mark.parametrize(
    "pop_paths",
    [
        [
            f"{os.path.dirname(__file__)}/assets/epoch={epoch}+ext=.spop"
            for epoch in range(4)
        ],
        [f"{os.path.dirname(__file__)}/assets/epoch=0+ext=.spop"],
    ],
)
def test_couple_colocal_taxa(pop_paths):
    pop_dfs = [*map(load_population_dataframe, pop_paths)]

    if len(pop_dfs) == 1:
        (stitched_df,) = pop_dfs
    else:
        stitched_df = stitch_population_phylogenies(pop_dfs)

    stitched_df_ = stitched_df.copy()
    coupled_df = couple_colocal_taxa(stitched_df)

    assert stitched_df.equals(stitched_df_)

    for group, group_df in coupled_df.groupby("colocal_uid"):
        assert group_df["epoch"].nunique() == 1
        assert group_df["site"].nunique() == 1

    id_col = "id" if "id" in stitched_df else "ID"
    assert {*coupled_df[id_col]} < {*stitched_df[id_col]}

    extant_mask = stitched_df["Number of currently living organisms"] > 0
    assert {*coupled_df[id_col]} == {*stitched_df.loc[extant_mask, id_col]}
