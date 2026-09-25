---
doc_id: STC-PRC-001
title: StepCue design precis
project: StepCue
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# StepCue design precis

StepCue is a thin insole with five force-sensing resistors and a coin vibration motor, wired by a flat flex tail to a small pod that clips over the heel of the shoe. The pod reads the pressure sensors and its own motion sensor 100 times a second, decides every 0.25 s whether a freeze is starting, and if so pulses the motor (or a buzzer) at the wearer's own walking rhythm until steps resume. First-order estimates suggest one instrumented insole costs about $106 in parts and runs about 3 days per charge. Whether the detector is fast and reliable enough (R3 to R5) cannot be shown on paper and is the main risk.

![StepCue concept: instrumented insole in a shoe (grey), with the heel pod clipped over the heel counter](../media/hero.png)

*Figure 1. Hero render. The grey shoe outsole and heel counter are shown for scale only.*

## How it works

1. **Sense.** Five force-sensing resistors (FSRs) laminated into the insole measure load under the heel, the lateral midfoot, the first and fifth metatarsal heads and the hallux. A 6-axis IMU in the heel pod measures the motion of the foot and shoe. All six signals are sampled at 100 Hz.
2. **Learn the wearer's rhythm.** A 30 s walk at the start of the day (or a stored value) sets the wearer's baseline cadence. Research systems such as GaitAssist used the same idea to tune cue tempo automatically ([Sweeney et al., Sensors, 2019](https://www.mdpi.com/1424-8220/19/6/1277)).
3. **Detect.** Every 0.25 s the firmware looks back over a 2 s window and computes a small set of features: whether heel strikes and toe-offs still alternate, how the center of pressure moves, the stride time compared with baseline, and the freeze index from the IMU (power in the 3 to 8 Hz freeze band divided by power in the 0.5 to 3 Hz locomotor band). A first detector is a set of thresholds; a small trained classifier (for example logistic regression) can replace it once labeled data are available. Plantar pressure alone has predicted freezes about 0.8 s before onset in the literature ([Pardoel et al., Frontiers in Neurology, 2022](https://www.frontiersin.org/articles/10.3389/fneur.2022.831063/pdf)).
4. **Cue.** When the detector fires, the coin motor under the arch pulses for 100 ms on each beat at the baseline cadence. An optional piezo buzzer in the pod beeps on the same beat. Cueing stops after three regular steps or 15 s, whichever comes first.
5. **Log.** Each cue is logged with a time stamp so the wearer or a clinician can later count cue events. The log leaves the pod only when the owner exports it.

![Closed-loop signal flow](../media/flow.png)

*Figure 2. Signal flow. Values marked "est." are estimates.*

## Main components

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Top cover | 1.2 mm PU foam with textile face | Cut from a thin commercial insole |
| 2 | Pressure sensors | 5 force-sensing resistors, 18 mm round (Interlink FSR 402 class) | DIY piezoresistive film (Velostat class) is a cheaper option |
| 3 | Sensor laminate | Copper tape or printed traces on 125 µm PET or polyimide film | No custom rigid PCB (R14) |
| 4 | Flat flex tail and connector | 8-way, 1.0 mm pitch flat flex cable; connector at the heel edge | Lets the pod come off for charging and the insole come out for drying |
| 5 | Haptic actuator | 10 mm coin ERM vibration motor under the medial arch | Low-load site; pocketed into the foam so nothing rigid sits under the heel or forefoot |
| 6 | Insole base | 3 mm EVA foam with motor pocket | |
| 7 | Heel pod base with clip | 3D-printed PETG tray with a clip over the heel counter | One-handed fitting (R12) |
| 8 | Battery | 400 mAh protected LiPo, 502535 class | Outside the shoe |
| 9 | Controller | ESP32-C3 module with USB-C charging (Seeed XIAO ESP32C3 class) plus an 8:1 analog multiplexer | The XIAO ESP32C3 exposes too few ADC pins for five FSRs, hence the multiplexer. See decision 2 |
| 10 | Motion sensor | 6-axis IMU breakout (LSM6DSO class) | |
| 11 | Audio cue | 12 mm piezo buzzer | Weak outdoors; see R7 |
| 12 | Heel pod lid | 3D-printed PETG | Pause button and status LED |

![Exploded view with BOM callouts](../media/exploded.png)

*Figure 3. Exploded view. Callout numbers match `bom/bom.csv`.*

![Section through the heel pod](../media/cutaway.png)

*Figure 4. Section through the heel pod and flex tail (insole layers hidden). From the left: lid, buzzer, controller above the IMU, LiPo cell, and the shoe-side wall. The gap between the pod and the vertical flex tail is where the shoe's heel counter sits; the clip bridges over it.*

## First-order numbers

All values are estimates for concept review and will be checked by calculation at TRL 3.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Sampling | 100 Hz on 6 channels | Nyquist 50 Hz, well above the 8 Hz top of the freeze band | R1, R2 met |
| Frequency resolution | 0.5 Hz | 2 s window | Enough to separate the 0.5 to 3 Hz and 3 to 8 Hz bands |
| Detection delay | Unknown; target 2 s or less | Research systems report about 0.5 to 3.2 s (Sweeney et al., 2019) | R3 not demonstrated |
| Detection accuracy | Unknown; about 77 to 80 % sensitivity, 83 to 85 % specificity with pressure alone in the literature | Pardoel et al. (2022) | R4 at risk |
| Cue start after detection | About 20 ms | GPIO switch plus motor spin-up | R6 met |
| Cue tempo | Baseline cadence, typically about 1.6 to 1.9 Hz (95 to 115 steps per minute) | Adjustable 60 to 130 per minute | R7 haptic met |
| Audio level at the ear | About 60 dB(A) | Piezo about 80 dB at 10 cm, minus about 24 dB spreading to 1.5 m | R7 audio at risk |
| Average current while worn | About 6 mA | ESP32-C3 in light sleep between samples, about 5 mA average; IMU about 0.6 mA; FSR dividers switched on only to sample, about 0.2 mA | |
| Cue energy | About 1 mAh per day | ERM about 70 mA at 17 % duty; about 300 s of cueing per day assumed | |
| Daily charge used | About 100 mAh | 16 h at about 6 mA, plus cues and overnight sleep | |
| Battery life | About 3 days (range 2 to 4) | 400 mAh cell, 80 % usable | R11 met |
| Insole stack | 5.0 mm | 3.0 mm EVA, 0.8 mm laminate with sensors, 1.2 mm cover | R9 met, no margin |
| Heel pod | About 28 g; 44 x 38 x 19 mm | Cell about 8 g, electronics about 5 g, printed shell about 15 g | R10 met |
| Parts cost | About $106 per instrumented insole | Indicative prices, see `bom/bom.csv` | R14 met for one insole |

## Key design choices

All choices below are proposed, awaiting Amish.

- **One instrumented insole, not a pair.** Keeps the build within the $200 budget and follows the finding that one side predicts about as well as both. A second insole can be added later.
- **Electronics in a heel pod, not in the insole.** Keeps the lithium cell and rigid parts out from under the foot, lets the insole be removed and dried, and makes charging possible without taking the shoe off the foot.
- **Pressure plus IMU.** The pitch describes a pressure-sensing insole. Adding a low-cost IMU in the pod lets the firmware use the well-studied freeze index alongside pressure features, at about $10 and 0.6 mA. This does not change the pitch but is recorded here as a proposal.
- **Haptic cue at the foot as the default, audio optional.** A vibration under the arch is private and works outdoors; audio is available where the wearer prefers it.
- **Cue only on detection, with a manual pause.** Closed-loop cueing avoids the fatigue of constant cueing; a pause button lets the wearer stop cues at any time.
- **Rule-based detector first.** Thresholds are inspectable and need little data; a trained classifier comes only when labeled data exist.

## Safety

> **Safety:** StepCue is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be relied on to prevent falls or to guide treatment. A missed cue or a false cue could startle the wearer or leave them without help during a freeze, so any use with people who freeze must be supervised, with ethics review, and belongs to TRL 4 or later.

> **Safety:** The heel pod contains a lithium polymer cell. Use a protected cell, keep it outside the shoe, never charge while worn or while the pod is wet, and stop using any pod that is swollen, damaged or warm.

- Pressure points under the foot can cause skin breakdown, especially in people with reduced sensation or diabetes. Nothing rigid may sit under the heel or metatarsal heads, and the skin should be checked after early wear.
- The flex tail and pod must not catch on clothing or furniture, and the pod must not affect how the shoe grips or how the wearer turns.
- A sudden vibration can itself startle. Cue intensity should start low and be set with the wearer.
- The event log is health data. Keep it on the device and the owner's computer, and share only with consent.

## Open questions for TRL 3

- Labeled data: is there an openly licensed plantar-pressure freeze data set, or must the first detector be developed on IMU-only data (for example the public Daphnet set used by Bächlin et al.)?
- Can five FSRs capture the center-of-pressure features the literature uses with dense pressure insoles?
- Is a coin motor under the arch clearly felt through a sock during walking, and does it stay out of the high-pressure zone for all foot shapes?
- Confirm the ESP32-C3 light-sleep current at 100 Hz sampling, or switch controller (decision 2 in `docs/REVIEW.md`).
- How the flex tail survives thousands of heel flexes where it passes over the heel counter.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
