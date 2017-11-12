import os
import abc
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from pyavagen.fields import AvatarField
from pyavagen.validators import (
    TypeValidator,
    ColorValidator,
    MinValueValidator,
)
from pyavagen.utils import get_random_hex_color


COLOR_LIST_FLAT = [
    '#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e',
    '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#2c3e50',
    '#f1c40f', '#e67e22', '#e74c3c', '#ecf0f1', '#95a5a6',
    '#f39c12', '#d35400', '#c0392b', '#bdc3c7', '#7f8c8d',
]

COLOR_LIST_MATERIAL = [
    '#D32F2F', '#C2185B', '#7B1FA2', '#512DA8', '#303F9F',
    '#1976D2', '#0288D1', '#0097A7', '#00796B', '#388E3C',
    '#689F38', '#AFB42B', '#FBC02D', '#FFA000', '#F57C00',
    '#E64A19', '#5D4037', '#616161', '#455A64', '#333333',
]


class AvatarMeta(type):
    def __new__(mcs, name, bases, attributes):
        cls = super().__new__(mcs, name, bases, attributes)

        for attr, obj in attributes.items():
            if isinstance(obj, AvatarField):
                obj.__set_name__(cls, attr)

        return cls


class CombinedMetaClasses(abc.ABCMeta, AvatarMeta):
    pass


class BaseAvatar(object, metaclass=CombinedMetaClasses):
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
        """Generates an image and must returns the PIL.Image.Image object."""

        pass


class ColorListMixin(object):
    """Mixin for assignment of color set.

    Args:
        color_list: list of colors.
            If it's empty list that will be generates random color.

    """

    COLOR_LIST_DEFAULT = COLOR_LIST_FLAT

    color_list = AvatarField(
        default=COLOR_LIST_DEFAULT,
        validators=[
            TypeValidator((list, tuple)),
        ]
    )

    def __init__(self, color_list=None, *args, **kwargs):
        self.color_list = color_list
        super(ColorListMixin, self).__init__(*args, **kwargs)

    def get_random_color(self):
        """
        Returns random color from self.color_list.
        If self.color_list passed as an empty list then it will
        be generate random color.
        """

        color_list = self.color_list
        color = (
            random.choice(color_list)
            if color_list
            else get_random_hex_color()
        )

        return color


class SquareAvatar(ColorListMixin, BaseAvatar):
    """Draws squares with different colors.

    Args:
        squares_on_axis: number of squares on axis. Has a default value.
        blur_radius: blur radius.
        rotate: background rotate. Has a default value.
        border_size: border size of square.
        border_color: color of border.

    """

    BORDER_COLOR_DEFAULT = 'black'
    BORDER_SIZE_DEFAULT = 0
    BORDER_SIZE_MIN = 0
    BLUR_RADIUS_MIN = 0
    BLUR_RADIUS_DEFAULT = 1

    squares_on_axis = AvatarField(
        default=lambda: random.randint(3, 4),
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
        default=lambda: random.randint(0, 360),
        validators=[
            TypeValidator(int),
        ]
    )
    border_color = AvatarField(
        default=BORDER_COLOR_DEFAULT,
        validators=[
            TypeValidator(str),
            ColorValidator(),
        ]
    )
    border_size = AvatarField(
        default=BORDER_SIZE_DEFAULT,
        validators=[
            TypeValidator(int),
            MinValueValidator(0)
        ]
    )

    def __init__(self, squares_on_axis=None, blur_radius=None,
                 rotate=None, border_size=None,
                 border_color=None, *args, **kwargs):
        self.border_color = border_color
        super(SquareAvatar, self).__init__(*args, **kwargs)

        self.blur_radius = blur_radius
        self.border_size = border_size
        self.rotate = rotate
        self.squares_on_axis = squares_on_axis
        self._squares_colors = []

    def get_initial_img(self):
        return Image.new(
            mode='RGB',
            color=self.border_color,
            size=tuple([self.size * 2]) * 2,
        )

    def _generate_square_color(self):
        """
        Generates colors of squares so that adjacent squares are different.
        Every color saved to self._squares_colors.
        After generation returns latest color from self._squares_colors.
        """

        squares_colors = self._squares_colors
        squares_colors.append(self.get_random_color())

        if squares_colors and len(squares_colors) > 1:
            if squares_colors[-1] == squares_colors[-2]:
                self._squares_colors = squares_colors[:-1]
                self._generate_square_color()

            if len(squares_colors) > self.squares_on_axis:
                upper_adjacent_square = -(self.squares_on_axis + 1)

                if squares_colors[-1] == squares_colors[upper_adjacent_square]:
                    self._squares_colors = squares_colors[:-1]
                    self._generate_square_color()

        return self._squares_colors[-1]

    def generate(self):
        draw = ImageDraw.Draw(self.img)
        size2x = self.size * 2
        square_side_length = size2x // self.squares_on_axis

        for i in range(size2x // square_side_length):
            for j in range(size2x // square_side_length):
                draw.rectangle(
                    xy=(
                        i * square_side_length + self.border_size,
                        j * square_side_length + self.border_size,
                        (i + 1) * square_side_length - self.border_size,
                        (j + 1) * square_side_length - self.border_size,
                    ),
                    fill=self._generate_square_color(),
                )

        self.img = self.img.rotate(self.rotate, resample=Image.BICUBIC)

        distance_a = math.sqrt(2) * self.size / 2
        distance_b = size2x - self.size - distance_a
        x0 = random.uniform(distance_a, distance_b)
        y0 = random.uniform(distance_a, distance_b)
        x1 = size2x - (size2x - self.size - x0)
        y1 = size2x - (size2x - self.size - y0)

        self.img = self.img.crop(box=(x0, y0, x1, y1))

        self.img = self.img.filter(ImageFilter.GaussianBlur(self.blur_radius))

        return self.img


class CharAvatar(ColorListMixin, BaseAvatar):
    """Draws a character on background with single color.

    Args:
        string: string, the first character of which will be used for
            displaying on generated image.
        font: TrueType or OpenType font file. Has default value.
        background_color: background color. If is None that will be generated
            random color.
        font_size: size of font. Has default value.
        font_outline: draw outline to chars or not.

    """

    DEFAULT_FONT = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'fonts/Comfortaa-Regular.ttf'
    )
    FONT_COLOR_DEFAULT = 'white'
    FONT_SIZE_MIN = 1
    FONT_OUTLINE_DEFAULT = False

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
        validators=[
            TypeValidator(str),
            ColorValidator(),
        ]
    )
    font_color = AvatarField(
        default=FONT_COLOR_DEFAULT,
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
    font_outline = AvatarField(
        default=FONT_OUTLINE_DEFAULT,
        validators=[
            TypeValidator(bool),
        ]
    )

    def __init__(self, string, font=None, font_color=None, font_outline=None,
                 background_color=None, font_size=None, *args, **kwargs):
        self.background_color = background_color
        super(CharAvatar, self).__init__(*args, **kwargs)
        self.font_size = font_size if font_size else int(0.6 * self.size)
        self.font = font
        self.font_color = font_color
        self.font_outline = font_outline
        self.string = string

    def get_initial_img(self):
        b_color = self.background_color
        b_color = b_color if b_color else self.get_random_color()

        img = Image.new(
            mode='RGB',
            size=tuple([self.size]) * 2,
            color=b_color,
        )

        return img

    def get_text_for_draw(self):
        """Returns a text in uppercase for draw.text.

        Returns two first chars of two first words that separated whitespaces.
        For example from string 'John Paul' returns  "JP" .
        If passed an one word then returns a first char of this word.
        For example from string 'John' returns  "J" .

        """

        return ''.join([s[0] for s in self.string.split()[:2]]).upper()

    def generate(self):
        draw = ImageDraw.Draw(self.img)
        img_width, img_height = self.img.size
        font = ImageFont.truetype(font=self.font, size=self.font_size)
        text = self.get_text_for_draw()
        text_width, text_height = font.getsize(text)
        text_height_offset = font.getoffset(text)[1]

        x, y = (
            (img_width - text_width) / 2,
            ((img_height - text_height) / 2) - text_height_offset / 2
        )

        if self.font_outline:
            for xy_offset in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                draw.text(xy=xy_offset, text=text, font=font, fill='black')

        draw.text(xy=(x, y), text=text, font=font, fill=self.font_color)

        return self.img


class CharSquareAvatar(SquareAvatar, CharAvatar):
    """Draws a character on background with squares with different colors."""

    def generate(self):
        self.img = SquareAvatar.generate(self)
        self.img = CharAvatar.generate(self)

        return self.img
