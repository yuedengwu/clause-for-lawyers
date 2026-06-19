---
name: privacy-law-daily-brief
description: >-
  Generates a "Daily Brief" on recent U.S. privacy and AI law developments as a
  styled, self-contained HTML file for attorneys. Researches the latest state
  privacy/AI laws, state enforcement actions and settlements, and federal activity,
  then renders them in a fixed print-newsletter layout with an "At a glance" box, a
  jurisdiction-filterable compliance calendar of upcoming deadlines, tagged articles,
  and must-read flags. Use this whenever the user asks for a privacy-law briefing,
  privacy/AI legal update, "what's new in privacy law," a data-privacy news digest,
  a regulatory roundup, a compliance-deadline tracker, or wants to refresh or
  regenerate an existing privacy brief — even if they don't name the format
  explicitly. Also use it when scheduling a recurring privacy-law update.
---

# Daily Brief: U.S. Privacy & AI Law

This skill produces a recurring legal-news briefing for an attorney who needs to keep
up with U.S. privacy and AI law. The look and structure are fixed and produced by a
bundled script; your job each run is to **research the current developments** and feed
them to the script as structured content. That division of labor is deliberate: the
attorney relies on the layout staying identical edition to edition, while the substance
must be freshly researched and accurate every time.

## Workflow

1. **Establish the date and windows.** Get today's date (run `date "+%A, %B %-d, %Y"`
   if unsure). Two windows matter:
   - **Coverage window** for the articles: roughly the past month (the brief reports
     what's new "in the past month," with the "What's new" item drawn from the past week).
   - **Compliance-calendar window**: today through **90 days** from today. Compute the
     end date explicitly (e.g., `date -d "+90 days" "+%b %-d, %Y"` or
     `python3 -c "import datetime;print((datetime.date.today()+datetime.timedelta(days=90)))"`).

2. **Research first — this is the bulk of the work.** Use web search and fetch to find
   genuinely significant developments. Do not write the brief from memory; privacy law
   moves weekly and prior knowledge goes stale. Search across the three buckets plus the
   calendar. See `references/content_guide.md` for what counts as "significant," good
   sources, and search strategies. Prefer primary sources (statutes, regulator press
   releases, official guidance) and reputable secondary sources (leading law-firm alerts,
   IAPP). **Verify every link resolves** before including it — a dead link in a legal
   brief is worse than no link.

3. **Assemble the content as JSON.** Build a `content.json` matching the schema in
   `references/content_guide.md`. `references/example_content.json` is a complete,
   real example you can pattern-match against. Populate:
   - `at_a_glance`: three one-to-two-sentence items (What's new / Ongoing / On the horizon).
   - `calendar.deadlines`: every compliance deadline that falls within the 90-day window.
   - `sections.state_laws` / `enforcement` / `federal`: up to 3 items each.

4. **Render the HTML with the script.** Never hand-write the HTML — the script owns the
   styling and keeps the calendar filter in sync with the data:
   ```
   python3 scripts/build_brief.py content.json brief.html
   ```
   Name the output with the date, e.g. `privacy-daily-brief-2026-06-02.html`.

5. **Present the file** to the user (use the file-presentation tool if available). Keep
   any chat summary short; the brief speaks for itself. If the user might want this on a
   cadence, offer to schedule it.

## Editorial rules

These encode what makes the brief useful, so follow the reasoning, not just the letter:

- **Significance over volume.** "Significant" means a real change in the law or a strong
  enforcement signal — a signed/passed bill, a settlement, finalized regulations, a
  consequential federal action — not merely what's most discussed. A think-piece or a
  bill with no momentum doesn't qualify.
- **Don't pad.** Each section holds *up to* three items. If a bucket has nothing real
  this period, leave it empty — the script prints an honest "No qualifying development
  this period" note. Three weak items is worse than one strong one.
- **Tag state-law items.** In the State-laws section, tag each item `["Privacy"]`,
  `["AI"]`, or both, so the reader sees at a glance which regime it touches. Other
  sections don't take tags.
- **Flag 1–3 must-reads across the whole edition** with `"must_read": true` — the single
  most important developments, not one per section by default.
- **90-day calendar, no further.** Include only deadlines on or before the 90-day cutoff.
  A law signed this month but effective in 8 months belongs in the article body (with its
  effective date noted), not the calendar. U.S. matters only — skip foreign deadlines
  (e.g., the EU AI Act) unless the user asks otherwise.
- **Calendar links: statute/guidance + analysis.** Each deadline row needs an official
  link (the bill text, codified statute, or a regulator's guidance page) and a reputable
  analysis link (a leading law-firm alert or IAPP). Verify both.
- **Length: a ~5-minute read.** Article summaries are 1–2 sentences. The expandable
  toggle on each article holds 1–3 sentences on what changed and the concrete compliance
  takeaway. Keep prose tight.
- **Editorial caveats are good.** If a development is pending (passed but not signed) or a
  date/figure is contested across sources, say so plainly rather than overstating it.

## What the layout includes (handled by the script)

You don't build any of this by hand, but knowing the anatomy helps you fill the content:
a serif/sans black-and-white print-newsletter design; a masthead with the date; the
"At a glance" box; the filterable compliance calendar (the jurisdiction dropdown is
generated from the deadlines you supply); the three sections in order — **State laws**,
**State enforcement actions & settlements**, **Federal** — each article with a title,
linked publisher, a one-line summary, an inline `[ + ]` toggle, optional tags, and an
optional must-read star; and a footer legend.

For the exact JSON schema, field-by-field guidance, sourcing tips, and the significance
bar, read `references/content_guide.md`.
