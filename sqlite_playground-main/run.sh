#!/usr/bin/env bash

set -eo pipefail

DC="${DC:-exec}"

# If we're running in CI we need to disable TTY allocation for docker-compose
# commands that enable it by default, such as exec and run.
TTY=""
if [[ ! -t 1 ]]; then
    TTY="-T"
fi

# -----------------------------------------------------------------------------
# Helper functions start with _ and aren't listed in this script's help menu.
# -----------------------------------------------------------------------------

function _dc {
    export DOCKER_BUILDKIT=1
    docker-compose ${TTY} "${@}"
}

function _use_local_env {
    sort -u environment/local.env | grep -v '^$\|^\s*\#' > './environment/local.env.tempfile'
    export "$(< environment/local.env.tempfile xargs)"
    rm environment/local.env.tempfile
}

# ----------------------------------------------------------------------------

function up {
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info
}

function reset {
    rm main.db
}

function erd {
    eralchemy -i sqlite:///./db/main.db -o erd_from_sqlite.pdf
}

db:makemigrations () {
    docker run -v "$(pwd)"/db/migrations:/migrations --network host migrate/migrate \
    create -ext sql -dir /migrations -seq "${@}"
}

db:migrate () {
    docker run -v "$(pwd)"/db:/db --network host migrate/migrate \
    -database sqlite3:///db/main.db -path /db/migrations "${@}"
}

db:shell () {
    sqlite3 ./db/main.db
}


# -----------------------------------------------------------------------------

function help {
    printf "%s <task> [args]\n\nTasks:\n" "${0}"

    compgen -A function | grep -v "^_" | cat -n
}

TIMEFORMAT=$'\nTask completed in %3lR'
time "${@:-help}"
