import re


def strip_comments_and_trailing_whitespace(content: str) -> str:
    """Remove comments starting with '#' and trailing whitespace from a string.

    Parameters
    ----------
    content : str
        The input string that might contain comments and trailing whitespaces.

    Returns
    -------
    str
        The cleaned string with comments and trailing whitespaces removed.

    Examples
    --------
    >>> remove_comments_and_trailing_whitespace("Hello # Comment")
    'Hello'

    >>> remove_comments_and_trailing_whitespace("Hello   ")
    'Hello'
    """
    # Remove comments starting with #
    content = re.sub(r"#.*", "", content)

    # Remove trailing whitespace from each line
    content = "\n".join(line.rstrip() for line in content.splitlines())

    return content
