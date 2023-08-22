import re

from ..auxlib import strip_comments_and_trailing_whitespace


def make_hostification_instset(instset_content: str) -> str:
    """Extend instset with Divide and Nop-X instructions, if necessary."""

    if not instset_content.endswith("\n"):
        instset_content += "\n"

    if not re.search(r"^INST Divide$", instset_content, re.MULTILINE):
        instset_content += "INST Divide\n"

    if not re.search(r"^INST Nop-X$", instset_content, re.MULTILINE):
        instset_content += "INST Nop-X\n"

    return instset_content
