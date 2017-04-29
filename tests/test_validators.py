import pytest
from pyavagen import validators


class TestMinValueValidator:
    def setup(self):
        self.validator = validators.MinValueValidator
        self.field_name = 'Field'
        self.min_value = 2

    def test_value_that_less_than_min(self):
        """
        Should raises ValueError if a passed value is less than minimum value.
        """

        v = self.validator(limit_value = self.min_value)

        with pytest.raises(ValueError):
            v(value=self.min_value - 1, field_name=self.field_name)

    def test_value_that_more_than_min(self):
        """
        Should returns None if a passed value is more than minimum value.
        """

        v = self.validator(limit_value=self.min_value)
        result = v(value=self.min_value + 1, field_name=self.field_name)

        assert result is None

    def test_value_that_is_equal_to_min(self):
        """
        Should returns None if a passed value is equal to minimum value.
        """

        v = self.validator(limit_value=self.min_value)
        result = v(value=self.min_value, field_name=self.field_name)

        assert result is None

    def test_wrong_limit_value(self):
        """
        Should returns TypeError if a passed limit value is wrong type.
        """

        with pytest.raises(TypeError):
            self.validator(limit_value=None)(
                value=self.min_value,
                field_name=self.field_name
            )

    def test_wrong_value(self):
        """
        Should returns TypeError if a passed value is wrong type.
        """

        with pytest.raises(TypeError):
            self.validator(limit_value=self.min_value)(
                value=None,
                field_name=self.field_name
            )


class TestTypeValidator:
    def setup(self):
        self.validator = validators.TypeValidator
        self.field_name = 'Field'

    def test_other_required_type(self):
        """
        Should raises ValueError if the type of a passed
        value is differs from required type.
        """

        v = self.validator(required_type=int)

        with pytest.raises(ValueError):
            v(value=None, field_name=self.field_name)

    def test_right_required_type(self):
        """
        Should return None if the type of a passed value is
        it coincides with the required type.
        """

        v = self.validator(required_type=int)
        result = v(value=1, field_name=self.field_name)

        assert result is None

    def test_wrong_required_type(self):
        """
        Should return TypeError if a passed required type is not type.
        """

        with pytest.raises(TypeError):
            self.validator(required_type=None)(
                value=1,
                field_name=self.field_name
            )


class TestColorValidator:
    def setup(self):
        self.validator = validators.ColorValidator()
        self.field_name = 'Field'
        self.color = '#000000'

    def test_right_color(self):
        """
        Should return None if a passed color is right.
        """

        result = self.validator(value=self.color, field_name=self.field_name)

        assert result is None

    def test_wrong_color(self):
        """
        Should return ValueError if a passed color value is not color.
        """

        with pytest.raises(ValueError):
            self.validator(value=-1, field_name=self.field_name)