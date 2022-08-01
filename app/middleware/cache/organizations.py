"""Organizations cache."""
from app.crud import organizations_crud
from app.schemas import OrganizationMetricsSchema

from .cache import Cache

TEN_MINUTES = 600


organizations_cache = Cache(
    OrganizationMetricsSchema(), organizations_crud, TEN_MINUTES
)
