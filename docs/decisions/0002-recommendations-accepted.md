---
doc_id: STC-DDR-002
title: StepCue recommendations accepted
project: StepCue
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 acceptance of all open recommendations
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "O1 decided by Amish as recommended (STC-DEC-001)"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items O2 and O3); item O1 decided by Amish on 2026-10-02: "i approve your recommendations for all 555 open decisions." (STC-DEC-001)

## Context

After the TRL 3 session, `docs/REVIEW.md` and STC-DDR-001 listed three items still awaiting Amish. On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every open item that carried a recommendation is therefore decided as recommended. An item with no recommendation stays open. TRL 4 remains on hold by Amish's instruction, and nothing in this record moves the design past TRL 3.

## Options considered

Table 1. Open items at the start of this decision.

| # | Item | Options | Recommendation |
| --- | --- | --- | --- |
| O1 | First co-design partner | Movement disorders clinic; physiotherapy practice; Parkinson's patient group | None |
| O2 | R6 cue-start target for the phone or earbud audio route | (a) keep 0.1 s and accept that audio misses it; (b) 0.3 s for the audio route only, 0.1 s kept for the haptic default | (b) |
| O3 | R9 insole thickness margin | (a) keep the 3.0 mm EVA base, 5.00 mm stack, zero margin; (b) 2.5 mm EVA base, 4.50 mm stack, with a 0.4 mm relief for the motor in the laminate | (b) |

## Decision

- **O2.** Decided by Amish, 2026-09-25: go with recommendation. R6 now reads: haptic cue 0.1 s or less after a detection; audio through a phone or earbuds 0.3 s or less. Latency shifts only the first beat, since the pod sends beat timing rather than a trigger per beat.
- **O3.** Decided by Amish, 2026-09-25: go with recommendation. The insole base is 2.5 mm EVA. The 2.7 mm coin motor sits on a 0.2 mm EVA floor in its pocket and stands 0.4 mm proud into a relief in the underside of the sensor laminate, leaving 0.4 mm of laminate over it.

Items left open on 2026-09-25, since decided:

- **O1.** First co-design partner. No recommendation was made on 2026-09-25. Decided by Amish, 2026-10-02, as later recommended: a Parkinson's patient group, recruited through a local support group affiliated with the Parkinson's Foundation (the first candidate to approach), with a physiotherapy practice brought in for the first supervised user session (STC-DEC-001).

No budget, pitch or problem change was recommended, so `budget_usd` stays at $200 and the pitch and problem lines are unchanged. No item needs a change in another repo. No item called for TRL 4 work.

## Consequences

Table 2. What changed in the repo.

| Item | File | Before | After |
| --- | --- | --- | --- |
| O2 | `docs/03-requirements.md` (STC-REQ-001 v0.4) | R6: 0.1 s for any cue; audio route not met (0.18 to 0.28 s) | R6: 0.1 s haptic, 0.3 s audio route; met (41 ms haptic, 0.18 to 0.28 s audio) |
| O2 | `docs/04-calcs/sizing.py`, `01-sizing.md` (STC-CAL-001 v0.2) | R6 status "Not met (audio route)" | Two targets checked; R6 met with 20 ms margin at worst on assumed audio latencies |
| O3 | `cad/src/model.py`, `cad/step/`, `cad/stl/` | `foam_t` 3.0 mm; motor top flush with the EVA | `foam_t` 2.5 mm; motor on a 0.2 mm floor; 0.4 mm relief cut in the laminate |
| O3 | `docs/03-requirements.md`, STC-CAL-001 | R9 at risk, 5.00 mm, zero margin | R9 met, 4.50 mm (4.3 to 4.7 mm with EVA tolerance) |
| O3 | `cad/drawings/STC-DWG-001` | Rev P1, stack 5.0 | Rev P2, stack 4.5, motor relief noted |
| O3 | `bom/bom.csv` | Line 6: 3 mm EVA | Line 6: 2.5 mm EVA; line 3 notes the motor relief; total unchanged at $83.44 |
| O2, O3 | `docs/02-concept.md` (STC-PRC-001 v0.4) | O2 and O3 listed as proposed | Recorded as decided; key numbers updated |
| O2, O3 | `docs/decisions/0001-trl2-review-decisions.md` (STC-DDR-001 v0.2) | O2 and O3 "Proposed, awaiting Amish" | Marked decided, pointing to this record |
| O3 | `media/` | 3.0 mm base | Regenerated from the updated model |

Requirement status at TRL 3 (STC-CAL-001 v0.2) moves from 9 met, 1 not met, 4 at risk and 1 not verifiable to 11 met, 0 not met, 3 at risk (R3, R4, R5) and 1 not verifiable (R12).

The design stops at TRL 3. Measuring the audio-route latency, the insole thickness and the felt motor intensity through the thinner stack is TRL 4 work and is on hold.
