#! /bin/bash

SOURCE_PATHS='parliamentarian tests'

echo "== Running pylint =="
poetry run pylint $SOURCE_PATHS
echo "== Running flake8 =="
poetry run flake8 $SOURCE_PATHS
echo "== Running black =="
poetry run black --check $SOURCE_PATHS
echo "== Running isort =="
poetry run isort --check $SOURCE_PATHS
echo "== Running mypy =="
poetry run mypy $SOURCE_PATHS

echo "== Running pytest =="
if [ -f .coverage ]; then
  rm .coverage
fi

export PRIVATE_TESTS=""
if [ -d parliamentarian/private_auditors/tests/ ]; then
  export PRIVATE_TESTS="parliamentarian/private_auditors/tests/"
fi

export COMMUNITY_TESTS
if [ -d parliamentarian/community_auditors/tests/ ]; then
  export COMMUNITY_TESTS="parliamentarian/community_auditors/tests/"
fi

poetry run pytest tests/unit --cov-report html --cov --cov-config=.coveragerc
