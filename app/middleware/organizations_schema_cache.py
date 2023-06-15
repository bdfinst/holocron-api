"""Organizations schema cache."""
from app.crud import organizations_crud
from app.processors.v1 import process_organization as process_organization_v1
from app.processors.v2 import process_organization as process_organization_v2
from app.schemas.v1 import MetricsV1Schema
from app.schemas.v2 import MetricsV2Schema

from .schema_cache import SchemaCache

organizations_cache_v1 = SchemaCache(
    MetricsV1Schema(), organizations_crud, process_organization_v1
)
organizations_cache_v2 = SchemaCache(
    MetricsV2Schema(), organizations_crud, process_organization_v2
)
