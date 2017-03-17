import os
import abc
import math
from random import randint, choice

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from pyavagen.validators import (
    TypeValidator,
    ColorValidator,
    MinValueValidator,
)
from pyavagen.utils import get_random_color


class AvatarField(object):

    def __init__(self, validators=None, default=None):
        self.validators = validators
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        value = self.get_default() if not value else value
        self.run_validators(value)
        instance.__dict__[self.name] = value

    def get_default(self):
        """
        Returns the default value for this field.
        """

        if self.default:
            if callable(self.default):
                return self.default()
            return self.default
        return None

    def run_validators(self, value):
        """
        Runs validators for a passed value.
        """

        if value and self.validators:
            for validator in self.validators:
                validator(value, self.name)


class BaseAvatar(metaclass=abc.ABCMeta):

    SIZE_MIN = 4

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
                    fill=get_random_color())

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

    DEFAULT_BACKGROUND_COLOR = get_random_color
    DEFAULT_FONT = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'fonts/Comfortaa-Regular.ttf'
    )

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

    def __init__(self, string, font=None, background_color=None, *args, **kwargs):
        self.background_color = background_color
        super(CharAvatar, self).__init__(*args, **kwargs)
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
        font = ImageFont.truetype(font=self.font, size=int(0.75 * self.size))
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

    def generate(self):
        self.img = SquareAvatar.generate(self)
        self.img = CharAvatar.generate(self)

        return self.img