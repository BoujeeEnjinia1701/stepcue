---
doc_id: STC-REQ-001
title: StepCue requirements
project: StepCue
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with concept status
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Targets adopted by Amish 2026-09-25 (STC-DDR-001); R7 audio route and R14 unit restated; TRL 3 status from STC-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); R6 audio-route target 0.3 s; R9 met with 2.5 mm EVA base
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from STC-CAL-001 v0.3 after the design for construction (STC-DDR-003, draft); R10 and R14 figures updated, no status changed
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: Status from STC-CAL-001 v0.4 after the model revision of 2026-10-02; R10 mass updated, no status changed
---

# StepCue requirements

Amish adopted targets R1 to R15 on 2026-09-25 (STC-DDR-001, decision D8). R7 and R14 are restated to match decisions D1 (one instrumented insole) and D5 (haptic cue by default, audio through a phone or earbuds). R6 is restated with a separate target for the audio route, decided by Amish on 2026-09-25 (STC-DDR-002, item O2). The status column gives the TRL 3 position from the calculation note STC-CAL-001 v0.4, after the design for construction changes of STC-DDR-003 (accepted by Amish on 2026-10-02) and the smooth insole outline and rounded pod decided the same day; nothing here has been measured.

Table 1. Requirements and TRL 3 status.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (STC-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Sense plantar loading at the main contact regions | 5 or more pressure sites (heel, lateral midfoot, first and fifth metatarsal heads, hallux), each sampled at 100 Hz or more | Design review; sampling calculation | Met: 5 FSRs at 104 Hz. Four sites exceed the 20 N sensor range at peak load, so force above 20 N is lost; timing and center-of-pressure features remain |
| R2 | Sense foot motion for the freeze band | 6-axis IMU at 100 Hz or more, covering the 3 to 8 Hz freeze band and the 0.5 to 3 Hz locomotor band | Datasheet; sampling calculation | Met: module IMU at 104 Hz, 0.50 Hz bins |
| R3 | Detect freezes quickly | Median delay from freeze onset to detection 2 s or less | Offline replay of labeled data | **At risk.** Method floor 1.50 s with one window, 2.50 s with the confirmation R5 needs (synthetic) |
| R4 | Detect freezes reliably | Episode sensitivity 80 % or more; window specificity 85 % or more | Offline replay of labeled data | **At risk.** Published pressure-only results are about 77 to 80 % and 83 to 85 % |
| R5 | Avoid nuisance cues | 1 false cue or fewer per 10 min of ordinary walking | Offline replay; later supervised trial | **At risk.** Needs 5 or more confirming windows at 85 % specificity |
| R6 | Start the cue promptly | Haptic cue starts 0.1 s or less after a detection; audio through a phone or earbuds starts 0.3 s or less after a detection | Firmware timing calculation | Met: haptic 41 ms; audio route about 0.18 to 0.28 s (estimate, 20 ms margin at worst) |
| R7 | Deliver a rhythmic cue the wearer can feel or hear | Haptic pulses at the wearer's baseline cadence (adjustable 60 to 130 per minute); where the wearer chooses audio, beeps of 60 dB(A) or more at the ear through a paired phone or earbuds | Calculation from datasheets; later bench measurement | Met: 203 Hz pulses stay distinct at 130 per minute; earbuds exceed 60 dB(A). Felt intensity through a sock cannot be shown on paper |
| R8 | Stop cueing when walking resumes | Cue stops within 3 regular steps, or after 15 s at most | Firmware logic review | Met by design (3 steps about 1.7 s) |
| R9 | Keep the shoe comfortable | Insole stack 5.0 mm or less; no rigid part thicker than 1 mm under the heel or metatarsal heads | Parametric model; later pressure mapping | Met: 4.50 mm with the 2.5 mm EVA base (4.7 mm at the upper EVA tolerance); FSRs 0.46 mm |
| R10 | Keep the heel pod light and small | Pod 35 g or less; body no larger than 45 x 40 x 20 mm | Parametric model; later weighing | Met: 26.8 g; 42 x 37 x 15 mm (20.3 mm deep including the clip) |
| R11 | Run a full day and more | 2 days or more between charges at 16 h per day of wear | Power budget calculation | Met: 12.5 days nominal, 7.4 days conservative |
| R12 | Usable with reduced dexterity | Pod clips on and off one-handed; USB-C charging with the pod off the shoe; one large button to pause cues | Design review; later user session | Not verifiable at TRL 3. Clip removal about 6 N by calculation; 10 mm button |
| R13 | Keep data with the wearer | Detection and cueing on the device; optional event log exported over USB or BLE by the owner only; no cloud | Design review | Met by design; the phone is used only for optional audio |
| R14 | Low cost and buildable | Parts cost $200 or less per unit, a unit being one instrumented insole and one heel pod; no custom rigid PCB for the first build | Priced BOM | Met: $89.94, $110.06 under the $200 value-engineering target |
| R15 | Safe to wear | Protected lithium cell outside the shoe; no exposed conductors; skin-contact materials suitable for footwear | Design review | Met by design |

## Requirements not met or at risk

No requirement is not met at TRL 3. R6 (audio route) and R9, listed here in STC-REQ-001 v0.3, are now met after Amish's 2026-09-25 decisions O2 and O3 (STC-DDR-002).

- **R3, R4 and R5, at risk.** The confirmation that R5 needs pushes the detection delay past R3, and published pressure-only accuracy sits at the edge of R4. None can be verified without a labeled plantar-pressure data set.
- **R12, not verifiable at TRL 3.** One-handed use needs a session with users, which is TRL 4 or later and on hold.

## Assumptions

- Freeze-related leg trembling sits in a 3 to 8 Hz band, compared with 0.5 to 3 Hz for normal stepping; this is the basis of the widely used freeze index ([Sweeney et al., 2019](https://www.mdpi.com/1424-8220/19/6/1277); [freeze index reliability, JNER 2023](https://jneuroengrehab.biomedcentral.com/articles/10.1186/s12984-023-01175-y)).
- Cueing near the person's own cadence helps, while cueing well below it can make freezing worse ([Sweeney et al., 2019](https://www.mdpi.com/1424-8220/19/6/1277), summarizing Arias and Cudeiro 2010 and Lee et al. 2012).
- Shoe size about EU 42 (US men's 8.5) for the massing model; the insole is cut to size in practice.
- Wear of 16 h per day with overnight charging.
- One instrumented insole, worn on the side where the wearer reports freezing most (decision D1).
