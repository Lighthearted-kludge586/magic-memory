# Methods reference

Detail behind `SKILL.md`. Load when you need a specific mode, want to diagnose a
misunderstanding, or want to judge mastery level.

---

## The five modes

Pick by concept type. Don't run all of them; pick the one that fits.

### fable
For abstract systems, incentives, feedback loops, economics, AI alignment, architecture *ideas* — things with no obvious physical handle.

- Write a short story whose **causal structure matches the concept**. Do **not** name the concept inside the story.
- Reveal the concept after the story.
- **Always** follow with a mapping table: story element → concept element.
- **Always** say where the story is incomplete or misleading.
- Don't over-use fables. If a crisp analogy or a contrasting pair carries the idea, use that instead — a cute story that doesn't constrain the idea is wasted effort.

### compare
For pairs or clusters of similar concepts. Output in this order:

1. **Short Answer** — the core difference in one sentence.
2. **Minimum Difference** — an example A vs B where changing *one* detail flips the answer. This is the heart of it.
3. **Comparison table** — purpose, mechanism, when to use, failure mode, common confusion.
4. **Decision Rule** — "If you see X, choose A. If you see Y, choose B."
5. **Test** — 3 classification questions (then stop and wait).

### code-trace
For programming mechanisms showable in a tiny example. Include:

- What problem the concept solves (motivate before mechanism).
- The smallest working mental model.
- A tiny example, then a **step-by-step trace** of what happens.
- **Worked example → faded → independent:** for novices, show a full example, then a version with a blank to fill in, then ask them to do one alone. (Cognitive-load theory: full worked examples beat "figure it out" for beginners; fade the scaffolding as they improve.)
- One common bug caused by misunderstanding it.
- A decision rule for when to use it, and a retrieval question.

### feynman
For a mastery check. The learner explains first; you find **one** gap at a time.

- Ask them to explain the concept in their own words.
- Identify only the **most important** gap (label it — see below).
- Prefer a question, a counterexample, or a tiny correction over a full re-lecture.
- Repeat until the explanation is accurate, simple, and transferable.

### review
For a later session or after an explanation. **Retrieval before re-explanation.** Use the flashcard `due` flow (see `review-protocol.md`); only re-teach the cards that fail.

---

## Gap labels (use these to name what's missing)

When the learner explains something, diagnose with a specific label rather than a vague "not quite":

- **factual-error** — a wrong statement.
- **jargon-dodge** — hides behind terms instead of unpacking them.
- **mechanism-blackbox** — knows the outcome, can't say what causes what.
- **boundary-blur** — confused with an adjacent concept.
- **analogy-overreach** — remembers the analogy but applies it too broadly.
- **example-gap** — no examples, or misleading ones.
- **transfer-gap** — can't solve a new case.
- **retention-gap** — gets it now, unlikely to remember later → that's what the flashcards are for.

Naming the gap is itself teaching: it tells the learner *which kind* of not-knowing they have.

---

## Mastery rubric (Bloom-style)

- **L1 Recognition** — recognizes the term.
- **L2 Plain Definition** — can explain it simply.
- **L3 Mechanism** — can explain what causes what.
- **L4 Transfer** — can apply it to a new scenario.
- **L5 Teaching** — can teach it simply, with an example, a boundary, and a common mistake.

Aim for L4 in a session; L5 is the real proof. Don't mistake L1 (recognition / nodding along) for understanding.

---

## Teaching rules

- Experience first, label second, for hard abstractions.
- Smallest useful model first, then expand. No long taxonomies up front.
- After any fable or analogy: a mapping, and a "where it breaks."
- For comparisons: always a minimum-difference example.
- For code: a runnable/pseudo-runnable example and a trace.
- When testing the learner in an interactive session, **stop and wait** for their answer.
- Distinguish recognition from recall — quiz, don't just re-state.

---

## Why this works (so the coach makes good calls, not just follows steps)

The design is grounded in established learning science; the names below are worth knowing so you can adapt rather than mechanically follow:

- **Testing effect / active recall** (Roediger & Karpicke): retrieving beats re-reading. Hence the mandatory retrieve step and the flashcards.
- **Spaced repetition** (Ebbinghaus forgetting curve; SM-2 / Anki): review at expanding intervals. The whole point of `flashcards.py`.
- **Desirable difficulties** (Bjork): making recall slightly hard *now* improves retention later — that's why "predict before reveal" and "answer before I show you" matter.
- **Generation effect**: learners remember what they produced. Hence "make your own hook / your own card."
- **Advance organizers / prior knowledge** (Ausubel): anchor the new to the known. Hence Step 0 calibration.
- **Cognitive load theory** (Sweller): worked-examples-then-fading for novices in code-trace.
- **Dual coding**: pair words with a diagram/visual where it helps.
- **Concrete-before-abstract & analogy** (cf. the ADEPT pattern — Analogy, Diagram, Example, Plain-English, Technical): intuition before formalism.
- **Interleaving** (Rohrer): mix topics in review rather than blocking one.

If a situation isn't covered by the steps, fall back to these principles.
