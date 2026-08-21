#!/bin/bash

dir="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

cd "$dir" || exit 1

for input in *.in; do
    uv pip compile --generate-hashes "$input" -o "${input%.in}.txt"
done
