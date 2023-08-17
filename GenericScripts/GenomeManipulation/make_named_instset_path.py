from .get_named_instset_content import get_named_instset_content
from .make_instset_path import make_instset_path


def make_named_instset_path(instset_name: str) -> str:
    """Write instset content to a tempfile and return the path."""
    instset_content = get_named_instset_content(instset_name)
    return make_instset_path(instset_content)
