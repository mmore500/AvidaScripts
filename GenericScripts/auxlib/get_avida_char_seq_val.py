import string


def get_avida_char_seq_val(i: int) -> str:
    """Returns the i-th character in the sequence a-z followed by A-Z.

    Parameters
    ----------
    i : int
        Index in the sequence.

    Returns
    -------
    str
        Character at the given index.

    Raises
    ------
    ValueError
        If i greater than 51.
    """
    if i < 26:
        return string.ascii_lowercase[i]
    elif i < 26 + 26:
        return string.ascii_uppercase[i - 26]
    else:
        raise ValueError
