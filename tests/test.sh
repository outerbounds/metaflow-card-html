#!/bin/bash

set -eu

python htmlflow.py run

EXPECTED_OUTPUT="<html><body><h1 style='color: blue'>Hello World</h1></body></html>"
RESULTS=$(python htmlflow.py card get end)


if [ "$RESULTS" = "$EXPECTED_OUTPUT" ]; then
    echo "Test Passed."
    exit 0
else
    echo "Test Failed. Got:\n $RESULTS\n Expected:\n $EXPECTED_OUTPUT"
    exit 1;
fi
