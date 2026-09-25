---
doc_id: STC-REQ-001
title: StepCue requirements
project: StepCue
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# StepCue requirements

These are first-pass requirements for the concept. Targets are proposals for review, awaiting Amish. The status column gives the TRL 2 position from the estimates in the design precis (STC-PRC-001); nothing here has been measured.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Sense plantar loading at the main contact regions | 5 or more pressure sites (heel, lateral midfoot, first and fifth metatarsal heads, hallux), each sampled at 100 Hz or more | Design review; firmware configuration | Met by design |
| R2 | Sense shank or foot motion for the freeze band | 6-axis IMU at 100 Hz or more, covering the 3 to 8 Hz freeze band and the 0.5 to 3 Hz locomotor band | Datasheet; sampling calculation | Met by design (heel pod IMU) |
| R3 | Detect freezes quickly | Median delay from freeze onset to detection 2 s or less | Offline replay of labeled data | **Not demonstrated.** Needs labeled data |
| R4 | Detect freezes reliably | Episode sensitivity 80 % or more; window specificity 85 % or more | Offline replay of labeled data | **At risk.** Published pressure-only results are about 77 to 80 % sensitivity and 83 to 85 % specificity |
| R5 | Avoid nuisance cues | 1 false cue or fewer per 10 min of ordinary walking | Offline replay; later supervised trial | **Not demonstrated** |
| R6 | Start the cue promptly | Cue starts 0.1 s or less after a detection | Firmware timing calculation | Met by estimate (about 20 ms) |
| R7 | Deliver a rhythmic cue the wearer can feel or hear | Haptic pulses at the wearer's baseline cadence (adjustable 60 to 130 per minute); audio beeps of 60 dB(A) or more at the ear | Calculation from datasheets; later bench measurement | Haptic met by estimate; **audio at risk** (about 60 dB(A) at 1.5 m, estimate) |
| R8 | Stop cueing when walking resumes | Cue stops within 3 regular steps, or after 15 s at most | Firmware logic review | Met by design |
| R9 | Keep the shoe comfortable | Insole stack 5.0 mm or less; no rigid part thicker than 1 mm under the heel or metatarsal heads | Massing model; later pressure mapping | Met, no margin (5.0 mm) |
| R10 | Keep the heel pod light and small | Pod 35 g or less; no larger than 45 x 40 x 20 mm | Massing model; later weighing | Met by estimate (about 28 g; 44 x 38 x 19 mm) |
| R11 | Run a full day and more | 2 days or more between charges at 16 h per day of wear | Power budget calculation | Met by estimate (about 3 days) |
| R12 | Usable with reduced dexterity | Pod clips on and off one-handed; USB-C charging with the pod off the shoe; one large button to pause cues | Design review; later user session | Met by design, not user-tested |
| R13 | Keep data with the wearer | Detection and cueing on the device; optional event log exported over USB or BLE by the owner only; no cloud | Design review | Met by design |
| R14 | Low cost and buildable | Parts cost $200 or less per unit, with one instrumented insole; no custom rigid PCB for the first build | Priced BOM | Met by estimate (about $106); a pair (about $212) would not meet it |
| R15 | Safe to wear | Protected lithium cell outside the shoe; no exposed conductors; skin-contact materials suitable for footwear | Design review | Met by design |

## Requirements not met or not yet demonstrated

- **R3, R4 and R5** (detection delay, reliability and nuisance cues) cannot be shown on paper. They need a labeled plantar-pressure and IMU data set, and published results suggest R4 is at the edge of what pressure data alone achieves.
- **R7 audio** is at risk: a small piezo at the heel gives about 60 dB(A) at the ear by estimate, which may be masked outdoors. A phone or earbud route would meet it.
- **R9** has no thickness margin.
- **R14** is met only for one insole. A pair would exceed the $200 budget.

## Assumptions

- Freeze-related leg trembling sits in a 3 to 8 Hz band, compared with 0.5 to 3 Hz for normal stepping; this is the basis of the widely used freeze index ([Sweeney et al., 2019](https://www.mdpi.com/1424-8220/19/6/1277); [freeze index reliability, JNER 2023](https://jneuroengrehab.biomedcentral.com/articles/10.1186/s12984-023-01175-y)).
- Cueing near the person's own cadence helps, while cueing well below it can make freezing worse ([Sweeney et al., 2019](https://www.mdpi.com/1424-8220/19/6/1277), summarizing Arias and Cudeiro 2010 and Lee et al. 2012).
- Shoe size about EU 42 (US men's 8.5) for the massing model; the insole is cut to size in practice.
- Wear of 16 h per day with overnight charging.
