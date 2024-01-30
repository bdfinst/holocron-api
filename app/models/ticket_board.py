"""Workflow ticket board model."""

from typing import List

from sqlalchemy.orm import Mapped, relationship

from .collector_target import CollectorTarget
from .ticket import Ticket


class TicketBoard(CollectorTarget):
    """Model class."""

    tickets: Mapped[List["Ticket"]] = relationship(default_factory=list)
