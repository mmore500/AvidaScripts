from AvidaScripts.GenericScripts.GenomeManipulation import (
    get_named_instset_content,
)


def test_get_named_instset_content():
    transsmt_content = get_named_instset_content("transsmt")
    assert "INSTSET transsmt:hw_type=2\n" in transsmt_content
    assert "\nEOF" in transsmt_content
