import random
import typing
import warnings

from ..GenomeManipulation import GenomeManipulator
from .calc_num_twostep_pointmuts import calc_num_twostep_pointmuts


def sample_twostep_pointmuts(
    sequence: str,
    manipulator: GenomeManipulator,
    n: int = 10000,
    seed: int = 1,
) -> typing.Dict[str, int]:
    """Sample n point mutants two steps from the reference sequence.

    Parameters
    ----------
    sequence : str
        A string of char representations of each instruction.

        Avida often reports back these genomic sequences which are based on
        assigning instructions in the instruction set a single char
        representation as shorthand.

    manipulator : GenomeManipulator
        An instance of GenomeManipulator initialized with the reference
        sequence's instruction set.

    n : int, default 10000
        Number observations to sample.

    Returns
    -------
    dict
        Mutant sequences and corresponding (lowest) point mutation distance to
        sequence.

        All point mutation distances will be 2.

    Notes
    -----
    Sample is determinsistic --- without specificying seed, the same smaple
    will always be returned.
    """
    alphabet = [*manipulator.inst_hash]
    num_twostep_pointmuts = calc_num_twostep_pointmuts(
        len(sequence),
        len(alphabet),
    )
    if n > num_twostep_pointmuts:
        raise ValueError("More samples requested than possible mutations.")
    elif n * 2 > num_twostep_pointmuts:
        warnings.warn(
            "Sampling more than half possible mutations may be inefficient.",
        )

    local_random = random.Random(seed)

    res = {}
    while len(res) < n:
        num_sites = len(sequence)
        low_site, high_site = sorted(local_random.sample(range(num_sites), 2))

        assert len(alphabet) > 1
        while True:
            low_char = local_random.choice(alphabet)
            if sequence[low_site] != low_char:
                break
        while True:
            high_char = local_random.choice(alphabet)
            if sequence[high_site] != high_char:
                break

        mutant = f"""{
            sequence[:low_site]
        }{
            low_char
        }{
            sequence[low_site + 1:high_site]
        }{
            high_char
        }{
            sequence[high_site + 1:]
        }"""
        assert mutant != sequence
        assert len(mutant) == len(sequence)
        res[mutant] = 2

    return res
