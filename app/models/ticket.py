"""Workflow ticket model."""

import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from ._base import MetadataBase, ModelBase


class TicketType(enum.Enum):
    """Enum for 'ticket_type' field of Ticket."""

    FEATURE = "FEATURE"
    DEFECT = "DEFECT"
    MAINTENANCE = "MAINTENANCE"
    UNPLANNED = "UNPLANNED"


class TicketStatus(enum.Enum):
    """Enum for 'status' field of Ticket."""

    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TicketPriority(enum.Enum):
    """Enum for 'priority' field of Ticket."""

    HIGHEST = "HIGHEST"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    LOWEST = "LOWEST"


class Ticket(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "tickets"
    __table_args__ = (UniqueConstraint("resource_id", "collector_target_id"),)

    resource_id: Mapped[str]
    assignee: Mapped[Optional[str]]

    priority: Mapped[TicketPriority] = mapped_column(
        Enum(TicketPriority, create_constraint=True, name="ticketpriority")
    )
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus, create_constraint=True, name="ticketstatus")
    )
    ticket_type: Mapped[TicketType] = mapped_column(
        Enum(TicketType, create_constraint=True, name="tickettype")
    )
    collector_target_id: Mapped[int] = mapped_column(
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

    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus, create_constraint=True, name="ticketstatus")
    )
    ticket_id: Mapped[int] = mapped_column(ForeignKey(Ticket.id, ondelete="CASCADE"))
    ticket: Mapped["Ticket"] = relationship(back_populates="status_history", init=False)
