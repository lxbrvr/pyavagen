from random import randint

from PIL import Image, ImageDraw, ImageFilter


class ValidationField(object):

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class SideSizesField(ValidationField):

    def __set__(self, instance, value):
        if type(value) != int:
            raise TypeError('Value for side_sizes may be only int.')

        if value < 4:
            raise ValueError('Min value for side_sizes is 4.')

        instance.__dict__[self.name] = value


class SquaresQuantityOnAxisField(ValidationField):

    def __set__(self, instance, value):

        if type(value) != int:
            raise TypeError('Value for squares_quantity may be only int.')

        if value <= 0:
            raise ValueError('Min value for squares_quantity is 1.')

        instance.__dict__[self.name] = value


class BlurRadiusField(ValidationField):

    def __set__(self, instance, value):

        if type(value) != int:
            raise TypeError('Value for blur_radius may be only int.')

        if value <= 0:
            raise ValueError('Min value for blur_radius is 0.')

        instance.__dict__[self.name] = value


class AvatarGenerator(object):
    side_sizes = SideSizesField()
    squares_quantity_on_axis = SquaresQuantityOnAxisField()
    blur_radius = BlurRadiusField()

    def __init__(self, side_sizes, squares_quantity_on_axis=randint(3, 4),
                 blur_radius=3):
        self.side_sizes = side_sizes
        self.blur_radius = blur_radius
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
                    fill=self.get_random_color())

        self.img = self.img.rotate(randint(0, 360))
        self.img = self.img.crop((
            self.side_sizes / 4,
            self.side_sizes / 4,
            self.side_sizes - self.side_sizes / 4,
            self.side_sizes - self.side_sizes / 4
        ))

        self.img = self.img.filter(ImageFilter.GaussianBlur(self.blur_radius))

        return self.img
