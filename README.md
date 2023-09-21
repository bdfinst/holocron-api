Python backend for remixed edition of Holocron application. Replaces the Hygieia-API and the Holocron-Team-Service services. Uses Flask.

Uses SQLAlchemy for ORM, marshmallow for JSON serialization, alembic for migrations, apispec to generate OpenAPI spec, and flasgger to serve the OpenAPI spec.


### Model Definitions

In addition to the fields below, all models have the following fields.

|Field|Type|Description|
|-----|----|-----------|
|id|integer|Auto-incrementing primary key.|
|created_at|datetime|When the item was inserted into the database.|
|updated_at|datetime|The last time the item was updated in the database.|

**organizations** - Top level organization structure for teams and valuestreams.

|Field|Type|Description|
|-----|----|-----------|
|name|string|The name of the organization, unique and non-nullable.|

**organization_users** - Many-to-many relationship between organizations and users.

**valuestreams** - Mid level organization structure.

|Field|Type|Description|
|-----|----|-----------|
|name|string|The name of the valuestream, non-nullable.*|
|organization_id|integer|Foreign key to `organizations.id`, non-nullable.*|

**valuestream_users** - Many-to-many relationship between valuestreams and users.

\*Combined unique constraint.

**teams** - Lowest level organization structure.

|Field|Type|Description|
|-----|----|-----------|
|name|string|The name of the team, non-nullable.*|
|team_size|integer|The number of members on the team, non-nullable.|
|valuestream_id|integer|Foreign key to `valuestreams.id`, non-nullable.*|
|is_workflow_only|boolean|Team only has workflow data.|
|view_owner_id|integer|Self-referential foreign key. If not null, this team is a view and the reference is to the owning team.

\*Combined unique constraint.

**team_history** - History of team size changes.

|Field|Type|Description|
|-----|----|-----------|
|team_size|integer|The number of members on the team, non-nullable.|
|team_id|integer|Foreign key to `teams.id`, non-nullable.|

**users** - Application users.

|Field|Type|Description|
|-----|----|-----------|
|sso_id|string|ID assigned by SSO, unique.|
|username|string|The name/handle of the user, unique.|
|is_org_leadership|boolean|Flag as to whether the user is part of organization leadership.|
|is_admin|boolean|Flag as to whether the user is an admin.|

**team_users** - Many-to-many relationship between teams and users.

**collectors** - The collector services self register in the database using this model.

|Field|Type|Description|
|-----|----|-----------|
|name|string|Collector name, unique and non-nullable.|
|target|string|The URL of the resource to collect from.|


**collector_targets** - The top level objects that the collectors collect. Currently this includes repositories, pipelines, and ticket boards.

| Field          | Type     | Description                                                             |
|----------------|----------|-------------------------------------------------------------------------|
| collector_id   | integer  | Foreign key to `collectors.id`, non-nullable.*                           |
| team_id        | integer  | Foreign key to `teams.id`.                                              |
| name           | string   | The name of the resource collected.                                     |
| url            | string   | The URL for the resource collected, non-nullable.*                       |
| is_deleted     | boolean  | A flag for soft delete.                                                 |
| resource_id    | string  | The ID used by the target service to identify this entity, non-nullable.*  |
| type | enum | The type of data collected, non-nullable. Possible values: `BUILD`, `PROJECT_ANALYSIS`, `SCM`, `WORKFLOW`. |
| trunk_branch   | string   | If target is a repository, this will be the name of the default branch. |
| last_collected | DateTime | The time the collector target was last collected from its url source.   |

**collector_target_config_items** - Key value pairs attached to collector targets for any additional info required by the application.

| Field                 | Type      | Description                                           |
|-----------------------|-----------|-------------------------------------------------------|
| collector_target_id   | integer   | Foreign key to `collector_targets.id`, non-nullable.* |
| key                   | string    | The key, non-nullable.*                               |
| value                 | string    | The associated value to the key, non-nullable.        |

\*Combined unique constraint.

**branches** - Branches collected from a repository collector target.

|Field|Type|Description|
|-----|----|-----------|
|collector_target_id|integer|Foreign key to `collector_targets.id`, non-nullable.|
|last_updated|datetime|When the branch was last updated, non-nullable.|
|name|string|The name of the branch, non-nullable.|
|url|string|The URL of the branch, unique and non-nullable.|
|is_default|boolean|Flag as to whether or not the branch is the default branch.|

**commits** - Commits collected from a repository collector target.

|Field|Type|Description|
|-----|----|-----------|
|collector_target_id|integer|Foreign key to `collector_targets.id`, non-nullable.*|
|sha|string|The commit hash, non-nullable.*|
|is_merged|boolean|Flag as to whether the commit was merged or directly committed.|
|date|datetime|When the commit was made, non-nullable.|
|author_username|string|The username of the individual who created the commit, non-nullable.|

\*Combined unique constraint.

**git_requests** - Merge/pull requests collected from a repository collector target.

|Field|Type|Description|
|-----|----|-----------|
|collector_target_id|integer|Foreign key to `collector_targets.id`, non-nullable.|
|title|string|The title of the request, non-nullable.|
|is_open|boolean|Flag as to whether the commit is currently open.|
|first_opened|When the request was first opened and not in draft.|
|merged_at|datetime|When the request was merged.|
|last_updated|datetime|When the request was last updated.|
|url|string|The URL of the request, unique and non-nullable.|

**builds** - Each run of a pipeline collected from a pipeline collector target.

|Field|Type|Description|
|-----|----|-----------|
|collector_target_id|integer|Foreign key to `collector_targets.id`, non-nullable.|
|build_url|string|The URL of the build, unique and non-nullable.|
|build_status|enum|The overall status of the build, non-nullable. Possible values: `PASSED`, `FAILED`, `PASSED_WITH_WARNINGS`.|
|start_time|datetime|When the build was started.|
|end_time|datetime|When the build finished.|
|is_deployed|boolean|Whether the pipeline executed a deploy.|

**tickets** - Work tickets collected from a ticketboard collector target.

|Field|Type|Description|
|-----|----|-----------|
|collector_target_id|integer|Foreign key to `collector_targets.id`, non-nullable.*|
|resource_id|string|The ID of the ticket assigned by the resource, non-nullable.*|
|assignee|string|The email of the person assigned the ticket.|
|status|enum|The current status of the ticket, non-nullable. Possible values: `TO_DO`, `IN_PROGRESS`, `DONE`.|
|ticket_type|enum|Whether the ticket is considered to be for features, defects, maintenance, or unplanned work. Possible values: `FEATURE`, `DEFECT`, `MAINTENANCE`, `UNPLANNED`.|
|super_ticket_id|integer|Foreign key to `tickets.id`.|
|priority|enum|The priority assigned to the ticket. Possible values: `HIGHEST`, `HIGH`, `MEDIUM`, `LOW`, `LOWEST`.|

\*Combined unique constraint.

**ticket_status_histories** - History of status changes for a ticket.

|Field|Type|Description|
|-----|----|-----------|
|ticket_id|integer|Foreign key to `tickets.id`, non-nullable.*|
|date|datetime|When the status was changed.*|
|status|enum|What the status was changed to. Possible values: `TO_DO`, `IN_PROGRESS`, `DONE`.|

\*Combined unique constraint.

## Getting started

To enable the pre-commit hook run `npm i` which will
setup husky.

To use this project, you need at least python 3.9 installed. With that, you should be able to use pip to install poetry. Either `pip install poetry` or `pip3 install poetry` as your system requires. [Poetry](https://python-poetry.org/) is our package and virtual environment manager. You can prepare your environment with `poetry install` at which point you can enter it with `poetry shell` or execute commands into it with `poetry run <command>`.

This package uses a variety of linting/formatting tools: pylint is a general linter, mypy is a type linter, pydocstyle is a comment linter, black is a code formatter, and isort is an import formatter.

For testing we use pytest with pytest-cov for coverage.

The various linting commands are as follows:

- `pylint app`
- `mypy .`
- `pydocstyle`
- `black .`
- `isort .`

Testing can be done with `pytest`, for a coverage report use `pytest --cov`.

If using VS Code, you can set linting with the following (after doing the poetry install):

- poetry env info
- Copy the path value under the Virtualenv header
- ctrl/cmd + shift + p
- Python: Select Linter
- Pylint
- ctrl/cmd + shift + p
- Python: Select Interpreter
- Enter interpreter path...
- Paste in the value from earlier

When running this project using the dev-environment repository, you can find the api at [localhost/api/v1](http://localhost/api/v1).

### Using poetry

Poetry is a package manager that automatically creates a [python virtual environment](https://docs.python.org/3/library/venv.html#venv-def), a project configuration file (pyproject.toml) and a dependency lock file (poetry.lock). To use the environment, use `poetry install` initially and whenever there are any dependency changes pulled. Afterwards, you can use `poetry run <command>` to execute a command in the virtual environment, or `poetry shell` to activate it and all future commands will be run in the environment until you give the `exit` command.

For pipeline compatibility, we need to export our dependencies to a requirements.txt file. After any update to the dependencies in pyproject.toml and poetry.lock, run the following command `poetry export -o requirements.txt --without-hashes --with dev`.

To add a dependency `poetry add <package_name>` or `poetry add -D <package_name>` for dev dependencies.

To remove a dependency `poetry remove <package_name>` or `poetry remove -D <package_name>` for dev dependencies.

To update dependencies `poetry update`.

## Updating this repo

As there are a few moving parts, the following is a step-by-step guide to add everything required to work with an entirely new type of collector. For this example, we will state that our product teams have one or more `forums` which each have a collection of `threads`.

### Creating our models

Model definitions are found under `app/models`. To start, we will create a file for our `Thread` model `thread.py`:

```python
"""Forum thread model."""
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase

class Thread(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "threads"
    __table_args__ = (UniqueConstraint("resource_id", "collector_target_id",),)

    resource_id: Mapped[str]

    collector_target_id: Mapped[int] = mapped_column(ForeignKey("collector_targets".id, ondelete="CASCADE"))
```

The model inherits from `MetadataBase` and `ModelBase` which provide data for migrations and the definitions for the primary key and some timestamp fields respectively. In addition, we defined a relationship to the `CollectorTarget` model which we will expand upon in the next file, as well as a `resource_id` field to connect what we input in our database with the unique identifier used by whatever service we are collecting from.

Next we will make our `Forum` model `forum.py`. 

```python
"""Forum model."""
from typing import List, Optional

from sqlalchemy.orm import Mapped, relationship

from .collector_target import CollectorTarget
from .thread import Thread


class Forum(CollectorTarget):
    """Model class."""

    resource_id: Mapped[str]
    description: Mapped[Optional[str]]

    threads: Mapped[List["Thread"]] = relationship(default_factory=list)
```

The `CollectorTarget` parent class applies several common fields that all these top level models utilize including inheriting the already discussed `MetadataBase` and `ModelBase`. We also establish the other side of the relationship established in `thread.py`.


Next we need to update the `Team` model in `team.py` to include a relationship to `Forum`.

```python
    class Team(MetadataBase, ModelBase):
        """Model class."""

        ...

        forums: Mapped[List["Forum"]] = relationship(overlaps="collector_targets", default_factory=list)
```

In addition, we need to add a new type to our `CollectorTargetType` enum in `collector_target.py`. We'll call this data type `DISCUSSION` data.

```python
class CollectorTargetType(enum.Enum):
    """Enum for 'type' field of CollectorTarget."""

    ...
    DISCUSSION = "DISCUSSION

```

Now we just need to add the new models to `__init__.py` for easy imports.

```python
from .forum import Forum
from .thread import Thread
```
### Migrations

After creating/updating a model, a new migration file needs to be created. You can generate a new migration by running the following command from within the dev environment backend container.

`docker compose up`

and then 

`docker exec holocron_backend alembic revision --autogenerate` 

If consolidating migration files is desired, delete any migration files that you want to merge, clear the database, and then run the command above.

Note: Automatic migrations may not work as desired and should be reviewed. This is especially true with enums which can often require quite a bit of custom commands. Look through previous migration files for examples if needed.

### Schemas

Next, we need to create the schemas. Schemas are found under `app/schemas`. We will start with `thread` so create `thread.py`.

```python
"""Schema for Thread model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Thread

from ._base import SchemaBase


class ThreadSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Thread model."""

    class Meta:
        """Configuration."""

        model = Thread
```

The `SchemaBase` parent class will set a few rules for the primary key and timestamp fields as well as convert snake_case to and from camelCase for proper naming conventions. The `SQLAlchemyAutoSchema` automatically applies the rest of the model fields to the schema.

Now we need a schema for `forum` so create `forum.py`.

```python
"""Schema for Forum model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Forum

from ._base import SchemaBase
from .collector_target_config import ConfigItemSchema


class ForumSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Forum model."""

    class Meta:
        """Configuration."""

        model = Forum
        include_relationships = True
        exclude: Tuple[str, ...] = ("threads",)

    team_id = auto_field()
    config = fields.Nested(ConfigItemSchema)
```

Here we create two different schemas for our model. This is so we can have a version that doesn't also fetch all of the threads to allow for a simpler response. Our second schema will inherit from the first and use `fields.Nested` to define how our `threads` should use the `ThreadSchema`.

And then a couple of small updates to `ExistingTeamSchema` in `team.py`.

```python
    class ExistingTeamSchema(TeamSchemaBase):
        """Existing team schema."""

    ...

    exclude = (..., "forums")
```

Now just add the new schemas to `__init__.py` for easy imports.

```python
from .forum import ForumSchema
from .thread import ThreadSchema
```

### CRUD functions

Now that we have a schema, we can make our CRUD logic. The CRUD files are found under `app.crud`. Let's make `forums.py`.

```python
"""BaseCRUD extension and instance for Forum model."""
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import CollectorTargetType, Forum

from ._base import BaseCRUD
from .teams import teams_crud

class ForumsCRUD(BaseCRUD[Forum]):
    """Base CRUD extension for Forum model."""

    def get_entity(self, session, id_: int) -> Forum:
        """Override get_entity to return only forum."""
        result = session.scalars(
            select(Forum)
            .where(Forum.type == CollectorTargetType.DISCUSSION)
            .where(Forum.id == id_)
        ).first()
        if result is None:
            raise HolocronIntegrityError(
                f"{Forum.__name__} id", f"Invalid id: {id_}"
            )
        return result

    def get_entities(self, session: Session) -> Sequence[Forum]:
        """Override get_entities to return only forums."""
        return session.scalars(
            select(Forum).where(Forum.type == CollectorTargetType.DISCUSSION)
        ).all()
    
    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> Sequence[Forum]:
        """Get all forums for a given team."""
        team = teams_crud.get_entity(team_id)
        return session.scalars(
            select(Forum)
            .where(Forum.team_id == team.id)
            .where(Forum.type == CollectorTargetType.DISCUSSION)
        ).all()


forums_crud = ForumsCRUD(Forum)
```

The `BaseCRUD` parent class defines several basic CRUD methods for our model. Here we override `get_entity` and `get_entities` because otherwise it can't differentiate between the different types of collector targets, so we tell it to only grab those with the proper type. We also define a similar method for getting all entities for a given `team_id`. Finally, we instantiate our class.

Next, let's make `threads.py`.

```python
"""BaseCRUD extension and instance for Thread model."""
from app.models import Forum, Thread

from ._base import BaseMetricCRUD


class ThreadsCRUD(BaseMetricCRUD[Thread]):
    """Base CRUD extension for Thread model."""


threads_crud = ThreadsCRUD(Thread, Forum)
```

Here we inherit `BaseMetricCRUD` which is a class that inherits `BaseCRUD` and also defines a generic method to get all entities for a given team. We don't need any new methods or overrides here so we then just instantiate our class. 

Now we just need to once again add our new class instances to the `__init__.py` for easy imports.

```python
from .forums import forums_crud
from .threads import threads_crud
```

### Routes

Now we can finally define our endpoints. These exist under `app/routes`.

Let's create `forums.py`.

```python
"""Forum routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import forums_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas import ForumSchema
from app.security import get_sanitized_id

schema = ForumSchema()


def list_forums() -> Tuple[Any, int]:
    """Get forums."""
    with generate_session() as session:
        raw_forums = forums_crud.get_entities(session)
        forums = [schema.dump(forum) for forum in raw_forums]
    result = {"result": forums}
    return jsonify(result), 200


@requires_security([requires_admin, requires_team_access])
def list_forums_for_team(team_id: str) -> Tuple[Any, int]:
    """Get forums for a given team id."""
    with generate_session() as session:
        try:
            raw_forums = forums_crud.get_entities_for_team(session,\
                get_sanitized_id(team_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        forums = [schema.dump(forum) for forum in raw_forums]
    result = {"result": forums}
    return jsonify(result), 200


def get_forum(forum_id: str) -> Tuple[Any, int]:
    """Get forum by id."""
    with generate_session() as session:
        try:
            raw_forum = forums_crud.get_entity(session,\
                get_sanitized_id(repo_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_forum)
    return jsonify(result), 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("forums", __name__, url_prefix="/forums")
    router.route("", methods=["GET"])(list_forums)
    router.route("/team/<team_id>", methods=["GET"])(list_forums_for_team)
    router.route("/<forum_id>", methods=["GET"])(get_project)
    return router
```

Here we created our a router and instantiated our schema class before defining our endpoints as functions. In each endpoint we connect to the database and run the corresponding CRUD operation as well as the schema dump. We include some error handling to return 404s when appropriate, otherwise we return with a 200 code.

Now we can make the endpoints for the `thread` model with `threads.py`.

```python
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import threads_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas import ThreadSchema
from app.security import get_sanitized_id

schema = ThreadSchema()


@requires_security([requires_admin, requires_team_access])
def list_threads_for_team(team_id: str):
    """Get threads for a given team id."""
    with generate_session() as session:
        try:
            raw_threads = threads_crud.get_entities_for_team(session,\
                get_sanitized_id(team_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        threads = [schema.dump(thread) for thread in raw_threads]
    result = {"result": threads}
    return jsonify(result), 200


@requires_security([requires_admin])
def get_thread(thread_id: str):
    """Get thread by id."""
    with generate_session() as session:
        try:
            raw_thread = threads_crud.get_entity(session,\
                get_sanitized_id(thread_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_thread)
    return jsonify(result), 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("threads", __name__, url_prefix="/threads")
    router.route("/team/<team_id>", methods=["GET"])(list_threads_for_team)
    router.route("/<thread_id>", methods["GET"])(get_thread)
    return router
```

Then we register these routers in the main router located in `__init__.py`.

```python
...
from .forums import router as forum_router
from .threads import router as thread_router

...
router.register_blueprint(forum_router)
router.register_blueprint(thread_router)
```

And now our endpoints are added to the application. If you check them out, they should function. Of course, there won't be any data unless you have built the collector or manually run some database inserts.

### OpenAPI Docs

Next, we want to update our OpenAPI docs to include these new endpoints. This is accomplished by expanding the docstring of the endpoint function. We will start with `forums.py`.

```python
def list_forums():
    """Get forums.

    ---
    get:
      description: Get forums
      responses:
        200:
          description: Get forums
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Forum'
    """
    ...


def list_forums_for_team(team_id: str):
    """Get forums for a given team id.

    ---
    get:
      description: Get forums belonging to a team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team to get forums for
      responses:
        200:
          description: Get forums belonging to a team
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Forum'
        404:
          description: Team not found
    """
    ...


def get_forum(forum_id: str):
    """Get forum by id.

    ---
    get:
      description: Get single forum by id
      parameters:
        - in: path
          name: forum_id
          schema:
            type: integer
          required: true
          description: ID of the forum
      responses:
        200:
          description: Get single forum by id
          content:
            application/json:
              schema: ForumSchema
        404:
          description: Forum not found
    """
    ...
```

For brevity, the updates to `threads.py` won't be included, but of course they should also be updated to be included in the OpenAPI docs.

You can see these updates at the /api/v1 endpoint.

### Tests

Of course the work isn't complete without tests. Our model files don't need any tests as they are just definitions without logic. Similarly our new schema files don't need any tests either, although we will want one updated test for our update to the `CollectorTargetSchema`.

So we will start with creating tests for our CRUD operations. We only need tests for any newly defined methods as the inherited methods are already covered. Let's create `tests/crud/forums_test.py`.

```python
"""Forums CRUD tests."""
from pytest import fixture

from app.crud import forums, forums_crud
from tests.mocks import mock_select


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(forums, "select", mock_select)


def test_get_entities(mock_sqlalchemy, mock_session):
    """Test get_entities method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.type = :type_1"
    )

    result = forums_crud.get_entities(mock_session)

    assert result[0].statement == expected


def test_get_entities_for_team(mock_sqlalchemy, mock_session):
    """Test get_entities_for_team method."""
    expected = (
      "SELECT * FROM collector_targets "
      + "WHERE collector_targets.team_id = :team_id_1 "
      + "WHERE collector_targets.type = :type_1"
    )

    result = forums_crud.get_entities_for_team(mock_session, 1)

    assert result[0].statement == expected
```

Here we use [pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html). We define a new fixture to mock our sqlalchemy `select` function using a mock defined under `tests/mocks/database.py`. The mock is set using a built-in fixture called `monkeypatch`. Our later test functions then call this new fixture as well as custom fixture defined in `tests/conftest.py`. Using these, we can test that the generated SQL statement for the method is what we would expect.

Next we need to test our endpoints. Let's create `tests/routes/forums.py`.

```python
"""Forum route tests."""
from pytest import fixture

from app.routes import forums
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(forums, "forums_crud", crud)


def test_list_forums(client, mock_crud):
    """Test GET /api/v1/forums endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/forums")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_forums_for_team(client, mock_crud):
    """Test GET /api/v1/forums/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/forums/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_forums_for_team_404(client, mock_crud):
    """Test GET /api/v1/forums/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/forums/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_forum(client, mock_crud):
    """Test GET /api/v1/forums/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/forums/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_forum_404(client, mock_crud):
    """Test GET /api/v1/forums/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/forums/-1")

    assert resp.text == expected
    assert resp.status_code == 404
```

Here we define another fixture to mock our crud object and use another custom fixture from `tests/conftest.py` to supply our test client object.

For brevity, the tests for `threads.py` routes won't be included, but of course they should also be created.

And once all that is done coverage should be complete.

## E2E Testing

For running e2e testing in dev-environment, run `npm run cypress:open` or `npm run cypress:run`.