---
doc_id: STC-DEC-001
title: StepCue design decisions register
project: StepCue
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open items from STC-DDR-001 to STC-DDR-003 and the review note; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 10 (STC-DDR-003 accepted); moved to decisions made"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: Smooth insole outline and rounded pod carried into the model; value engineering checked (no price change)
---

# StepCue design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

StepCue is a research and educational prototype, not a medical device.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The pressure sensor's tail reaches about 12 mm past the disc and its two tabs are 2.54 mm apart | The tab pads on the carrier are placed for this; a longer tail moves them | STC-DDR-003, P2 |
| 2 | How far the controller module's USB-C receptacle stands past its board end (1.4 mm assumed) | Sets whether a plug seats fully in the bottom-wall notch | STC-DDR-003, P8 |
| 3 | The 8-way flat flex cable has same-side contacts and its 9 mm width matches the ZIF connector | The tail must go into the connector with its contacts toward the board | STC-DDR-003, P5 and P7 |
| 4 | The cell is 502535 class (about 35 x 25 x 5 mm) and protected | The pod's inside is sized round it, and R15 needs a protected cell | STC-CAL-001, R10 and R15 |
| 5 | The heel counter of the test shoe is about 3.5 mm thick and curved at about 32 mm radius inside | The clip's 1 mm grip and its curve are set for this counter | STC-CAL-001, R12 |
| 6 | The polyimide film takes solder at about 300 °C without lifting its adhesive | The sensors, tail strips and motor leads are soldered to pads on it | STC-DDR-003, P1 |

## Value engineering

Value-engineering target: USD 200. Estimated cost of the constructable design: USD 89.94 (USD 110.06 under the target). The target is a hypothetical control figure, not a limit; the estimate is for one instrumented insole and one heel pod, and is unchanged by the smooth insole outline and rounded pod carried into the model on 2026-10-02. Main cost drivers and savings worth trying:

- The largest lines are the controller module (USD 15.99), the sensor laminate materials (USD 15.00), the five pressure sensors (USD 14.95), the cell (USD 7.00), and the interface board parts and hardware (USD 6.00 each).
- Making the design constructable added the tail connector (USD 2.50) and the spacer foam (USD 3.00) and repriced the hardware line (USD 5.00 to USD 6.00); the estimate rose from USD 83.44 to USD 89.94.
- Savings worth trying: buy laminate materials (polyimide film, copper tape) in quantities shared across several insoles, since most of the USD 15.00 is a minimum pack; a second insole for the other foot adds about USD 47 for the insole parts alone if it shares one pod design.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: one instrumented insole; nRF52840 module with built-in IMU; pressure plus IMU; electronics in a clip-on heel pod; haptic cue by default with audio through a phone or earbuds; rule-based detector first; commercial FSRs; requirement targets R1 to R15 adopted | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | STC-DDR-001 |
| 2026-09-25 | O2: separate 0.3 s cue-start target for the phone or earbud audio route (0.1 s kept for haptic) | Amish: "i accept all your recommendations, go with them across all repos." | STC-DDR-002 |
| 2026-09-25 | O3: 2.5 mm EVA insole base, 4.50 mm stack (the motor floor and laminate relief of that decision are since replaced by a through-hole, STC-DDR-003, accepted on 2026-10-02) | Amish, same instruction | STC-DDR-002 |
| 2026-09-26 | This repo chosen for the first batch of product renders | Amish | Review note, 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | STC-DDR-003 (changes accepted on 2026-10-02, below) |
| 2026-10-01 | Budget treated as a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 as modelled (option a) | Amish: "i approve your recommendations for all 555 open decisions." | STC-DDR-003, Table 1 |
| 2026-10-02 | Charging: insole and pod come out of the shoe together (option a) for the supervised prototype sessions; an outside connector so the pod unplugs from the tail (option b) is to be decided before any take-home use | Amish: "i approve your recommendations for all 555 open decisions." | STC-DDR-003, A1 |
| 2026-10-02 | Pod 37 mm wide with four M2 lid screws (option a); a snap lid can follow once the pod is printed | Amish: "i approve your recommendations for all 555 open decisions." | STC-DDR-003, A2 |
| 2026-10-02 | Traces across the arch and ball of the foot: build as modelled (option a), check every trace for continuity before each wear session, and inspect after the first wear trials at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | STC-DDR-003, A3 |
| 2026-10-02 | First co-design partner: a Parkinson's patient group, recruited through a local support group affiliated with the Parkinson's Foundation (the first candidate to approach), with a physiotherapy practice brought in for the first supervised user session | Amish: "i approve your recommendations for all 555 open decisions." | STC-DDR-001 and STC-DDR-002, O1 |
| 2026-10-02 | Hero render: the 8 degree toe-up insole tilt for the hero render only; the flat fitted state stays the reference | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 1 |
| 2026-10-02 | Smooth spline insole outline adopted at the next model revision; the traces keep their 1.5 mm edge margin (in the model since 2026-10-02) | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 2 |
| 2026-10-02 | Printed sensor rings, forefoot perforations, grip ribs, lid bezel recess and cadence mark are appearance only | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 3 |
| 2026-10-02 | Rounded pod envelope with a 5 mm corner radius and a parting-line groove adopted at the next model revision (in the model since 2026-10-02) | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 4 |
| 2026-10-02 | Clay shoe shell and foot kept for the renders only | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 5 |
