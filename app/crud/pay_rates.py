"""BaseCRUD extension and instance for PayRate model."""

from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import PayRate

from ._base import BaseCRUD


class PayRatesCRUD(BaseCRUD[PayRate]):
    """Base CRUD extension for PayRate model."""

    @staticmethod
    def upsert_entity(session: Session, json: Dict[str, Any]) -> PayRate:
        """Upsert pay rate in database."""
        email = json["email"]
        rate = json["rate"]
        pay_rate = session.scalars(
            select(PayRate).where(PayRate.email == email)
        ).first()
        if pay_rate is None:
            pay_rate = PayRate(email=email, rate=rate)
        else:
            pay_rate.rate = rate
            pay_rate.email = email

        session.add(pay_rate)
        session.commit()
        session.refresh(pay_rate)

        return pay_rate


pay_rates_crud = PayRatesCRUD(PayRate)
