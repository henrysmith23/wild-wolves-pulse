# ABOUTME: Fetches Liverpool FC match results from football-data.org API.
# ABOUTME: Computes cumulative goals scored/conceded by matchweek and saves to data.json.

import json
import os
from datetime import datetime, timezone

import requests

API_BASE = "https://api.football-data.org/v4"
TEAM_ID = 64
COMPETITION = "PL"
DATA_FILE = "data.json"

SEASONS = {
    "2025-26": 2025,
    "2026-27": 2026,
}


def get_api_key():
    key = os.environ.get("FOOTBALL_DATA_API_KEY")
    if not key:
        raise RuntimeError("FOOTBALL_DATA_API_KEY environment variable not set")
    return key


def fetch_matches(api_key, season_year):
    url = f"{API_BASE}/teams/{TEAM_ID}/matches"
    params = {
        "competitions": COMPETITION,
        "season": season_year,
        "status": "FINISHED",
    }
    headers = {"X-Auth-Token": api_key}

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()["matches"]


def compute_cumulative(matches):
    matches_by_week = sorted(matches, key=lambda m: m["matchday"])

    results = []
    cum_scored = 0
    cum_conceded = 0

    for match in matches_by_week:
        if match["homeTeam"]["id"] == TEAM_ID:
            scored = match["score"]["fullTime"]["home"]
            conceded = match["score"]["fullTime"]["away"]
        else:
            scored = match["score"]["fullTime"]["away"]
            conceded = match["score"]["fullTime"]["home"]

        cum_scored += scored
        cum_conceded += conceded

        results.append({
            "matchweek": match["matchday"],
            "scored": scored,
            "conceded": conceded,
            "cum_scored": cum_scored,
            "cum_conceded": cum_conceded,
        })

    return results


def run():
    api_key = get_api_key()
    seasons = {}

    for label, year in SEASONS.items():
        print(f"Fetching {label} season (year={year})...")
        matches = fetch_matches(api_key, year)
        print(f"  {len(matches)} finished matches")

        if matches:
            seasons[label] = compute_cumulative(matches)
        else:
            seasons[label] = []

    data = {
        "seasons": seasons,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved to {DATA_FILE}")


if __name__ == "__main__":
    run()
