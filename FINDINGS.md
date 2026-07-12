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

## F3 — Error share of breaches vs the "hacker" mental model — VERIFIED
2,681 of 10,042 incidents (26.7%) involve error; hacking 3,364 (33.5%); overlap is
only 27 incidents. **2,650 incidents (26.4%) are purely self-inflicted** (error with
no hacking or social action). For every four attacker-caused breaches, three are
self-inflicted. Caveat: VCDB coverage bias (VA import inflates error class) — present
as "within this corpus".

## F4 — The blast radius ladder: interface abstraction × records exposed
Median records exposed, where a count is known (from coded.csv × incidents.csv):
- C1 wrong-recipient: **median 2** (n=802) — individual-scale, intimate harm
- C4 unprotected portability: median 808 (n=335)
- C2 visibility-state: median 1,581 (n=256)
- C8 phishing: median 3,020 (n=116)
- C3 unsafe defaults/misconfiguration: **median 700,000** (n=236)
Sharp version: a person can only mis-send one letter at a time; a console checkbox
exposes seven hundred thousand people. The blast radius of a design failure scales
with the abstraction of the interface — and the duty of care in the design should
scale with it. Caveat: record counts known for only ~30% of incidents; medians, not
means (means are dominated by outliers).

## F5 — Failure modes migrate with the medium
Incident counts by 5-year bucket per class: physical-era classes C1 (misdelivery),
C4 (loss), C5 (disposal) peak in 2010–2014 and collapse after; C3 (misconfiguration)
peaks 2015–2019 and persists into the 2020s (56 → 182 → 90+ post-2020). The corpus
watches breach causation move from mailrooms and dumpsters to cloud consoles.
Caveat: overall VCDB coverage also declines post-2020 (SPEC P0) — present C3's
*relative share*, not absolute counts.

## F6 — Industry skews per class (for the report's small multiples)
C1/C2/C8 lead with Public administration (VA bias for C1 esp.); C4/C5 lead with
Health care; C3 uniquely leads with **Information** industry — cloud-native failure
mode in cloud-native companies. C9 (pretexting/BEC) concentrates in Finance +
Public admin.
