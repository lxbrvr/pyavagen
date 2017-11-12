from pyavagen.version import *  # noqa
from pyavagen.generators import (
    COLOR_LIST_FLAT,
    COLOR_LIST_MATERIAL,
    SquareAvatar,
    CharSquareAvatar,
    CharAvatar,
)

__all__ = [
    'Avatar',
    'SQUARE_AVATAR',
    'CHAR_SQUARE_AVATAR',
    'CHAR_AVATAR',
    'COLOR_LIST_MATERIAL',
    'COLOR_LIST_FLAT',
]

SQUARE_AVATAR = 'square'
CHAR_AVATAR = 'char'
CHAR_SQUARE_AVATAR = 'char_square'


class Avatar(object):

    """Factory of avatar classes.

    Args:
        avatar_class: a class that generates an avatar.
        kwargs: keyword arguments are passed to specified avatar_class.

    """

    AVATAR_MAP = {
        SQUARE_AVATAR: SquareAvatar,
        CHAR_AVATAR: CharAvatar,
        CHAR_SQUARE_AVATAR: CharSquareAvatar,
    }

    def __init__(self, avatar_type, **kwargs):

        self.avatar_class = self.AVATAR_MAP.get(avatar_type, None)

        if not self.avatar_class:
            raise AttributeError('The passed avatar type not found.')

        self.avatar_class = self.avatar_class(**kwargs)
        self.kwargs = kwargs

    def generate(self):
        """Implements calling an generate method in specified avatar_class."""

        return self.avatar_class.generate()
