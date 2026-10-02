---
doc_id: STC-DEC-001
title: StepCue design decisions register
project: StepCue
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open items from STC-DDR-001 to STC-DDR-003 and the review note; budget treated as a value-engineering target
---

# StepCue design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

StepCue is a research and educational prototype, not a medical device.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction changes P1 to P12 (two-layer laminate, routed traces with one crossover, sensor tabs on pads, motor through-hole, 9 mm slit tail, curved clip, tail connector in the pod, USB-C through the bottom wall, taped internal parts, screwed lid, button cap, heel notch) | (a) accept as modelled; (b) accept with changes | (a): each keeps what StepCue does, and the model passes 471 constructability checks | The whole build plan is drawn to these changes | STC-DDR-003, Table 1 |
| 2 | How the insole and pod are charged | (a) insole and pod come out of the shoe together, as modelled; (b) an outside connector so the pod unplugs from the tail, adding a part and a wear point | (a) for the prototype; revisit after the first user session at TRL 4 | Tail connector inside the pod (section 3.11, step 12) | STC-DDR-003, A1 |
| 3 | Pod width and lid fixing | (a) 37 mm wide with four M2 screws; (b) 34 mm with a snap-fit lid and no screws | (a): screws are easier to get right first time; a snap lid can follow once the pod is printed | Pod base, lid, screws (sections 3.8 and 3.12) | STC-DDR-003, A2 |
| 4 | Copper tape traces across the flexing arch and ball of the foot | (a) build as modelled and inspect after the first wear trials at TRL 4; (b) lay the traces in a zigzag where they cross the ball of the foot | (a): keep the first build simple; flex life is a TRL 4 test | Carrier film and traces (section 3.2) | STC-DDR-003, A3 |
| 5 | First co-design partner | Movement disorders clinic; physiotherapy practice; Parkinson's patient group | None made | Not part of the TRL 3 build; needed before any user session | STC-DDR-001 and STC-DDR-002, O1 |
| 6 | Appearance model: insole tilted 8 degrees toe-up in the hero render | Keep for the render only; drop | Keep for the render only; the flat fitted state stays the reference | Renders only | Review note, 2026-09-26, item 1 |
| 7 | Smooth spline insole outline | Adopt in the model at the next revision; keep the polygon | Adopt at the next model revision | Insole outline template (Figure 4 of the build plan) | Review note, 2026-09-26, item 2 |
| 8 | Appearance-only features (printed sensor rings, forefoot perforations, grip ribs, lid bezel recess, cadence mark) | Treat as appearance only; add to the model | Appearance only. The four M2 lid screws and their bosses are now in the model (STC-DDR-003) | Renders only | Review note, 2026-09-26, item 3 |
| 9 | Rounded pod envelope (5 mm corner radius) with a parting-line groove | Adopt in the model; keep the square tray and flat lid | Adopt at the next model revision; it softens the edges near the wearer's heel | Pod base and lid shape | Review note, 2026-09-26, item 4 |
| 10 | Clay shoe shell and foot as render context | Keep for renders; use in the concept media too | Keep for renders only | Renders only | Review note, 2026-09-26, item 5 |

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

Value-engineering target: USD 200 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 89.94 for one instrumented insole and one heel pod (USD 110.06 under the target). Main cost drivers and savings worth trying:

- The largest lines are the controller module (USD 15.99), the sensor laminate materials (USD 15.00), the five pressure sensors (USD 14.95), the cell (USD 7.00), and the interface board parts and hardware (USD 6.00 each).
- Making the design constructable added the tail connector (USD 2.50) and the spacer foam (USD 3.00) and repriced the hardware line (USD 5.00 to USD 6.00); the estimate rose from USD 83.44 to USD 89.94.
- Savings worth trying: buy laminate materials (polyimide film, copper tape) in quantities shared across several insoles, since most of the USD 15.00 is a minimum pack; a second insole for the other foot adds about USD 47 for the insole parts alone if it shares one pod design.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: one instrumented insole; nRF52840 module with built-in IMU; pressure plus IMU; electronics in a clip-on heel pod; haptic cue by default with audio through a phone or earbuds; rule-based detector first; commercial FSRs; requirement targets R1 to R15 adopted | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | STC-DDR-001 |
| 2026-09-25 | O2: separate 0.3 s cue-start target for the phone or earbud audio route (0.1 s kept for haptic) | Amish: "i accept all your recommendations, go with them across all repos." | STC-DDR-002 |
| 2026-09-25 | O3: 2.5 mm EVA insole base, 4.50 mm stack (the motor floor and laminate relief of that decision are since replaced by a through-hole, STC-DDR-003, open above) | Amish, same instruction | STC-DDR-002 |
| 2026-09-26 | This repo chosen for the first batch of product renders | Amish | Review note, 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | STC-DDR-003 (draft, changes open above) |
| 2026-10-01 | Budget treated as a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register |
