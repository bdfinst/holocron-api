"""BaseCRUD extension and instance for CollectorCRUD model."""

import logging
from typing import Any, Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Collector

from ._base import BaseCRUD


class CollectorsCRUD(BaseCRUD[Collector]):
    """Base CRUD extension for CollectorCRUD model."""

    def update_entity(
        self, session: Session, json: Dict[str, Any], id_: int
    ) -> Collector:
        """Update collector in database."""
        collector: Collector = self.get_entity(session, id_)
        collector.target = json["target"]
        collector.target_url = json["target_url"]
        collector.collector_interval_seconds = json["collector_interval_seconds"]
        collector.look_back_days = json["look_back_days"]
        collector.collector_targets_intrvl_secs = json["collector_targets_intrvl_secs"]
        collector.max_requests_per_minute = json["max_requests_per_minute"]

        try:
            session.add(collector)
        except IntegrityError as err:
            session.rollback()
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.commit()
        session.refresh(collector)

        return collector


collectors_crud = CollectorsCRUD(Collector)
