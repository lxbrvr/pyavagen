from random import randint


def get_random_hex_color():
    """Generates and returns a random hex color."""

    color = '#' + ''.join(['{:02X}'.format(randint(0, 255)) for _ in range(3)])
    return color
