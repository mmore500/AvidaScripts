import os

import pytest

from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    make_named_instset_path,
    get_named_instset_content,
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    get_onestep_pointmut_neighborhood,
)


@pytest.mark.parametrize("sequence", ["", "a", "b", "aa", "abab"])
def test_get_onestep_pointmut_neighborhood(sequence: str):

    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    num_insts_in_set = get_named_instset_content("transsmt").count("\nINST ")

    neighborhood = get_onestep_pointmut_neighborhood(sequence, manipulator)

    assert sequence in neighborhood
    assert all(0 <= step <= 1 for step in neighborhood.values())

    for neighbor, step in neighborhood.items():
        assert sum(a != b for a, b in zip(sequence, neighbor)) == step

    # +1 is for original sequence
    expected_neighborhood_size = len(sequence) * (num_insts_in_set - 1) + 1
    assert len(neighborhood) == expected_neighborhood_size
