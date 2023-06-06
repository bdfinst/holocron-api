"""Organizations schema cache."""
from app.crud import organizations_crud
from app.processors.v1 import process_organization as process_organization_v1
from app.processors.v2 import process_organization as process_organization_v2
from app.schemas.v1 import MetricsSchema as MetricsSchemaV1
from app.schemas.v2 import MetricsSchema as MetricsSchemaV2

from .schema_cache import SchemaCache

organizations_cache_v1 = SchemaCache(
    MetricsSchemaV1(), organizations_crud, process_organization_v1
)
organizations_cache_v2 = SchemaCache(
    MetricsSchemaV2(), organizations_crud, process_organization_v2
)
