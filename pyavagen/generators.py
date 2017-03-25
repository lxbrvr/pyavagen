import os
import abc
import math
from random import randint, choice

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from pyavagen.fields import AvatarField
from pyavagen.validators import (
    TypeValidator,
    ColorValidator,
    MinValueValidator,
)
from pyavagen.utils import get_random_hex_color


class BaseAvatar(metaclass=abc.ABCMeta):

    """Abstract class for avatar generators.

    Args:
        size: output image size.

    """

    SIZE_MIN = 1

    size = AvatarField(
        validators=[
            TypeValidator(int),
            MinValueValidator(SIZE_MIN),
        ]
    )

    def __init__(self, size):
        self.size = size
        self.img = self.get_initial_img()

    def get_initial_img(self):
        """
        Returns new PIL.Image.Image object for self.img from __init__ method.
        """

        return Image.new(
            mode='RGB',
            size=tuple([self.size]) * 2,
        )

    @abc.abstractmethod
    def generate(self):
        """
        Generates an image and must returns the PIL.Image.Image object.
        """

        pass


class SquareAvatar(BaseAvatar):

    """Draws squares with different colors.

    Demo:
        ../examples/demo1.png,
        ../examples/demo2.png,
        ../examples/demo3.png.

    Args:
        squares_quantity_on_axis: number of squares on axis. Has a default value.
        blur_radius: blur radius.
        rotate: background rotate. Has a default value.
        square_border: border color of squares.

    """

    BLUR_RADIUS_MIN = 0
    BLUR_RADIUS_DEFAULT = 1

    squares_quantity_on_axis = AvatarField(
        validators=[
            TypeValidator(int),
            MinValueValidator(1),
        ]
    )
    blur_radius = AvatarField(
        default=BLUR_RADIUS_DEFAULT,
        validators=[
            TypeValidator(int),
            MinValueValidator(BLUR_RADIUS_MIN),
        ]
    )
    rotate = AvatarField(
        validators=[
            TypeValidator(int),
        ]
    )
    square_border = AvatarField(
        validators=[
            TypeValidator(str),
            ColorValidator(),
        ]
    )

    def __init__(self, squares_quantity_on_axis=None, blur_radius=None,
                 rotate=None, square_border=None, *args, **kwargs):
        super(SquareAvatar, self).__init__(*args, **kwargs)

        self.blur_radius = blur_radius
        self.square_border = square_border
        self.rotate = rotate if rotate else randint(0, 360)
        self.squares_quantity_on_axis = (
            squares_quantity_on_axis if
            squares_quantity_on_axis else
            randint(3, 4)
        )

    def get_initial_img(self):
        return Image.new(
            mode='RGB',
            size=tuple([self.size * 2]) * 2,
        )

    def generate(self):
        draw = ImageDraw.Draw(self.img)
        size2x = self.size * 2
        square_side_length = size2x // self.squares_quantity_on_axis

        for i in range(size2x // square_side_length):
            for j in range(size2x // square_side_length):
                draw.rectangle(
                    xy=(
                        i * square_side_length,
                        j * square_side_length,
                        (i + 1) * square_side_length,
                        (j + 1) * square_side_length
                    ),
                    outline=self.square_border,
                    fill=get_random_hex_color())

        self.img = self.img.rotate(self.rotate)

        distance_a = math.sqrt(2) * self.size / 2
        distance_b = size2x - self.size - distance_a

        x0 = choice([distance_a, distance_b])
        y0 = choice([distance_a, distance_b])
        x1 = size2x - (size2x - self.size - x0)
        y1 = size2x - (size2x - self.size - y0)

        self.img = self.img.crop(box=(x0, y0, x1, y1))

        self.img = self.img.filter(ImageFilter.GaussianBlur(self.blur_radius))

        return self.img


class CharAvatar(BaseAvatar):

    """Draws a character on background with single color.

    Demo:
        ../examples/demo4.png,
        ../examples/demo5.png.

    Args:
        string: string, the first character of which will be used for displaying
            on generated image.
        font: TrueType or OpenType font file. Has default value.
        background_color: background color. If is None that will be generated
            random color.
        font_size: size of font. Has default value.

    """

    DEFAULT_BACKGROUND_COLOR = get_random_hex_color
    DEFAULT_FONT = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'fonts/Comfortaa-Regular.ttf'
    )
    FONT_SIZE_MIN = 1

    string = AvatarField(
        validators=[
            TypeValidator(str),
        ]
    )
    font = AvatarField(
        default=DEFAULT_FONT,
        validators=[
            TypeValidator(str),
        ]
    )
    background_color = AvatarField(
        default=DEFAULT_BACKGROUND_COLOR,
        validators=[
            TypeValidator(str),
            ColorValidator(),
        ]
    )
    font_size = AvatarField(
        validators=[
            TypeValidator(int),
            MinValueValidator(FONT_SIZE_MIN)
        ]
    )

    def __init__(self, string, font=None, background_color=None,
                 font_size=None, *args, **kwargs):
        self.background_color = background_color
        super(CharAvatar, self).__init__(*args, **kwargs)
        self.font_size = font_size if font_size else int(0.6 * self.size)
        self.font = font
        self.string = string

    def get_initial_img(self):
        img = Image.new(
            mode='RGB',
            size=tuple([self.size]) * 2,
            color=self.background_color,
        )
        return img

    def generate(self):
        draw = ImageDraw.Draw(self.img)
        img_width, img_height = self.img.size
        font = ImageFont.truetype(font=self.font, size=self.font_size)
        char = self.string[0].upper()
        char_width, char_height = font.getsize(char)
        char_offset_by_height = font.getoffset(char)[1]

        char_position = (
            (img_width - char_width) / 2,
            ((img_height - char_height) / 2) - char_offset_by_height / 2
        )
        draw.text(xy=char_position, text=char, font=font)

        return self.img


class CharSquareAvatar(SquareAvatar, CharAvatar):

    """Draws a character on background with squares with different colors.

    Demo:
        ../examples/demo6.png,
        ../examples/demo7.png,
        ../examples/demo8.png,
        ../examples/demo9.png.

    """

    def generate(self):
        self.img = SquareAvatar.generate(self)
        self.img = CharAvatar.generate(self)

        return self.img


class Avagen(object):

    """Factory of avatar classes.

    Args:
        avatar_class: a class that generates an avatar.
        kwargs: keyword arguments are passed to specified avatar_class.

    """

    SQUARE = SquareAvatar
    CHAR = CharAvatar
    CHAR_SQUARE = CharSquareAvatar

    AVATAR_CLASSES = (SQUARE, CHAR_SQUARE, CHAR,)

    def __init__(self, avatar_class, **kwargs):

        if avatar_class not in self.AVATAR_CLASSES:
            raise AttributeError('The passed avatar type not found.')

        self.avatar_class = avatar_class
        self.kwargs = kwargs

    def generate(self):
        """Implements calling an generate method in specified avatar_class."""

        return self.avatar_class(**self.kwargs).generate()