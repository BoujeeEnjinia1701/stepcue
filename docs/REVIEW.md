# Review note: StepCue

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (STC-PRB-001 v0.2): problem with sourced prevalence, cueing evidence, prior detection research and commercial prices; users and context; constraints; out of scope; open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (STC-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, planned verification and a TRL 2 status column; a list of requirements not met; assumptions.
- `docs/02-concept.md` (STC-PRC-001 v0.2): how it works, 12 numbered components, first-order numbers, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of a five-layer insole (cover, FSRs, laminate, motor, EVA base), flat flex tail and a clip-on heel pod (base, cell, controller, IMU, buzzer, lid), with a grey shoe outsole and heel counter as the scale context (small-object rule, as in TremorTrace).
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with BOM callouts, `cutaway.png` (heel pod section), `flow.png` (closed-loop signal flow, estimates marked), `model.glb` and `viewer.html`. Temporary `_views` folders removed.
- `bom/bom.csv`: 14 lines with indicative prices; lines 1 to 12 match the exploded-view callouts, lines 13 and 14 are not modeled.
- `README.md`: hero image and links line added before "Problem"; concept paragraph, key components and safety note updated.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem are still accurate.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Sensing | 5 FSRs plus 6-axis IMU, 100 Hz | R1, R2 met by design |
| Cue start after detection | about 20 ms | R6 met |
| Audio at the ear | about 60 dB(A) at 1.5 m | R7 audio at risk |
| Insole stack | 5.0 mm | R9 met, no margin |
| Heel pod | about 28 g, 44 x 38 x 19 mm | R10 met |
| Average current | about 6 mA; about 100 mAh per day | |
| Battery life | about 3 days on 400 mAh (range 2 to 4) | R11 met |
| Parts cost | about $106 for one instrumented insole | R14 met; a pair (about $212) would not be |

Requirements not met or not demonstrated:

- **R3 (detection delay 2 s or less), R4 (80 % sensitivity, 85 % specificity) and R5 (1 false cue or fewer per 10 min) are not demonstrated** and cannot be on paper. R4 is at risk: published pressure-only results are about 77 to 80 % sensitivity and 83 to 85 % specificity (Pardoel et al., 2022).
- **R7 audio at risk:** a heel-mounted piezo gives about 60 dB(A) at the ear by estimate.
- **R9 has no margin** (5.0 mm against 5.0 mm).
- **R14 would not be met by a pair** of insoles; `budget_usd` ($200) is not exceeded by the proposed single-insole build, so no budget change is proposed.

### Proposed, awaiting Amish

1. **One instrumented insole or a pair.** Options: (a) one insole on the side the wearer reports freezing most, about $106; (b) a pair, about $212, over budget. Recommendation: (a), since one-sided pressure data predicted freezes about as well as two-sided data in the literature.
2. **Controller.** Options: (a) ESP32-C3 (XIAO ESP32C3 class) as scaffolded, plus a separate IMU and an analog multiplexer, because that module exposes too few ADC pins for five FSRs; (b) nRF52840 with built-in IMU (XIAO nRF52840 Sense class, about $16), which has six analog inputs, lower sleep current and matches TremorTrace, removing lines 10 and 13 in part. Recommendation: (b) for battery life and shared firmware; the concept and BOM are drawn with (a) so the pitch's key components are unchanged until you decide.
3. **Add a 6-axis IMU to a "pressure-sensing insole".** Options: pressure only, or pressure plus IMU. Recommendation: pressure plus IMU (about $10 and 0.6 mA) so the firmware can use the freeze index; it does not change the pitch.
4. **Electronics in a clip-on heel pod** rather than embedded in the insole. Recommendation: heel pod (cell outside the shoe, removable for charging).
5. **Default cue.** Options: haptic under the arch, piezo audio in the pod, or audio on a phone or earbuds over BLE. Recommendation: haptic default, with phone or earbud audio as the audio route rather than the piezo, to meet R7.
6. **Detector approach.** Rule-based thresholds first, trained classifier later once labeled data exist.
7. **Sensor type.** Commercial FSRs (about $37.50 for five) or DIY piezoresistive film (a few dollars, less repeatable). Recommendation: commercial FSRs for the first build.
8. **First co-design partner:** a movement disorders clinic, a physiotherapy practice or a Parkinson's patient group.
9. **Requirement targets R1 to R15** as written in STC-REQ-001 v0.2.

### Safety concerns

- Not a medical device; must not be relied on to prevent falls. A missed or false cue during a freeze is a fall risk, so any use with people who freeze needs supervision and ethics review, which is TRL 4 or later.
- Lithium cell in the heel pod: protected cell, outside the shoe, no charging while worn or wet.
- Pressure injury under the foot, especially with reduced sensation or diabetes: nothing rigid under the heel or metatarsal heads; check skin in early wear.
- Startle from sudden vibration; snag risk from the pod and flex tail.
- The cue log is health data: local by default, shared only with consent.

### Problems and notes

- Several research pages (PubMed, PMC) blocked automated fetching, so some figures come from the open-access versions on journal, DOAJ and Parkinson's UK pages. Prevalence figures are from the abstract of the 2020 Chinese Neurosurgical Journal meta-analysis; the author list was not checked.
- In the exploded view the smallest parts (motor 5, IMU 10, buzzer 11) sit mostly behind their callout markers; the legend and BOM identify them. A kit option to offset callouts would fix this.
- The cutaway hides the insole layers (they are about 5 mm thick over 272 mm and unreadable at that scale) so the heel pod section is legible.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 3. If you approve, run `/advance-trl3` to check the power budget, sampling, cue timing, audio level and insole stack by calculation, identify a labeled data set for the detector, and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Authority: on 2026-09-25 Amish wrote "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session advanced StepCue from TRL 2 to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (STC-DDR-001 v0.1): records decisions D1 to D8 and the items still open.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` moved to v0.3: decisions recorded; nRF52840 module with built-in IMU replaces the ESP32-C3, IMU breakout and multiplexer; piezo removed in favor of phone or earbud audio; R7 audio route and R14 unit restated; TRL 3 status column; numbers replaced by STC-CAL-001 values.
- `docs/04-calcs/01-sizing.md` (STC-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: FSR range and divider, sampling and window, synthetic freeze-index timing, false-cue arithmetic, cue timing, audio level, insole stack, pod mass, clip retention, power budget and cost, with a results table for R1 to R15. The script prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model (insole stack, FSR sites, motor pocket, flex tail route, heel pod with clip, USB-C and tail openings, button and LED windows). Exports `cad/step/stepcue-assembly.step`, `stepcue-heel-pod.step` and part files, and `cad/stl/` for the base, lid and insole layers.
- `cad/src/sheets.py` builds `cad/drawings/STC-DWG-001` (general arrangement, Rev P1, svg, pdf and png), marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". STC-DWG-001 was free because the concept blueprint uses STC-DWG-010.
- `bom/bom.csv`: 12 lines, all priced, total $83.44 against the $200 budget; `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds the media from `model.py`; all media refreshed and checked (hero, blueprint, exploded with callouts 1 to 11 matching the BOM, cutaway, flow, 3D viewer). Temporary `_views` folders removed.
- `project.yaml`: trl 3, trl_target 3, evidence list extended. `README.md`: TRL badge, concept paragraph and key components updated. Pitch, problem and budget unchanged.

### Requirement status (STC-CAL-001, Table 1)

9 met, 1 not met, 4 at risk, 1 not verifiable at TRL 3.

- **Not met: R6 for the audio route.** A phone or earbud cue starts about 0.18 to 0.28 s after detection (estimate) against 0.1 s. The haptic default meets it at 41 ms.
- **At risk: R3, R4, R5.** The confirmation that R5 needs (5 consecutive windows at 85 % specificity) pushes the synthetic method floor from 1.50 s to 2.50 s, past the 2 s of R3; published pressure-only accuracy (77 to 80 %, 83 to 85 %) sits at the edge of R4. None can be verified without labeled data.
- **At risk: R9.** The insole stack is exactly 5.00 mm.
- **Not verifiable at TRL 3: R12.** One-handed use; the clip calculation supports it (7.5 N clamp, 6 N removal).
- **Met:** R1 (five FSRs at 104 Hz, though four of five sites saturate above 20 N), R2, R7, R8, R10 (25.2 g, 42 x 34 x 15 mm body), R11 (12.5 days nominal, 7.4 conservative), R13, R14 ($83.44), R15.

Corrections to TRL 2 figures: the heel piezo would give 56.5 dB at the ear, not about 60 dB (moot, since D5 removes it); battery life rises from about 3 days to 12.5 days with the nRF52840; the parts cost falls from about $106 to $83.44; the pod shrinks from 44 x 38 x 19 mm to 42 x 34 x 15 mm.

### Decisions recorded (STC-DDR-001)

Decided by Amish, 2026-09-25: go with recommendation, for D1 one instrumented insole; D2 XIAO nRF52840 Sense class controller; D3 pressure plus IMU; D4 clip-on heel pod; D5 haptic default with phone or earbud audio, no piezo; D6 rule-based detector first; D7 commercial FSRs; D8 requirement targets as written, with R7 and R14 restated. Budget kept at $200, defined as one instrumented insole and one heel pod (R14). Pitch and problem unchanged.

### Still awaiting Amish

1. **O1. First co-design partner** (movement disorders clinic, physiotherapy practice or Parkinson's patient group). No recommendation; portfolio guidance is to pick partners per area later.
2. **O2. R6 target for the audio route.** Options: keep 0.1 s and accept that audio misses it, or set 0.3 s for the audio route only. Recommendation: 0.3 s for audio, 0.1 s for haptic.
3. **O3. R9 margin.** Options: keep the 3.0 mm EVA base (zero margin) or use 2.5 mm (4.5 mm stack) with a 0.4 mm motor relief in the laminate. Recommendation: 2.5 mm.

### Safety concerns

- Not a medical device; must not be relied on to prevent falls. The calculations show that fast, reliable and quiet detection conflict, so false or late cues are likely in early firmware. Any use with people who freeze needs supervision and ethics review, which is TRL 4 or later and on hold.
- Lithium cell in the heel pod: protected cell, outside the shoe, no charging while worn or wet.
- The clip finger rests against the wearer's heel inside the counter; it needs rounded edges and a skin check.
- Pressure injury under the foot, especially with reduced sensation or diabetes; nothing rigid over 0.46 mm under the heel or metatarsal heads.
- Startle from sudden vibration; snag risk from the pod and flex tail.
- The cue log is health data: local by default, shared only with consent.

### Citations and notes

- The prevalence citation flagged at TRL 2 was checked on 2026-09-25: Ge et al., "The prevalence of freezing of gait in Parkinson's disease and in patients with different disease durations and severities," Chinese Neurosurgical Journal, 2020; 39.9 % overall, 22.4 % under 5 years, 70.8 % at 10 years or more. STC-PRB-001 now names the authors.
- New sources used at TRL 3 (FSR 402 data sheet and store price, Precision Microdrives 310-103 datasheet, Seeed XIAO nRF52840 wiki, Adafruit 3898 listing) are listed in STC-CAL-001, section 12. Plantar pressures, FSR resistance law, BLE and audio latencies, heel-strike acceleration and PETG properties are marked as assumed.
- No TRL 4 material exists in the repo; `build-log/README.md` is the original scaffold and was left untouched.

### Recommended next step

TRL 4 is on hold by Amish's instruction; no TRL 4 work was started. Next, decide O1 to O3. The most useful paper work while TRL 4 is on hold is to identify an openly licensed, labeled plantar-pressure or foot-IMU freeze data set, since R3 to R5 depend on it.

For reference only, TRL 4 would need: bench measurements of the FSR divider response and saturation, the motor's felt intensity through a sock and cover, the insole stack thickness, the pod mass and the clip retention; an offline replay of the detector on labeled data for R3 to R5; a measured power budget; and a lab test report (TST) with `environment: lab`, with ethics review before any use with people who freeze.
