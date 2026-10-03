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

Status update: items 1 to 7 and 9 were decided by Amish on 2026-09-25, going with the recommendations (STC-DDR-001, D1 to D8). Item 8 has no recommendation and remains proposed, awaiting Amish.

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
2. **O2. R6 target for the audio route.** Options: keep 0.1 s and accept that audio misses it, or set 0.3 s for the audio route only. Recommendation: 0.3 s for audio, 0.1 s for haptic. Decided by Amish, 2026-09-25: go with recommendation (STC-DDR-002).
3. **O3. R9 margin.** Options: keep the 3.0 mm EVA base (zero margin) or use 2.5 mm (4.5 mm stack) with a 0.4 mm motor relief in the laminate. Recommendation: 2.5 mm. Decided by Amish, 2026-09-25: go with recommendation (STC-DDR-002).

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

## Session 2026-09-25: recommendations accepted

Authority: on 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation". Items without a recommendation stay open. Recorded in `docs/decisions/0002-recommendations-accepted.md` (STC-DDR-002 v0.1).

### Decisions applied and what changed

- **O2, R6 audio-route target.** R6 split into 0.1 s for the haptic default and 0.3 s for phone or earbud audio. R6 moves from not met (audio 0.18 to 0.28 s against 0.1 s) to met (haptic 41 ms; audio 0.18 to 0.28 s against 0.3 s, 20 ms margin at worst on assumed latencies). Files: STC-REQ-001 v0.4, STC-CAL-001 v0.2 and `sizing.py`, STC-PRC-001 v0.4.
- **O3, 2.5 mm EVA base.** `foam_t` 3.0 mm to 2.5 mm; insole stack 5.00 mm (zero margin) to 4.50 mm (4.3 to 4.7 mm with EVA tolerance). The 2.7 mm motor sits on a 0.2 mm EVA floor and stands 0.4 mm proud into a new relief in the laminate underside, leaving 0.4 mm of laminate over it. R9 moves from at risk to met. Files: `cad/src/model.py` with STEP and STL re-exported, STC-DWG-001 Rev P1 to P2, `bom/bom.csv` lines 3 and 6 (total unchanged at $83.44), media regenerated, STC-CAL-001 v0.2, STC-REQ-001 v0.4, STC-PRC-001 v0.4.
- STC-DDR-001 v0.2 marks O2 and O3 as decided; the TRL 2 and TRL 3 sessions above are annotated.
- Budget: `budget_usd` unchanged at $200 (no budget recommendation). Pitch and problem unchanged (no rewording recommendation).
- README: "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" sections added before "Problem"; the inspiration point is the Daphnet wearable assistant (Bächlin et al., 2010). Media, drawings and PDFs were regenerated so the footer shows designmolecule.com.

### Requirement status (STC-CAL-001 v0.2, Table 1)

11 met, 0 not met, 3 at risk, 1 not verifiable at TRL 3 (was 9 met, 1 not met, 4 at risk, 1 not verifiable).

- **Not met:** none.
- **At risk: R3, R4, R5.** Detection delay, reliability and nuisance cues pull against one another (method floor 1.50 s, 2.50 s with the 5 confirming windows R5 needs; published pressure-only accuracy 77 to 80 % and 83 to 85 %). They need labeled data.
- **Not verifiable at TRL 3: R12** (one-handed use).
- **Met:** R1, R2, R6, R7, R8, R9, R10, R11, R13, R14, R15.

### Still awaiting Amish

1. **O1. First co-design partner** (movement disorders clinic, physiotherapy practice or Parkinson's patient group). No recommendation; proposed, awaiting Amish.

### Cross-repo actions

None. No decision in this repo needs a change elsewhere.

### Safety concerns

- Unchanged from the TRL 3 session. The thinner EVA base puts slightly less foam between the foot and the 0.46 mm FSRs; nothing rigid over 1 mm sits under the heel or metatarsal heads, and the skin check after early wear still applies.
- The 0.3 s audio target rests on assumed BLE and phone audio latencies; audio is optional and the haptic default is unaffected.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No build, test, measurement, PCB, firmware or purchasing work was started. `trl: 3` and `trl_target: 3` are unchanged.

## Session 2026-09-26: sources strengthened

Three uncited rows in the README "By country or region" table were rewritten so each rests on a checked source. No budget change.

- United States: uncited claim about a university gait-research base replaced with the estimate of about 930,000 people aged 45 and over with Parkinson's in 2020 and about 1.24 million by 2030 ([Marras et al., *npj Parkinson's Disease*, 2018](https://www.nature.com/articles/s41531-018-0058-0)).
- India: uncited claim about device costs relative to incomes replaced with the UNFPA India Ageing Report 2023 figures (older share projected to double to over 20 % by 2050; over 40 % of older people in the poorest wealth quintile), citing [UNFPA India](https://india.unfpa.org/en/news/india-ageing-elderly-make-20-population-2050-unfpa-report).
- Brazil: uncited claim about the public health system and ageing replaced with the ELSI-Brazil estimate of about 535,000 people with Parkinson's disease in 2024 and about 1.25 million by 2060 ([Schlickmann et al., 2025](https://www.sciencedirect.com/science/article/pii/S2667193X25000560)).
- Kept and rechecked: WHO Parkinson's fact sheet, the freezing-of-gait meta-analysis (Springer), the Cochrane falls review and Xu et al. (2024) for China. The Parkinson's UK Technology Guide price pages and the PubMed record for Bächlin et al. (2010) could not be refetched this session (fetch restrictions and a PubMed security check); they were left unchanged.
- `docs/01-problem.md` does not repeat the rewritten rows, so it was not changed.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added an appearance model for photoreal renders; the renders themselves (`media/render-hero.png`, `media/render-exploded.png`) are produced separately from it.

### What was done

- New `cad/src/product_model.py`: `product_parts()` (24 parts: 9 shell, 13 internal, 2 context), `TITLE` and `RENDER_VIEWS` (hero from the front left and above at 30 deg, looking along the insole from the heel; exploded from the front left and above at 28 deg). It imports `PARAMS`, `derived()`, `build_parts()` and `outline()` from `model.py` and keeps every main dimension and interface: insole stack thicknesses, the five FSR sites, the motor pocket and laminate relief, the flex tail route over the counter, the pod envelope, clip bridge and finger, the USB-C, tail, pause button and LED openings, and the internal envelopes.
- Appearance detail added:
  - Insole: smooth spline outline through the model's outline points; light textile top cover with a filleted edge, printed teal rings over the five sensor sites and a field of forefoot perforations; FSRs with visible active areas; amber polyimide laminate with indicative copper traces from each sensor to the tail pad; dark EVA base.
  - Heel pod: filleted graphite base with a parting-line groove, ribbed side grips and a filleted clip; light lid with a recessed bezel, teal pause button cap, lit status LED light pipe, a small raised cadence mark and four M2 lid screws; stadium USB-C opening.
  - Internals dressed from the model envelopes: LiPo pouch with label, controller PCB with shield can and USB-C receptacle, perfboard with tact switch and MOSFETs, tail connector.
  - Context (clay): a smooth shoe shell whose heel counter matches `counter_t` and `counter_h`, and a smooth left foot and lower leg standing beside it.
- README hero image now points to `media/render-hero.png`, with an "Exploded render" link added to the links line.
- Self-check previews made with the kit renderer in `/tmp/stepcue-prod/` (not part of the repo).

### Where the appearance model differs from `model.py` (each proposed, awaiting Amish)

1. **Insole lifted at the toe in the hero pose.** The insole layers are tilted 8 deg toe-up about the top of the heel so the sensor-site rings read in the render; the flex tail's bonded pad tilts with them while the run up the counter stays put. Proposed, awaiting Amish. Recommendation: keep for the render only; the fitted, flat state in `model.py` stays the reference.
2. **Smooth insole outline.** The layers use a periodic spline through the same `outline()` points instead of the model's polygon. Proposed, awaiting Amish. Recommendation: adopt the spline in `model.py` at the next model revision; the change in area is negligible.
3. **Features not in the model or BOM wording:** printed sensor-site rings and forefoot perforations in the top cover, copper trace routing, side grip ribs, a lid bezel recess, a raised cadence mark, and four M2 lid screws (M2 screws are already in BOM line 12). Proposed, awaiting Amish. Recommendation: treat all as appearance only; if the screws are kept, the lid needs bosses at TRL 4, which is on hold.
4. **Pod split.** The lid and base share one filleted envelope with a 0.5 mm parting-line groove, so the pod reads as one product rather than a tray and a flat plate. Proposed, awaiting Amish. Recommendation: adopt the rounded envelope (5 mm corner radius) in the next model revision; it softens the edges near the wearer's heel, which the safety notes already ask for.
5. **Hero context.** The clay shoe shell replaces the model's blocky `shoe_context()` for renders only, with a clay foot beside it for scale. Proposed, awaiting Amish. Recommendation: keep for renders; leave `shoe_context()` for the concept media.

### Status

This is an appearance model only, for renders: no tolerances, PCB layout or fabrication detail. `model.py`, the BOM and the controlled documents were not changed. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, design for construction and illustrated build plan (BLD-001)

Run under the build plan rollout brief (kit 1.7.0) and `/build-plan` steps 1 to 5, with Amish's instruction of 2026-09-30 to "fix the design assumptions to match and be physically feasible as you draw the illustrations", his 2026-09-30 rule that open decisions go in a separate register, and his 2026-10-01 rule that `budget_usd` is a value-engineering target. Commit and push were skipped by instruction (cloud copy, no git). TRL cap respected: no PCB layout, firmware, purchasing list, test plan or build log; the interface circuit is perfboard wired at block level.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` matches `.kit/CLAUDE.md`.
- `cad/src/model.py`: made constructable (below) and given 471 build123d constructability checks (`python cad/src/model.py --check`: no overlaps, every part touches what holds it, required gaps open, traces clear of each other, the sensor discs and the edge, each pod part slides into the open tray in order, print and size limits). All 471 pass. The export now writes single parts before the assembly compounds, which had stopped the single-part STEP files being written.
- `cad/step/` and `cad/stl/`: assembly, heel pod and single parts (base, lid, foam, film, spacer, cover, laminate) regenerated.
- `cad/drawings/STC-DWG-001` Rev P3 (general arrangement), parts list now including lines 12 to 14.
- `media/`: hero, cutaway, exploded (pod parts now pulled clear behind the heel), flow, concept blueprint, `model.glb` and `viewer.html` regenerated from the constructable model (`cad/src/concept_media.py`, which can now render one image per process; key figure now about $90).
- `cad/src/build_plan_media.py` (new, uses `.kit/build_views.py`): overview, seven making sketches (`cad/drawings/STC-DWG-101` to `107`), the insole circuit layout, block wiring, eight joint close-ups and fourteen assembly step pictures in `docs/05-build-plan/`.
- `docs/05-build-plan.md` (STC-BLD-001 v0.1, new): plain-English plan by component in build order, with first checks, safety stops S1 to S7, tools, and sources. No open decisions in it.
- `docs/06-design-decisions.md` (STC-DEC-001 v0.1, new): ten open decisions, six items to confirm when parts are bought, a value engineering section and the decisions made with Amish's words.
- `docs/decisions/0003-design-for-construction.md` (STC-DDR-003 v0.1, draft): every change, with the reason.
- `docs/04-calcs/01-sizing.md` (STC-CAL-001 v0.3), `docs/03-requirements.md` (STC-REQ-001 v0.5), `docs/02-concept.md` (STC-PRC-001 v0.5), `bom/bom.csv`, `bom/bom-notes.md`: stack description, pod size and mass, cost and components updated.
- `project.yaml`: `design_state: constructable`; STC-DDR-003, STC-BLD-001 and STC-DEC-001 added to `trl_evidence`. `budget_usd` unchanged.
- `README.md`: "Prototype build plan" link and a "Building the prototype" section before "Safety"; parts figure now about $90. Credits and `CONTRIBUTORS.md` unchanged (Dr. Geeti Chadha kept as contributor).

### Design changes made for construction (STC-DDR-003, draft, open for Amish's review)

1. Sensor laminate: one solid 0.8 mm sheet became a 0.3 mm polyimide carrier with copper tape traces under a 0.5 mm closed-cell foam spacer with windows; stack unchanged at 4.50 mm.
2. Pressure sensors: tails and two solder tabs added, soldered to tab pads on the carrier; tails pointed to suit the routing.
3. Circuit: eight routed copper tape traces (0.8 mm apart, 1.5 mm inside the edge) with one insulated crossover on a polyimide patch.
4. Motor: 0.2 mm foam floor and laminate relief replaced by a through-hole in the base and carrier; motor bonded under the spacer, 1.7 mm of foam over it.
5. Flex tail: 12 mm became 9 mm (a real 8-way cable); its insole end slit into strips soldered to pads 4 mm apart.
6. Clip finger and bridge curved to the 32 mm heel counter; the flat finger and tail had cut into the counter.
7. Tail connector (ZIF, new BOM line 13) on top of the interface board; board moved above the module; tail enters through a slot under the roof.
8. Controller module turned USB-C down, the receptacle in a notch in the bottom wall.
9. Cell, module and interface board held by double-sided tapes.
10. Lid held by four M2 thread-forming screws into corner bosses; pod widened from 34 to 37 mm.
11. Pause button cap 9.4 mm, standing 1 mm out of the lid.
12. Heel notch in the spacer and cover for the tail.

### Key results

- Requirement status unchanged: 11 met, none not met, 3 at risk (R3, R4, R5), 1 not verifiable at TRL 3 (R12).
- Pod 27.2 g (was 25.2 g) against 35 g; body 42 x 37 x 15 mm against 45 x 40 x 20 mm. Clip hold 6.0 N against 2.7 N at heel strike.
- Value-engineering target: USD 200. Estimated cost of the constructable design: USD 89.94 (USD 110.06 under the target); was USD 83.44.

### Decisions proposed and awaiting Amish

All in `docs/06-design-decisions.md`: acceptance of STC-DDR-003 P1 to P12, charging with the insole and pod together (A1), 37 mm pod with screws (A2), copper traces across the flexing forefoot (A3), the first co-design partner (O1) and the five appearance-model items of 2026-09-26.

### Safety

- The build plan keeps the cell out of the pod until safety stops S2 and S3, never charges it while worn or wet, and limits any wear to the builder, standing and seated. Wear trials with people who freeze belong to later, supervised work with ethics review. StepCue is a research and educational prototype, not a medical device.
- New hazards from construction: soldering on thin film (burns, fumes) and spray contact adhesive (flammable fumes); both are covered by stop S1 and the workspace notes.

### Recommended next step

Amish reviews STC-DDR-003 and the register. TRL 4 (building and testing to the plan) stays on hold until he says otherwise.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." The recommendations written for this repo's open decisions are recorded as decided.

### Decisions recorded

10 decisions, moved from "Open decisions" to "Decisions made" in the register (STC-DEC-001 v0.2):

1. Design for construction P1 to P12 accepted as modelled (STC-DDR-003).
2. Charging: insole and pod come out together for the supervised prototype sessions; an outside connector is to be decided before any take-home use (A1).
3. Pod 37 mm wide with four M2 lid screws (A2).
4. Traces built as modelled, checked for continuity before each wear session, and inspected after the first wear trials at TRL 4 (A3).
5. First co-design partner: a Parkinson's patient group through a local support group affiliated with the Parkinson's Foundation (first candidate to approach), with a physiotherapy practice for the first supervised user session (O1).
6. The 8 degree toe-up tilt for the hero render only.
7. Smooth spline insole outline at the next model revision.
8. Sensor rings, perforations, grip ribs, bezel recess and cadence mark are appearance only.
9. 5 mm pod corner radius and parting-line groove at the next model revision.
10. Clay shoe shell and foot for the renders only.

### Documents changed

- `docs/06-design-decisions.md`: STC-DEC-001 v0.2
- `docs/decisions/0001-trl2-review-decisions.md`: STC-DDR-001 v0.3
- `docs/decisions/0002-recommendations-accepted.md`: STC-DDR-002 v0.2
- `docs/decisions/0003-design-for-construction.md`: STC-DDR-003 v0.2 (accepted; status kept Draft)
- `docs/01-problem.md`: STC-PRB-001 v0.4 (partner)
- `docs/02-concept.md`: STC-PRC-001 v0.6 (decisions paragraph)

### Follow-up actions to carry approved decisions into the design

1. Decision 2: decide the outside connector (option b) before any take-home use, and model it then (model).
2. Decision 4: add a continuity check of every trace to the checklist for each wear session when TRL 4 is opened (docs).
3. Decision 5: approach a local support group affiliated with the Parkinson's Foundation, and a physiotherapy practice for the first supervised session; nothing is agreed (docs).
4. Decision 7: change the insole outline in `cad/src/model.py` to the smooth spline, keeping the 1.5 mm trace edge margin, and regenerate the drawing and the insole outline template picture (Figure 4 of the build plan) (model, drawings, pictures).
5. Decision 9: give the pod base and lid a 5 mm corner radius and a parting-line groove in the model, and regenerate the pod making sketches and build plan pictures (model, drawings, pictures).
6. Decisions 1 and 3: regenerate the photoreal renders, card and social preview on Amish's Mac for the 37 mm pod with USB-C in the bottom wall, the curved clip and the 9 mm tail, with the render-only choices of decisions 6, 8 and 10 (pictures).

### Points found in the review

- R10 limits the pod body to 20 mm deep and the requirements table shows 20.3 mm including the clip while reporting R10 as met; it should say whether the clip counts.
- The cost is $89.94 against a $200 target, $110.06 under, so the target no longer drives any value-engineering choice; a second insole for the other foot (about $47) would still leave it well under.
- Item 2 and R12 conflict: with the connector inside the pod the pod cannot come off the shoe on its own.

## Session 2026-10-02: approved follow-ups carried out

Amish, 2026-10-02: "APPROVED CHANGES, COMPLETE THESE" for the follow-up actions of the open-decision sign-off, and "COMPLETE THESE" for the out-of-date renders, whose scenes are prepared here. Run on a cloud copy without git, so nothing was committed or pushed. TRL cap respected: no hardware, test plan or build record.

### Follow-ups

1. Decision 2 (outside connector before any take-home use): not done. The decision itself defers it until take-home use is planned; there is nothing to model yet. Stays with Amish.
2. Decision 4 (continuity check of every trace before each wear session): done in the plan. Safety stop S6 of STC-BLD-001 v0.2 now requires every one of the eight traces to read continuous, connector way to pad, before each wear, however short. The TRL 4 wear-session checklist does not exist yet; carry the same line into it when TRL 4 is opened.
3. Decision 5 (approach a local support group affiliated with the Parkinson's Foundation and a physiotherapy practice): not done. It is outreach by Amish; nothing is agreed and nothing was sent. STC-PRB-001 v0.4 already records the decision.
4. Decision 7 (smooth spline insole outline, 1.5 mm trace margin): done. `cad/src/model.py` now builds every insole layer, the shoe context and the layout from one closed spline. Its control points are the earlier outline resampled every 30 mm (so the old corners are not copied into it) plus the exact heel arc where the clip and tail fit the counter. The outline moves up to about 2.4 mm from the old polyline; every trace keeps its 1.5 mm margin and every sensor stays inside. The general arrangement (STC-DWG-001 Rev P4), the insole layout template (build plan Figure 4) and the insole making sketches STC-DWG-101 to 104 (Rev P2) are redrawn.
5. Decision 9 (5 mm pod corner radius and parting-line groove): done. Base and lid have their four long edges rounded to 5 mm (cavity 3.5 mm, so the wall stays 1.5 mm), and the base rim a 0.5 x 0.5 mm groove at the lid. The corner bosses stay inside the rounded corner and clear of the groove. Making sketches STC-DWG-105 and 107 are Rev P2; the overview, joints and steps are redrawn.
6. Decisions 1 and 3 with 6, 8 and 10 (photoreal renders, card and social preview): scenes prepared, images not made. `cad/src/product_model.py` is rebuilt on the solids of `model.py`, so it shows the 37 mm rounded pod with the parting groove, the USB-C receptacle in the bottom wall, the curved clip, the 9 mm tail, the two-layer laminate, the motor in its through-hole and the tail connector, with the render-only choices of decisions 6 (8 degree toe-up tilt), 8 (rings, perforations, grip ribs, bezel recess, cadence mark) and 10 (clay shoe and foot). Scenes for the hero and exploded views are in `/home/claude/renders/stepcue/`. `media/render-hero.png`, `render-exploded.png`, `card.png` and `social-preview.png` are to be made on Amish's Mac.

### Model and checks

- `python cad/src/model.py --check`: 485 checks, all pass (was 471). New checks: the outline is a smooth spline (tightest bend 22.6 mm radius) through its control points; base and lid corners are rounded; the cavity keeps the 1.5 mm wall round the corners; the groove leaves 1.0 mm of rim; each of the four lid bosses stays inside the rounded corner and the groove; each M2 pilot keeps 1.3 mm of plastic to the groove.
- The simplified shoe context now fits the insole with 0.02 mm clearance, so no faces coincide; it is context only.
- `cad/step/` and `cad/stl/` regenerated (assembly, heel pod and single parts).

### Results

- Requirement status unchanged: 11 met, none not met, 3 at risk (R3 to R5), 1 not verifiable at TRL 3 (R12).
- Pod mass 26.8 g (was 27.2 g) against 35 g: base 7.49 g, lid 3.62 g. Clip hold 6.0 N against 2.6 N at heel strike.
- Value-engineering target: USD 200. Estimated cost of the constructable design: USD 89.94 (USD 110.06 under the target). No price changed; `budget_usd` unchanged.

### Documents changed and new versions

- `cad/src/model.py`, `cad/src/product_model.py`, `cad/src/sheets.py`, `cad/src/build_plan_media.py`
- `docs/05-build-plan.md`: STC-BLD-001 v0.2 (outline and pod text, two rows added to the table of changes, S6 continuity check, figures)
- `docs/04-calcs/01-sizing.md`: STC-CAL-001 v0.4; `docs/03-requirements.md`: STC-REQ-001 v0.6; `docs/02-concept.md`: STC-PRC-001 v0.7; `docs/06-design-decisions.md`: STC-DEC-001 v0.3
- `bom/bom.csv` (lines 6, 7 and 11 described; masses 7.5 g and 3.6 g), `bom/bom-notes.md`
- `README.md`: parts cost corrected to $89.94 (it still said $83.44); STC-DDR-003 shown as accepted; outline and pod described
- `cad/drawings/STC-DWG-001` Rev P4; STC-DWG-101 to 105 and 107 Rev P2 (106 unchanged)
- `docs/05-build-plan/`: insole layout, overview, joints 1 to 8 and steps 1 to 14 (wiring unchanged)
- `media/`: hero, cutaway, exploded, concept blueprint, `model.glb`, `viewer.html` (flow unchanged)
- The "Stale media" note of 2026-10-01 is superseded by item 6 above; the appearance model is no longer stale. (The note itself was removed on 2026-10-02 when the renders were redone.)

### Cross-repo actions

None.

### Still open

- The review point on R10 (whether the clip counts toward the 20 mm depth) and the conflict between the charging decision and R12 remain as written on 2026-10-02, for Amish.

### Safety

No change to the safety case. StepCue remains a research and educational prototype, not a medical device; the added continuity check before each wear makes a broken trace less likely to go unnoticed.

## Session 2026-10-02: Photoreal renders redone on the constructable design

Amish, 2026-10-02: "Photoreal renders are out of date in most repos ... COMPLETE THESE". Rendered with Blender Cycles on Amish's Mac (batch F1) from the scenes exported from `cad/src/product_model.py`, captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Each raw render was looked at once. No commit or push; `trl` unchanged.

- Views: `media/render-hero.png`, `media/render-exploded.png` (the two views in `RENDER_VIEWS`).
- Re-render: hero and exploded, twice each. The first renders showed dark streaks across the heel pod lid face; they came from the four 1 mm countersink cones and the 0.5 to 0.3 mm lid face fillet, features too small for the edge bevel and 0.05 mm vertex merge in `.kit/photoreal.py`. In `cad/src/product_model.py` the fillet is removed (the first re-render, which still streaked), then the countersinks are filled and the M2 screws drawn as flush heads 0.15 mm proud (the second re-render, clean). Appearance only; `model.py` keeps the countersunk holes and screws. New appearance deviation, Proposed, awaiting Amish; recommendation: accept as render only.
- Kit action (not edited here): the same merge and bevel limits put faint streaks on small features in other repos; lower the merge distance or skip it for small parts.
- Appearance deviations already logged (decisions 6, 8 and 10): 8 degree toe-up tilt; sensor-site rings, perforations, grip ribs, bezel recess and cadence mark; clay shoe, foot and lower leg. Unchanged.
- `python3 .kit/image_qc.py`: 4 images, 0 problems. `python3 .kit/render.py --check`: no FAIL, and the missing render-hero warning is gone.
- The "Stale media" note of the 2026-10-01 session is removed; this work resolves it.
