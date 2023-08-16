import re
import typing


def iter_environment_tasks(environment_content: str) -> typing.Iterable[str]:
    """Extract reaction names from environment config in order defined."""
    yield from re.findall(r"REACTION (\S+)", environment_content)
