from .get_named_environment_content import get_named_environment_content


def count_environment_tasks(environment_content: str) -> str:
    """Count number of tasks defined in environment configuration."""
    return environment_content.count("REACTION ")
