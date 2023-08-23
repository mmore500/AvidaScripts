import pytest

from AvidaScripts.GenericScripts.auxlib import (
    get_avida_char_seq_val,
)


def test_get_avida_char_seq_val():
    assert get_avida_char_seq_val(0) == "a"
    assert get_avida_char_seq_val(25) == "z"
    assert get_avida_char_seq_val(26) == "A"
    assert get_avida_char_seq_val(51) == "Z"


def test_get_avida_char_seq_val_invalid():
    with pytest.raises(ValueError):
        get_avida_char_seq_val(52)
