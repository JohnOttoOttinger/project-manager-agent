#!/usr/bin/env bash
set -e
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
"${PROJECT_ROOT}/scripts/set-apify-token.sh"
echo "Press any key to close this window."
read -n 1 -s
