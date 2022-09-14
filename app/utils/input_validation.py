"""Input validation module."""
from marshmallow import ValidationError, validate

from app.config import SECURITY_SETTINGS


def exceeds_char_limit(input_str: str):
    """Validate that input does not exceed limit."""
    if len(input_str) > SECURITY_SETTINGS["MAX_INPUT_CHAR_LEN"]:
        raise ValidationError("Exceeds max char limit.")


input_name_validator = validate.And(
    exceeds_char_limit, validate.Regexp(SECURITY_SETTINGS["VALID_NAME_CHARS"])
)
