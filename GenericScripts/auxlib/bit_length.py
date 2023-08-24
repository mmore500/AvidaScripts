def _calc_bit_length(i: int) -> int:
    """Count up the bit length of binary representation of i with a loop."""
    length = 0
    i = abs(i)
    while i:
        i >>= 1
        length += 1

    return length


def bit_length(i: int) -> int:
    """Count up the bit length of binary representation of i using built-in
    method, falling back to manual implementation if necessary."""
    try:
        return int(i).bit_length()
    except AttributeError:
        return _calc_bit_length(i)
