"""Schema Cache."""
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generator, Union

from marshmallow import Schema

from app.crud._base import BaseCRUD
from app.database import generate_session
from app.exceptions import HolocronError


class SchemaCacheNotReady(HolocronError):
    """Error for cache not being ready."""


@dataclass
class SchemaCache:
    """A cache to store the resulting schemas of selected model."""

    schema: Schema
    crud: Union[BaseCRUD, Any]
    process_func: Callable[[Any], Any]
    data: Dict[int, Dict] = field(default_factory=dict)

    def _get_ids(self) -> Generator[int, None, None]:
        """Retrieve the IDs of each entity."""
        with generate_session() as session:
            items = self.crud.get_entities(session)
        return (item.id for item in items)

    def _set_cache(self, id_: int):
        """Retrieve the data for the corresponding entity and store the schema dump."""
        with generate_session() as session:
            item = self.crud.get_entity(session, id_)
            processed_item = self.process_func(item)
            self.data[id_] = self.schema.dump(processed_item)

    def run(self):
        """Update the cache for each entity."""
        start = time.time()
        logging.info("---Starting cache run...---")

        item_ids = self._get_ids()
        for item_id in item_ids:
            self._set_cache(item_id)

        end = time.time()
        logging.info(f"---Finished cache run in {round(end - start, 2)} seconds.---")

    def get_entity(self, id_: int) -> Any:
        """Retrieve entity from cache."""
        with generate_session() as session:
            self.crud.get_entity(session, id_)
            if id_ in self.data:
                return self.data.get(id_)
            raise SchemaCacheNotReady("Data not ready.")
