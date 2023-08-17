import typing

import pandas as pd

from .assess_phenotypes import assess_phenotypes

from ..GenomeManipulation import count_instset_insts
from ..MutationalNeighborhood.calc_num_onestep_pointmuts import (
    calc_num_onestep_pointmuts,
)
from ..MutationalNeighborhood.calc_num_twostep_pointmuts import (
    calc_num_twostep_pointmuts,
)


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

        (num_sites,) = phen_df["Genome Sequence"].str.len().unique()
        num_insts = count_instset_insts(instset_content)
        phen_df["Num Point Mutations at Distance"] = phen_df[
            "Mutational Distance"  # noqa fmt
        ].map(
            {
                0: 1,  # original seauence
                1: calc_num_onestep_pointmuts(num_sites, num_insts),
                2: calc_num_twostep_pointmuts(num_sites, num_insts),
            },
        )

    assert len(phen_df) == len(neighborhood_dict)

    return phen_df
