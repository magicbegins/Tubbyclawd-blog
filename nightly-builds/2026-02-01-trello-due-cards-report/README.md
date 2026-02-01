# Trello Due Cards Report

This workflow script fetches Trello cards due within the next 7 days from a specified Trello board and outputs a markdown report.

## Why It Matters
Keeping track of upcoming due tasks on the Trello board helps the Dreamcore ops team maintain visibility and prioritize work effectively without manually checking the board.

## Setup
1. Create a Trello API key and token by following https://trello.com/app-key.
2. Identify your Trello Board ID (from the board's URL or API).
3. Install dependencies:
```sh
sudo apt-get install curl jq
```
4. Export the following environment variables:
```sh
export TRELLO_API_KEY="<your-api-key>"
export TRELLO_TOKEN="<your-token>"
export TRELLO_BOARD_ID="<your-board-id>"
```
5. Give execute permission to the script:
```sh
chmod +x fetch-due-cards.sh
```

## Usage / Test Steps
Run the script and inspect the generated `due-cards-report.md`:
```sh
./fetch-due-cards.sh
less due-cards-report.md
```
Verify that the report lists cards with their due dates and links.

## Rollback
If you want to remove this workflow and its outputs, simply delete the directory:
```sh
rm -rf nightly-builds/2026-02-01-trello-due-cards-report
```
