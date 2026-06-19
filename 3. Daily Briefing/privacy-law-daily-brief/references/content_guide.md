# Content guide & JSON schema

This file explains exactly what to research and how to structure it for
`scripts/build_brief.py`. Pair it with `example_content.json`, which is a complete,
real edition you can imitate.

## Table of contents
1. The three buckets — what to look for
2. The compliance calendar — what qualifies
3. Sourcing & verification
4. JSON schema (field by field)
5. Common mistakes

---

## 1. The three buckets

The brief always reports in this order. Each section takes **up to 3** items; fewer is
fine and often better.

**State laws (privacy & AI).** New or amended state laws: comprehensive privacy acts,
children's/teens' privacy laws, AI laws (frontier models, automated decision-making,
chatbots, provenance), data-broker laws, neural/biometric data laws. Capture whether the
bill was *passed*, *signed*, or *effective*, and the effective date. Tag each item
`Privacy`, `AI`, or both.

**State enforcement actions & settlements.** AG or state privacy-agency settlements,
fines, consent decrees, investigative sweeps, and notable enforcement-priority shifts
(e.g., a regulator announcing a focus area). A single strong settlement beats three minor
items.

**Federal.** FTC rulemaking/enforcement (COPPA, health/data, dark patterns), Congressional
bills with real momentum, executive actions, federal preemption of state law, and agency
guidance. Federal privacy law moves slowly, so it's legitimate for this section to be thin
or report "no qualifying development."

### At a glance (three framings of the period)
- **What's new** — the single biggest development from the past week.
- **Ongoing** — a topic that has dominated for longer than a week.
- **On the horizon** — a coming change: an effective date, a bill likely to pass, a
  pending federal action.

---

## 2. The compliance calendar

List every U.S. privacy/AI compliance deadline that falls **on or before the 90-day
cutoff** from today. These are dates that require company action: a law's effective date,
a registration deadline, the start of an enforcement obligation, a regulation's compliance
date.

- Compute the cutoff explicitly each run. A deadline 91+ days out does **not** belong here
  (mention it in an article instead, noting the date).
- Exclude foreign deadlines unless asked.
- One row per deadline. Each row states who is impacted (be specific — e.g., "businesses
  with $25M+ gross revenue," "registered data brokers," "operators of services directed at
  children") and the concrete action required, in 1–2 sentences.
- The jurisdiction dropdown in the rendered page is generated automatically from the
  `jurisdiction` values you provide, so spell them consistently (e.g., always "California,"
  not sometimes "CA").

---

## 3. Sourcing & verification

- **Search broadly, then verify.** Useful starting points: IAPP news, leading law-firm
  privacy blogs (Hunton, Wiley, Holland & Knight, WilmerHale, Troutman, Kean Miller, etc.),
  state AG and privacy-agency press pages, and legislative trackers. Search with the
  current month/year in the query.
- **Prefer primary sources for facts and links.** Link the statute/bill text or the
  regulator's own press release/guidance where possible; use a law-firm alert as the
  reader-facing "analysis."
- **Verify every URL resolves** (fetch it) before including it. Confirm dates and dollar
  figures against the primary source — secondary summaries sometimes get the month or the
  amount wrong.
- **Watch for stale or pending status.** Distinguish "passed the legislature" from "signed"
  from "effective." Say which one it is.

---

## 4. JSON schema

Top-level object:

```json
{
  "date": "Tuesday, June 2, 2026",          // display date in the masthead
  "window_label": "May – early June 2026",   // coverage window, shown in the footer
  "at_a_glance": { "whats_new": "...", "ongoing": "...", "on_the_horizon": "..." },
  "calendar": { "window": "Deadlines within 90 days · June 2 – Aug. 31, 2026",
                "deadlines": [ /* deadline objects */ ] },
  "sections": {
    "state_laws":  [ /* article objects */ ],
    "enforcement": [ /* article objects */ ],
    "federal":     [ /* article objects */ ]
  }
}
```

**Deadline object:**
```json
{
  "date": "Jul 1, 2026",
  "jurisdiction": "Connecticut",
  "impacted": "Who must act, specifically.",
  "action": "What they must do, in 1–2 sentences.",
  "statute": [{ "label": "Public Act 25-113", "url": "https://..." }],
  "analysis": { "label": "Wiley", "url": "https://..." }
}
```
- `statute` is a list (a row may cite both a bill and a guidance page).
- `analysis` may be a single `{label,url}` object or a list.

**Article object:**
```json
{
  "title": "Headline of the development",
  "url": "https://...",                 // the reader-facing source link
  "publisher": "IAPP",
  "meta": "signed May 27, 2026 · effective Oct. 2026 – Jan. 2028",  // status/dates; optional
  "tags": ["Privacy", "AI"],            // state_laws only; [] elsewhere
  "must_read": true,                     // 1–3 true across the whole edition
  "summary": "1–2 sentence description of what it is and why it matters.",
  "toggle": "1–3 sentences: what changed in the law and the concrete compliance takeaway."
}
```

Notes:
- An empty section (`[]`) renders an honest "No qualifying development this period" note —
  use it rather than padding.
- `meta` is free text for status and effective dates; omit or leave `""` if not relevant
  (e.g., an enforcement-trend item with no single date).
- Text fields are HTML-escaped by the script, so write plain text (curly quotes, ≤, &, $
  are all fine).

---

## 5. Common mistakes
- Padding a section to three items. Don't — quality over count.
- Putting a far-future effective date in the calendar. The calendar is 90 days only.
- Forgetting to tag state-law items, or tagging items in other sections.
- Marking everything must-read. Reserve it for the 1–3 biggest items.
- Writing the brief from memory. Always research; always verify links.
- Hand-editing the generated HTML. Change the content JSON and re-run the script so the
  styling and calendar filter stay correct.
