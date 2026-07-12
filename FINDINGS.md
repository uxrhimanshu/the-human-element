# Findings scratch (P3 seeds) — running log

Numbers computed from data/derived/incidents.csv (pipeline of 2026-07-12).
Every finding here needs its caveat carried into the final report.

## F1 — Organizations don't catch their own mistakes
Of 2,681 error-caused incidents, discovery category is known for 1,248. Of those:
**78.1% discovered externally** (975 external / 263 internal / 11 partner).
Top external discoverers: **Customer 371**, Security researcher 180, Found documents 158,
Unrelated 3rd party 77, Actor disclosure 38, Law enforcement 13, Audit 8.
Sharp version: the single most common way an organization learns about its own
error-caused breach is that *the exposed person finds it*.
Comparison: hacking incidents are 85.4% external-discovered (n=2,375 known) — expected,
attackers hide. For self-inflicted errors there is no adversary hiding anything, and
orgs still don't see them.
Caveat: 53% of error incidents have unknown discovery; externally-discovered incidents
are plausibly more likely to be reported at all (selection bias) — disclose.

## F2 — Misdelivery is physical more than digital (from P2 narrative survey)
Within Misdelivery summaries: letter 187 / envelope 62 / mailing 72 / fax 57 vs
email ~214. Mail-merge and envelope-stuffing are recurring mechanisms. Identity
confusability (same/similar names) is a distinct recurring mechanism.

## F3 — (candidate) Error share of breaches vs the "hacker" mental model
2,681 of 10,042 incidents (26.7%) involve error as an action; compare against
hacking 3,364 (33.5%). Roughly: for every four breaches caused by attackers,
three are self-inflicted. Verify overlap handling before using.
