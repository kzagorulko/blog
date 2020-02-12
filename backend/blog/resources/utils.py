def no_spacing_string(max_length=None, min_length=None):
    def validate(value):
        if ' ' in value:
            raise ValueError('There must be no spaces in this field')
        if max_length and len(value) > max_length:
            raise ValueError(
                f'This field must be shorter than {max_length} characters'
            )
        if min_length and len(value) < min_length:
            raise ValueError(
                f'This field must be longer than {min_length} characters'
            )
        return value
    return validate
