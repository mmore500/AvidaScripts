def _calc_bit_count(i: int) -> int:
    """Count up the number of set bits with a loop."""
    count = 0
    i = abs(i)
    while i:
        count += i & 1
        i >>= 1

    return count

def bit_count(i: int) -> int:
    """Calculate number of set bits in an integer using the built-in method,
    falling back to a manual implementation if necessary."""
    try:
        return int(i).bit_count()
    except AttributeError:
        return _calc_bit_count(i)
