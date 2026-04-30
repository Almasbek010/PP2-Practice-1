import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE    = "settings.json"

DEFAULT_SETTINGS = {
    "car_color":  [0, 120, 255],
    "difficulty": "normal",
    "sound":      False,
}



def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)



def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_leaderboard(entries):
    entries_sorted = sorted(entries, key=lambda x: x["score"], reverse=True)
    top10 = entries_sorted[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(top10, f, indent=4)
    return top10


def add_score(username, score, distance, coins):
    entries = load_leaderboard()
    entries.append({
        "name":     username,
        "score":    score,
        "distance": distance,
        "coins":    coins,
    })
    return save_leaderboard(entries)