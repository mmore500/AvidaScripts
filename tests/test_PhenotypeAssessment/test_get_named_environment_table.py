from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    get_named_environment_table,
)


def test_get_named_environment_table():
    table = get_named_environment_table()
    assert "top25" in table
    assert "RESOURCE resECHO:inflow=125:outflow=0.10\n" in table["top25"]
    assert "\nREACTION LOG3CC logic_3CC process:resource=resECHO:value=0.0:type=add:frac=1.0:min=0:max=1:  requisite:reaction_max_count=1" in table["top25"]
