"""Schema for Ticket model."""

from marshmallow import fields

from app.models import TicketPriority, TicketStatus, TicketType

from ._base import SchemaBase


class StatusHistoryV2Schema(SchemaBase):
    """Schema for Ticket StatusHistory model."""

    status = fields.Enum(TicketStatus, by_value=True)
    date = fields.DateTime()
    ticket_id = fields.Integer()


class TicketV2Schema(SchemaBase):
    """Schema for Ticket model."""

    status_history = fields.Nested(StatusHistoryV2Schema, many=True)
    ticket_type = fields.Enum(TicketType, by_value=True)
    priority = fields.Enum(TicketPriority, by_value=True)
    status = fields.Enum(TicketStatus, by_value=True)
    resource_id = fields.String()
    assignee = fields.String(allow_none=True)
    collector_target_id = fields.Integer()
    super_ticket_id = fields.Integer(allow_none=True)
    sub_tickets = fields.Nested("TicketV2Schema", many=True)
