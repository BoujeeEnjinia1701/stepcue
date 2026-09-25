---
doc_id: STC-CAL-001
title: StepCue sizing calculations
project: StepCue
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First-principles sizing for TRL 3 against STC-REQ-001 v0.3
---

# StepCue sizing calculations

On paper, the design meets nine of the fifteen requirements in STC-REQ-001, including battery life (12.5 days nominal against 2 days), pod mass (25.2 g against 35 g) and cost ($83.44 against $200). One requirement is not met: the optional phone or earbud audio route starts a cue in about 0.18 to 0.28 s against the 0.1 s target (R6); the haptic default meets it at 41 ms. Four are at risk: detection delay, reliability and nuisance cues (R3 to R5) pull against one another and cannot be shown without labeled data, and the insole stack (R9) has no thickness margin. One (R12, one-handed use) cannot be verified at TRL 3.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root). Geometry and volumes come from `cad/src/model.py`; cost comes from `bom/bom.csv`. Values marked "assumed" have no source and are to be confirmed.

> **Safety:** StepCue is a research and educational prototype, not a medical device, and must not be relied on to prevent falls. The heel pod holds a lithium polymer cell: use a protected cell, keep it outside the shoe, and never charge while worn or wet. Nothing in this note shows that the detector is safe to use with a person who freezes; that needs supervised work with ethics review, which is TRL 4 or later and on hold.

## 1. Results against requirements

Table 1 lists every requirement, not met and at-risk items first. Status is one of met, not met, at risk, or not verifiable at TRL 3.

Table 1. Requirement status at TRL 3.

| ID | Target | Value from this note | Status |
| --- | --- | --- | --- |
| R6 | Cue starts 0.1 s or less after a detection | Haptic 41 ms to first vibration, 88 ms to 50 % amplitude; phone or earbud audio 180 to 280 ms (estimate) | Not met for the audio route; met for the haptic default |
| R3 | Median delay from onset to detection 2 s or less | Method floor 1.50 s with one window; 2.00 s with 3 confirming windows; 2.50 s with 5 (synthetic) | At risk |
| R4 | Episode sensitivity 80 % or more; window specificity 85 % or more | Published pressure-only results 77 to 80 % and 83 to 85 % | At risk |
| R5 | 1 false cue or fewer per 10 min of walking | At 85 % window specificity, 5 confirming windows are needed even if windows were independent | At risk |
| R9 | Stack 5.0 mm or less; no rigid part over 1 mm under heel or metatarsal heads | 5.00 mm, zero margin; FSR 0.46 mm | At risk |
| R12 | One-handed clip; USB-C with the pod off; one large pause button | Clip clamp 7.5 N, hold 6.0 N against 2.5 N at heel strike, removal about 6 N; 10 mm button | Not verifiable at TRL 3 |
| R1 | 5 or more pressure sites at 100 Hz or more | 5 FSRs at 104 Hz; four of five sites exceed the 20 N sensor range at peak load | Met |
| R2 | 6-axis IMU at 100 Hz or more covering 0.5 to 8 Hz | LSM6DS3TR-C at 104 Hz; 0.50 Hz bins; Nyquist 52 Hz | Met |
| R7 | Haptic at cadence, 60 to 130 per minute; audio 60 dB(A) or more at the ear | 203 Hz ERM pulses with a 247 ms quiet gap at 130 per minute; audio by earbuds; phone in a pocket about 61 dB | Met |
| R8 | Stop within 3 regular steps or 15 s | 3 steps take 1.7 s; 15 s cap | Met (design review) |
| R10 | Pod 35 g or less; within 45 x 40 x 20 mm | 25.2 g; body 42 x 34 x 15 mm (20.3 mm deep including the clip over the counter) | Met |
| R11 | 2 days or more at 16 h per day | 12.5 days nominal, 7.4 days conservative | Met |
| R13 | Detection and cueing on the device; owner-only export; no cloud | No cloud path; phone used only for optional audio | Met (design review) |
| R14 | $200 or less per unit (one instrumented insole and one heel pod); no custom rigid PCB | $83.44 over 12 priced lines; perfboard only | Met |
| R15 | Protected cell outside the shoe; no exposed conductors; footwear-safe materials | Protected cell in the pod outside the counter; sensors laminated under the cover | Met (design review) |

Counts: 9 met, 1 not met, 4 at risk, 1 not verifiable at TRL 3.

## 2. Pressure sensing (R1)

Assumptions: Interlink FSR 402 sensors (datasheet: 14.68 mm active diameter, 0.46 mm thick, sensitivity range about 0.2 to 20 N, part-to-part variation 6 %, durability 10 million actuations at 1 kg); peak in-shoe plantar pressures during walking of 250 kPa at the heel, 300 kPa at the first metatarsal head, 250 kPa at the hallux, 150 kPa at the fifth metatarsal head and 80 kPa at the lateral midfoot (assumed); a resistance law R = 10 kΩ x F^-0.9 (F in N) read from the datasheet curve (assumed).

- The active area is 169.3 mm². At peak pressure the heel sensor carries 42.3 N, the first metatarsal head 50.8 N, the hallux 42.3 N and the fifth metatarsal head 25.4 N. All four exceed the 20 N range, so they saturate during stance; only the lateral midfoot (13.5 N) stays in range. Saturation does not defeat the concept, because the detector uses timing (heel strike and toe-off alternation, stance time) and the center of pressure between sites rather than absolute force, but force magnitude above about 20 N is lost.
- Each sensor feeds a divider to a 1 kΩ resistor. The resistor that best spreads 2 to 50 N is the geometric mean of the end resistances, 1,259 Ω, so 1 kΩ is close. The output runs from 0.17 V at 0.5 N to 2.42 V at 40 N (208 to 3,008 counts of 4,095), leaving headroom below the 3.3 V rail.
- A P-MOSFET switches the divider rail on for 0.3 ms per 9.6 ms sample (3.1 % duty). At 40 N each divider draws 2.42 mA while on.
- The nRF52840 SAADC scans five channels at 40 µs acquisition in 0.21 ms, 2.2 % of the time. The module has six analog inputs, so no multiplexer is needed (decision D2); one input is spare.

## 3. Motion sensing and the freeze-index window (R2)

Assumptions: the module's LSM6DS3TR-C runs at an output data rate of 104 Hz and the FSR scan is triggered on the same data-ready tick; the detector looks back over 2 s every 0.25 s; the locomotor band is 0.5 to 3 Hz and the freeze band 3 to 8 Hz.

- A window holds 208 samples, giving 0.50 Hz bins and a 52 Hz Nyquist limit, 6.5 times the top of the freeze band. The locomotor band spans 5 bins and the freeze band 11.
- The IMU sits in the heel pod, on the shoe rather than the shank where the freeze index was first defined. Heel-strike impacts add high-frequency power that may raise the index during normal walking; this can only be checked on real foot-mounted data.

## 4. Detection delay, reliability and nuisance cues (R3 to R5)

These requirements cannot be verified without labeled data. The script checks only the arithmetic of the method on a synthetic signal: walking modeled as the first 11 harmonics of a 0.875 Hz stride (amplitude falling as k^-1.5), switching at a known onset to 5.5 Hz trembling with a slow sway, plus noise (all assumed).

- Walking windows gave a freeze index of 0.05 or less and full-freeze windows 19.0 or more; the threshold was set at their geometric mean, 1.00. The synthetic separation is far cleaner than real data and says nothing about R4.
- Because the 2 s window must fill with trembling before the ratio crosses the threshold, the first window over threshold ended 1.50 s after onset. Requiring 3 consecutive windows moves detection to 2.00 s; requiring 5 moves it to 2.50 s.
- R5 sets how much confirmation is needed. A 10 min walk contains 2,400 decisions. At the 85 % window specificity of R4 (a 15 % false-positive rate per window), keeping false cues to one per 10 min needs 5 consecutive positive windows even if windows were independent, which they are not, since successive 2 s windows share 1.75 s of data. The result is the same at 83 %.

The three requirements therefore pull against each other: the confirmation that R5 needs pushes the method floor past the 2 s of R3, and published pressure-only accuracy sits at the edge of R4 (Pardoel et al., 2022, cited in STC-PRB-001). All three are at risk. The ways out, a shorter window, features that respond before trembling fills the window (such as the pre-freeze pressure changes Pardoel et al. used), or a trained classifier (decision D6), need labeled plantar-pressure data.

## 5. Cue start (R6)

Assumptions: firmware reaction under 1 ms from the decision to the MOSFET gate; motor figures from the Precision Microdrives 310-103 datasheet (lag 40 ms, rise to 50 % amplitude 87 ms, stop 115 ms, 58 mA, 12,200 rpm); for the audio route, 30 ms for a BLE connection event, 50 ms for the phone app, and 100 ms (phone speaker) or 200 ms (Bluetooth earbuds) of audio output latency (all assumed).

- Haptic: 1 ms plus the 40 ms lag gives 41 ms to first vibration and 88 ms to half amplitude. Met.
- Audio route: 180 ms through the phone speaker and 280 ms through earbuds. Not met. The latency delays only the first beat; later beats keep the cadence if the pod sends the beat timing rather than a trigger per beat. Item O2 in STC-DDR-001 proposes a separate 0.3 s target for the audio route.

## 6. Cue delivery (R7) and stop (R8)

- The motor spins at 12,200 rpm, a 203 Hz vibration, close to the 200 to 250 Hz band where the skin's vibration receptors are most sensitive. Whether it is felt through a sock and foam cover, by an older adult with raised vibration thresholds, cannot be shown on paper.
- A 100 ms pulse runs down over a further 115 ms. At 60, 105 and 130 beats per minute the quiet gaps are 785, 356 and 247 ms and the drive duty is 10, 18 and 22 %. Even at 130 per minute the beats stay distinct. A 150 ms pulse would still leave a 197 ms gap if a stronger pulse is wanted.
- Audio: a 12 mm piezo at the heel (80 dB at 10 cm, assumed) would give 56.5 dB at the ear 1.5 m away, below 60 dB. The TRL 2 precis said about 60 dB; the spreading loss was understated. Decision D5 removes the piezo. Earbuds exceed 60 dB(A) at the ear with ordinary volume settings; a phone speaker in a trouser pocket (80 dB at 10 cm, 0.9 m from the ear, assumed) gives about 61 dB before pocket muffling, which is marginal. R7 is met by the haptic cue and by earbuds.
- R8: three regular steps at 105 steps per minute take 1.7 s, and a 15 s cap stops any cue. Met by the firmware logic.

## 7. Insole stack (R9)

The stack in `cad/src/model.py` is 3.0 mm EVA plus a 0.8 mm laminate (0.46 mm FSR and 0.34 mm film and adhesive) plus a 1.2 mm cover, 5.00 mm against the 5.0 mm limit. With an assumed EVA sheet tolerance of 0.2 mm the stack is 4.8 to 5.2 mm, so R9 is at risk. A 2.5 mm EVA base gives 4.50 mm, but the 2.7 mm motor then needs a 0.4 mm relief in the laminate or a thinner motor (item O3 in STC-DDR-001). The only rigid parts under the heel and metatarsal heads are the 0.46 mm FSRs, under the 1 mm limit; the motor sits under the medial arch.

## 8. Heel pod size and mass (R10)

The pod body is 42 mm high, 34 mm wide and 15 mm deep, inside the 45 x 40 x 20 mm limit. Including the clip, which straddles the 3.5 mm heel counter, it is 20.3 mm deep. Removing the piezo and the separate IMU made the pod 4 mm thinner and 4 mm narrower than the TRL 2 massing model (44 x 38 x 19 mm).

Table 2. Heel pod mass.

| Part | Mass, g | Basis |
| --- | --- | --- |
| Heel pod base with clip, PETG | 7.06 | Model volume at 1.27 g/cm³ |
| Heel pod lid, PETG | 3.41 | Model volume at 1.27 g/cm³ |
| LiPo cell, 400 mAh | 8.20 | Adafruit 3898 listing, same capacity class |
| Controller module with IMU | 3.00 | Assumed |
| Interface board and pause button | 2.00 | Assumed |
| Wire, tail connector, foam, screws | 1.50 | Assumed |
| **Total** | **25.2** | |

## 9. Clip over the heel counter (R12)

Assumptions: PETG modulus 2,000 MPa; friction coefficient 0.4 between PETG and shoe lining; peak heel-strike acceleration at the counter 10 g (all assumed).

- The finger inside the counter is 26 mm wide, 1.5 mm thick and 18 mm long, with a 1.0 mm interference between its free-state gap (2.8 mm) and the fitted counter plus tail (3.8 mm). As a cantilever it clamps with 7.5 N at 0.69 % bending strain, well within what PETG tolerates for a snap fit.
- Friction on both faces holds 6.0 N against 2.5 N of pod inertia at heel strike, a margin of 2.4. Removal takes about 6 N, within one-handed reach. Whether people with reduced dexterity can fit it cannot be shown on paper.
- The finger presses the flex tail against the inside of the counter, which also keeps the tail from moving. The finger sits against the wearer's heel above the insole, so its edges need rounding and its fit needs checking on skin at a later stage.

## 10. Power budget (R11)

Assumptions (Table 3): 16 h per day worn and 8 h off the shoe with the IMU in wake-on-motion; a 400 mAh protected cell with 85 % usable above a 3.5 V cutoff and a further 90 % for ageing and cold, giving 306 mAh usable; an nRF52840 run current of 6.3 mA at 64 MHz (assumed).

The MCU duty is estimated per second: reading 104 six-axis samples (12 bytes each) over I²C at 400 kHz takes 2.8 % if the CPU waits on the bus; waking for the SAADC scan takes 3.1 %; the FFT and features every 0.25 s take 0.4 %. The total, 6.3 %, gives 0.404 mA including standby.

Table 3. Current while worn, mA.

| Load | Nominal | Conservative | Basis |
| --- | --- | --- | --- |
| IMU, accelerometer and gyroscope | 0.90 | 0.90 | ST figure for combined high-performance mode |
| MCU | 0.404 | 1.00 | Duty estimate above; conservative allows untuned firmware |
| FSR dividers | 0.114 | 0.378 | Half of sensors loaded at 10 N; all loaded at 40 N; 3.1 % duty |
| BLE advertising or phone link | 0.03 | 0.15 | Assumed |
| Status LED | 0.002 | 0.01 | Assumed |
| Cell protection circuit | 0.003 | 0.005 | Assumed |
| **Total worn** | **1.45** | **2.44** | |

The motor adds 0.85 mAh per day for 300 s of cueing (nominal) and 1.35 mAh for 480 s (conservative, adding twelve 15 s false cues). Daily use is 24.5 mAh nominal and 41.1 mAh conservative, so one charge lasts 12.5 days nominal and 7.4 days conservative. R11 is met with a wide margin. The TRL 2 estimate for the ESP32-C3 (6 mA worn) gives 98 mAh per day and 3.1 days, which is why decision D2 matters. The module's BQ25101 charger charges the cell in about 9.6 h at 50 mA (0.125 C) or 4.8 h at 100 mA (0.25 C); either suits overnight charging, and both are well under the cell's 1 C limit.

## 11. Cost (R14)

`bom/bom.csv` has 12 priced lines totaling $83.44 for one unit, well under the $200 budget. A second instrumented insole with its own pod would add about the same again, so even a pair ($166.88) would fit, although decision D1 keeps the first build to one insole. The FSR price ($2.99 each at the Interlink store) and the Adafruit 3898 cell price were checked on 2026-09-25; the other prices are indicative. The TRL 2 total of about $106 fell mainly because the FSR price was lower than assumed and the IMU breakout and multiplexer were removed.

## 12. Sources

- Interlink Electronics, [FSR 400 Series data sheet](https://media.digikey.com/pdf/Data%20Sheets/Interlink%20Electronics.PDF/FSR400ForceSensingRes.pdf): FSR 402 active diameter 14.68 mm, overall 18.3 mm, thickness 0.46 mm, range about 0.2 to 20 N, durability, part-to-part variation. [FSR 402 store listing](https://buyinterlinkelectronics.com/products/fsr-model-402): $2.99.
- Precision Microdrives, [310-103 10 mm vibration motor datasheet](https://precisionmicrodrives.com/cdn/catalog_product/89437681-576e-46e1-97cf-5ae185adeb1c/310-103-datasheet.pdf): 3 V, 58 mA, 12,200 rpm, lag 40 ms, rise 87 ms, stop 115 ms, 10 x 2.7 mm, 1 g.
- Seeed Studio, [XIAO nRF52840 Series wiki](https://wiki.seeedstudio.com/XIAO_BLE/): six analog inputs, eleven GPIO, LSM6DS3TR-C IMU, 21 x 17.8 mm, 50 or 100 mA charge current, standby under 5 µA.
- STMicroelectronics, [LSM6DS3TR-C datasheet](https://www.st.com/resource/en/datasheet/lsm6ds3tr-c.pdf): 0.90 mA combined high-performance current.
- Adafruit, [Lithium Ion Polymer Battery 3.7 V 400 mAh, product 3898](https://www.adafruit.com/product/3898): 8.2 g, protection circuit, $6.95.
- Pardoel et al., Frontiers in Neurology, 2022, and Sweeney et al., Sensors, 2019, as cited in STC-PRB-001.
