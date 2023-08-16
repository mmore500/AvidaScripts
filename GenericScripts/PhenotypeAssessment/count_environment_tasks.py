from .get_named_environment_content import get_named_environment_content


def count_environment_tasks(environment_content: str) -> str:
    """Get config file content for named instset."""
    return environment_content.count("REACTION ")
