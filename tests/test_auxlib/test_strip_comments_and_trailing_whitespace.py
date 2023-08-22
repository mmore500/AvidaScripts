from AvidaScripts.GenericScripts.auxlib import (
    strip_comments_and_trailing_whitespace,
)


def test_nop():
    strip_comments_and_trailing_whitespace("Ho;wdy") == "Ho;wdy"
    strip_comments_and_trailing_whitespace(" Howdy") == " Howdy"


def test_strip_comments():
    assert strip_comments_and_trailing_whitespace("Hello # Comment") == "Hello"
    assert (
        strip_comments_and_trailing_whitespace("Hello World!  # Another comment")
        == "Hello World!"
    )


def test_strip_whitespace():
    assert strip_comments_and_trailing_whitespace("Hello   ") == "Hello"
    assert strip_comments_and_trailing_whitespace("  Hello   ") == "  Hello"


def test_strip_comments_and_whitespace():
    assert (
        strip_comments_and_trailing_whitespace(
            "Hello   # Comment here",
        )
        == "Hello"
    )
