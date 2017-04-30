import pytest
from pyavagen import validators, utils


def test_get_random_hex_color():
    """Should return a valid color value."""

    color = utils.get_random_hex_color()

    try:
        validators.ColorValidator()(value=color, field_name='color')
    except ValueError:
        pytest.fail("A passed value to ColorValidator is not color.")
