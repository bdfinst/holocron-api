"""Workflow ticket board model."""
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .collector_target import CollectorTarget
from .ticket import Ticket


class TicketBoard(CollectorTarget):
    """Model class."""

    board_id: Mapped[Optional[int]] = mapped_column(index=True)
    tickets: Mapped[List["Ticket"]] = relationship()
