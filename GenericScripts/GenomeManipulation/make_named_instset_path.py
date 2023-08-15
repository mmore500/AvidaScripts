import tempfile

from .get_named_instset_content import get_named_instset_content


def make_named_instset_path(instset_name: str) -> str:
    """Write instset content to a tempfile and return the path."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp:
        content = get_named_instset_content(instset_name)
        temp.write(content)
        return temp.name
