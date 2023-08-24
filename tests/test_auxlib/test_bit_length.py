from AvidaScripts.GenericScripts.auxlib import bit_length


def test_bit_length():
    # Test a basic case
    assert bit_length(0b1010) == 4

    # Test a case where no bits are set
    assert bit_length(0b0) == 0

    # Test a case where one bit is set
    assert bit_length(0b1) == 1
    assert bit_length(0b10) == 2

    # Test a case where all bits are set
    assert bit_length(0b1111) == 4

    # Test a random case
    assert bit_length(0b101010101010) == 12
