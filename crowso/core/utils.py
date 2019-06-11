from django.core.exceptions import ValidationError


def validate_percent(percent):
    if percent > 100:
        raise ValidationError('value {} is more than 100.'.format(percent))
