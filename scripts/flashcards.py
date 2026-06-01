#!/usr/bin/env python3
"""
Magic Memory — spaced-repetition flashcard engine (SM-2 lite).

This is the retention half of Magic Memory. Understanding a concept once is not
remembering it; cards created here are scheduled for retrieval over days/weeks so
the concept actually survives the forgetting curve.

Storage: a single JSON file. Default ~/.magic-memory/cards.json
         override with env var MAGIC_MEMORY_FILE.

Usage:
  flashcards.py add  --deck DECK --front "Q" --back "A" [--hook "memory hook"] [--tags a,b]
  flashcards.py add-batch [FILE]      # FILE or stdin: JSON array of {deck,front,back,hook?,tags?}
  flashcards.py due  [--deck DECK] [--limit N]      # cards to review now (front hidden answer)
  flashcards.py grade ID QUALITY                    # QUALITY 0-5; reschedules via SM-2
  flashcards.py list [--deck DECK] [--all]
  flashcards.py stats
  flashcards.py decks

Grading scale (SM-2 quality):
  5 perfect | 4 correct, slight hesitation | 3 correct but hard
  2 wrong, but answer felt familiar | 1 wrong | 0 total blank
  A grade < 3 resets the card to "learning again" (interval -> 1 day).
"""
import argparse
import datetime as dt
import json
import os
import sys
import uuid

DEFAULT_PATH = os.path.expanduser(
    os.environ.get("MAGIC_MEMORY_FILE", "~/.magic-memory/cards.json")
)


def today():
    return dt.date.today()


def parse_date(s):
    return dt.datetime.strptime(s, "%Y-%m-%d").date()


def load():
    path = DEFAULT_PATH
    if not os.path.exists(path):
        return {"cards": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    path = DEFAULT_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def new_card(deck, front, back, hook=None, tags=None):
    return {
        "id": uuid.uuid4().hex[:8],
        "deck": deck or "default",
        "front": front,
        "back": back,
        "hook": hook or "",
        "tags": tags or [],
        "created": today().isoformat(),
        # SM-2 state
        "ef": 2.5,
        "interval": 0,
        "reps": 0,
        "due": today().isoformat(),
        "last_grade": None,
        "history": [],
    }


def sm2(card, q):
    """Update SM-2 scheduling state in place given quality q in 0..5."""
    q = max(0, min(5, int(q)))
    if q < 3:
        card["reps"] = 0
        card["interval"] = 1
    else:
        if card["reps"] == 0:
            card["interval"] = 1
        elif card["reps"] == 1:
            card["interval"] = 6
        else:
            card["interval"] = round(card["interval"] * card["ef"])
        card["reps"] += 1
        ef = card["ef"] + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        card["ef"] = max(1.3, round(ef, 3))
    card["due"] = (today() + dt.timedelta(days=card["interval"])).isoformat()
    card["last_grade"] = q
    card["history"].append({"date": today().isoformat(), "q": q})
    return card


# ---- commands ----

def cmd_add(a):
    data = load()
    tags = [t.strip() for t in a.tags.split(",")] if a.tags else []
    c = new_card(a.deck, a.front, a.back, a.hook, tags)
    data["cards"].append(c)
    save(data)
    print(f"added {c['id']} to deck '{c['deck']}' (due today)")


def cmd_add_batch(a):
    raw = sys.stdin.read() if not a.file else open(a.file, encoding="utf-8").read()
    items = json.loads(raw)
    data = load()
    added = []
    for it in items:
        c = new_card(
            it.get("deck"), it["front"], it["back"],
            it.get("hook"), it.get("tags"),
        )
        data["cards"].append(c)
        added.append(c["id"])
    save(data)
    print(f"added {len(added)} cards: {', '.join(added)}")


def is_due(card):
    return parse_date(card["due"]) <= today()


def cmd_due(a):
    data = load()
    due = [c for c in data["cards"] if is_due(c)]
    if a.deck:
        due = [c for c in due if c["deck"] == a.deck]
    due.sort(key=lambda c: c["due"])
    if a.limit:
        due = due[: a.limit]
    if not due:
        print("Nothing due. The forgetting curve is on your side today.")
        return
    print(f"{len(due)} card(s) due:\n")
    for c in due:
        print(f"[{c['id']}] ({c['deck']})  {c['front']}")
    print("\nAnswer from memory FIRST. Reveal answers with `list --all`, then `grade ID 0-5`.")


def cmd_grade(a):
    data = load()
    for c in data["cards"]:
        if c["id"] == a.id:
            sm2(c, a.quality)
            save(data)
            print(f"{c['id']} graded {a.quality} -> next due {c['due']} "
                  f"(interval {c['interval']}d, ef {c['ef']})")
            return
    print(f"card {a.id} not found", file=sys.stderr)
    sys.exit(1)


def cmd_list(a):
    data = load()
    cards = data["cards"]
    if a.deck:
        cards = [c for c in cards if c["deck"] == a.deck]
    if not a.all:
        cards = [c for c in cards if is_due(c)]
    for c in cards:
        print(f"[{c['id']}] ({c['deck']}) due {c['due']}")
        print(f"   Q: {c['front']}")
        print(f"   A: {c['back']}")
        if c["hook"]:
            print(f"   hook: {c['hook']}")


def cmd_stats(a):
    data = load()
    cards = data["cards"]
    due = sum(1 for c in cards if is_due(c))
    young = sum(1 for c in cards if c["interval"] < 7)
    mature = sum(1 for c in cards if c["interval"] >= 21)
    print(f"total {len(cards)} | due now {due} | learning(<7d) {young} | mature(>=21d) {mature}")


def cmd_decks(a):
    data = load()
    from collections import Counter
    cnt = Counter(c["deck"] for c in data["cards"])
    for deck, n in sorted(cnt.items()):
        due = sum(1 for c in data["cards"] if c["deck"] == deck and is_due(c))
        print(f"{deck}: {n} cards, {due} due")


def main():
    p = argparse.ArgumentParser(description="Magic Memory flashcard engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("add"); s.add_argument("--deck"); s.add_argument("--front", required=True)
    s.add_argument("--back", required=True); s.add_argument("--hook"); s.add_argument("--tags")
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("add-batch"); s.add_argument("file", nargs="?"); s.set_defaults(fn=cmd_add_batch)

    s = sub.add_parser("due"); s.add_argument("--deck"); s.add_argument("--limit", type=int)
    s.set_defaults(fn=cmd_due)

    s = sub.add_parser("grade"); s.add_argument("id"); s.add_argument("quality", type=int)
    s.set_defaults(fn=cmd_grade)

    s = sub.add_parser("list"); s.add_argument("--deck"); s.add_argument("--all", action="store_true")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("stats"); s.set_defaults(fn=cmd_stats)
    s = sub.add_parser("decks"); s.set_defaults(fn=cmd_decks)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
