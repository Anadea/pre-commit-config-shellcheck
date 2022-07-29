#!/usr/bin/env sh

set -e;

RESULT=$(pre_commit_config_shellcheck.py "${INPUT_CONFIG}");

echo "::set-output name=result::\"${RESULT}\"";
