# StepCue

**Area:** BioMedical · **Status:** Concept · **Prototype budget:** about $200 USD · **Difficulty:** 3 of 5

Pressure-sensing insole that detects the onset of a freeze and triggers a rhythmic haptic or audio cue.

## Problem

Freezing of gait in Parkinson's causes falls, and cueing devices are expensive.

## Concept

Pressure-sensing insole that detects the onset of a freeze and triggers a rhythmic haptic or audio cue.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- FSR sensors (4 to 6)
- Flex PCB or laminated film
- ESP32-C3
- Coin vibration motor
- LiPo cell

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or monitor any person.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
