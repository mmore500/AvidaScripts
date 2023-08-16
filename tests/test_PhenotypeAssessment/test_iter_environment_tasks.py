from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    count_environment_tasks,
    get_named_environment_content,
    iter_environment_tasks,
)


def test_get_named_environment_content():
    top25_content = get_named_environment_content("top25")
    num_tasks = count_environment_tasks(top25_content)
    assert num_tasks == len([*iter_environment_tasks(top25_content)])
    first, second, *__, last = iter_environment_tasks(top25_content)
    assert first == "NAND"
    assert second == "NOT"
    assert last == "LOG3CC"
