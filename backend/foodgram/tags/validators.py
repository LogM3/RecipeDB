import re

from django.core.exceptions import ValidationError


def hex_color_validate(value):
    if not re.match(r'^#([A-Fa-f0-9]{6})', value):
        raise ValidationError('Unknown HEX color')
    if len(value) != 7:
        raise ValidationError('HEX color length must be equal 7')
