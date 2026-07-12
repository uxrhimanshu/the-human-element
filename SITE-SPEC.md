# Site spec — "The Human Element" report (P4)

Build `site/index.html` — one fully self-contained file (all CSS/JS inline, zero
external requests: no CDNs, no webfonts, no fetch). Charts are hand-built inline
SVG rendered by vanilla JS from a `const DATA = {...}` block. Netlify-ready static.

## Register
Long-form editorial research report, not a dashboard. Generous whitespace, measured
pace, ~68ch prose column, charts break wider (max ~880px). Serif for headlines and
body prose (`Georgia, 'Times New Roman', serif`); ALL chart text, figures, captions,
labels in system sans (`system-ui, -apple-system, "Segoe UI", sans-serif`). No
emojis, no decorative icons. Reads like a serious publication.

## Color tokens (pre-validated reference palette — use exactly these)
```css
:root { /* light */
  --page:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink-2:#52514e;
  --muted:#898781; --grid:#e1e0d9; --baseline:#c3c2b7;
  --accent:#2a78d6;          /* the ONLY data hue */
  --accent-deep:#1c5cab; --accent-light:#9ec5f4;
  --gray-bar:#c3c2b7;        /* de-emphasis series */
  --border:rgba(11,11,11,0.10);
}
@media (prefers-color-scheme: dark) { :root {
  --page:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink-2:#c3c2b7;
  --muted:#898781; --grid:#2c2c2a; --baseline:#383835;
  --accent:#3987e5; --accent-deep:#6da7ec; --accent-light:#184f95;
  --gray-bar:#52514e; --border:rgba(255,255,255,0.10);
}}
```
Every chart: single accent hue + de-emphasis gray (emphasis form) or single-hue
magnitude. No multi-hue categorical anywhere. Chart text uses ink tokens, never
the series color. Thin marks; horizontal bars 20px tall, 10px gap, 4px rounded
right end only (flat at baseline); hairline grid; recessive axes. Direct labels
(value at bar end, sans, --ink-2); no legend needed anywhere (≤2 series, always
direct-labeled). Hover: per-mark tooltip (small sans card: label, value, and where
relevant "n=" note), hit target = full row height. Each figure gets a numbered
caption (Figure 1…6) in sans, --muted, plus a `<details>Data table</details>`
fallback beneath with the exact numbers.

## Page structure & copy (copy is FINAL unless marked draft — do not rewrite it)

### Hero
Kicker (sans, letterspaced, --muted): A DESIGN-RESEARCH STUDY
H1: The Human Element
Deck: What 10,042 real security incidents reveal about design failure.
Byline: Himanshu Kalra · UX researcher · July 2026 · Data: VERIS Community Database

Three stat tiles (sans; value ≥40px, label beneath):
- 3,321 — incidents involving human error or deception
- 78% — of error-caused breaches were discovered by outsiders
- 700,000 — median records exposed by a single misconfiguration

### Section 1 — The wrong villain
Prose:
"Ask someone to picture a data breach and they picture an attacker: hooded,
foreign, brilliant. The record disagrees. In the VERIS Community Database — ten
thousand publicly documented security incidents, coded by a community of analysts
on a common schema — mistakes rival malice. 2,681 incidents involve error as an
action. 2,650 of them involve no hacking and no social engineering at all: no
adversary, no exploit, nobody to blame but the way the work was designed.

For every four breaches caused by attackers in this corpus, three are
self-inflicted.

This matters for design because the security industry is organized around the
attacker. Budgets, tooling, and attention all face outward. The inward-facing
failures — the misaddressed letter, the public bucket, the dumpster — belong to
no one. This study reads them as what they are: design failures, in the tradition
of Don Norman and James Reason. When the same mistake recurs across thousands of
organizations, the interesting question is not who erred, but what design made
the error easy."

**Figure 1** — "What causes breaches in this corpus". Horizontal bar, incidents
per action type (multi-label; sums exceed total): Hacking 3,364 / **Error 2,681
(accent, all others --gray-bar)** / Misuse 1,789 / Malware 1,646 / Physical 1,626
/ Social 644. Caption notes multi-label coding.

### Section 2 — A taxonomy of design failure
Prose:
"Every human-element incident was assigned to one of nine design-failure classes,
derived from VERIS's own action varieties and refined against the incident
narratives. The names deliberately describe the system, not the person. 'Misdelivery'
sounds like someone's fault; 'wrong-recipient failure' asks what let the wrong
recipient happen."

**Figure 2** — "The nine classes". Horizontal bar, single hue (--accent), sorted
desc: Wrong-recipient failures 973 / Trust-cue failures 431 / Unprotected
portability 415 / Visibility-state failures 397 / Unsafe defaults &
configuration 336 / End-of-life failures 321 / Authority-verification failures 70
/ Ambient & verbal disclosure 41 / Input-integrity failures 12. Caption: "359
further incidents carry a human element but fall outside these classes
(programming errors, bribery, extortion…)."

Then nine class cards (stacked, generous). Each card: class name + n + one-line
definition + "The missing design:" line + one verbatim exemplar quote (styled as
a pull quote, sans, on --surface with hairline border; attribution "VCDB incident
narrative"). Copy:

C1 — Wrong-recipient failures (n=973). Information reaches the wrong person
through a legitimate channel. Postal mail, not email, is the leading mechanism —
mail merges, stuffed envelopes, look-alike names. The missing design: recipient
confirmation, and disambiguation when two records nearly collide.
Quote: "Medication for Veteran A was mailed to Veteran B. The first and last name
was the same for both veterans."
**Figure 3 (inside this card)** — mini horizontal bar "Mechanisms mentioned in
narratives": postal 393 / email 209 / fax 57 / wrong attachment 54. Single hue.
Caption: "Keyword mentions; indicative, not exhaustive."

C2 — Visibility-state failures (n=397). Private content enters a public state
without the actor understanding the state change — posted files, indexed
documents, data visible on screens and envelope windows. The missing design: a
legible public/private state, and a preview of what will actually be exposed.
Quote: "There was a privacy breach this morning for a brief period (10-15 minutes)
where the Pharmacy Bingo Board was displaying private patient information on
monitors throughout the hospital."

C3 — Unsafe defaults & configuration complexity (n=336). Open-by-default
datastores, authentication never enabled, settings silently lost during upgrades.
The person configuring never sees the delta between intended and actual exposure.
The missing design: secure defaults and an exposure preview.
Quote: "The information of more than 2 million Dow Jones customers was left
exposed online after the company made an error in the access preferences on a
cloud storage system."

C4 — Unprotected portability (n=415). Data walks out of controlled space and is
lost. In the narratives, paper outnumbers laptops. The missing design: encryption
by default, and minimizing what portable artifacts carry at all.
Quote: "A VA employee lost an inpatient roster with 24 patients' information…
He cannot recall where he left this paper and it is in essence floating."

C5 — End-of-life failures (n=321). Records in dumpsters, storage units auctioned
with patient files inside, interview tapes left in a decommissioned building.
Disposal is the least-designed moment in the data lifecycle. The missing design:
a forcing function between "sensitive" and "gone".
Quote: "An employee removed two IV bags with PII of two Veterans on the labels
from the regular trash."

C6 — Ambient & verbal disclosure (n=41). The interface is social space itself:
conversations overheard, information posted to personal feeds.
Quote: "Employee A overheard Employee B and C discussing and reviewing a
patient's information."

C7 — Input-integrity failures (n=12). Mis-keyed identifiers, missing sensitivity
flags. Almost certainly undercounted — entry errors usually surface downstream
as some other failure. (No pull quote; keep card short.)

C8 — Trust-cue failures (n=431). Phishing works because the channel gives the
recipient no reliable way to tell authentic from forged — sender, links and
attachments are all spoofable at the surface the user can see. Several of the
most sophisticated intrusion campaigns in the corpus begin with the least
sophisticated element: an email that looked right.
Quote: "The prosecutor's office was hit by ransomware in January 2015 when an
employee clicked on a link embedded in a phishing email."

C9 — Authority-verification failures (n=70). Urgent instructions from apparent
authority, in workflows with no out-of-band confirmation step. Business email
compromise, W-2 harvests, and — already in this corpus — a synthesized voice.
Quote: "The CEO of an unnamed UK-based energy company thought he was talking on
the phone with his boss… who'd asked him to urgently transfer €220,000."

### Section 3 — Nobody catches their own mistakes
Prose:
"How does an organization learn that it has breached itself? Mostly, it doesn't.
Where the discovery method is recorded — 1,248 of the 2,681 error incidents —
78% were discovered by someone outside the organization. The single most common
discoverer is the customer: the person whose data was exposed is the person who
finds the exposure. Attackers at least have a reason to stay hidden; a
misdelivered letter hides nothing, and still the institution is the last to know.

One caveat is owed here: incidents discovered by outsiders are also more likely
to become public at all, so the true external share is probably lower. The
asymmetry, not the exact figure, is the finding."

**Figure 4** — two-part figure. (a) One horizontal 100% stacked bar "Who
discovers error-caused breaches" — External 78% (--accent) / Internal 21%
(--gray-bar) / Partner 1% (--baseline); 2px surface gaps between segments; direct
labels, sans. (b) Horizontal bar "External discoverers": **Customer 371 (accent)**
/ Security researcher 180 / Found documents 158 / Unrelated third party 77 /
Actor disclosure 38 / Other 17 / Law enforcement 13 / Audit 8 (all gray except
Customer). Caption: "n = 1,248 error incidents with a recorded discovery method."

### Section 4 — The blast-radius ladder
Prose:
"Not all design failures are the same size, and the pattern in their sizes is
the sharpest finding in this corpus. Where a record count is known, the median
wrong-recipient failure exposes two records — one letter, one wrong hands. The
median misconfiguration exposes seven hundred thousand.

A person can only mis-send one envelope at a time. A checkbox on a cloud console
operates on everything behind it. As the interface becomes more abstract — from
envelope to attachment to bucket policy — the same-sized human slip touches more
people. The duty of care owed by the design scales the same way: an error-proof
console matters five orders of magnitude more than an error-proof envelope."

**Figure 5** — "Median records exposed per failure class" — horizontal dot plot
on a log10 x-axis (10⁰…10⁶, gridlines at powers of ten, labeled 1 / 10 / 100 /
1k / 10k / 100k / 1M, sans): Wrong-recipient 2 (n=802) / Unprotected portability
808 (n=335) / Visibility-state 1,581 (n=256) / Trust-cue (phishing) 3,020 (n=116)
/ **Unsafe defaults 700,000 (n=236, accent; others --gray-bar)**. Dots ≥10px,
value direct-labeled beside each dot, n= in tooltip. Caption: "Medians; record
counts are known for roughly 30% of incidents. Log scale."

### Section 5 — Failure follows the medium
Prose:
"The corpus also watches failure move. Among human-element incidents of 2010–2014,
the physical world dominates: misdelivered letters, lost paper, dumpsters. A
decade later the physical classes have collapsed and one digital class has taken
over: by 2020–2024, unsafe defaults and misconfiguration account for over half of
coded human-element incidents. The mistake did not go away — it moved into the
console, and grew six orders of magnitude in reach.

Reporting also declined in this period, so shares are more trustworthy than
counts; the direction is unambiguous."

**Figure 6** — "Share of human-element incidents by era". Line chart, x = three
eras (2010–14, 2015–19, 2020–24), y = share (0–60%). Four lines: Unsafe defaults
& configuration 3% → 16% → 54% (**accent, 2px**); Wrong-recipient 36% → 23% → 8%,
Unprotected portability 16% → 8% → 2%, End-of-life 11% → 9% → 1% (all --gray-bar,
2px, direct-labeled at line end, sans). Markers ≥8px with 2px surface ring.
Caption: "Era totals: 1,889 / 1,166 / 166 incidents — the last era is small;
read shares, not counts."

### Section 6 — What this asks of design (short close)
Prose:
"Security has a well-funded conversation about attackers and a nearly empty one
about defaults, confirmation steps, state legibility, and end-of-life. The
findings here are an argument that the second conversation belongs to design
research: the failures are patterned, the patterns are legible in ordinary
qualitative data, and every one of the nine classes names a designable surface.
The human element is not the weakest link. It is the part of the system that was
never given a designer."

### Method (its own visually quieter section, sans, slightly smaller)
Content (draft register is fine, keep all points):
- Source: VERIS Community Database (VCDB), the open incident corpus behind
  Verizon's DBIR; combined JSON of 2026-07-03; 10,042 incidents, 9,523 with
  free-text narratives. Single-source by design.
- Unit & coding: incidents multi-labeled into nine design-failure classes by
  deterministic rules over VERIS action varieties (mapping table published in the
  repo); sub-mechanisms from word-boundary keyword matching over narratives,
  reported as "at least n mentions".
- All prevalence figures are within-corpus, not population estimates. VCDB
  bulk-imported US Veterans Affairs privacy reports, inflating healthcare/public-
  administration and postal mechanisms; coverage peaks 2010–2019 and thins after
  2020; record counts are known for ~30% of incidents; the discovery-method
  finding carries a visibility bias acknowledged in the text.
- Pipeline: Python, deterministic, re-runnable (fetch → tidy → code → profile);
  exemplar quotes are verbatim incident narratives from the public dataset,
  lightly truncated.
- Author: Himanshu Kalra. Built as a public design-research study, 2026.

### Footer
"Himanshu Kalra — UX researcher." (placeholder link himanshukalra.com), year.

## Interactions
- Tooltips as specced (vanilla JS, one absolutely-positioned card, sans).
- Smooth-scroll nav: a slim sticky top bar (sans, --muted) with section links,
  visible after scrolling past hero.
- No scrolljacking, no animation beyond 150ms fades. prefers-reduced-motion: none.
- Keyboard: figures focusable, tooltips shown on focus; all data also in the
  <details> tables.

## Acceptance criteria (verify before finishing)
1. Every number on the page matches this spec exactly (they are pre-verified
   against the dataset — do not recompute, do not invent).
2. Zero external requests (grep for http src/href besides internal anchors and
   the footer link); works from file://.
3. Light AND dark render correctly (tokens above; test both).
4. No horizontal page scroll at 360px, 768px, 1280px; charts scale (SVG
   viewBox + width:100%).
5. Copy used verbatim from this spec (typography quotes/dashes may be normalized).
6. Valid single HTML file at site/index.html. No console errors.
7. Do not modify anything outside site/. Do not commit.
