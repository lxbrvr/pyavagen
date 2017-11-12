import pytest
from pyavagen import fields, validators


class TestAvatarField:
    def setup(self):
        self.avatar_field = fields.AvatarField()

    @pytest.mark.parametrize(
        argnames="default,result",
        argvalues=[
            (None, None),
            (1, 1),
            (0, 0),
            ('', ''),
            (lambda: 1, 1),
        ]
    )
    def test_get_default_method(self, default, result):
        """
        Should return a default value if it passed else return None.
        If a passed default value is callable then should call it and
        return a result of callable.
        """

        self.avatar_field.default = default
        assert self.avatar_field.get_default() == result

    def test_run_validators(self):
        """
        Checks launch of validators for a passed value.
        """

        min_value_validator = validators.MinValueValidator(limit_value=2)
        self.avatar_field.validators = [min_value_validator]

        with pytest.raises(Exception):
            self.avatar_field.run_validators(value=1)

    @pytest.mark.parametrize(
        argnames="default,value,result",
        argvalues=[
            (1, 2, 2),
            (1, None, 1),
            (None, None, None),
            (None, 1, 1),
        ]
    )
    def test_set_instance_attribute(self, default, value, result):
        """
        A instance attribute should be equal to a passed value or if instance
        attribute is not set, then should equal to a default value.
        """

        avatar_field = fields.AvatarField(default=default)
        avatar = type('Avatar', (object,), {'field': avatar_field})()
        avatar.field = value

        assert avatar.field == result
