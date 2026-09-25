"""StepCue concept media, generated from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py. Proportions and main parts only; not for fabrication.

Coordinates (mm): X runs heel (0) to toe, Y points to the medial (big-toe) side of a
right insole, Z is up with the underside of the insole at Z = 0. The heel pod clips
over the shoe heel counter behind the heel (negative X).
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
from concept import Part, render_all  # noqa: E402
import model  # noqa: E402

m = model.build_parts()

# Numbers match bom/bom.csv lines 1 to 11 (line 12, consumables, is not modeled)
parts = [
    Part("Top cover, PU foam and textile", m["cover"], "#8CC7C0", 1, (0, 0, 70)),
    Part("Force-sensing resistors (5)", m["fsrs"], "#D4A017", 2, (0, 0, 48)),
    Part("Sensor laminate", m["laminate"], "#C2410C", 3, (0, 0, 30)),
    Part("Flat flex tail and connector", m["tail"], "#EA580C", 4, (0, 0, -75)),
    Part("Coin vibration motor", m["motor"], "#0F766E", 5, (0, 0, -45)),
    Part("Insole base, EVA foam", m["foam"], "#374151", 6, (0, 0, 0)),
    Part("Heel pod base with clip", m["base"], "#9CA3AF", 7, (250, 0, 70)),
    Part("LiPo cell, 400 mAh", m["cell"], "#B91C1C", 8, (225, 0, 70)),
    Part("Controller module with IMU", m["module"], "#1D4ED8", 9, (200, 0, 90)),
    Part("Interface board and pause button", m["iface"], "#0F766E", 10, (200, 0, 50)),
    Part("Heel pod lid", m["lid"], "#D1D5DB", 11, (175, 0, 70)),
]
INSOLE = ("Top cover, PU foam and textile", "Force-sensing resistors (5)", "Sensor laminate",
          "Coin vibration motor", "Insole base, EVA foam")

# Context for scale: a simplified shoe (outsole and heel counter), hero only
context = [Part("Shoe outsole and heel counter", model.shoe_context(), "#C8CDD3")]

if __name__ == "__main__":
    render_all(
        parts, project="StepCue", title="Cueing insole concept", dwg_no="STC-DWG-010",
        key_figures=["5 FSRs plus 6-axis IMU, sampled at 104 Hz",
                     "Freeze decision every 0.25 s on a 2 s window",
                     "Haptic cue at the wearer's cadence, 60 to 130 per min",
                     "About 12 days per charge, 400 mAh (7 conservative)",
                     "About $83 in parts, one insole (STC-CAL-001)"],
        scale_figure=False, context=context, cut_exclude=INSOLE,
        flow={"title": "closed-loop signal flow (all on the pod, no cloud)", "unit": "",
              "stages": [("Foot sensing", "5 FSRs + IMU, 104 Hz"),
                         ("Freeze detector", "every 0.25 s"),
                         ("Cue driver", "about 41 ms (est.)"), ("Haptic cue", "about 1.75 Hz (est.)"),
                         ("Walking resumes", "cue stops")]},
    )
