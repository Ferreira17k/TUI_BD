from textual.widgets import Input
from textual.validation import Number
from datetime import datetime


def validate_date(value: str) -> bool:
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False


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
        validators = [Number]
    elif generic_type == "date":
        validators = [validate_date]

    return Input(
        initial_value
        placeholder=f"Digite um valor ({input_type})",
        validators=validators,
    )
