#!/bin/sh
# this is a very simple script that tests the docker configuration for cookiecutter-django-wagtail
# it is meant to be run from the root directory of the repository, eg:
# sh tests/test_docker.sh

set -o errexit
set -x

# create a cache directory
mkdir -p .cache/docker
cd .cache/docker

# create the project using the default settings in cookiecutter.json
cookiecutter ../../ --no-input --overwrite-if-exists use_docker=y "$@"
cd my_awesome_project

# Lint by running pre-commit on all files
# Needs a git repo to find the project root
# We don't have git inside Docker, so run it outside
git init
git add .
pre-commit run --show-diff-on-failure -a

# make sure all images build
docker-compose -f docker-compose.yml build

# run the project's type checks
docker-compose -f docker-compose.yml run django mypy my_awesome_project

# run the project's tests
docker-compose -f docker-compose.yml run django pytest

# return non-zero status code if there are migrations that have not been created
docker-compose -f docker-compose.yml run django python manage.py makemigrations --dry-run --check || { echo "ERROR: there were changes in the models, but migration listed above have not been created and are not saved in version control"; exit 1; }

# Test support for translations
docker-compose -f docker-compose.yml run django python manage.py makemessages --all

# Make sure the check doesn't raise any warnings
docker-compose -f docker-compose.yml run django python manage.py check --fail-level WARNING

# Generate the HTML for the documentation
docker-compose -f docker-compose.yml run docs make html

# Run npm build script if package.json is present
if [ -f "package.json" ]
then
    docker-compose -f docker-compose.yml run node npm run build
fi
