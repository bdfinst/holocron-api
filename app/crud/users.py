"""BaseCRUD extension and instance for User model."""
from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config
from app.models import User

from ._base import BaseCRUD


class UserCRUD(BaseCRUD[User]):
    """Base CRUD extension for User model."""

    @staticmethod
    def upsert_sso_user(session: Session, token: Dict[str, Any]) -> User:
        """Upsert user in database using sso."""
        user = session.scalars(
            select(User).where(User.sso_id == token.get("sub"))
        ).first()
        if user is None:
            user = User()
        user.sso_id = token.get("sub")
        user.username = token.get(config.SSO_USERNAME_KEY)

        groups = token.get(config.SSO_GROUPS_KEY)
        if not isinstance(groups, list):
            raise Exception("Invalid groups in JWT")
        user.is_org_leadership = config.SSO_LEADERSHIP_GROUP in groups
        user.is_admin = config.SSO_ADMIN_GROUP in groups

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


users_crud = UserCRUD(User)
