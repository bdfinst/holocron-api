"""Workflow ticket board model."""
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .collector_target import CollectorTarget


class TicketBoard(CollectorTarget):
    """Model class."""

    board_id = Column(Integer, index=True)
    tickets = relationship("Ticket")
