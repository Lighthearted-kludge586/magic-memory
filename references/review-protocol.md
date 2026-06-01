# Review protocol & flashcard reference

The retention half of Magic Memory. Understanding once ≠ remembering; these cards
bring concepts back for retrieval on an expanding schedule.

---

## Where cards live

A single JSON file, by default `~/.magic-memory/cards.json` (override with the
`MAGIC_MEMORY_FILE` env var). One store across all projects, organized by `deck`
(usually the topic). The file is plain JSON — easy to back up or export to Anki later.

---

## Card format

One card tests **one** idea. Prefer the learner's own words for the back/hook.

| Field | Meaning |
|---|---|
| `deck` | topic, e.g. `rust`, `system-design`, `react` |
| `front` | the question — phrased so it forces recall, not recognition |
| `back` | the answer, concise |
| `hook` | optional one-line memory hook (ideally the learner's own) |
| `tags` | optional |

**Good cards** ask "why/how/what-if", not "what is the definition of". Split compound
ideas into separate cards. A card you can answer by recognizing a keyword is a weak card.

---

## Creating cards

Single:

```bash
python3 scripts/flashcards.py add --deck "rust" \
  --front "Why does the borrow checker reject two &mut to the same value?" \
  --back  "It enforces one-writer-XOR-many-readers to prevent data races at compile time" \
  --hook  "one writer OR many readers, never both"
```

Batch (preferred when closing a session with 2–3 cards) — JSON array via stdin or file:

```bash
echo '[
  {"deck":"rust","front":"...","back":"...","hook":"..."},
  {"deck":"rust","front":"...","back":"..."}
]' | python3 scripts/flashcards.py add-batch
```

---

## The review session

1. **What's due:** `python3 scripts/flashcards.py due [--deck X] [--limit N]`
   Shows the **front only**. Cards are due when their scheduled date ≤ today.
2. **Recall first:** the learner answers from memory. Wait. Do not reveal.
3. **Reveal:** `python3 scripts/flashcards.py list --all` (or just state the back).
4. **Self-grade & reschedule:** `python3 scripts/flashcards.py grade <id> <0-5>`

Interleave decks when several are due — mixing is a desirable difficulty.

### Grading scale (SM-2 quality)

| q | meaning | effect |
|---|---|---|
| 5 | perfect, instant | interval grows most |
| 4 | correct, slight hesitation | interval grows |
| 3 | correct but hard | interval grows slowly |
| 2 | wrong, but answer felt familiar | **reset to 1 day** |
| 1 | wrong | reset to 1 day |
| 0 | total blank | reset to 1 day |

A grade below 3 means "learning again": the card returns tomorrow. When that happens,
don't just re-show the back — diagnose the gap (see gap labels in `methods.md`) and
re-explain that one thing.

### Scheduling (SM-2 lite)

- First correct review → due in **1 day**; second → **6 days**; after that → `interval × ease`.
- Ease factor starts at 2.5, nudged up by easy grades and down by hard ones (floor 1.3).
- So a well-known card drifts out to weeks/months; a shaky one stays close. This is the
  forgetting curve working *for* the learner.

---

## Other commands

```bash
python3 scripts/flashcards.py decks    # decks with counts and how many are due
python3 scripts/flashcards.py stats    # total / due / learning(<7d) / mature(>=21d)
python3 scripts/flashcards.py list --deck rust --all   # full dump of a deck
```

---

## Coaching notes

- Don't end a real learning session without saving cards — that's the difference
  between "understood it" and "will remember it".
- 2–3 strong cards beat 10 weak ones. Quality of the *question* is what matters.
- Nudge the learner to write the hook themselves before you offer one (generation effect).
- If they come back days later, lead with `due`, not with re-explaining.
