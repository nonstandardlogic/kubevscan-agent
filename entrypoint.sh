#!/bin/sh
# Docker Entrypoint Script
set -e

script="$1"

if [ -z $1 ]; then
        echo "Parameter 1 is empty"
        exit 1
elif [ "${script}"  = "script.py" ]; then
        echo "Parameter 1 is not empty"
        exec $(which python3) "${script}"
        exit 0
fi

exec "${@}"