#!/bin/sh
alembic revision --autogenerate
if ! alembic upgrade head; then exit 1; fi

exec $@
