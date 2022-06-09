"""BaseCRUD extension and instance for Ticket model."""
from app.models import Ticket, TicketBoard

from ._base import BaseMetricCRUD


class TicketsCRUD(BaseMetricCRUD[Ticket]):
    """Base CRUD extension for Ticket model."""


tickets_crud = TicketsCRUD(Ticket, TicketBoard)
