from .get_named_instset_table import get_named_instset_table


def get_named_instset_content(instset_name: str) -> str:
    """Get config file content for named instset."""
    return get_named_instset_table()[instset_name]
