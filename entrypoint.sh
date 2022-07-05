#!/bin/sh

if ! python -m alembic upgrade head; then exit 1; fi

exec $@
