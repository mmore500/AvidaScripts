import tempfile

from .get_named_instset_content import get_named_instset_content


def make_instset_path(instset_content: str) -> str:
    """Write instset content to a tempfile and return the path."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp:
        temp.write(instset_content)
        return temp.name
