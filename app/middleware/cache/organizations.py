"""Organizations cache."""
from app.crud import organizations_crud
from app.processors import process_organization
from app.schemas import MetricsSchema

from .cache import Cache

TEN_MINUTES = 600


organizations_cache = Cache(
    MetricsSchema(), organizations_crud, TEN_MINUTES, process_organization
)
