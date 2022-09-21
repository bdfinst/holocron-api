"""Input validation module."""
from marshmallow import ValidationError, validate

from app.security import MAX_INPUT_CHAR_LEN, VALID_NAME_CHARS


def exceeds_char_limit(input_str: str):
    """Validate that input does not exceed limit."""
    if len(input_str) > MAX_INPUT_CHAR_LEN:
        raise ValidationError("Exceeds max char limit.")


input_name_validator = validate.And(
    exceeds_char_limit, validate.Regexp(VALID_NAME_CHARS)
)
