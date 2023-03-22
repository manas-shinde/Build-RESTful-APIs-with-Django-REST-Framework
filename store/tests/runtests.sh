#!/bin/bash
set -e

# Initialization
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Run the test and dump the coverage
python -m pytest $SCRIPT_DIR 