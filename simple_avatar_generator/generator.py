from PIL import Image, ImageDraw
import random


class ImageSize(object):
    def __get__(self, obj, objtype):
        return self.val

    def __set__(self, obj, val):

        if type(val) != int:
            raise TypeError('Value for side_sizes may be only int.')

        if val < 4:
            raise ValueError('Min value for side_sizes is 4.')

        self.val = val


class SquaresQuantity(object):
    def __get__(self, obj, objtype):
        return self.val

    def __set__(self, obj, val):

        if type(val) != int:
            raise TypeError('Value for squares_quantity may be only int.')

        if val <= 0:
            raise ValueError('Min value for squares_quantity is 1.')

        self.val = val


class AvatarGenerator(object):
    side_sizes = ImageSize()
    squares_quantity_on_axis = SquaresQuantity()

    def __init__(self, side_sizes, squares_quantity_on_axis):
        self.side_sizes = side_sizes
        self.squares_quantity_on_axis = squares_quantity_on_axis
        self.distance = self.side_sizes // self.squares_quantity_on_axis
        self.img = Image.new('RGB', (self.side_sizes, self.side_sizes))
        self.draw = ImageDraw.Draw(self.img)

    @staticmethod
    def get_random_color():
        color = '#' + ''.join([f'{random.randint(0, 255):02X}' for _ in range(3)])
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

        self.img = self.img.rotate(random.randint(0, 360))
        self.img = self.img.crop((
            self.side_sizes / 4,
            self.side_sizes / 4,
            self.side_sizes - self.side_sizes / 4,
            self.side_sizes - self.side_sizes / 4
        ))

        return self.img

    def save(self, filename):
        self.img.save(filename)
