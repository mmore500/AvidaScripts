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
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    get_onestep_pointmut_neighborhood,
    get_twostep_pointmut_neighborhood,
)


@pytest.mark.parametrize("sequence", ["", "a", "b", "aa", "abab", None])
def test_onestep_pointmut_neighborhood(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))

    if sequence is not None:
        neighborhood = get_onestep_pointmut_neighborhood(sequence, manipulator)
    else:
        neighborhood = dict()
    phenotypes_df = assess_mutational_neighborhood_phenotypes(
        neighborhood,
        get_named_environment_content("top25"),
        get_named_instset_content("transsmt"),
    )
    if sequence is not None:
        assert sequence in neighborhood
    assert all(0 <= step <= 1 for step in neighborhood.values())

    for __, row in phenotypes_df.iterrows():
        neighbor = row["Genome Sequence"]
        step = row["Mutational Distance"]
        assert sum(a != b for a, b in zip(sequence, neighbor)) == step

    assert len(phenotypes_df) == len(neighborhood)


@pytest.mark.parametrize("sequence", ["", "a", "b", "aa", "abab", None])
def test_twostep_pointmut_neighborhood(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))

    if sequence is not None:
        neighborhood = get_twostep_pointmut_neighborhood(sequence, manipulator)
    else:
        neighborhood = dict()
    phenotypes_df = assess_mutational_neighborhood_phenotypes(
        neighborhood,
        get_named_environment_content("top25"),
        get_named_instset_content("transsmt"),
    )
    if sequence is not None:
        assert sequence in neighborhood
    assert all(0 <= step <= 2 for step in neighborhood.values())

    for __, row in phenotypes_df.iterrows():
        neighbor = row["Genome Sequence"]
        step = row["Mutational Distance"]
        assert sum(a != b for a, b in zip(sequence, neighbor)) == step

    assert len(phenotypes_df) == len(neighborhood)


@pytest.mark.parametrize("assess_parasites", ["hostify", "simulate"])
def test_twostep_pointmut_neighborhood_parasite(assess_parasites: str):

    sequence = "aba"
    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    neighborhood = get_twostep_pointmut_neighborhood(sequence, manipulator)

    phenotypes_df = assess_mutational_neighborhood_phenotypes(
        neighborhood,
        get_named_environment_content("top25"),
        get_named_instset_content("transsmt"),
        assess_parasites=assess_parasites,
    )
    assert sequence in neighborhood
    assert all(0 <= step <= 2 for step in neighborhood.values())

    for __, row in phenotypes_df.iterrows():
        neighbor = row["Genome Sequence"]
        step = row["Mutational Distance"]
        assert sum(a != b for a, b in zip(sequence, neighbor)) == step

    assert len(phenotypes_df) == len(neighborhood)
