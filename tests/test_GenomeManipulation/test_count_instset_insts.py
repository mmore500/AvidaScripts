from AvidaScripts.GenericScripts.GenomeManipulation import (
    count_instset_insts,
    get_named_instset_content,
)


def test_count_instset_insts():
    transsmt_content = get_named_instset_content("transsmt")
    assert count_instset_insts(transsmt_content) == 33
