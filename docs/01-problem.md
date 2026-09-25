---
doc_id: STC-PRB-001
title: StepCue problem statement
project: StepCue
doc_type: Problem statement
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work with sources)
---

# StepCue problem statement

Freezing of gait is a sudden, brief inability to step that affects a large share of people with Parkinson's disease and is a major cause of their falls. Cueing (a rhythm the person can step to) often helps them get moving again, but the wearable devices that deliver a cue at the right moment cost several hundred pounds or more, and none is open for others to build, audit or adapt.

## The problem

During a freeze the feet feel "glued to the floor" for a few seconds, most often when starting to walk, turning, passing through a doorway or approaching a target. A 2020 meta-analysis of 29 studies put the prevalence of freezing of gait at about 40 % of people with Parkinson's disease, rising from about 22 % in the first five years after diagnosis to about 71 % after ten years ([Chinese Neurosurgical Journal, 2020](https://link.springer.com/article/10.1186/s41016-020-00197-y)). Freezing is triggered by specific situations, which the research literature has catalogued in detail ([Frontiers in Neurology systematic review, 2023](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2023.1326300/full)), and it responds only partly to medication.

External cues are one of the best-supported management strategies: a rhythmic sound, a vibration or a line on the floor gives the brain an external timing signal for the next step ([Ginis et al., narrative review of cueing for freezing of gait, 2018](https://www.sciencedirect.com/science/article/pii/S1877065717304049)). Cueing that runs all the time can become irritating and less effective, so research systems detect the onset of a freeze and cue only then. A review of wearable cueing devices reports closed-loop research systems with detection sensitivities of about 73 % to 97 % and detection delays of about 0.5 to 3.2 s, using accelerometers on the shank, trunk or ankles ([Sweeney et al., Sensors, 2019](https://www.mdpi.com/1424-8220/19/6/1277)). Plantar pressure alone has also been used to predict freezes: one study using insole pressure data identified about 94 to 95 % of episodes with about 77 to 80 % sensitivity and 83 to 85 % specificity at the window level, about 0.8 s before onset, and found one insole about as good as two ([Pardoel et al., Frontiers in Neurology, 2022](https://www.frontiersin.org/articles/10.3389/fneur.2022.831063/pdf); see also [Shalin et al., Journal of NeuroEngineering and Rehabilitation, 2021](https://jneuroengrehab.biomedcentral.com/articles/10.1186/s12984-021-00958-5)).

Commercial options exist but are costly. The Path Finder laser shoe attachment is listed at £834 ([Parkinson's UK Tech Guide](https://techguide.parkinsons.org.uk/catalogue/path-finder)). The CUE1+ chest-worn vibrotactile device is listed at £795 plus VAT, plus £60 a year for patches, and its sales were paused at the time of writing ([Parkinson's UK Tech Guide](https://techguide.parkinsons.org.uk/catalogue/cue1plus)). Neither is open hardware, and neither combines foot-pressure sensing with an on-demand cue at the foot.

The gap StepCue addresses: an open, low-cost, inspectable insole that senses how the foot is loading, recognizes the pattern of a freeze, and triggers a rhythmic cue only when it is needed, as a platform that researchers, clinics and patient groups can build and study.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Person with Parkinson's who freezes | A cue that arrives quickly when a freeze starts and stops once walking resumes; nothing that changes how the shoe feels | At home and outdoors, in their own shoes, several hours a day |
| Care partner | Fewer falls; a simple device that does not need daily fiddling | Home |
| Physiotherapist or clinician | Adjustable cue type and tempo; a record of how often cues fired | Clinic sessions and home programs |
| Researcher | An open reference design and data format for studying detection and cueing | University labs, gait studies |
| Open hardware community | A reproducible, buildable design | Makerspaces |

## Constraints

- Garage-buildable prototype, about $200 USD per unit (`budget_usd` in `project.yaml`), from off-the-shelf sensors and modules and 3D-printed parts.
- Fits in the wearer's own shoes: the insole must be no thicker than a normal replacement insole, and nothing rigid may sit under the heel or the metatarsal heads.
- Lithium cell and electronics stay outside the shoe, not under the foot.
- People with Parkinson's often have reduced hand dexterity: charging, fitting and switching must be possible with one hand and large features.
- Detection and cueing run on the device, with no phone or cloud needed for the core function; data stays with the wearer.
- Research and educational use only. StepCue is not a medical device and must not be relied on to prevent falls.

## Out of scope

- Diagnosis, disease staging or any clinical decision.
- Stimulation beyond a perceptible cue (no electrical stimulation).
- Cloud services and remote monitoring.
- Fall detection or emergency alerts.

## Open questions

- Which partner to co-design with first: a movement disorders clinic, a physiotherapy practice or a Parkinson's patient group? Proposed, awaiting Amish.
- One insole or a pair for the first build? Proposed: one insole on the side the wearer reports freezing most, since unilateral pressure data performed about as well as bilateral data in Pardoel et al. (2022). Awaiting Amish.
- Where to obtain labeled plantar-pressure freeze data to develop the detector before any human testing, which in any case needs ethics approval and belongs to TRL 4 or later.
