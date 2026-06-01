# Magic Memory

**An AI concept-learning coach that makes you *understand* and *remember*.**

Most AI explanations optimize one moment: you ask, it explains, you nod — and three days
later it's gone. Magic Memory fixes both halves of learning:

- **Understand** — it builds intuition *before* definitions, makes you predict and retrieve
  instead of passively reading, and catches the exact gap in your mental model.
- **Remember** — it turns what you understood into flashcards on a spaced-repetition
  schedule, so concepts survive the forgetting curve instead of evaporating after the chat.

It's built for learning unfamiliar concepts — abstract mechanisms, programming/framework
ideas, architecture tradeoffs, and confusing pairs of terms ("what's the difference between
X and Y?").

---

## How it works

A single learning loop:

```
calibrate → build intuition → predict → reveal → map → mark boundaries
          → make you retrieve → compress into flashcards → spaced review
```

- **Calibrate first** — finds what you already know, why you're learning it, and how deep to
  go. Crucially, it matches examples to *your* background (no code snippets thrown at
  non-programmers).
- **Intuition before formalism** — analogy, fable, tiny example, or real case first.
- **Active recall** — it stops and makes *you* answer before revealing. Nodding along isn't
  learning.
- **Spaced repetition** — strong moments become flashcards scheduled by an SM-2 engine.

---

## What's in this repo

| File | What it is |
|---|---|
| `SKILL.md` | The coach's instructions — the portable "brain". This is the prompt. |
| `references/methods.md` | The five teaching modes, gap-label vocabulary, mastery rubric, learning-science rationale. |
| `references/review-protocol.md` | Flashcard format, grading scale, the spaced-review workflow. |
| `scripts/flashcards.py` | A standalone SM-2 spaced-repetition engine. Pure Python 3, **zero dependencies**. |

---

## Install & use — works across tools

Magic Memory is deliberately portable: it's just **a text instruction file** plus **a
standalone Python script**. Anywhere you can give an AI instructions *and* run Python, it
works. Pick your setup:

### Claude Code / Claude skills
Drop the folder into your skills directory:
```bash
git clone https://github.com/<you>/magic-memory.git ~/.claude/skills/magic-memory
```
Then just ask to learn something, or invoke `/magic-memory`. The agent loads `SKILL.md`
automatically and runs the flashcard script for you.

### Claude.ai Projects
Paste the contents of `SKILL.md` into the Project's custom instructions. Add
`references/*.md` if you want the deeper methods available. Run the flashcard script locally
when it gives you the commands.

### Codex / Cursor / Windsurf / other coding agents
Point the agent at `SKILL.md`, or copy its contents into your `AGENTS.md` / system prompt /
custom-instructions field. The agent calls `scripts/flashcards.py` through its own shell —
nothing Claude-specific is required.

### ChatGPT / Gemini / any chatbot
Paste `SKILL.md` as a system prompt or custom instruction. The model will coach you through
the loop and hand you the `flashcards.py` commands to run on your own machine for review.

### The flashcard engine on its own
It's fully standalone — use it with or without any AI:
```bash
python3 scripts/flashcards.py --help
python3 scripts/flashcards.py add --deck rust --front "Q" --back "A" --hook "memory hook"
python3 scripts/flashcards.py due        # what's due today
python3 scripts/flashcards.py grade <id> 5   # self-grade 0–5, auto-reschedules
```
Cards are stored in `~/.magic-memory/cards.json` (override with the `MAGIC_MEMORY_FILE`
env var). Plain JSON — easy to back up or export to Anki later.

---

## 💬 Tip: answer by voice

The single cheapest way to get more out of this skill: **answer out loud, in your own words,
using voice-to-text.**

When you *speak* your answer instead of typing a short fragment, you're doing real active
recall and Feynman-style self-explanation — the exact things that build memory. It's also
far faster, so you actually explain in full sentences instead of one-word replies (which
teach you nothing).

- If your device has built-in dictation, turn it on.
- If not, install a speech-input keyboard. The author uses **豆包输入法 (Doubao)**, whose
  voice-to-text is excellent — but any good dictation tool works.

This skill is best used as a *conversation you talk through*, not a wall of text you read.

---

## Requirements

- Python 3.7+ (standard library only — no `pip install` needed).

## License

MIT — see [LICENSE](LICENSE). Free to download, use, modify, and share.
