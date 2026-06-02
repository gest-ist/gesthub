#!/bin/sh
set -eu

manage collectstatic --noinput

exec "$@"
