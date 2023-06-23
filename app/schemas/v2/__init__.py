"""V2 schemas."""
from app.schemas.v1 import *

from .branch import BranchV2Schema
from .build import BuildV2Schema
from .commit import CommitV2Schema
from .git_request import GitRequestV2Schema
from .metrics import MetricsV2Schema
from .pipeline import PipelineV2Schema
from .repository import RepositoryV2Schema
from .ticket import TicketV2Schema
from .ticket_board import TicketBoardV2Schema
