# The Human Element — status

## Context
Design-research study of the VERIS Community Database (VCDB, ~10k security incidents,
~3.3k human-element) → interactive research report positioning Himanshu as a serious
enterprise UXR practitioner. Chosen 2026-07-12 from the sociological-projects brainstorm
(idea #14). Full working contract in `SPEC.md`.

## Done
- 2026-07-12: Sources verified live (VCDB fresh as of 3 Jul 2026; CISA KEV 200 OK).
  Dataset profiled: 10,042 incidents, 9,523 with narratives; error 2,681 / social 644.
  Design-failure taxonomy v0 drafted (SPEC.md). Project scaffolded, git init.
- 2026-07-12: P1 pipeline delegated to Codex (gpt-5.6-terra, medium).
- 2026-07-12: P1 DONE. Codex built fetch/build/profile (stdlib-only; couldn't run live —
  sandbox has no network). Claude ran it, found + fixed two data-shape bugs
  (discovery_method is a nested dict; 23 incident_ids shared across 44 rows → row_id).
  All ground-truth counts reconcile exactly (10,042 / 9,523 / 2,681 / 644; Misdelivery 973
  … Pretexting 70). Outputs: data/derived/{incidents,narratives}.csv, stats.json, PROFILE.md.

## To-do
- P2: refine taxonomy against real narratives; exemplar selection.
- P3: analysis (discovery-method/time-to-discovery likely headline finding).
- P4: interactive report site (dataviz skill for charts).
- P5: method section, edit, Netlify deploy, link from portfolio.

## Awaiting
- Nothing from Himanshu right now.

## Next step
P2: refine the taxonomy against real narratives (read PROFILE.md samples + narratives.csv),
rule-based class assignment, exemplar selection.
