"""Workflow ticket model."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from ._base import MetadataBase, ModelBase


class Ticket(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "tickets"
    __table_args__ = (UniqueConstraint("ticket_id", "board_id"),)

    ticket_id: Mapped[int]
    status: Mapped[str]
    ticket_type: Mapped[Optional[str]]
    priority: Mapped[Optional[str]]
    assignee: Mapped[Optional[str]]

    board_id: Mapped[int] = mapped_column(
        ForeignKey("collector_targets.id", ondelete="CASCADE")
    )
    super_ticket_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tickets.id"))

    sub_tickets: Mapped[List["Ticket"]] = relationship(
        backref=backref("super_ticket", remote_side="Ticket.id"), default_factory=list
    )
    status_history: Mapped[List["StatusHistory"]] = relationship(default_factory=list)


class StatusHistory(MetadataBase, ModelBase):
    """Model class for ticket status history."""

    __tablename__ = "ticket_status_histories"
    __table_args__ = (UniqueConstraint("ticket_id", "date"),)

    date: Mapped[datetime]
    status: Mapped[str]

    ticket_id: Mapped[int] = mapped_column(ForeignKey(Ticket.id, ondelete="CASCADE"))
    ticket: Mapped["Ticket"] = relationship(back_populates="status_history", init=False)
