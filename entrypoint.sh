#!/usr/bin/env sh

set -eau pipefail; \

INPUT_CONFIG="${INPUT_CONFIG:-.pre-commit-config.yaml}"; \
export INPUT_CONFIG; \

/opt/.env/bin/pre_commit_config_shellcheck.py "${INPUT_CONFIG}"
