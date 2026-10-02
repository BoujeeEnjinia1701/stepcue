---
doc_id: STC-PRC-001
title: StepCue design precis
project: StepCue
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 (decisions D1 to D8 recorded, nRF52840 controller, piezo removed, numbers from STC-CAL-001, parametric model and STC-DWG-001)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); 2.5 mm EVA base with motor relief, audio-route cue target, STC-DWG-001 Rev P2
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design for construction (STC-DDR-003, draft); components, figures and key numbers updated from STC-CAL-001 v0.3; STC-DWG-001 Rev P3
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Design for construction accepted; partner, charging, pod, traces and next model revision as decided on 2026-10-02 (STC-DEC-001)"
---

# StepCue design precis

StepCue is a thin insole with five force-sensing resistors and a coin vibration motor, wired by a flat flex tail to a small pod that clips over the heel of the shoe. The pod reads the pressure sensors and its own motion sensor 104 times a second, decides every 0.25 s whether a freeze is starting, and if so pulses the motor at the wearer's own walking rhythm until steps resume. The calculation note STC-CAL-001 puts one unit at $89.94 in parts and 12.5 days per charge (7.4 days conservative). The insole stack is 4.50 mm against a 5.0 mm limit. Whether the detector is fast and reliable enough (R3 to R5) cannot be shown on paper and is the main risk; the calculations show those three requirements pull against one another.

![StepCue concept: instrumented insole in a shoe (grey), with the heel pod clipped over the heel counter](../media/hero.png)

*Figure 1. Hero render from the TRL 3 parametric model. The grey shoe outsole and heel counter are shown for scale only.*

## How it works

1. **Sense.** Five force-sensing resistors (FSRs) laminated into the insole measure load under the heel, the lateral midfoot, the first and fifth metatarsal heads and the hallux. The 6-axis IMU on the controller module in the heel pod measures the motion of the shoe. All six signals are sampled at 104 Hz on the IMU's data-ready tick.
2. **Learn the wearer's rhythm.** A 30 s walk at the start of the day (or a stored value) sets the wearer's baseline cadence. Research systems such as GaitAssist used the same idea to tune cue tempo automatically ([Sweeney et al., Sensors, 2019](https://www.mdpi.com/1424-8220/19/6/1277)).
3. **Detect.** Every 0.25 s the firmware looks back over a 2 s window and computes a small set of features: whether heel strikes and toe-offs still alternate, how the center of pressure moves, the stride time compared with baseline, and the freeze index from the IMU (power in the 3 to 8 Hz freeze band divided by power in the 0.5 to 3 Hz locomotor band). The first detector is a set of thresholds; a small trained classifier replaces it once labeled data are available (decision D6). Plantar pressure alone has predicted freezes about 0.8 s before onset in the literature ([Pardoel et al., Frontiers in Neurology, 2022](https://www.frontiersin.org/articles/10.3389/fneur.2022.831063/pdf)).
4. **Cue.** When the detector fires, the coin motor under the arch pulses for 100 ms on each beat at the baseline cadence. Where the wearer prefers audio, the pod sends the beat timing over BLE to a paired phone, which plays it through its speaker or earbuds (decision D5). Cueing stops after three regular steps or 15 s, whichever comes first.
5. **Log.** Each cue is logged with a time stamp so the wearer or a clinician can later count cue events. The log leaves the pod only when the owner exports it.

![Closed-loop signal flow](../media/flow.png)

*Figure 2. Signal flow. Values marked "est." are estimates from STC-CAL-001.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and the exploded view.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Top cover | 1.2 mm PU foam with textile face | Cut from a thin commercial insole |
| 2 | Pressure sensors | 5 Interlink FSR 402 (18.3 mm round, 0.46 mm thick) | Commercial FSRs (decision D7) |
| 3 | Sensor laminate | Two layers, 0.8 mm in all: copper tape traces on a 125 µm polyimide carrier film (0.3 mm), and a 0.5 mm closed-cell foam spacer with a window round each FSR | No custom rigid PCB (R14); the spacer foam is BOM line 14 (STC-DDR-003) |
| 4 | Flat flex tail and connector | 8-way, 1.0 mm pitch, 9 mm wide; the insole end slit into strips soldered to pads, the pod end in a ZIF connector (BOM line 13) | Runs up the inside of the heel counter under the clip finger and over its top into the pod |
| 5 | Haptic actuator | 10 x 2.7 mm coin ERM (Precision Microdrives 310-103 class) under the medial arch | Low-load site; in a hole through the base, bonded under the spacer, so nothing rigid sits under the heel or forefoot |
| 6 | Insole base | 2.5 mm EVA foam with a motor through-hole | Decision O3 (STC-DDR-002); through-hole by STC-DDR-003 |
| 7 | Heel pod base with clip | 3D-printed PETG tray, 37 mm wide, with a clip curved to the heel counter and four lid screw bosses | One-handed fitting (R12) |
| 8 | Battery | 400 mAh protected LiPo, 502535 class | Outside the shoe |
| 9 | Controller module with IMU | Seeed XIAO nRF52840 Sense class: nRF52840, LSM6DS3TR-C IMU, six analog inputs, charger, USB-C | Decision D2; USB-C faces down through a notch in the pod's bottom wall (STC-DDR-003) |
| 10 | Interface board | Perfboard with the FSR dividers, a P-MOSFET that powers them only while sampling, the motor MOSFET and diode, and a 12 mm pause button | Replaces the TRL 2 multiplexer |
| 11 | Heel pod lid | 3D-printed PETG, four M2 screws | Pause button cap and status LED windows |

![Exploded view with BOM callouts](../media/exploded.png)

*Figure 3. Exploded view. Callout numbers match `bom/bom.csv`.*

![Section through the heel pod](../media/cutaway.png)

*Figure 4. Section through the heel pod and flex tail (insole layers hidden). From the left: lid, the interface board above the controller module, the LiPo cell, and the shoe-side wall. The gap between the pod and the vertical flex tail is where the shoe's heel counter sits; the clip bridges over it and its finger presses the tail against the inside of the counter.*

The general arrangement drawing is [STC-DWG-001 Rev P3](../cad/drawings/STC-DWG-001.pdf); the parametric model is `cad/src/model.py`.

## Key numbers

All values are from STC-CAL-001 and are calculations or estimates, not measurements.

Table 2. Key numbers.

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Sampling | 104 Hz on 6 channels | IMU data rate; Nyquist 52 Hz, 6.5 times the 8 Hz top of the freeze band | R1, R2 met |
| FSR range | Four of five sites exceed 20 N at peak load | 169 mm² active area, assumed peak pressures | R1 met; force above 20 N lost |
| Frequency resolution | 0.50 Hz | 208-sample, 2 s window | Separates the two bands |
| Detection delay | Method floor 1.50 s; 2.50 s with 5 confirming windows | Synthetic signal | R3 at risk |
| Detection accuracy | About 77 to 80 % sensitivity, 83 to 85 % specificity with pressure alone in the literature | Pardoel et al. (2022) | R4 at risk |
| Nuisance cues | 5 or more confirming windows needed at 85 % specificity | 2,400 decisions per 10 min | R5 at risk |
| Cue start after detection | 41 ms haptic; about 0.18 to 0.28 s through a phone or earbuds | Motor lag 40 ms; assumed BLE and audio latency; targets 0.1 s haptic, 0.3 s audio | R6 met |
| Cue | 203 Hz pulses, 100 ms per beat, distinct up to 130 per minute | Motor 12,200 rpm, stop time 115 ms | R7 met |
| Audio level | Earbuds above 60 dB(A); phone in a pocket about 61 dB | The removed piezo would have given 56.5 dB at 1.5 m, not the 60 dB estimated at TRL 2 | R7 met by earbuds |
| Average current while worn | 1.45 mA nominal, 2.44 mA conservative | IMU 0.90 mA plus MCU, FSR dividers, BLE | |
| Battery life | 12.5 days nominal, 7.4 days conservative | 306 mAh usable of 400 mAh | R11 met |
| Insole stack | 4.50 mm (4.3 to 4.7 mm with EVA tolerance) | 2.5 mm EVA, 0.8 mm two-layer laminate round the FSRs, 1.2 mm cover | R9 met, 0.5 mm margin |
| Heel pod | 27.2 g; 42 x 37 x 15 mm (20.3 mm deep with the clip) | Model volumes and part masses | R10 met |
| Clip | 7.5 N clamp; 6.0 N hold against 2.7 N at heel strike | PETG cantilever, 1.0 mm interference | R12 supports; not verifiable |
| Parts cost | $89.94 per unit, $110.06 under the $200 value-engineering target | `bom/bom.csv`, 14 priced lines | R14 met |

## Design choices

Amish decided the following on 2026-09-25, going with the recommendations of the TRL 2 review (STC-DDR-001).

- **One instrumented insole, not a pair (D1).** Worn on the side where the wearer reports freezing most, following the finding that one side predicts about as well as both.
- **nRF52840 module with built-in IMU (D2).** Six analog inputs remove the multiplexer, the built-in IMU removes the breakout, and sleep between samples gives about four times the battery life of the ESP32-C3 estimate.
- **Pressure plus IMU (D3).** The module's IMU lets the firmware use the well-studied freeze index alongside pressure features. The pitch is unchanged.
- **Electronics in a heel pod (D4).** Keeps the lithium cell and rigid parts out from under the foot, lets the insole be removed and dried, and allows charging off the shoe.
- **Haptic cue by default, audio through a phone or earbuds (D5).** The piezo buzzer is removed: at the heel it could not reach 60 dB at the ear.
- **Rule-based detector first (D6)**, a trained classifier only when labeled data exist.
- **Commercial FSRs (D7)** for the first build.
- **Requirement targets adopted (D8)**, with the R7 audio route and the R14 unit restated.

Amish also decided, on 2026-09-25, the two items raised at TRL 3, again going with the recommendations (STC-DDR-002):

- **Separate cue-start target for the audio route (O2).** R6 keeps 0.1 s for the haptic default and sets 0.3 s for phone or earbud audio, since latency shifts only the first beat and not the rhythm.
- **2.5 mm EVA base (O3).** The stack falls from 5.00 mm to 4.50 mm. At the time the 2.7 mm motor sat on a 0.2 mm EVA floor under a relief in the laminate; STC-DDR-003 replaces both with a through-hole, keeping the 4.50 mm stack.

On 2026-10-01, under Amish's 2026-09-30 instruction to make every design physically buildable, the model was made constructable (STC-DDR-003, accepted by Amish on 2026-10-02): a two-layer laminate, routed traces, a motor through-hole, a 9 mm tail with a connector in the pod, a curved clip, a 37 mm pod with a screwed lid and USB-C through its bottom wall. The prototype build plan is STC-BLD-001.

Decided by Amish on 2026-10-02 (STC-DEC-001): the first co-design partner is a Parkinson's patient group, recruited through a local support group affiliated with the Parkinson's Foundation (the first candidate to approach), with a physiotherapy practice brought in for the first supervised user session (O1). Insole and pod come out of the shoe together for charging in the supervised prototype sessions; an outside connector is to be decided before any take-home use. The pod is 37 mm wide with four M2 lid screws. The traces are built as modelled and checked for continuity before each wear session. The smooth insole outline and the rounded pod with a parting-line groove are adopted at the next model revision.

## Safety

> **Safety:** StepCue is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be relied on to prevent falls or to guide treatment. A missed cue or a false cue could startle the wearer or leave them without help during a freeze, so any use with people who freeze must be supervised, with ethics review, and belongs to TRL 4 or later, which is on hold.

> **Safety:** The heel pod contains a lithium polymer cell. Use a protected cell, keep it outside the shoe, never charge while worn or while the pod is wet, and stop using any pod that is swollen, damaged or warm.

- Pressure points under the foot can cause skin breakdown, especially in people with reduced sensation or diabetes. Nothing rigid may sit under the heel or metatarsal heads (the FSRs are 0.46 mm), and the skin should be checked after early wear.
- The clip finger sits inside the heel counter against the wearer's heel above the insole. Its edges must be rounded and its fit checked on skin.
- The flex tail and pod must not catch on clothing or furniture, and the pod must not affect how the shoe grips or how the wearer turns.
- A sudden vibration can itself startle. Cue intensity should start low and be set with the wearer.
- The event log is health data. Keep it on the device and the owner's computer, and share only with consent. The optional phone link carries beat timing only.

## Open questions

- Labeled data: is there an openly licensed plantar-pressure freeze data set, or must the first detector be developed on IMU-only data (for example the public Daphnet set used by Bächlin et al.)? This decides whether R3 to R5 can be addressed.
- Does a heel-mounted IMU give a usable freeze index, given heel-strike impacts that shank-mounted sensors do not see?
- Can five FSRs, four of them saturating at peak load, capture the center-of-pressure features the literature uses with dense pressure insoles?
- Is a coin motor under the arch clearly felt through a sock during walking?
- How the flex tail survives thousands of heel flexes where it passes over the heel counter.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
