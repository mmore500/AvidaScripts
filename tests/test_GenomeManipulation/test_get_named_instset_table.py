from AvidaScripts.GenericScripts.GenomeManipulation import (
    get_named_instset_table,
)


def test_get_named_instset_table():
    table = get_named_instset_table()
    assert "transsmt" in table
    assert "INSTSET transsmt:hw_type=2\n" in table["transsmt"]
    assert "\nINST Divide-Erase" in table["transsmt"]
