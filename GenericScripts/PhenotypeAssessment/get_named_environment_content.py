from .get_named_environment_table import get_named_environment_table


def get_named_environment_content(environment_name: str) -> str:
    """Get config file content for named environment."""
    return get_named_environment_table()[environment_name]
