import math

import pytest

from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    make_named_instset_path,
    get_named_instset_content,
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    get_onestep_pointmut_neighborhood,
    get_twostep_pointmut_neighborhood,
)


@pytest.mark.parametrize("sequence", ["", "a", "b", "aa", "abab"])
def test_get_twostep_pointmut_neighborhood(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    num_insts_in_set = get_named_instset_content("transsmt").count("\nINST ")

    neighborhood = get_twostep_pointmut_neighborhood(sequence, manipulator)

    onestep_neighborhood = get_onestep_pointmut_neighborhood(
        sequence,
        manipulator,
    )
    assert {*onestep_neighborhood.keys()} <= {*neighborhood.keys()}

    assert sequence in neighborhood
    assert all(0 <= step <= 2 for step in neighborhood.values())
    if len(sequence) > 1:
        assert all(x in neighborhood.values() for x in range(3))

    for neighbor, step in neighborhood.items():
        assert sum(a != b for a, b in zip(sequence, neighbor)) == step

    num_site_pairs = math.comb(len(sequence), 2)
    num_twostep_pairs = num_site_pairs * (num_insts_in_set - 1) ** 2
    expected_neighborhood_size = num_twostep_pairs + len(onestep_neighborhood)
    assert len(neighborhood) == expected_neighborhood_size
