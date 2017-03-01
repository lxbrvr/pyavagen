from random import randint

from PIL import Image, ImageDraw, ImageFilter, ImageColor


class MinValueValidator(object):

    def __init__(self, limit_value):
        self.limit_value = limit_value

    def __call__(self, value, field_name):
        if value < self.limit_value:
            raise ValueError(
                f'{field_name} must not be less {self.limit_value}'
            )


class TypeValidator(object):

    def __init__(self, required_type):
        self.required_type = required_type

    def __call__(self, value, field_name):
        if not isinstance(value, self.required_type):
            raise ValueError(
                f'{field_name} must be {self.required_type.__name__} type.'
            )


class ColorValidator(object):

    def __call__(self, value, field_name):
        if value:
            try:
                ImageColor.getcolor(value, 'RGB')
            except Exception as e:
                raise ValueError(f'{field_name} {e}')


class AvatarField(object):

    def __init__(self, validators=None):
        self.validators = validators

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):

        if self.validators:
            for validator in self.validators:
                validator(value, self.name)

        instance.__dict__[self.name] = value


class AvatarGenerator(object):
    side_sizes = AvatarField(
        validators=[
            TypeValidator(int),
            MinValueValidator(4),
        ]
    )
    squares_quantity_on_axis = AvatarField(
        validators=[
            TypeValidator(int),
            MinValueValidator(1),
        ]
    )
    blur_radius = AvatarField(
        validators=[
            TypeValidator(int),
            MinValueValidator(0),
        ]
    )
    rotate = AvatarField(
        validators=[
            TypeValidator(int),
        ]
    )
    border = AvatarField(
        validators=[
            TypeValidator(str),
            ColorValidator(),
        ]
    )

    def __init__(self, side_sizes, squares_quantity_on_axis=None,
                 blur_radius=2, rotate=None, border='black'):
        self.side_sizes = side_sizes
        self.blur_radius = blur_radius
        self.rotate = rotate if rotate else randint(0, 360)
        self.border = border
        self.squares_quantity_on_axis = (
            squares_quantity_on_axis if
            squares_quantity_on_axis else
            randint(3, 4)
        )
        self.distance = self.side_sizes // self.squares_quantity_on_axis
        self.img = Image.new('RGB', (self.side_sizes, self.side_sizes))
        self.draw = ImageDraw.Draw(self.img)

    @staticmethod
    def get_random_color():
        color = '#' + ''.join([f'{randint(0, 255):02X}' for _ in range(3)])
        return color

    def generate(self):
        for i in range(self.side_sizes // self.distance):
            for j in range(self.side_sizes // self.distance):
                self.draw.rectangle(
                    xy=(
                        i * self.distance,
                        j * self.distance,
                        (i + 1) * self.distance,
                        (j + 1) * self.distance
                    ),
                    outline=self.border or None,
                    fill=self.get_random_color())

        self.img = self.img.rotate(self.rotate)
        self.img = self.img.crop((
            self.side_sizes / 4,
            self.side_sizes / 4,
            self.side_sizes - self.side_sizes / 4,
            self.side_sizes - self.side_sizes / 4
        ))
        self.img = self.img.filter(ImageFilter.GaussianBlur(self.blur_radius))

        return self.img
