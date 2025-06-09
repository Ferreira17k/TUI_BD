from textual.widgets import Input
from textual.validation import Number, Validator, ValidationResult
from datetime import datetime


class DateValidator(Validator):  
    def validate(self, value: str) -> ValidationResult:
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return self.success()
        except ValueError:
            return self.failure("Invalid date")


def input_field(initial_value, input_type: str) -> Input:
    generic_type = {
        "character": "text",
        "character varying": "text",
        "text": "text",
        "integer": "int",
        "date": "date"
    }[input_type]

    validators = []
    if generic_type == "int":
        validators = [Number()]
    elif generic_type == "date":
        validators = [DateValidator()]

    return Input(
        initial_value,
        placeholder=f"Digite um valor ({input_type})",
        validators=validators,
        validate_on=["changed"]
    )
