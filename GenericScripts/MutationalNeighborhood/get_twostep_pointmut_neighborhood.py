import copy
import typing

from ..GenomeManipulation import GenomeManipulator
from .get_onestep_pointmut_neighborhood import (
    get_onestep_pointmut_neighborhood,
)


def get_twostep_pointmut_neighborhood(
    sequence: str,
    manipulator: GenomeManipulator,
) -> typing.Dict[str, int]:
    """Enumerate all point mutants within one step of the reference sequence.

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

    Returns
    -------
    dict
        Mutant sequences and corresponding (lowest) point mutation distance to
        sequence.

        Includes the reference sequence.
    """
    one_step_neighborhood = get_onestep_pointmut_neighborhood(
        sequence,
        manipulator,
    )

    res = copy.copy(one_step_neighborhood)
    for one_step_genome, step in one_step_neighborhood.items():
        if step == 0:
            continue
        assert step == 1

        for two_step_genome, step_ in get_onestep_pointmut_neighborhood(
            one_step_genome,
            manipulator,
        ).items():
            if step_ == 0:
                continue
            assert step == 1

            # don't update zero-step, one-step entries
            res.setdefault(two_step_genome, 2)

    return res
