from AvidaScripts.GenericScripts.GenomeManipulation import (
    make_named_instset_path,
)


def test_make_named_instset_path():
    transsmt_path = make_named_instset_path("transsmt")
    with open(transsmt_path) as transsmt_file:
        transsmt_content = transsmt_file.read()
        assert "INSTSET transsmt:hw_type=2\n" in transsmt_content
        assert "\nINST Divide-Erase" in transsmt_content
