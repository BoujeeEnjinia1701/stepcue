# StepCue

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** BioMedical · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $200 USD · **Difficulty:** 3 of 5

Pressure-sensing insole that detects the onset of a freeze and triggers a rhythmic haptic or audio cue.

![StepCue concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Freezing of gait in Parkinson's causes falls, and cueing devices are expensive.

## Concept

A thin insole with five force-sensing resistors and a coin vibration motor connects by a flat flex tail to a small pod clipped over the heel of the shoe. The pod samples the pressure sensors and its own motion sensor 100 times a second, checks every 0.25 s for the pattern of a freeze, and pulses the motor (or an optional buzzer) at the wearer's own cadence until walking resumes. First-order estimates: about $106 in parts for one instrumented insole and about 3 days per charge. Detection speed and reliability are not yet demonstrated.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Force-sensing resistors (5)
- Laminated sensor film with a flat flex tail
- ESP32-C3 controller and 6-axis IMU in a heel pod
- Coin vibration motor and optional piezo buzzer
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
