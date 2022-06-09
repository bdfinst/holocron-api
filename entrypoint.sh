#!/bin/sh

if ! alembic upgrade head; then exit 1; fi

exec $@
