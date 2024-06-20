from django.core.exceptions import ValidationError


def validate_not_numeric(value  : str):
  if value.isnumeric():
    raise ValidationError(f'{value} is numeric and should not be used as a value for this field')