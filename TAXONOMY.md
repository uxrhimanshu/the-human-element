# Design-failure taxonomy — v1 (2026-07-12)

Refined from taxonomy v0 (SPEC.md) after reading spread samples of real narratives per
VERIS variety (P2). Each class names the *system* failure, not the person's mistake —
the framing throughout is Norman/Reason: error-inviting design, not careless users.

## Classes

**C1 — Wrong-recipient failures** (VERIS `error.variety = Misdelivery`, n=973)
Information reaches the wrong person through a legitimate channel. The narratives kill
the "email autocomplete" stereotype: postal letters, envelope stuffing and mail-merge
errors outnumber email; fax misdials persist. A recurring mechanism is **identity
confusability** — two patients with the same name, medication mailed to the wrong
veteran. Absent design: recipient confirmation, identity disambiguation at selection,
structural pairing of document ↔ addressee.
Exemplars (row_id prefix): `0AAD933B` (same first+last name → wrong medication),
`9C7D3EFE` (transplant records emailed to patient's aunt), `B66DAE70` (repeat wrong-
veteran appointment letters).

**C2 — Visibility-state failures** (`Publishing error`, n=397)
Private content enters a public state without the actor understanding the state change:
files posted to websites, documents indexed by search engines, **ambient displays**
(hospital "Pharmacy Bingo Board" showing patient data on every monitor), PII printed
visible through envelope windows. Absent design: legible public/private state,
pre-publication preview of what will actually be exposed.
Exemplars: `552945F3` (bingo board), `08BA778C` (Stanford ER data on a public site for
a year), `02037087` (AOL search-query release), `A875C73C` (PII visible on envelope).

**C3 — Unsafe defaults & configuration complexity** (`Misconfiguration`, n=336)
Open-by-default datastores (Elasticsearch, MongoDB, S3), authentication never enabled,
settings silently lost **during upgrades/migrations**. The person configuring gets no
view of the delta between intended and actual exposure. Absent design: secure defaults,
exposure previews, config-change diffs.
Exemplars: `376ceb50` (Dow Jones cloud access preferences), `ef6f8c20` (LA County 211 —
settings misconfigured during an upgrade), `feb24580` (Royal Enfield: three databases,
no passwords).

**C4 — Unprotected portability** (`Loss`, n=415)
Data walks out of controlled space and is lost. Paper dominates devices in the
narratives (consent forms, rosters, clipboards) — "paper is an interface too."
Devices that are lost are typically unencrypted. Absent design: encryption by default,
data minimization on portable artifacts, accountability for physical documents.
Exemplars: `2E6C0F08` (inpatient roster "in essence floating"), `AB6E8720`
(unencrypted laptop, patient data), the elevator-ledge clipboard (42 patients' SSNs).

**C5 — End-of-life failures** (`Disposal error`, n=321)
No forcing function between "sensitive artifact" and "gone": records in dumpsters,
storage units auctioned with patient files inside, police interview tapes left in a
decommissioned building, IV bags with labeled PII in regular trash. Disposal is the
least-designed moment in the data lifecycle.
Exemplars: `131ECD74` (IV bags), `05B7D079` (auctioned storage unit), `E258C54F`
(Kent Police basement, £100k ICO fine).

**C6 — Ambient & verbal disclosure** (`Gaffe`, n=41)
Overheard conversations, social-media posts, information spoken to the wrong party.
Small class; kept separate because the "interface" is social space itself.
Exemplar: `EA3C9F0F` (suicide case discussed within earshot).

**C7 — Input-integrity failures** (`Data entry error` + `Classification error`, n=12)
Mis-keyed identifiers, missing sensitivity flags. Almost certainly **undercoded** in
VCDB (entry errors usually surface as some downstream variety); flag this in method.
Exemplar: `BB796274` (HIV medication added without its sensitivity code).

**C8 — Trust-cue failures** (social `Phishing`, n=431)
The channel gives the recipient no reliable way to distinguish authentic from forged —
sender identity, link targets and attachments all spoofable at the interface surface.
Includes major APT campaigns (Red October, Miniduke): the entry point of sophisticated
intrusions is routinely the *least* sophisticated element, an email UI.
Exemplar: `A564EB84` (prosecutor's office ransomware via one link click).

**C9 — Authority-verification failures** (`Pretexting`, n=70)
Urgent instructions from apparent authority, with no out-of-band verification step
built into the workflow: CEO fraud/BEC, W-2 requests from a fake superintendent,
deepfake voice. The design gap is procedural: payment/disclosure flows without a
confirmation affordance that doesn't depend on the compromised channel.
Exemplars: `bbcbdeb0` (deepfake-voice CEO, €220k), `90C9F428` (fake superintendent
W-2 harvest), `FE435E44` (caller "pretended to be the victim's son", bank complied).

**C0 — Other human-element** (everything else with `action.error` or `action.social`)
Programming error, Malfunction, Maintenance error, Bribery, Extortion, etc. Human
element per VERIS but not interface/workflow design failures. Kept for denominator
honesty; excluded from the design analysis. Bribery/extortion are willful-actor
problems, not error-inviting design.

## Machine-readable assignment rules (for `pipeline/taxonomy.py`)

Multi-label; an incident can carry several classes.

| Class | Rule (on incidents.csv fields) |
|---|---|
| C1 | `Misdelivery` in error_varieties |
| C2 | `Publishing error` in error_varieties |
| C3 | `Misconfiguration` in error_varieties |
| C4 | `Loss` in error_varieties |
| C5 | `Disposal error` in error_varieties |
| C6 | `Gaffe` in error_varieties |
| C7 | `Data entry error` or `Classification error` in error_varieties |
| C8 | `Phishing` in social_varieties |
| C9 | `Pretexting` in social_varieties |
| C0 | (action_error or action_social) and none of C1–C9 matched |

## Sub-mechanism rules (lowercase substring match on summary; multi-label)

| Class | Sub-mechanism | Keywords |
|---|---|---|
| C1 | channel:email | `email`, `e-mail` |
| C1 | channel:postal | `letter`, `envelope`, `mailed`, `mailing`, ` mail `, `postal` |
| C1 | channel:fax | `fax` |
| C1 | wrong-attachment | `attach` |
| C2 | web-posting | `website`, `web site`, `online`, `posted`, `published`, `uploaded` |
| C2 | search-indexed | `google`, `search engine`, `indexed` |
| C2 | ambient-display | `monitor(s)`, `screen(s)`, `display(s)` — whole words only |
| C3 | open-datastore | `elasticsearch`, `mongodb`, `s3`, `bucket`, `database`, `rsync` |
| C3 | during-change | `upgrade`, `migration`, `updated`, `update` |
| C3 | no-auth | `password`, `unsecured`, `unprotected` |
| C4 | paper | `paper`, `document`, `folder`, `binder`, `clipboard`, `form(s)` (whole word — else it matches "information"), `records` |
| C4 | device-media | `laptop`, `usb`, `thumb drive`, `flash drive`, `phone`, `cd(s)` (whole word), `disk`, `tape`, `computer`, `hard drive`, `external drive` |
| C5 | trash-stream | `dumpster`, `trash`, `recycl`, `landfill`, `curb` |
| C5 | resale-abandonment | `sold`, `auction`, `donated`, `storage unit`, `abandoned` |
| C5 | shred-failure | `shred` |

Sub-mechanisms are indicative (keyword recall is imperfect); report them as "at least
n mentions", never as complete counts. Incidents with empty summaries get classes but
no sub-mechanisms.

## Method caveats logged during P2
- **VA/healthcare source bias**: VCDB bulk-imported US Veterans Affairs privacy
  incident reports; Misdelivery/Loss/Gaffe narratives are heavily VA. Report
  prevalence *within* the corpus, never as population rates; disclose the skew.
- Coverage peaks 2010–2019 (from SPEC.md P0) — trends after 2020 are unreliable.
- `Unknown` varieties (50 error incidents) carry action_error but no variety → they
  land in C0.
- C7 is systematically undercoded; do not headline its small n.
