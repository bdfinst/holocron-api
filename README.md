Python backend for remixed edition of Holocron application. Replaces the Hygieia-API and the Holocron-Team-Service services. Uses Flask.

Uses SQLAlchemy for ORM, marshmallow for JSON serialization, alembic for migrations, apispec to generate OpenAPI spec, and flasgger to serve the OpenAPI spec.

## Getting started

To enable the pre-commit hook run `git config core.hookPath .githooks`.

To use this project, you need at least python 3.9 installed. With that, you should be able to use pip to install poetry. Either `pip install poetry` or `pip3 install poetry` as your system requires. Poetry is our package and virtual environment manager. You can prepare your environment with `poetry install` at which point you can enter it with `poetry shell` or execute commands into it with `poetry run <command>`.

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

## Updating this repo

As there are a few moving parts, the following is a step-by-step guide to adding a new model with corresponding endpoints and documentation to this repository.

### Creating a model

Model definitions are found under `app/models`. To create a new model that doesn't inherit from an existing one, create a new class with the following imports, like so:

```python
from ._base import MetadataBase, ModelBase

class MyModel(MetadataBase, ModelBase):

    __tablename__ = "my_models"
```

Then you can define the properties using sqlalchemy columns.

```python
from sqlalchemy import Column, Integer, ForeignKey, String

from ._base import MetadataBase, ModelBase
from .repository import Repository

class MyModel(MetadataBase, ModelBase):

    __tablename__ = "my_models"

    name = Column(String(), nullable=False, unique=True)
    repository_id = Column(Integer, ForeignKey(Repository.id), nullable=False)
```

### Migrations

After creating/updating a model, a new migration file needs to be created. If you created a model, you will need to import it into `alembic/env.py`. First import it into the `app.models.__init__.py`:

```python
from .my_model import MyModel
```

Then add it to the list of imports in `alembic/env.py`.

```python
from app.models import (... MyModel)
```

Now you can generate a new migration by running the following command from within the dev environment backend container.

`alembic revision --autogenerate`

### Schemas

Next, we need to create the schemas. Schemas are found under `app/schemas`. Create classes for new and existing items which inherit the base, and define the model it is using in the metadata.

```python
"""Schema for My Model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import MyModel

from ._base import SchemaBase


class MyModelSchema(SQLAlchemyAutoSchema, SchemaBase):

    class Meta:
        model = MyModel
```

Then, make sure you import your schemas in `app/schemas/__init__.py`

```python
from .my_model import MyModelSchema
```

### CRUD functions

Now that we have a schema, we can make our CRUD logic. We will inherit one of the base classes, and add or overwrite methods as needed.

```python
from sqlalchemy import select

from app.models import MyModel, Repository

from ._base import BaseCRUD, BaseMetricCRUD


# If your model includes a reference to a collector target, such as repository
# Use the BaseMetricCRUD class

class MyModelsCRUD(BaseMetricCRUD[MyModel]):
  # add or overwrite methods if needed
  @staticmethod
  def get_entities_by_name(session, name):
    return session.scalars(
      select(MyModel).where(MyModel.name == name)
    ).first()

# IF your model does not include a reference to a collector target
# Use the BaseCRUD class

class MyModelsCRUD(BaseCRUD[MyModel]):
  # If you don't need to adjust the class, just pass
  pass

# Instantiate the class
my_models_crud = MyModelsCRUD(MyModel)
# or
my_models_crud = MyModelsCRUD(MyModel, Repository)
```

Then import the instance into `app/crud/__init__.py`.

```python
from .my_models import my_models_crud
```

### Views

Now we can finally define our endpoints. These exist under `app/views`.

```python
from flask import Blueprint, jsonify, request

from app.crud import my_models_crud
from app.database import generate_session
from app.schemas import MyModelSchema

router = Blueprint("my_models", __name__, url_prefix="/my_models")

schema = MyModelSchema()


@router.route("", methods=["GET"])
def list_my_models():
    name = request.args.get("name")
    with generate_session() as session:
        if name is not None:
          raw_my_models = my_models_crud.get_entities_by_name(session, name)
        else:
          raw_my_models = my_models_crud.get_entities(session)
        my_models = [schema.dump(my_model) for my_model in raw_my_models]
    result = {"result": my_models}
    return jsonify(result), 200


@router.route("/<id>", methods=["GET"])
def get_my_model(id):
    with generate_session() as session:
        raw_my_model = my_models_crud.get_entity(session, id)
        result = schema.dump(raw_my_model)
    return jsonify(result), 200
```

Then we register this router in the main router located in `app/views/__init__.py`.

```python
"""Views."""
from flask import Blueprint

# ... other router imports
from .my_models import router as my_model_router

router = Blueprint("v1", __name__, url_prefix="/api/v1")
# ... other router registrations
router.register_blueprint(my_model_router)
```

And now our endpoints are added to the application.

### OpenAPI Docs

To add the new endpoints to the OpenAPI docs, you need to create a docstring with the appropriate OpenAPI spec for the view functions. For example:

```python
@router.route("", methods=["GET"])
def list_my_models():
    """List my_models.

    ---
    get:
      description: List my models.
      parameters:
        - in: query
          name: name
          schema:
            type: string
          required: false
          description: Name of the my_model
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schema/MyModel'
    """
    name = request.args.get("name")
    with generate_session() as session:
        if name is not None:
          raw_my_models = my_models_crud.get_entities_by_name(session, name)
        else:
          raw_my_models = my_models_crud.get_entities(session)
        my_models = [schema.dump(my_model) for my_model in raw_my_models]
    result = {"result": my_models}
    return jsonify(result), 200


@router.route("/<id>", methods=["GET"])
def get_my_model(id):
    """Get my_model by id.

    ---
    get:
      description: Get my_model by id.
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the my_model
      responses:
        200:
          content:
            application/json:
              schema: MyModelSchema
    """
    with generate_session() as session:
        raw_my_model = my_models_crud.get_entity(session, id)
        result = schema.dump(raw_my_model)
    return jsonify(result), 200
```

And now that endpoint will be documented and served at /api/v1.

### Tests

Of course the work isn't complete without tests. We use pytest fixtures to handle our mocking, and due to the nature of python imports that means we need to add our new files to the relevant fixtures. They are located in `tests/conftest.py`.

If you wrote new or updated CRUD methods, then you will likely need to mock the appropriate sqlalchemy functions. Find examples like below:

```python
session_patch.setattr(app.crud.teams, "select", mock_select)
```

You will need to add an equivalent for the new model as appropriate.

```python
session_patch.setattr(app.crud.my_models, "select", mock_select)
```

If you added a method to the CRUD class then you may also need to update the mocked CRUD class located in `tests/mocks/crud.py`. If your function signature isn't there, you will need to add it.

```python
def get_entities_by_name(self, session, name):
  return [{"name": name}]
```

With our mocks and fixtures updated, we can start by testing our CRUD operations. These tests are located in `tests/crud`. Create the `my_models_test.py` file there.

```python
from app.crud import MyModelsCRUD

def test_get_my_models_by_name(mock_session):
    expected = "SELECT * FROM my_models WHERE my_models.name = :name_1"

    result = MyModelsCRUD.get_entities_by_name(mock_session, "test")

    assert result[0].statement == expected
```

Now we also need tests for our view. These are located in `tests/views`. Create a `my_models_test.py` there.

```python
def test_get_my_models(client, mock_crud):
    expected = {"result": []}

    resp = client.get("/api/v1/my_models")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_my_models_by_name(client, mock_crud):
  expected = {"result": [{"name": "test"}]}

  resp = client.get("/api/v1/my_models?name=test")

  assert resp.json == expected
  assert resp.status_code == 200

def test_get_my_model(client, mock_crud):
    expected = {"id": 1}

    resp = client.get("/api/v1/my_models/1")

    assert resp.json == expected
    assert resp.status_code == 200
```
