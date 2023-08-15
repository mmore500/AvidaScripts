import typing

from ..GenomeManipulation import GenomeManipulator


def get_onestep_pointmut_neighborhood(
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

    # dict of genomes -> mutational step
    mutants_1_step = {
        neighbor: 1  # noqa fmt
        for neighbor in manipulator.generate_all_point_mutants(sequence)
    }

    # Ancestral state is NOT a mutant
    return {
        **mutants_1_step,
        **{sequence: 0},
    }
