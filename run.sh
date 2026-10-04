#!/bin/zsh
# Run JARVIS with its configured environment
SCRIPT_DIR="$(cd "$(dirname "${(%):-%N}")" 2>/dev/null || cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/main.py" "$@"
