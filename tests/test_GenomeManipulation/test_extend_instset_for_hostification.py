from AvidaScripts.GenericScripts.GenomeManipulation import (
    extend_instset_for_hostification,
)


def test_add_newline_if_missing():
    input = "INST Example"
    result = extend_instset_for_hostification(input)
    assert result.endswith("\n")
    assert "INST Example\n" in result
    assert input in result


def test_add_divide_if_missing():
    input = "INST Example\n"
    result = extend_instset_for_hostification(input)
    assert "INST Divide\n" in result
    assert input in result


def test_no_duplicate_divide():
    input = "INST Divide\n"
    result = extend_instset_for_hostification(input)
    assert result.count("INST Divide\n") == 1
    assert input in result


def test_add_nop_x_if_missing():
    input = "INST Example\n"
    result = extend_instset_for_hostification(input)
    assert "INST Nop-X\n" in result
    assert input in result


def test_no_duplicate_nop_x():
    input = "INST Nop-X\n"
    result = extend_instset_for_hostification(input)
    assert result.count("INST Nop-X\n") == 1
    assert input in result


def test_add_both_instructions():
    input = "INST Divide-Erase\n"
    result = extend_instset_for_hostification(input)
    assert result.endswith("INST Divide\nINST Nop-X\n")
    assert input in result


def test_add_divide_in_multiline_content():
    input = "INST A\nINST B\n"
    result = extend_instset_for_hostification(input)
    assert "INST Divide\n" in result
    assert input in result


def test_no_duplicate_divide_in_multiline_content():
    input = "INST A\nINST Divide\nINST B\n"
    result = extend_instset_for_hostification(input)
    assert result.count("INST Divide\n") == 1
    assert input in result


def test_add_nop_x_in_multiline_content():
    input = "INST A\nINST B\n"
    result = extend_instset_for_hostification(input)
    assert "INST Nop-X\n" in result
    assert input in result


def test_no_duplicate_nop_x_in_multiline_content():
    input = "INST A\nINST Nop-X\nINST B\n"
    result = extend_instset_for_hostification(input)
    assert result.count("INST Nop-X\n") == 1
    assert input in result


def test_add_both_instructions_in_multiline_content():
    input = "INST A\nINST B\nINST C\n"
    result = extend_instset_for_hostification(input)
    assert result.endswith("INST Divide\nINST Nop-X\n")
    assert input in result
