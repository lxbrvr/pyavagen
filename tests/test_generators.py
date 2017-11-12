from PIL import Image
import pytest
import pyavagen
from pyavagen import validators, generators


class TestAvatar:
    @pytest.mark.parametrize(
        argnames="avatar_type,avatar_class,avatar_kwargs",
        argvalues=[
            (pyavagen.CHAR_AVATAR, pyavagen.CharAvatar, {'string': 'string'}),
            (pyavagen.SQUARE_AVATAR, pyavagen.SquareAvatar, {}),
            (pyavagen.CHAR_SQUARE_AVATAR, pyavagen.CharSquareAvatar, {
                'string': 'string',
            }),
        ]
    )
    def test_avatar_class_arg(self, avatar_type, avatar_class, avatar_kwargs):
        """
        'avatar_class' argument should return an avatar class defined
        to an avatar type.
        If a passed avatar type is undefined in 'Avatar' class then should
        raise AttributeError.
        """

        avatar_kwargs.update({
            'avatar_type': avatar_type,
            'size': 2,
        }),

        avatar = pyavagen.Avatar(**avatar_kwargs)
        assert isinstance(avatar.avatar_class, avatar_class)

    def test_avatar_class_arg_with_none(self):
        """
        Should raise AttributeError if a passed avatar class is None.
        """

        with pytest.raises(AttributeError):
            pyavagen.Avatar(avatar_type=None)

    @pytest.mark.parametrize(
        argnames="avatar_type,avatar_kwargs",
        argvalues=[
            (pyavagen.CHAR_AVATAR, {'string': 'string'}),
            (pyavagen.SQUARE_AVATAR, {}),
            (pyavagen.CHAR_SQUARE_AVATAR, {'string': 'string'}),
        ]
    )
    def test_generate_method(self, avatar_type, avatar_kwargs):
        """
        'generate' method of 'Avatar' class should return Image.Image object.
        """

        avatar_kwargs.update({
            'avatar_type': avatar_type,
            'size': 2,
        }),

        avatar = pyavagen.Avatar(**avatar_kwargs)

        assert isinstance(avatar.generate(), Image.Image)


class TestColorListMixin:
    @pytest.mark.parametrize(
        argnames="color_list",
        argvalues=[
            None,
            generators.COLOR_LIST_FLAT,
            generators.COLOR_LIST_MATERIAL,
        ]
    )
    def test_get_random_color_method(self, color_list):
        """Should return string that contains a color value."""

        color_list_object = generators.ColorListMixin(color_list=color_list)
        color_validator = validators.ColorValidator()(
            value=color_list_object.get_random_color(),
            field_name='field',
        )

        assert color_validator is None


class TestSquareAvatar:
    @pytest.fixture(scope="module")
    def avatar_data(self):
        return dict(
            size=4,
            border_color='black',
            blur_radius=2,
            border_size=2,
            rotate=2,
            squares_on_axis=2,
            color_list=pyavagen.COLOR_LIST_MATERIAL,
        )

    @pytest.fixture(scope="module")
    def avatar_object(self, avatar_data):
        return generators.SquareAvatar(**avatar_data)

    def test_compare_attributes_with_passed_values(
            self,
            avatar_object,
            avatar_data):
        assert avatar_object.size == avatar_data['size']
        assert avatar_object.color_list == avatar_data['color_list']
        assert avatar_object.border_color == avatar_data['border_color']
        assert avatar_object.border_size == avatar_data['border_size']
        assert avatar_object.blur_radius == avatar_data['blur_radius']
        assert avatar_object.rotate == avatar_data['rotate']
        assert avatar_object.squares_on_axis == avatar_data['squares_on_axis']

    def test_generate_with_full_set(self, avatar_object):
        assert isinstance(avatar_object.generate(), Image.Image)


class TestCharAvatar:
    @pytest.fixture(scope="module")
    def avatar_data(self):
        return dict(
            size=4,
            background_color='black',
            font_size=2,
            font_color='black',
            font_outline=True,
            color_list=pyavagen.COLOR_LIST_MATERIAL,
            string='string',
        )

    @pytest.fixture(scope="module")
    def avatar_object(self, avatar_data):
        return generators.CharAvatar(**avatar_data)

    def test_compare_attributes_with_passed_values(
            self,
            avatar_object,
            avatar_data):
        assert (
            avatar_object.background_color == avatar_data['background_color']
        )
        assert avatar_object.size == avatar_data['size']
        assert avatar_object.font_color == avatar_data['font_color']
        assert avatar_object.font_size == avatar_data['font_size']
        assert avatar_object.font_outline == avatar_data['font_outline']
        assert avatar_object.color_list == avatar_data['color_list']
        assert avatar_object.string == avatar_data['string']

    def test_generate_with_full_set(self, avatar_object):
        assert isinstance(avatar_object.generate(), Image.Image)

    def test_get_text_for_draw_with_one_word(self, avatar_object):
        avatar_object.string = 'One'
        assert avatar_object.get_text_for_draw() == 'O'

    def test_get_text_for_draw_with_two_words(self, avatar_object):
        avatar_object.string = 'One two'
        assert avatar_object.get_text_for_draw() == 'OT'

    def test_get_text_for_draw_with_multiple_words(self, avatar_object):
        avatar_object.string = 'One two free'
        assert avatar_object.get_text_for_draw() == 'OT'


class TestCharSquareAvatar:
    @pytest.fixture(scope="module")
    def avatar_data(self):
        return dict(
            size=4,
            background_color='black',
            font_size=2,
            font_color='black',
            font_outline=True,
            color_list=pyavagen.COLOR_LIST_MATERIAL,
            string='string',
            border_color='black',
            blur_radius=2,
            border_size=2,
            rotate=2,
            squares_on_axis=2,
        )

    @pytest.fixture(scope="module")
    def avatar_object(self, avatar_data):
        return generators.CharSquareAvatar(**avatar_data)

    def test_compare_attributes_with_passed_values(
            self,
            avatar_object,
            avatar_data):
        assert (
            avatar_object.background_color == avatar_data['background_color']
        )
        assert avatar_object.size == avatar_data['size']
        assert avatar_object.font_color == avatar_data['font_color']
        assert avatar_object.font_size == avatar_data['font_size']
        assert avatar_object.font_outline == avatar_data['font_outline']
        assert avatar_object.color_list == avatar_data['color_list']
        assert avatar_object.string == avatar_data['string']
        assert avatar_object.border_color == avatar_data['border_color']
        assert avatar_object.border_size == avatar_data['border_size']
        assert avatar_object.blur_radius == avatar_data['blur_radius']
        assert avatar_object.rotate == avatar_data['rotate']
        assert avatar_object.squares_on_axis == avatar_data['squares_on_axis']

    def test_generate_with_full_set(self, avatar_object):
        assert isinstance(avatar_object.generate(), Image.Image)
