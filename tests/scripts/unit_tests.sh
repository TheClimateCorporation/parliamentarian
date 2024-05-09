#! /bin/bash
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

pytest tests/unit --cov-report html --cov --cov-config=.coveragerc
