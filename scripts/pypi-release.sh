#!/usr/bin/env bash

#
# Utility script to automatically upload a created package to pypi if
# the package version is not available on the server yet.
#

set -e

PACKAGE_FILES=$@

if [[ -z ${PACKAGE_NAME} ]]; then
    printf "error: environment variable \"PACKAGE_NAME\" must be defined\n"
    exit 1
fi

if [[ -z ${PACKAGE_VERSION} ]]; then
    printf "error: environment variable \"PACKAGE_VERSION\" must be defined\n"
    exit 1
fi

if [[ -z ${VENV_PYTHON} ]]; then
    printf "error: environment variable \"VENV_PYTHON\" must be defined\n"
    exit 1
fi

python -m twine upload \
    --non-interactive \
    --skip-existing \
    --verbose \
    --repository testpypi ${PACKAGE_FILES}


