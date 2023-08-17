import pytest

from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    make_named_instset_path,
    get_named_instset_content,
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    calc_num_twostep_pointmuts,
    get_twostep_pointmut_neighborhood,
)


@pytest.mark.parametrize("sequence", ["", "a", "b", "aa", "abab", "abaaa"])
def test_calc_num_twostep_pointmuts(sequence: str):
    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    num_insts = get_named_instset_content("transsmt").count("\nINST ")

    neighborhood = get_twostep_pointmut_neighborhood(sequence, manipulator)
    actual_num = sum(step == 2 for seq, step in neighborhood.items())
    expected_num = calc_num_twostep_pointmuts(len(sequence), num_insts)
    assert actual_num == expected_num
