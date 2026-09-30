#!/bin/bash
# Run the whole regression suite.
#
#   tests/run.sh              # everything
#   tests/run.sh -k devices   # one module
#
# pytest is not importable from the sandboxed interpreter and ~/.cache and
# ~/Library/Python are both write-denied, so it is vendored into a scratch dir
# under $TMPDIR and reinstalled if that has been cleaned. Nothing here touches
# the network unless the install is needed.
set -uo pipefail
SK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/Library/Frameworks/Python.framework/Versions/3.10/bin/python3}"
[ -x "$PY" ] || PY=python3
VENDOR="${TMPDIR:-/tmp}/ddr-pytest"

if ! PYTHONPATH="$VENDOR" "$PY" -c 'import pytest' 2>/dev/null; then
    echo "bootstrapping pytest into $VENDOR ..."
    "$PY" -m pip install --quiet --target="$VENDOR" pytest || {
        echo "could not install pytest; run this outside the sandbox" >&2; exit 1; }
fi

cd "$SK"
PYTHONPATH="$VENDOR" exec "$PY" -m pytest tests/ "$@"
