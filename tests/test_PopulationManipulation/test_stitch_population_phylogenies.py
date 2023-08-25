import os

from hstrat import _auxiliary_lib as hstrat_auxlib
import pytest

from AvidaScripts.GenericScripts.PopulationManipulation import (
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
def test_stitch_population_phylogenies(pop_paths):
    pop_dfs = [*map(load_population_dataframe, pop_paths)]

    stitched_df = stitch_population_phylogenies(pop_dfs)

    assert hstrat_auxlib.alifestd_validate(stitched_df)

    num_initial_roots = (
        pop_dfs[0]["Parent ID(s)"]
        .str.contains(
            "(none)",
            regex=False,
        )
        .sum()
    )
    num_stitched_roots = len(hstrat_auxlib.alifestd_find_root_ids(stitched_df))
    assert num_initial_roots == num_stitched_roots

    assert hstrat_auxlib.alifestd_validate(stitched_df)
