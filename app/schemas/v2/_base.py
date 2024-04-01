"""Base schema class for model base."""

from marshmallow import Schema, fields


def camelcase(string: str) -> str:
    """Convert snake case to camel case."""
    parts = iter(string.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class SchemaBase(Schema):
    """Schema."""

    def on_bind_field(self, field_name: str, field_obj: fields.Field):
        """Convert field names from snake case to camel case."""
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
