"""Workflow ticket model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import backref, relationship

from ._base import MetadataBase, ModelBase
from .ticket_board import TicketBoard


class Ticket(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "tickets"

    board_id = Column(Integer, ForeignKey(TicketBoard.id), nullable=False)
    ticket_id = Column(Integer, nullable=False)
    assignee = Column(String())
    status = Column(String(), nullable=False)
    ticket_type = Column(String())
    super_ticket_id = Column(Integer, ForeignKey("tickets.id"))
    sub_tickets = relationship(
        "Ticket", backref=backref("super_ticket", remote_side="Ticket.id")
    )
    priority = Column(String())

    UniqueConstraint(ticket_id, board_id)


class StatusHistory(MetadataBase, ModelBase):
    """Model class for ticket status history."""

    __tablename__ = "ticket_status_histories"

    ticket_id = Column(Integer, ForeignKey(Ticket.id), nullable=False)
    ticket = relationship("Ticket", backref=backref("status_history"))
    date = Column(DateTime(), nullable=False)
    status = Column(String(), nullable=False)

    UniqueConstraint(ticket_id, date)
