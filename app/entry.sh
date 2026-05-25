#!/bin/sh
set -e

alembic upgrade head
uvicorn main:app --host 127.0.0.0 --port 8000