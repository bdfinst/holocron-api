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

**valuestreams** - Mid level organization structure.

|Field|Type|Description|
|-----|----|-----------|
|name|string|The name of the valuestream, non-nullable.*|
|organization_id|integer|Foreign key to `organizations.id`, non-nullable.*|

\*Combined unique constraint.

**teams** - Lowest level organization structure.

|Field|Type|Description|
|-----|----|-----------|
|name|string|The name of the team, non-nullable.*|
|team_size|integer|The number of members on the team, non-nullable.|
|valuestream_id|integer|Foreign key to `valuestreams.id`, non-nullable.*|

\*Combined unique constraint.

**users** - Application users.

|Field|Type|Description|
|-----|----|-----------|
|sso_id|string|ID assigned by SSO, unique.|
|username|string|The name/handle of the user, unique.|
|is_org_leadership|boolean|Flag as to whether the user is part of organization leadership.|
|is_admin|boolean|Flag as to whether the user is an admin.|

*team_users* - Many-to-many relationship between teams and users.

**collectors** - The collector services self register in the database using this model.

|Field|Type|Description|
|-----|----|-----------|
|name|string|Collector name, unique and non-nullable.|
|target|string|The URL of the resource to collect from.|

**collector_targets** - The top level objects that the collectors collect. Currently this includes repositories, pipelines, and ticket boards.

| Field          | Type     | Description                                                             |
|----------------|----------|-------------------------------------------------------------------------|
| collector_id   | integer  | Foreign key to `collectors.id`, non-nullable.                           |
| team_id        | integer  | Foreign key to `teams.id`.                                              |
| name           | string   | The name of the resource collected.                                     |
| url            | string   | The URL for the resource collected, non-nullable.                       |
| is_deleted     | boolean  | A flag for soft delete.                                                 |
| board_id       | integer  | If target is a ticketboard, this will be the ID given by the resource.  |
| pipeline_id    | integer  | If target is a pipeline, this will be the ID given by the resource.     |
| repository_id  | integer  | If target is a repository, this will be the ID given by the resource.   |
| trunk_branch   | string   | If target is a repository, this will be the name of the default branch. |
| last_collected | DateTime | The time the collector target was last collected from its url source.   |

**branches** - Branches collected from a repository collector target.

|Field|Type|Description|
|-----|----|-----------|
|repository_id|integer|Foreign key to `collector_targets.id`, non-nullable.|
|last_updated|datetime|When the branch was last updated, non-nullable.|
|name|string|The name of the branch, non-nullable.|
|url|string|The URL of the branch, unique and non-nullable.|

**commits** - Commits collected from a repository collector target.

|Field|Type|Description|
|-----|----|-----------|
|repository_id|integer|Foreign key to `collector_targets.id`, non-nullable.*|
|sha|string|The commit hash, non-nullable.*|
|is_merged|boolean|Flag as to whether the commit was merged or directly committed.|
|date|datetime|When the commit was made, non-nullable.|

\*Combined unique constraint.

**git_requests** - Merge/pull requests collected from a repository collector target.

|Field|Type|Description|
|-----|----|-----------|
|repository_id|integer|Foreign key to `collector_targets.id`, non-nullable.|
|title|string|The title of the request, non-nullable.|
|is_open|boolean|Flag as to whether the commit is currently open.|
|last_updated|datetime|When the request was last updated.|
|url|string|The URL of the request, unique and non-nullable.|

**builds** - Each run of a pipeline collected from a pipeline collector target.

|Field|Type|Description|
|-----|----|-----------|
|pipeline_id|integer|Foreign key to `collector_targets.id`, non-nullable.|
|build_url|string|The URL of the build, unique and non-nullable.|
|build_status|string|Whether the build passed or failed overall, non-nullable.|
|start_time|datetime|When the build was started.|
|end_time|datetime|When the build finished.|

**jobs** - The individual job of a build.

|Field|Type|Description|
|-----|----|-----------|
|build_id|integer|Foreign key to `builds.id`, non-nullable.|
|name|string|The name of the job, non-nullable.|
|status|string|Whether the job passed or failed, non-nullable.|
|stage|string|The name of the stage, non-nullable.|
|job_id|integer|The ID of the job assigned by the resource, non-nullable.|
|job_url|string|The URL of the job, unique and non-nullable.|

**tickets** - Work tickets collected from a ticketboard collector target.

|Field|Type|Description|
|-----|----|-----------|
|board_id|integer|Foreign key to `collector_targets.id`, non-nullable.*|
|ticket_id|integer|The ID of the ticket assigned by the resource, non-nullable.*|
|assignee|string|The email of the person assigned the ticket.|
|status|string|The current status of the ticket, non-nullable.|
|super_ticket_id|integer|Foreign key to `tickets.id`.|
|priority|string|The priority assigned to the ticket.|

\*Combined unique constraint.

**ticket_status_histories** - History of status changes for a ticket.

|Field|Type|Description|
|-----|----|-----------|
|ticket_id|integer|Foreign key to `tickets.id`, non-nullable.*|
|date|datetime|When the status was changed.*|
|status|string|What the status was changed to.|
.
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

For pipeline compatibility, we need to export our dependencies to a requirements.txt file. After any update to the dependencies in pyproject.toml and poetry.lock, run the following command `poetry export -o requirements.txt --without-hashes --dev`.

To add a dependency `poetry add <package_name>` or `poetry add -D <package_name>` for dev dependencies.

To remove a dependency `poetry remove <package_name>` or `poetry remove -D <package_name>` for dev dependencies.

To update dependencies `poetry update`.

## Updating this repo

As there are a few moving parts, the following is a step-by-step guide to add everything required to work with an entirely new type of collector. For this example, we will state that our product teams have one or more `forums` which each have a collection of `threads`.

### Creating our models

Model definitions are found under `app/models`. To start, we will create a file for our `forum` model `forum.py`:

```python
"""Forum model."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .collector_target import CollectorTarget


class Forum(CollectorTarget):
    """Model class."""

    forum_id = Column(Integer, index=True)
    description = Column(String)
    threads = relationship("Thread")
```

The `CollectorTarget` parent class applies several common fields that all these top level models utilize. It also inherits from `MetadataBase` and `ModelBase` which provide data for migrations and the definitions for the primary key and some timestamp fields respectively.

Next, we will create our `thread` model in a new file `thread.py`.

```python
"""Forum thread model."""
from sqlalchemy import Column, Integer, ForeignKey, String

from ._base import MetadataBase, ModelBase
from .forum import Forum

class Thread(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "threads"

    forum_id = Column(Integer, ForeignKey(Forum.id, ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False, unique=True)
```

Next we need to update the `Team` model in `team.py` to include a relationship to `Forum`.

```python
    class Team(MetadataBase, ModelBase):
        """Model class."""

        ...

        forums = relationship("Forum", overlaps="collector_targets")
```

Now we just need to add the new models to `__init__.py` for easy imports.

```python
from .forum import Forum
from .thread import Thread
```
### Migrations

After creating/updating a model, a new migration file needs to be created. You can generate a new migration by running the following command from within the dev environment backend container.

`docker compose up &`

and then 

`docker exec holocron_backend alembic revision --autogenerate` 

If consolidating migration files is desired, delete any migration files that you want to merge, clear the database, and then run the command above.

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
from .thread import ThreadSchema


class ForumSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Forum model."""

    class Meta:
        """Configuration."""

        model = Forum
        include_relationships = True
        exclude: Tuple[str, ...] = ("threads",)
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
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Forum

from ._base import BaseCRUD
from .teams import teams_crud

class ForumsCRUD(BaseCRUD[Forum]):
    """Base CRUD extension for Forum model."""

    def get_entities(self, session: Session) -> List[Forum]:
        """Override get_entities to return only forums."""
        return session.scalars(
            select(Forum).where(Forum.forum_id.is_not(None))
        ).all()
    
    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> List[Forum]:
        """Get all forums for a given team."""
        team = teams_crud.get_entity(team_id)
        return session.scalars(
            select(Forum)
            .where(Forum.team_id == team.id)
            .where(Forum.forum_id.is_not(None))
        ).all()


forums_crud = ForumsCRUD(Forum)
```

The `BaseCRUD` parent class defines several basic CRUD methods for our model. Here we override `get_entities` because otherwise it can't differentiate between the different types of collector targets, so we tell it to only grab those with a `forum_id`. We also define a similar method for getting all entities for a given `team_id`. Finally, we instantiate our class.

Next, let's make `threads.py`.

```python
"""BaseCRUD extension and instance for Thread model."""
from app.models import Forum, Thread

from ._base import BaseMetricCRUD


class ThreadsCRUD(BaseMetricCRUD[Thread]):
    """Base CRUD extension for Thread model."""


threads_crud = ThreadsCRUD(Thread, Forum, "form_id")
```

Here we inherit `BaseMetricCRUD` which is a class that inherits `BaseCRUD` and also defines a generic method to get all entities for a given team. We don't need any new methods or overrides here so we then just instantiate our class. Additionally, `Thread` has a foreign key to `Form` named `form_id`
which we need to pass in the constructor.

We do need to then make a small update to that class to include our new `Forum` model. Add the import and a couple of new lines to the `__init__` method found in `_base.py`.

```python
from app.models import (... Forum)

...

class BaseMetricCRUD(BaseCRUD[T]):
    """Extended base class for CRUD methods on team metric models."""

    def __init__(self, model: Type[ModelBase], target_model: Type[CollectorTarget]):
        """Initialize with the given model with collector target parent."""
        ...
        elif target_model == Forum:
            id_field = "forum_id"
```

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
from flask import Blueprint, jsonify

from app.crud import forums_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import ForumSchema
from app.security import get_sanitized_id

router = Blueprint("forums", __name__, url_prefix="/forums")

schema = ForumSchema()


@router.route("", methods=["GET"])
def list_forums():
    """Get forums."""
    with generate_session() as session:
        raw_forums = forums_crud.get_entities(session)
        forums = [schema.dump(forum) for forum in raw_forums]
    result = {"result": forums}
    return jsonify(result), 200


@router.route("/team/<team_id>", methods=["GET"])
def list_forums_for_team(team_id: str):
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


@router.route("/<forum_id>", methods=["GET"])
def get_forum(forum_id: str):
    """Get forum by id."""
    with generate_session() as session:
        try:
            raw_forum = forums_crud.get_entity(session,\
                get_sanitized_id(repo_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_forum)
    return jsonify(result), 200
```

Here we created our a router and instantiated our schema class before defining our endpoints as functions. In each endpoint we connect to the database and run the corresponding CRUD operation as well as the schema dump. We include some error handling to return 404s when appropriate, otherwise we return with a 200 code.

Now we can make the endpoints for the `thread` model with `threads.py`.

```python
from flask import Blueprint, jsonify

from app.crud import threads_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import ThreadSchema
from app.security import get_sanitized_id

router = Blueprint("threads", __name__, url_prefix="/threads")

schema = ThreadSchema()


@router.route("/team/<team_id>", methods=["GET"])
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


@router.route("/<thread_id>", methods=["GET"])
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
@router.route("", methods=["GET"])
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


@router.route("/team/<team_id>", methods=["GET"])
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


@router.route("/<forum_id>", methods=["GET"])
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

The final change is to ensure the OpenAPI specification understands our generated schemas correctly. Make a small change to `app/spec.py`:

```python
from app.schemas import (
    ...,
    ForumMetricsSchema,
)

...

def serve_spec(app: Flask, spec: APISpec):
    """Serve the API spec."""
    template = spec.to_flasgger(
        app,
        definitions=[
            ...,
            ForumMetricsSchema,
        ],
    )
    template = override_collector_target_spec(template, "forums", "ForumMetrics")
```

You can see all these updates at the /api/v1 endpoint.

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
        + "WHERE collector_targets.forum_id IS NOT NULL"
    )

    result = forums_crud.get_entities(mock_session)

    assert result[0].statement == expected


def test_get_entities_for_team(mock_sqlalchemy, mock_session):
    """Test get_entities_for_team method."""
    expected = (
      "SELECT * FROM collector_targets "
      + "WHERE collector_targets.team_id = :team_id_1 "
      + "WHERE collector_targets.forum_id IS NOT NULL"
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

# e2e tests
We are using cypress for our e2e tests. You can
run cypress in dev mode by first starting your dev
environment, and running `npx cypress run --config-file cypress/config/development.json` (This won't work right now since
we are still on Cypress9. The way to test e2e on dev
manually at the moment is to install cypress version 9.7.0--which might ot work on everyone's computer--as
dev dependency and run `npm run test:e2e`. This command needs to go away after the migration). For e2e
tests in pipeline, we do not need any of the dependencies, and
just `package.json` which has the scripts command `npm run test:e2e-ci` which uses pipeline's cypress.