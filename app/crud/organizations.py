"""BaseCRUD extension and instance for Organization model."""
import logging
from typing import Any, Dict, Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Organization, Valuestream

from ._base import BaseCRUD
from .users import users_crud


def get_valuestream_without_team_views(valuestream: Valuestream) -> Valuestream:
    """Get valuestream without team views method."""
    new_vs = Valuestream(
        name=valuestream.name,
        organization_id=valuestream.organization_id,
        users=valuestream.users,
        teams=[team for team in valuestream.teams if team.view_owner_id is None],
    )
    new_vs.id = valuestream.id
    return new_vs


class OrganizationsCRUD(BaseCRUD[Organization]):
    """Base CRUD extension for Organization model."""

    def get_entity_without_team_views(self, session: Session, id_: int) -> Organization:
        """Get organization by id without team views."""
        org: Organization = self.get_entity(session, id_)

        result = Organization(
            name=org.name,
            users=org.users,
            valuestreams=[
                get_valuestream_without_team_views(vs) for vs in org.valuestreams
            ],
        )
        result.id = org.id
        return result

    def get_entities_without_team_views(
        self, session: Session
    ) -> Sequence[Organization]:
        """Get all organizations without team views."""
        organizations: Sequence[Organization] = self.get_entities(session)
        result = []
        for org in organizations:
            new_org = Organization(
                name=org.name,
                users=org.users,
                valuestreams=[
                    get_valuestream_without_team_views(vs) for vs in org.valuestreams
                ],
            )
            new_org.id = org.id
            result.append(new_org)
        return result

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> Organization:
        """Insert organization in database."""
        new_organization = Organization(name=json["name"])

        new_organization.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]

        try:
            session.add(new_organization)
        except IntegrityError as err:
            session.rollback()
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.commit()
        session.refresh(new_organization)
        return new_organization

    def update_entity(
        self, session: Session, json: Dict[str, Any], id_: int
    ) -> Organization:
        """Update organization in database."""
        organization: Organization = self.get_entity(session, id_)
        organization.name = json["name"]

        organization.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]

        try:
            session.add(organization)
        except IntegrityError as err:
            session.rollback()
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.commit()
        session.refresh(organization)

        org_no_team_views = Organization(
            name=organization.name,
            users=organization.users,
            valuestreams=[
                get_valuestream_without_team_views(vs)
                for vs in organization.valuestreams
            ],
        )
        org_no_team_views.id = organization.id

        return org_no_team_views


organizations_crud = OrganizationsCRUD(Organization)
