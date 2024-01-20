from rest_framework.serializers import ValidationError

from decimal import Decimal


def decimal_choices_validator(value):
    if value not in [Decimal(str(i/2)) for i in range(1, 11)]:
        raise ValidationError("rate not in range:", [i/2 for i in range(1, 11)])