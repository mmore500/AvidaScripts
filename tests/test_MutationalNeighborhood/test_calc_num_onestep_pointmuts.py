import pytest

from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    make_named_instset_path,
    get_named_instset_content,
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    calc_num_onestep_pointmuts,
    get_onestep_pointmut_neighborhood,
)


@pytest.mark.parametrize("sequence", ["", "a", "b", "aa", "abab", "abaaa"])
def test_calc_num_onestep_pointmuts(sequence: str):
    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
    num_insts = get_named_instset_content("transsmt").count("\nINST ")

    neighborhood = get_onestep_pointmut_neighborhood(sequence, manipulator)
    expected_num = calc_num_onestep_pointmuts(len(sequence), num_insts)
    # -1 excludes original sequence
    assert len(neighborhood) - 1 == expected_num
