import json
import os
from pathlib import Path

from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    make_named_instset_path,
)


def test_GenomeManipulator():
    instset_path = make_named_instset_path("transsmt")
    manipulator = GenomeManipulator(instset_path)
    assert manipulator.sequence_to_genome("ab") == ["Nop-A", "Nop-B"]

    all_point_mutants = manipulator.generate_all_point_mutants("ab")
    assert all(len(seq) == 2 for seq in all_point_mutants)
    assert "ab" not in all_point_mutants
    assert len(all_point_mutants) >= len("ab")

    all_mutants = manipulator.generate_all_mutants("ab")
    assert "ab" not in all_mutants
    assert not all(len(seq) == 2 for seq in all_mutants)
    assert all(1 <= len(seq) <= 3 for seq in all_mutants)
    assert len(all_mutants) > len("ab")
    assert set(all_mutants) > set(all_point_mutants)


def test_hostify_parasite_genome():
    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))

    input_path = f"{os.path.dirname(__file__)}/assets/parasite-genome.json"
    input = json.loads(Path(input_path).read_text())

    expected_output_path = (
        f"{os.path.dirname(__file__)}/assets/hostified-parasite-genome.json"
    )
    expected_output = json.loads(Path(expected_output_path).read_text())

    assert manipulator.hostify_parasite_genome(input) == expected_output


def test_hostify_parasite_sequence():
    manipulator = GenomeManipulator(make_named_instset_path("transsmt"))

    input_path = f"{os.path.dirname(__file__)}/assets/parasite-genome.json"
    input_genome = json.loads(Path(input_path).read_text())
    input_sequence = manipulator.genome_to_sequence(input_genome)

    expected_output_path = (
        f"{os.path.dirname(__file__)}/assets/hostified-parasite-genome.json"
    )
    expected_output_genome = json.loads(Path(expected_output_path).read_text())
    expected_output_sequence = manipulator.genome_to_sequence(
        expected_output_genome,
    )

    assert (
        manipulator.hostify_parasite_sequence(input_sequence)
        == expected_output_sequence
    )  # noqa fmt
