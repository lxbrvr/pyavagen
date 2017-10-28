class AvatarField(object):
    """Avatar helper.

    Checks and sets a passed value.

    Args:
        validators: list of validators.
            A passed value will be sent to every validator. Order is important.
        default: default value.

    """

    def __init__(self, validators=None, default=None):
        self.validators = validators
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        value = self.get_default() if value is None else value
        self.run_validators(value)
        instance.__dict__[self.name] = value

    def get_default(self):
        """Returns the default value for this field."""

        if self.default is not None:
            if callable(self.default):
                return self.default()
            return self.default
        return None

    def run_validators(self, value):
        """Runs validators for a passed value."""

        if value and self.validators:
            for validator in self.validators:
                validator(value, self.name)
