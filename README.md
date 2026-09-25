# StepCue

![TRL 2](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** BioMedical · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $200 USD · **Difficulty:** 3 of 5

Pressure-sensing insole that detects the onset of a freeze and triggers a rhythmic haptic or audio cue.

![StepCue concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/STC-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Freezing of gait in Parkinson's causes falls, and cueing devices are expensive.

## Concept

A thin insole with five force-sensing resistors and a coin vibration motor connects by a flat flex tail to a small pod clipped over the heel of the shoe. The pod samples the pressure sensors and its own motion sensor 104 times a second, checks every 0.25 s for the pattern of a freeze, and pulses the motor at the wearer's own cadence until walking resumes; audio, where preferred, plays through a paired phone or earbuds. The TRL 3 calculations (STC-CAL-001) give $83.44 in parts for one instrumented insole and heel pod and 12.5 days per charge (7.4 conservative). Detection speed, reliability and nuisance cues are at risk and cannot be shown without labeled data.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Force-sensing resistors (5)
- Laminated sensor film with a flat flex tail
- nRF52840 controller module with built-in 6-axis IMU in a clip-on heel pod
- Coin vibration motor under the arch
- 400 mAh protected LiPo cell (in the pod, outside the shoe)

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or monitor any person, or relied on to prevent falls. The heel pod holds a lithium cell: use a protected cell and never charge it while worn.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (STC-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `STC-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
