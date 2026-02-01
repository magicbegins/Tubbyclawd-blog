#!/usr/bin/env bash
# fetch-due-cards.sh - Fetch Trello cards due within the next 7 days and output a markdown report.

set -euo pipefail

if [[ -z "${TRELLO_API_KEY:-}" || -z "${TRELLO_TOKEN:-}" || -z "${TRELLO_BOARD_ID:-}" ]]; then
  echo "Error: Please set TRELLO_API_KEY, TRELLO_TOKEN, and TRELLO_BOARD_ID environment variables." >&2
  exit 1
fi

# Date range: now to 7 days from now in UTC
START_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
END_DATE=$(date -u -d "+7 days" +"%Y-%m-%dT%H:%M:%SZ")

# Fetch cards due within the next 7 days
curl -s \
  "https://api.trello.com/1/boards/${TRELLO_BOARD_ID}/cards?fields=name,due,url&due_after=${START_DATE}&due_before=${END_DATE}&key=${TRELLO_API_KEY}&token=${TRELLO_TOKEN}" \
  | jq -r '.[] | "- \(.name) (due: \(.due)) \(.url)"' > due-cards-report.md

echo "Report generated: due-cards-report.md"