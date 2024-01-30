"""Project issue instance model."""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class ProjectIssueType(enum.Enum):
    """Enum for 'type' field of ProjectIssue."""

    MAINTAINABILITY = "MAINTAINABILITY"
    POSSIBLE_BUG = "POSSIBLE_BUG"
    VULNERABILITY = "VULNERABILITY"
    UNKNOWN = "UNKNOWN"


class ProjectIssueSeverity(enum.Enum):
    """Enum for 'severity' field of ProjectIssue."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ProjectIssue(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "project_issues"

    resource_id: Mapped[str]
    package: Mapped[str]

    collector_target_id: Mapped[int] = mapped_column(
        ForeignKey("collector_targets.id", ondelete="CASCADE")
    )
    severity: Mapped[ProjectIssueSeverity] = mapped_column(
        Enum(ProjectIssueSeverity, create_constraint=True)
    )
    type: Mapped[ProjectIssueType] = mapped_column(
        Enum(ProjectIssueType, create_constraint=True)
    )
    issue_url: Mapped[str] = mapped_column(unique=True)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    closed_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
