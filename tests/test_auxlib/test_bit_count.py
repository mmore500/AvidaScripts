from AvidaScripts.GenericScripts.auxlib import bit_count


def test_bit_count():
    # Test a basic case
    assert bit_count(0b1010) == 2

    # Test a case where no bits are set
    assert bit_count(0b0) == 0

    # Test a case where one bit is set
    assert bit_count(0b1) == 1
    assert bit_count(0b10) == 1

    # Test a case where all bits are set
    assert bit_count(0b1111) == 4

    # Test a random case
    assert bit_count(0b101010101010) == 6
