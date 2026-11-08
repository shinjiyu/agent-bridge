#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)/starter:${PYTHONPATH:-}"
python3 -m pytest -q --tb=short tests
