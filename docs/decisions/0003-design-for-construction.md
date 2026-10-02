---
doc_id: STC-DDR-003
title: StepCue design for construction
project: StepCue
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish, including the recommendations for A1 to A3"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 to A3), which are now decided as recommended and recorded in the design decisions register (STC-DEC-001). A1 is decided for the supervised prototype sessions; an outside connector is to be decided before any take-home use. A3 adds a continuity check of every trace before each wear session.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated build plan showing how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept, fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of STC-DDR-002 showed what StepCue does (an insole with five sensors and a coin motor, a flex tail over the heel counter and a clip-on heel pod) but several of its parts could not be made, joined or fitted as drawn. Checking the model with build123d found two clashes (the flat clip finger and the flat tail cut 281 mm³ and 117 mm³ into the curved heel counter) and five parts held by nothing (cell, module, interface board, lid, and the tail end in the pod). Working through how each part is made found the rest.

The changes keep what StepCue does: the same five sensor sites, the same motor site and cue, the same controller, cell and interface circuit, the same 4.50 mm insole stack, the same clip over the heel counter and the same pod height and depth. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 471 constructability checks (`python cad/src/model.py --check`): nothing overlaps, every part touches what holds it, the gaps that must stay open do, every trace is clear of its neighbours, the sensor discs and the insole edge, and each pod part slides into the open tray without hitting what is already there. All 471 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The sensor laminate was one solid 0.8 mm sheet with pockets for the sensors. No such sheet can be bought or made, nothing filled the space round the 0.46 mm sensors, and there were no conductors from the sensors to the tail. | Two layers. A carrier of 125 µm polyimide film with 1.5 mm copper tape traces (0.3 mm with its adhesive), and a 0.5 mm closed-cell polyethylene foam spacer with a window round each sensor, the tail end, the motor leads and the crossover. The stack is unchanged at 0.8 mm (4.50 mm in all). | Copper tape on film is the simplest hand-made flexible circuit; polyimide takes solder where PET melts. The spacer fills the space round the sensors so the cover stays flat. |
| P2 | The sensors were plain discs with no tails or tabs, so they could not be connected. | Each sensor has its tail (7 mm wide, about 12 mm past the disc, short-tail type) with two tabs 2.54 mm apart, soldered to two tab pads on the carrier. Tails point to where the traces run: heel toward the toe, big-toe ball toward the centre line, the other three toward the heel. | The FSR 402 is joined by its tabs; pointing the tails lets eight traces reach every sensor with one crossover. |
| P3 | No trace routing: five sensors (each with a signal and the shared supply) and the motor need eight conductors on one face. | Eight traces at least 0.8 mm apart and 1.5 mm inside the insole edge, routed round the heel sensor and the motor. The supply runs down the centre line with branches to each sensor. One crossing is unavoidable (the outer midfoot sensor's supply branch over the little-toe-side ball trace); it crosses over an 8 x 8 mm polyimide tape patch. | Checked in 2D: no trace passes over a sensor disc; one insulated crossover is standard practice in copper tape circuits. |
| P4 | The 2.7 mm motor sat on a 0.2 mm EVA floor in a 2.3 mm blind pocket, and stood 0.4 mm into a relief cut in the underside of the laminate. Neither can be cut by hand in soft foam or a 0.8 mm film stack. | An 11 mm (10.6 mm) hole right through the EVA and the carrier, with a 4.4 mm lead notch. The motor's adhesive face sticks to the underside of the spacer; it stands 0.1 mm clear of the shoe's floor. Its leads come up through the notch to two pads beside the hole. | A punched through-hole is easy to make; the motor keeps 1.7 mm of foam over it, as before (0.5 spacer and 1.2 cover against 0.4 laminate and 1.2 cover), and the stack is unchanged. |
| P5 | The tail was drawn 12 mm wide and "bonded flush in the laminate" with no electrical joint. An 8-way, 1.0 mm pitch flat flex cable is 9 mm wide, and its 1.0 mm pitch is too fine to solder by hand onto copper tape. | Tail 9 mm wide. Its last 10 mm is slit into eight strips, fanned out and each soldered to a 2 x 5 mm pad; the pads are 4 mm apart, 10 to 15 mm from the back of the heel. | Slitting a flat flex cable into strips is a known hand technique; 4 mm pad spacing leaves room for a soldering iron. |
| P6 | The flat tail and the flat clip finger were drawn against a flat heel counter, but a moulded counter is curved (32 mm radius inside at the heel): the finger cut 281 mm³ into the counter and the tail 117 mm³. | The finger (1.5 mm) and the bridge are curved to the counter: the finger's outer face is 0.3 mm inside the counter's inner face, so it presses the tail against it. The tail bends to the same curve across its 9 mm width. The pod's flat shoe-side face touches the counter on the heel centre line and stands up to 5 mm off it at its edges. | The clip, not the pod body, holds the pod square; a curved finger grips evenly across its 26 mm width. A flat pod face keeps the pod 15 mm deep and its insides square. |
| P7 | The tail ended just inside the pod wall, at the top, with no connector, while the interface board it must reach was at the bottom behind the cell. The 9 mm tail cannot pass the 25 mm cell, which fills the shoe-side half of the pod. | An 8-way ZIF connector on a small adapter board (new BOM line 13) stands on the top edge of the interface board. The interface board moves to the top of the outer half of the pod and the controller module to the bottom. The tail enters through a 10 x 0.6 mm slot under the roof, crosses over the cell (3 mm clear) and drops 2 mm into the connector. | The shortest path for the tail, with no fold behind the cell. The ZIF holds a flat flex cable without solder, so the insole can be changed. |
| P8 | With the module at the bottom, its USB-C faces down instead of up, and the receptacle stopped 1.5 mm inside the wall, so a plug could not seat. | The receptacle stands 1.4 mm past the board end into a 9.4 mm notch in the bottom wall, its mouth 0.3 mm inside the outer face. The notch is open to the lid side so the module slides in, and the lid closes it. | A plug seats fully. Facing down, the port does not collect dirt or rain while the pod is on the shoe; charging is off the shoe in any case (R12). |
| P9 | The cell, module and interface board floated in the pod with no fixing. | The cell is held to the shoe-side wall by 0.3 mm double-sided transfer tape. The module and the interface board are held to the cell by 0.5 mm double-sided foam tape. These fill the gaps the concept left (0.3 and 0.5 mm). | No new parts in the pod; the lid then holds everything in place. |
| P10 | The lid had no fixing. | Four M2 x 6 countersunk thread-forming screws through the lid into four 4 mm bosses moulded in the tray corners. The pod is 37 mm wide (was 34) so the bosses clear the 25 mm cell as it slides in. | Screws are simple to print for and to undo for service. The pod stays within the 45 x 40 x 20 mm limit of R10. |
| P11 | The pause button was a 12 mm tact switch on the interface board, 0.5 mm short of the lid; nothing reached the 10 mm lid opening. | A 9.4 mm round cap on the switch stands 1 mm out of the lid, with 0.3 mm clearance in the opening. | The large button R12 asks for, reachable with the lid shut. |
| P12 | The cover and laminate covered the heel edge where the tail turns up the counter. | An 11 mm wide notch at the heel edge of the spacer and cover. | The tail turns up without being pinched. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Pod base heavier (wider tray, bosses); connector, cap, screws and tapes added. Pod 27.2 g (was 25.2 g) against 35 g [R10]. | Parts added for construction. |
| Cost | BOM lines 3, 4, 6, 7, 10, 11 and 12 respecified, line 12 repriced (USD 5.00 to USD 6.00), lines 13 (tail connector, USD 2.50) and 14 (spacer foam, USD 3.00) added. Estimated cost USD 89.94 against the USD 200 value-engineering target (`budget_usd`), USD 110.06 under. | Parts added for construction. |
| Drawing | STC-DWG-001 Rev P3; making sketches STC-DWG-101 to 107 added. | Follows the model. |
| Documents | STC-CAL-001 v0.3, STC-REQ-001 v0.5, STC-PRC-001 v0.5: stack description, pod size and mass, cost and the tail updated. No requirement changed status. | Follows the model. |
| Insole stack | Unchanged at 4.50 mm (2.5 EVA, 0.3 carrier, 0.5 spacer, 1.2 cover); motor under 1.7 mm of foam. | |
| Clip | Unchanged in size: 1.5 mm finger 18 mm long, 26 mm wide, 1 mm interference, 7.5 N clamp [R12]. | |

*Table 3. Items that would change what StepCue does: proposed, then decided by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Daily charging. With the connector inside the pod, the insole and pod come out of the shoe together for charging (USB-C with the pod off the shoe, as R12 asks), and the insole cannot be left in the shoe. | (a) as modelled: insole and pod come out as one; (b) an outside connector so the pod unplugs from the tail; this adds a part and a wear point. | (a) for the prototype; revisit after the first user session at TRL 4. Decided by Amish, 2026-10-02: (a) for the supervised prototype sessions; decide on (b) before any take-home use. |
| A2 | The pod is 37 mm wide (was 34 mm), leaving 3 mm of the 40 mm R10 limit, to make room for the lid screws. | (a) accept 37 mm with screws; (b) keep 34 mm with a snap-fit lid and no screws. | (a): screws are easier to get right first time; a snap lid can follow once the pod is printed. Decided by Amish, 2026-10-02: (a). |
| A3 | The copper tape traces cross the arch and ball of the foot, where the insole flexes with every step, and may crack. | (a) build as modelled and inspect after the first wear trials at TRL 4; (b) lay the traces in a zigzag where they cross the ball of the foot. | (a): keep the first build simple; the flex life is a TRL 4 test. Decided by Amish, 2026-10-02: (a), with every trace checked for continuity before each wear session. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan STC-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register STC-DEC-001.
- With A1 to A3 decided on 2026-10-02: insole and pod come out together for charging in supervised sessions, with an outside connector to be decided before take-home use; the pod is 37 mm wide with four M2 lid screws; the traces are built as modelled and checked for continuity before each wear session.
- Requirement status is unchanged: 11 met, none not met, 3 at risk (R3, R4, R5), 1 not verifiable at TRL 3 (R12) (STC-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the 34 mm pod with USB-C on top, the flat clip and the 12 mm tail; they need updating on Amish's Mac, where Blender is.
- The sensor tail length and tab spacing, and how far the module's USB-C receptacle stands past its board, are taken as typical values and are confirmed when the parts are bought (STC-DEC-001).
