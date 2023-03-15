from rest_framework import serializers


class MaxDurationValidator:
    """
    Validator checks if time between start_date_field and end_date_field is less or equal to hours.
    """

    MESSAGE = 'Maximal allowed duration is 8 hours'

    # TODO possible move maximal duration to constants for given usa case
    def __init__(
            self,
            start_date_field: str = 'start_time',
            end_date_field: str = 'end_time',
            maximal_duration_in_minutes: int = 8*60,
            message: str | None = None,
    ):
        self.start_date_field = start_date_field
        self.end_date_field = end_date_field
        self.message = message or self.MESSAGE
        self.maximal_duration_in_seconds = maximal_duration_in_minutes * 60

    def __call__(self, attrs: dict, *args, **kwargs) -> None:  # Could be possibly checked on model level
        if (
                attrs[self.end_date_field] - attrs[self.start_date_field]
        ).total_seconds() > self.maximal_duration_in_seconds:
            raise serializers.ValidationError(self.message, code='duration_limit_reached')
