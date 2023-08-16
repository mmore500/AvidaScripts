from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    count_environment_tasks,
    get_named_environment_content,
)


def test_get_named_environment_content():
    top25_content = get_named_environment_content("top25")
    assert count_environment_tasks(top25_content) == 25
