---
doc_id: STC-DDR-001
title: StepCue TRL 2 review decisions
project: StepCue
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review points
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); O2 and O3 marked decided
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items D1 to D8); items O2 and O3 decided by Amish on 2026-09-25 (recorded in STC-DDR-002); item O1 remains proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25, /populate) listed nine items marked "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided as recommended. The item without a recommendation stays open.

## Options considered

Table 1. Items with a recommendation.

| # | Item | Options | Recommendation |
| --- | --- | --- | --- |
| D1 | One instrumented insole or a pair | (a) one insole on the side the wearer reports freezing most, about $106 at TRL 2; (b) a pair, about $212, over budget | (a) one insole |
| D2 | Controller | (a) ESP32-C3 module plus separate IMU and analog multiplexer; (b) nRF52840 module with built-in IMU and six analog inputs (Seeed XIAO nRF52840 Sense class) | (b) nRF52840 with built-in IMU |
| D3 | Sensing | Pressure only; pressure plus 6-axis IMU | Pressure plus IMU |
| D4 | Where the electronics go | Clip-on heel pod; embedded in the insole | Clip-on heel pod |
| D5 | Default cue and audio route | Haptic under the arch; piezo audio in the pod; audio on a phone or earbuds over BLE | Haptic by default; audio through a phone or earbuds rather than the piezo |
| D6 | Detector approach | Rule-based thresholds; trained classifier | Rule-based first, trained classifier once labeled data exist |
| D7 | Sensor type | Commercial FSRs; DIY piezoresistive film | Commercial FSRs for the first build |
| D8 | Requirement targets | R1 to R15 as written in STC-REQ-001 v0.2 | Adopt as written |

## Decision

- **D1.** Decided by Amish, 2026-09-25: go with recommendation. One instrumented insole, worn on the side where the wearer reports freezing most. A pair is out of scope for the first build.
- **D2.** Decided by Amish, 2026-09-25: go with recommendation. Seeed Studio XIAO nRF52840 Sense class module (nRF52840, LSM6DS3TR-C IMU, six analog inputs, BQ25101 charger, USB-C). The separate IMU breakout and the analog multiplexer are removed from the design.
- **D3.** Decided by Amish, 2026-09-25: go with recommendation. Pressure plus the module's 6-axis IMU. The pitch ("pressure-sensing insole") is unchanged.
- **D4.** Decided by Amish, 2026-09-25: go with recommendation. Electronics and the lithium cell live in a clip-on heel pod outside the shoe.
- **D5.** Decided by Amish, 2026-09-25: go with recommendation. The coin motor under the arch is the default cue. Audio, where the wearer prefers it, is played by a paired phone or earbuds over BLE. The piezo buzzer is removed from the pod.
- **D6.** Decided by Amish, 2026-09-25: go with recommendation. The first detector is a set of inspectable thresholds; a trained classifier follows only once labeled data exist.
- **D7.** Decided by Amish, 2026-09-25: go with recommendation. Five commercial force-sensing resistors (Interlink FSR 402 class).
- **D8.** Decided by Amish, 2026-09-25: go with recommendation. Targets R1 to R15 are adopted as written, with the R7 audio route and the R14 unit definition restated to match D1 and D5 (STC-REQ-001 v0.3).

Budget and pitch: the TRL 2 review recommended keeping `budget_usd` at $200 with the budget defined as one unit of one instrumented insole and one heel pod. That definition is written into R14. The review made no recommendation to reword the pitch or problem lines, so they are unchanged.

Items that remain open:

- **O1.** First co-design partner: a movement disorders clinic, a physiotherapy practice or a Parkinson's patient group. No recommendation was made; portfolio guidance is that community designs pick co-design partners per area later. Proposed, awaiting Amish.

New items raised at TRL 3, later decided (STC-DDR-002):

- **O2.** R6 for the audio route. The phone or earbud route of D5 starts a cue about 0.18 to 0.28 s after detection by estimate (STC-CAL-001, section 6), against the 0.1 s target. Options: (a) keep 0.1 s and accept that the audio route does not meet it; (b) set 0.3 s for the audio route only, keeping 0.1 s for the haptic default. Recommendation: (b), since latency shifts only the first beat and not the rhythm. Decided by Amish, 2026-09-25: go with recommendation (STC-DDR-002).
- **O3.** R9 thickness margin. The stack is exactly 5.0 mm. Options: (a) keep the 3.0 mm EVA base and accept zero margin; (b) use a 2.5 mm EVA base, giving 4.5 mm, with a 0.4 mm relief for the motor in the laminate. Recommendation: (b). Decided by Amish, 2026-09-25: go with recommendation (STC-DDR-002).

## Consequences

- STC-REQ-001 v0.3: R7 names the phone or earbud audio route; R14 defines a unit as one instrumented insole and one heel pod; status column replaced by the TRL 3 status from STC-CAL-001.
- STC-PRC-001 v0.3: D1 to D8 are recorded as decided; components, first-order numbers and figures follow the TRL 3 model and STC-CAL-001.
- STC-PRB-001 v0.3: the one-or-two-insoles question is closed; the partner question stays open.
- `bom/bom.csv`: the ESP32-C3 module, IMU breakout, multiplexer and piezo buzzer lines are removed; the XIAO nRF52840 Sense class module and an interface board are added.
- The design stops at TRL 3. TRL 4 is on hold by Amish's instruction.
