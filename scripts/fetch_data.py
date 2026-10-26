#!/usr/bin/env python3
"""Henter data fra FPL Draft API'et og skriver data/league.json.

Køres af GitHub Actions (se .github/workflows/update.yml), men kan også køres lokalt:
    python3 scripts/fetch_data.py
"""
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
API = "https://draft.premierleague.com/api"
HEADERS = {"User-Agent": "Mozilla/5.0 (fantasy-overblik)", "Accept": "application/json"}


def get(path, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(f"{API}{path}", headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))


def main():
    league_id = CONFIG["league_id"]
    game = get("/game")
    details = get(f"/league/{league_id}/details")
    bootstrap = get("/bootstrap-static")

    current = game.get("current_event") or 0
    events = [
        {"id": e["id"], "finished": bool(e.get("finished")), "deadline": e.get("deadline_time")}
        for e in bootstrap["events"]["data"]
        if e["id"] <= current
    ]

    entries, history = [], {}
    for le in details["league_entries"]:
        if not le.get("entry_id"):
            continue  # fx en "average"-modstander i H2H
        entries.append({
            "id": le["id"],
            "entry_id": le["entry_id"],
            "team": le["entry_name"],
            "first": le["player_first_name"],
            "last": le["player_last_name"],
            "short": le["short_name"],
        })
        h = get(f"/entry/{le['entry_id']}/history")
        history[str(le["entry_id"])] = [
            {"event": x["event"], "points": x["points"], "total": x["total_points"]}
            for x in h["history"]
        ]
        time.sleep(0.3)

    out = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "league": {
            "id": details["league"]["id"],
            "name": details["league"]["name"],
            "scoring": details["league"]["scoring"],
        },
        "current_event": current,
        "current_event_finished": bool(game.get("current_event_finished")),
        "events": events,
        "entries": entries,
        "history": history,
        "standings": details.get("standings", []),
        "matches": details.get("matches", []),
    }
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "league.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"OK: {out['league']['name']} – GW {current}, {len(entries)} hold")


if __name__ == "__main__":
    main()
