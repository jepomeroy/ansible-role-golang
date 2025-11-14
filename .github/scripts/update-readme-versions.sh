#!/bin/bash
set -euo pipefail

# Script to update README.md with the latest Go SDK versions
# Extracts the latest patch version for each major.minor from vars/versions/

VARS_DIR="vars/versions"
README_FILE="README.md"

# Check if vars/versions directory exists
if [ ! -d "$VARS_DIR" ]; then
  echo "Error: $VARS_DIR directory not found"
  exit 1
fi

# Extract unique version numbers from filenames (remove architecture suffix)
# Format: 1.24.9-amd64.yml -> 1.24.9
declare -A latest_versions

for file in "$VARS_DIR"/*.yml; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")
    # Remove .yml extension and architecture suffix (-amd64, -arm64, -armv6l)
    version=$(echo "$filename" | sed -E 's/-(amd64|arm64|armv6l)\.yml$//')

    # Extract major.minor (e.g., 1.24 from 1.24.9)
    major_minor=$(echo "$version" | grep -oE '^[0-9]+\.[0-9]+')

    # Keep the highest patch version for each major.minor
    if [ -z "${latest_versions[$major_minor]:-}" ]; then
      latest_versions[$major_minor]=$version
    else
      # Compare versions and keep the higher one
      current="${latest_versions[$major_minor]}"
      if printf '%s\n' "$current" "$version" | sort -V | tail -n1 | grep -q "^$version$"; then
        latest_versions[$major_minor]=$version
      fi
    fi
  fi
done

# Sort versions in descending order and format as comma-separated list with line breaks
version_list=$(
  for key in "${!latest_versions[@]}"; do
    echo "${latest_versions[$key]}"
  done | sort -Vr | awk '{
    if (NR > 1) printf ", "
    if (NR % 6 == 1 && NR > 1) printf "\n"
    printf "%s", $0
  } END { printf "\n" }'
)

# Update README.md between the comment markers
if [ -f "$README_FILE" ]; then
  # Create a temporary file with updated content
  awk -v versions="$version_list" '
    /<!-- BEGIN GO VERSIONS -->/ {
      print $0
      print versions
      skip=1
      next
    }
    /<!-- END GO VERSIONS -->/ {
      skip=0
    }
    !skip { print }
  ' "$README_FILE" > "${README_FILE}.tmp"

  mv "${README_FILE}.tmp" "$README_FILE"
  echo "✓ Updated $README_FILE with latest Go versions"
  echo "Latest versions: $version_list"
else
  echo "Error: $README_FILE not found"
  exit 1
fi
