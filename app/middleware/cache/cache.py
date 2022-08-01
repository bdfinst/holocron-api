"""Class."""
import time
from dataclasses import dataclass, field
from threading import Thread
from typing import Dict, Generator

from marshmallow import Schema

from app.crud._base import BaseCRUD
from app.database import generate_session


@dataclass
class Cache:
    """A cache to store the resulting schemas of selected model."""

    schema: Schema
    crud: BaseCRUD
    update_time: int
    data: Dict[int, str] = field(default_factory=dict)

    def _get_ids(self) -> Generator[int, None, None]:
        """Retrieve the IDs of each entity."""
        with generate_session() as session:
            items = self.crud.get_entities(session)
        return (item.id for item in items)

    def _set_cache(self, id_: int) -> str:
        """Retrieve the data for the corresponding entity and store the schema dump."""
        with generate_session() as session:
            item = self.crud.get_entity(session, id_)
            self.data[id_] = self.schema.dump(item)
            return self.data[id_]

    def _update_cache(self):
        """Update the cache for each entity."""
        item_ids = self._get_ids()
        for item_id in item_ids:
            self._set_cache(item_id)

    def _run_cache(self):
        """Run cache update on a timer. Use in a thread."""
        while True:
            self._update_cache()
            time.sleep(self.update_time)

    def start(self):
        """Start running in a thread."""
        Thread(target=self._run_cache).start()

    def get_entity(self, id_: int) -> str:
        """Retrieve entity from cache, setting it if not in cache."""
        # Use or instead of the .get default for lazy evaluation
        return self.data.get(id_) or self._set_cache(id_)
