import pytest

from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    make_named_instset_path,
    get_named_instset_content,
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    get_onestep_pointmut_neighborhood,
    get_twostep_pointmut_neighborhood,
    sample_twostep_pointmuts,
)


@pytest.mark.parametrize("sequence", ["aba", "abab"])
def test_sample_twostep_pointmuts(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    num_insts_in_set = get_named_instset_content("transsmt").count("\nINST ")

    onestep_neighborhood = get_onestep_pointmut_neighborhood(
        sequence,
        manipulator,
    )
    twostep_neighborhood = get_twostep_pointmut_neighborhood(
        sequence,
        manipulator,
    )
    expected_superset = {*twostep_neighborhood.items()} - {
        *onestep_neighborhood.items()
    }  # noqa fmt

    twostep_sample = sample_twostep_pointmuts(
        sequence,
        manipulator,
        n=100,
    )
    assert {*twostep_sample.items()} < expected_superset


@pytest.mark.parametrize("sequence", ["", "a", "aba"])
def test_sample_twostep_pointmuts_n_limit(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    with pytest.raises(ValueError):
        sample_twostep_pointmuts(sequence, manipulator, n=10000)


@pytest.mark.parametrize("sequence", ["abab", "ababa"])
def test_sample_twostep_pointmuts_seed(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    assert sample_twostep_pointmuts(
        sequence, manipulator, n=100
    ) == sample_twostep_pointmuts(sequence, manipulator, n=100)
    assert sample_twostep_pointmuts(
        sequence, manipulator, n=100, seed=9
    ) == sample_twostep_pointmuts(sequence, manipulator, n=100, seed=9)
    assert sample_twostep_pointmuts(
        sequence, manipulator, n=100, seed=8
    ) != sample_twostep_pointmuts(sequence, manipulator, n=100, seed=9)
