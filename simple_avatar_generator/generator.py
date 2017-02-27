from random import randint

from PIL import Image, ImageDraw, ImageFilter


class Field(object):

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class TypeIntRequiredField(Field):
    def __set__(self, instance, value):

        if type(value) != int:
            raise TypeError(f'Value for {self.name} may be only int type.')

        super(TypeIntRequiredField, self).__set__(instance, value)


class MinValueField(Field):
    min_value = None

    def __set__(self, instance, value):

        if value < self.min_value:
            raise ValueError(f'Min value for {self.name} is {self.min_value}.')

        super(MinValueField, self).__set__(instance, value)


class SideSizesField(TypeIntRequiredField, MinValueField):
    min_value = 4


class SquaresQuantityOnAxisField(TypeIntRequiredField, MinValueField):
    min_value = 1


class BlurRadiusField(TypeIntRequiredField, MinValueField):
    min_value = 0


class RotateField(TypeIntRequiredField):
    pass


class AvatarGenerator(object):
    side_sizes = SideSizesField()
    squares_quantity_on_axis = SquaresQuantityOnAxisField()
    blur_radius = BlurRadiusField()
    rotate = RotateField()

    def __init__(self, side_sizes, squares_quantity_on_axis=randint(3, 4),
                 blur_radius=3, rotate=randint(0, 360)):
        self.side_sizes = side_sizes
        self.blur_radius = blur_radius
        self.rotate = rotate
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

        self.img = self.img.rotate(self.rotate)
        self.img = self.img.crop((
            self.side_sizes / 4,
            self.side_sizes / 4,
            self.side_sizes - self.side_sizes / 4,
            self.side_sizes - self.side_sizes / 4
        ))
        self.img = self.img.filter(ImageFilter.GaussianBlur(self.blur_radius))

        return self.img
