---
name: contract-review-client-email
description: >-
  Draft the client cover email at the end of a contract review and save it as a
  Gmail draft. Use this whenever you have just reviewed, redlined, or marked up a
  contract or agreement and it's time to send the client the final plus the
  redline — or when the user says things like "draft the client email," "email
  the client the redline," "write the cover note," or "send these out." Offer it
  proactively right after producing a redline. The skill reads the actual tracked
  changes, summarizes them into a few high-level bullets in plain business
  language, fills the user's fixed email template, and creates a Gmail draft. It
  NEVER sends.
---

# Contract Review → Client Email Draft

Turn a finished contract review into a ready-to-review client cover email, saved
as a Gmail draft. The point is to save the lawyer the rote step of writing the
"here's the final and the redline, here's what we changed" note — while keeping
the summary accurate to what was actually edited.

## When this runs

Trigger at the end of a contract review, once a redline / set of tracked
changes and a final version exist (in this conversation or as files the user
points to). If there's no redline to summarize, stop and say so.

## What you need before drafting

Gather these from the conversation or the files. Only ask the user for what you
genuinely can't determine:

- **The redline / tracked changes** — the source of truth for the bullets.
- **Final agreement** — to confirm the agreement's exact name.
- **Company name** and **agreement name** — for the subject line.
- **Recipient name** (the client contact) — for the salutation. If unknown,
  leave `[Name]` for the user to fill rather than guessing.

## Build the change bullets (the only real work)

Read the actual redline and summarize it into the bullet list. This is the part
that must be right.

- **Generate the bullets fresh from the redline every time.** 
- **Stay high-level. 5 bullets maximum.** Group related edits into one bullet point
  (e.g. expanded definitions for Confidential Information and Inventions to include AI related processes and work product, added AI definitions (e.g. AI-assisted work product, Artificial Intelligence) → "Revised and added definitions to include AI use and work product. Expanded definition for 'Confidential Information,' 'Inventions', added definitions for AI and AI-assisted work product"). Lead with the most substantive change.
- **Plain business language, not legalese.** The reader is the client's business
  or HR contact, not a lawyer. Say what changed and why it matters in a clause,
  not which subsection moved. Skip purely formatting/typo fixes.
- If a change is sensitive or strategic, describe it neutrally; when in doubt,
  flag it, do not guess.

## Fill the template

Use this template **exactly**. Only fill the bracketed placeholders and the
bullet list — do not reword the rest.

```
Subject: [Company Name] [Name of Agreement]

Dear [Name],

Please see attached 1) the final [Name of Agreement]; and 2) the redline showing our edits.

As discussed, we made the following changes:
- [Change 1, high-level]
- [Change 2, high-level]
- [Change 3, high-level]

Best,
Yue
```

- Subject: `[Company Name] [Name of Agreement]`, both filled.
- Sign-off defaults to **Yue**; change if the user indicates otherwise.
- Leave any placeholder you can't fill (e.g. `[Name]`) in brackets so it's
  obvious what the user still needs to complete.

## Create the Gmail draft

Call `Gmail:create_draft` with:
- `subject` — the filled subject line.
- `body` — the filled email (everything from "Dear …" through "Yue").
- **Omit `to`.** The user reviews the draft and adds the recipient before
  sending.

The draft lands in the user's own Gmail. **Never send it** — this skill only
drafts.

### Attachments

The Gmail draft tool **cannot attach files**, even though the email references
two attachments. So:
- Create the draft with the body text as-is (keep the "Please see attached…"
  line — it's a reminder).
- Tell the user the draft is ready but they need to **attach the final and the
  redline manually** before sending.
- If those two files were produced in this session, present them (or point to
  their paths) so they're easy to grab.

## Close out

In your reply, confirm: the draft is in their Gmail, show the bullets you wrote
so they can sanity-check the summary, and remind them to (1) add the recipient
and (2) attach the two files before sending.

## Edge cases

- **No redline found** → don't draft; ask the user to point you to the tracked
  changes.
- **Tons of changes** → still cap at 5 bullets by grouping; offer to expand a
  bullet if they want more detail on one item.
- **User wants tweaks** → edit the draft body and update the Gmail draft, or just
  show the revised text for them to paste.
