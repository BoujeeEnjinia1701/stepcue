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
