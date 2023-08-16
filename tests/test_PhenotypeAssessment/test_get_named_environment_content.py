from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    get_named_environment_content,
)


def test_get_named_environment_content():
    top25_content = get_named_environment_content("top25")
    assert "RESOURCE resECHO:inflow=125:outflow=0.10\n" in top25_content
    assert "\nREACTION LOG3CC logic_3CC process:resource=resECHO:value=0.0:type=add:frac=1.0:min=0:max=1:  requisite:reaction_max_count=1" in top25_content
