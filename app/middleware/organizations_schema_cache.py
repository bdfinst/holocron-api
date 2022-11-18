"""Organizations schema cache."""
from app.crud import organizations_crud
from app.processors import process_organization
from app.schemas import MetricsSchema

from .schema_cache import SchemaCache

organizations_cache = SchemaCache(
    MetricsSchema(), organizations_crud, process_organization
)
