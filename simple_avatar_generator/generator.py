from random import randint

from PIL import Image, ImageDraw, ImageFilter, ImageColor


class Field(object):

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class RequiredTypeField(Field):
    required_type = None

    def __set__(self, instance, value):
        if not isinstance(value, self.required_type):
            raise TypeError(
                f'{self.name}: may be only {self.required_type} type.'
            )

        instance.__dict__[self.name] = value


class MinValueField(Field):
    min_value = None

    def __set__(self, instance, value):

        if value < self.min_value:
            raise ValueError(
                f'{self.name}: min is {self.min_value}.'
            )

        instance.__dict__[self.name] = value


class SideSizesField(RequiredTypeField, MinValueField):
    required_type = int
    min_value = 4


class SquaresQuantityOnAxisField(RequiredTypeField, MinValueField):
    required_type = int
    min_value = 1


class BlurRadiusField(RequiredTypeField, MinValueField):
    required_type = int
    min_value = 0


class RotateField(RequiredTypeField):
    required_type = int


class BorderField(RequiredTypeField):
    required_type = str

    def __set__(self, instance, value):
        super(BorderField, self).__set__(instance, value)

        if value != '':
            try:
                ImageColor.getcolor(value, 'RGB')
            except Exception as e:
                raise ValueError(f'{self.name}: {e}')

        instance.__dict__[self.name] = value


class AvatarGenerator(object):
    side_sizes = SideSizesField()
    squares_quantity_on_axis = SquaresQuantityOnAxisField()
    blur_radius = BlurRadiusField()
    rotate = RotateField()
    border = BorderField()

    def __init__(self, side_sizes, squares_quantity_on_axis=randint(3, 4),
                 blur_radius=3, rotate=randint(0, 360), border='black'):
        self.side_sizes = side_sizes
        self.blur_radius = blur_radius
        self.rotate = rotate
        self.border = border
        self.squares_quantity_on_axis = squares_quantity_on_axis
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
