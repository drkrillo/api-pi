#!/bin/bash

# If first argument starts with -, runs uvicorn
if [[ "$1" == -* ]]; then
  set -- uvicorn main:app --reload --host 0.0.0.0 "$@"
fi

# If command is pytest, run tests
if [[ "$1" == "pytest" ]]; then
  exec "$@"
fi

# Executes command
exec "$@"
