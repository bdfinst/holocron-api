"""BaseCRUD extension and instance for User model."""

from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import config
from app.exceptions import HolocronError
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

        username = token.get(config.SSO_USERNAME_KEY)
        if not isinstance(username, str):
            raise HolocronError("Invalid username in JWT")
        groups = token.get(config.SSO_GROUPS_KEY)
        if not isinstance(groups, list):
            raise HolocronError("Invalid groups in JWT")

        sso_id = token.get("sub")
        is_org_leadership = config.SSO_LEADERSHIP_GROUP in groups
        is_admin = config.SSO_ADMIN_GROUP in groups
        if user is None:
            user = User(
                sso_id=sso_id,
                username=username,
                is_org_leadership=is_org_leadership,
                is_admin=is_admin,
            )
        else:
            user.sso_id = sso_id
            user.username = username
            user.is_org_leadership = is_org_leadership
            user.is_admin = is_admin

        username_num = 0
        while True:
            try:
                session.add(user)
            except IntegrityError as err:
                session.rollback()
                if "psycopg2.errors.UniqueViolation" not in str(
                    err
                ) or "users_username_key" not in str(err):
                    raise err
                username_num += 1
                user.username = username + str(username_num)
            else:
                session.commit()
                session.refresh(user)
                break
        return user


users_crud = UserCRUD(User)
