import os

import pytest

from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    make_named_instset_path,
    get_named_instset_content,
)
from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    assess_mutational_neighborhood_phenotypes,
    get_named_environment_content,
    summarize_mutational_neighborhood_phenotypes,
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    get_onestep_pointmut_neighborhood,
    get_twostep_pointmut_neighborhood,
)


@pytest.mark.parametrize("sequence", ["", "a", "b", "aa", "abab"])
def test_onestep_pointmut_neighborhood(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))

    neighborhood = get_onestep_pointmut_neighborhood(sequence, manipulator)
    phenotype_df = assess_mutational_neighborhood_phenotypes(
        neighborhood,
        get_named_environment_content("top25"),
        get_named_instset_content("transsmt"),
    )

    summarized_df = summarize_mutational_neighborhood_phenotypes(phenotype_df)
    assert len(summarized_df) == phenotype_df["Mutational Distance"].nunique()


@pytest.mark.parametrize("sequence", ["", "a", "b", "aa", "abab"])
def test_twostep_pointmut_neighborhood(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    neighborhood = get_twostep_pointmut_neighborhood(sequence, manipulator)

    phenotype_df = assess_mutational_neighborhood_phenotypes(
        neighborhood,
        get_named_environment_content("top25"),
        get_named_instset_content("transsmt"),
    )

    summarized_df = summarize_mutational_neighborhood_phenotypes(phenotype_df)
    assert len(summarized_df) == phenotype_df["Mutational Distance"].nunique()
