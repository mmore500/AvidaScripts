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
    hostify_sequences: bool = False,
) -> pd.DataFrame:
    """Calculate phenotypes of sequences in a given mutational neighborhood.

    Delegates to `assess_phenotypes`.

    Parameters
    ----------
    neighborhood_dict : typing.Dict[str, int]
        Mapping of genome sequences to mutational distances from reference
        genome.

        See `get_onestep_pointmut_neighborhood` and
        `get_twostep_pointmut_neighborhood`.

    environment_content : str
        Avida environment configuration, specifying available tasks.

    instset_content : str
        Avida instruction set configuration, specifying available instructions.

    hostify_sequences : bool
        Should inject instructions be replaced with divide instructions?

        Makes parasite genomes compatible with Avida analysis mode,

    Returns
    -------
    pd.DataFrame
        Summary of sequence's phenotypes and mutational distances from
        reference genome.

        One row per sequence in `neighborhood_dict`.
    """
    phen_df = assess_phenotypes(
        neighborhood_dict.keys(),
        environment_content,
        instset_content,
        hostify_sequences=hostify_sequences,
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
