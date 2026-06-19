---
name: piia-playbook
description: >-
  A playbook for updating Proprietary Information and Inventions
  Agreements (PIIAs) — also called CIIAAs or Employee Invention Assignment
  Agreements — for a U.S. employer, NEW EMPLOYEES only (signed at
  hire). Use it to draft a PIIA/CIIAA for a new employee in one or more states,
  assemble the core confidentiality and invention-assignment provisions, add
  state-specific invention-assignment carve-outs and notices (California §2870,
  Washington, Illinois, Minnesota), set up the Prior Inventions exhibit (Exhibit
  A) and Inventors' Rights Statutes exhibit (Exhibit B), draft a flexible
  multi-state governing-law clause, or handle AI provisions (AI tool use,
  ownership of AI-assisted inventions and AI-assisted work product, AI-related
  confidentiality, and referencing the company's AI use policy). Trigger even when the user says "inventions agreement," "IP assignment
  for a new hire," or "confidentiality and invention assignment" without naming
  "PIIA."
---

# PIIA Playbook (Multi-State U.S. Employer, New Employees)

> **THIS IS NOT LEGAL ADVICE.** This skill is provided for informational and
> educational purposes only and does not constitute legal advice. Using this
> skill, and relying on its outputs, does not create an attorney–client
> relationship. You should not rely on any output from this skill without review
> by a qualified legal professional. We recommend that you seek advice from an
> attorney licensed in the relevant jurisdiction(s) for advice tailored to your
> specific situation.

**Scope — read this first.**

- **Employees only.** This playbook is for W-2 employees. It does **not** cover
  consultants, independent contractors, advisors, or other non-employees. If the
  signer is not an employee, stop.
- **New hires only.** Assume the agreement is signed **at hire, as a condition of
  employment**, so the offer of employment is the consideration.
- **No restrictive covenants.** Non-compete, non-solicit (of employees or
  customers), and related covenants are out of scope.
- **AI provisions are optional.** If the company has a workforce that uses AI tools regularly, include the AI module (see `references/ai-provisions.md`); otherwise omit
  it. Assume that the company uses AI tools, and/or builds on top of foundation models, but does not train its own models.

## What this produces, and what it is not

This skill produces an **attorney work-product draft** — a clean draft PIIA with
its exhibits, or a clause-level compliance check of a draft — for a licensed
attorney to review before use. See the disclaimer above. State law on invention
assignment changes, so **statutory details must be re-verified at draft time**
(see `references/state-statutes.md`).

## The Core and add-ons

The **Core** is the set of provisions that belong in every PIIA (see
`references/clause-playbook.md`, Part 1) — always include them. The **add-ons** (Part 2) are included only when a
triggering circumstance is present: the employee's work state (state carve-outs and notices), a multi-state
form (revise governing law), or AI exposure (the AI module). Each module
notes whether it is mandatory or elective once its trigger applies.

## Intake

1. **Jurisdiction.** The controlling variable in a PIIA is usually the employee's state of employment
(i.e., where the employee physically works). It affects required
invention-assignment carve-outs, notice provisions, and, in some cases, governing
law and venue.

Before drafting, establish:

State(s) of employment. For remote employees, this is the state where the employee
physically works, which may differ from the company's offices or the employee's
residence. For multi-state templates, identify all applicable states.

If the user has not provided the state(s), ask before drafting. Do not guess.

2. **Employment Relationship.** Confirm that the form is for an employee. Stop if the user is drafting an agreement for consultants, independent contractors, advisors, or other non-employees.

## Exhibit convention

Exhibits are referenced by these letters in the body:

- **Exhibit A — Prior Inventions.** The employee's list of prior/background
  inventions excluded from assignment. **Always attach.**
- **Exhibit B — Inventors' Rights Statutes.** The text of the
  invention-assignment limitation statute(s) for the employee's state(s) (e.g.,
  Cal. Lab. Code § 2870). **Attach only when a relevant state requires a carve-out
  or notice** (see `references/state-statutes.md`); for a multi-state agreement,
  compile each applicable state's statute, titled "Inventors' Rights Statutes." If no
  applicable state requires it, omit Exhibit B.

## Modes

There are two modes:

1. **Full Draft Update** — run the DRAFT workflow below over an existing
   agreement.
2. **Targeted Edit** — when the user asks for a specific provision to be updated
   (e.g., AI provisions only, or adding state-specific language for a new state),
   make only the requested change and leave the rest of the agreement alone.

## Tracked changes

If you make any changes, use tracked changes. For each change, add a comment that
starts with "Claude: " then explain why you made the change.

For **Full Draft Update**, propose changes for attorney review. For **Targeted Edit**, make changes directly in the document, track changes, and include a comment with your reasoning for each edit.

## Full draft workflow

1. Run the intake above.
2. Check that the **Core** from `references/clause-playbook.md` is present
   and materially similar to the standard positions.
3. Flag the **add-ons** that apply and are not present or are materially different than standard positions. See `references/state-statutes.md`, and if the
   company uses AI, the AI module from `references/ai-provisions.md`.
4. Flag any **out-of-scope** provisions for removal (restrictive covenants,
   consultant/advisor terms, mid-employment consideration — see the "Out of scope"
   list in `references/clause-playbook.md`).
5. Check that **Exhibit A** (Prior Inventions) is attached.
6. If Company is in a state that has Inventors' Rights Statutes, check that **Exhibit B** is attached and contains the required information (see
   `references/state-statutes.md`).
7. Review the draft for consistency (e.g., formatting, defined terms,
   cross-references, exhibit references, section numbering, and internal
   citations).
8. Output a **cover memo**. Follow the structure laid out in the section below titled "Cover memo"

## Cover memo

Draft a cover memo with the following sections:
- High-level summary of proposed changes. No more than 2-3 paragraphs, unless the changes are substantial.
- A list of provisions that need to be added or revised. Sort them by Risk Level (see Risk Levels defined below), starting with 🔴. For each 🔴 and 🟡 issue, follow the format below. For 🟢 issues, include 1-2 sentences on proposed changes.

### [Section X.X]: [Clause name]

**Recommendation:** [plain-English explanation, one or two sentences, of what the proposed change is, and why it's needed]

**Risk:** 🔴 High | 🟡 Medium | 🟢 Low

**Proposed redline (if 🔴 or 🟡):**
> "[specific replacement language]" When possible, use the language in the reference files. Indicate whether the proposed language is from the reference files or generated from scratch.

**Open question:** [If uncertain whether the clause achieves intended purpose, flag for attorney review. Do not silently decide a subjective allocation question.]

**Link to Section:** if this skill is being run from the Word Plugin, and you're able to, link to the section so user can navigate to the relevant section easily.

### Risk level
- 🔴 High: Don't sign without fixing. Assignment gap in a document that should have one. Legally required notice missing.
- 🟡 Medium: Could be worth a revision. Imprecise language, survival periods shorter than standard. If you're unsure if a deviation matters, flag it as medium risk and explain the uncertainty.
- 🟢 Low: Note it, but don't need to address now. A stylistic deviation that doesn't change the allocation.

## Reference files

- **`references/clause-playbook.md`** — clause-by-clause list, organized as **Part 1 —
  Core** (always include) and **Part 2 — Add-ons** (include when
  triggered). Read when drafting or reviewing.
- **`references/model-language.md`** — sample text for key provisions.
- **`references/ai-provisions.md`** — the AI module: definitions, standard positions,
  sample language, and drafting notes on AI authorship/inventorship law.
  *(Drop additional AI language here.)*
- **`references/state-statutes.md`** — the state requirements: the Inventors' Rights
  Statutes to drop into Exhibit B (include only the states where the company has
  employees), plus governing-law sample language (multi-state and single-state).

