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
        if user is None:
            user = User()
        user.sso_id = token.get("sub")
        username = token.get(config.SSO_USERNAME_KEY)
        if not isinstance(username, str):
            raise HolocronError("Invalid username in JWT")
        user.username = username

        groups = token.get(config.SSO_GROUPS_KEY)
        if not isinstance(groups, list):
            raise HolocronError("Invalid groups in JWT")
        user.is_org_leadership = config.SSO_LEADERSHIP_GROUP in groups
        user.is_admin = config.SSO_ADMIN_GROUP in groups

        username_num = 0
        while True:
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                break
            except IntegrityError as err:
                if "psycopg2.errors.UniqueViolation" in str(
                    err
                ) and "users_username_key" in str(err):
                    session.rollback()
                    username_num += 1
                    user.username = username + str(username_num)
                else:
                    raise err
        return user


users_crud = UserCRUD(User)
