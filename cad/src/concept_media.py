"""StepCue concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates (mm): X runs heel (0) to toe, Y points to the medial (big-toe) side of a
right insole, Z is up with the underside of the insole at Z = 0. The heel pod clips
over the shoe heel counter behind the heel (negative X).
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Face, Wire, Vector, extrude
from concept import Part, render_all

# Insole layers, about EU 42 (US men's 8.5); thicknesses in mm
L = 272.0
FOAM_T, LAM_T, TOP_T = 3.0, 0.8, 1.2
FSR_R, FSR_T = 9.0, 0.5


def outline(grow=0.0, n=40):
    """Right-foot insole outline as a list of (x, y) points, optionally grown outward."""
    xs = np.linspace(32, 255, n)
    lat = np.interp(xs, [32, 100, 180, 230, 255], [32, 33, 42, 38, 28]) + grow
    med = np.interp(xs, [32, 100, 140, 190, 230, 255], [32, 24, 30, 52, 50, 38]) + grow
    pts = [(x, -w) for x, w in zip(xs, lat)]
    for t in np.linspace(-np.pi / 2, np.pi / 2, 24)[1:-1]:          # toe cap
        pts.append((255 + (17 + grow) * np.cos(t), 5 + (33 + grow) * np.sin(t)))
    pts += [(x, w) for x, w in zip(xs[::-1], med[::-1])]
    for t in np.linspace(np.pi / 2, 3 * np.pi / 2, 24)[1:-1]:       # heel cup
        pts.append((32 + (32 + grow) * np.cos(t), (32 + grow) * np.sin(t)))
    return pts


def slab(z0, t, grow=0.0):
    face = Face(Wire.make_polygon([Vector(x, y, 0) for x, y in outline(grow)], close=True))
    return Pos(0, 0, z0) * extrude(face, amount=t)


# 1 to 6: the insole stack
top_z = FOAM_T + LAM_T
cover = slab(top_z, TOP_T)
FSR_XY = [(34, 0), (110, -24), (185, 28), (178, -30), (246, 24)]   # heel, lateral midfoot, MTH1, MTH5, hallux
fsrs = None
for x, y in FSR_XY:
    d = Pos(x, y, FOAM_T + LAM_T - FSR_T / 2) * Cylinder(FSR_R, FSR_T)
    fsrs = d if fsrs is None else fsrs + d
laminate = slab(FOAM_T, LAM_T - FSR_T)
# 4, flat flex tail to the pod: runs back from the heel, up the inside of the heel counter and over its top edge
TAIL_W = 12.0
tail = (Pos(3.8, 0, FOAM_T + LAM_T - FSR_T + 0.15) * Box(8.5, TAIL_W, 0.3)
        + Pos(-0.25, 0, 29.4) * Box(0.4, TAIL_W, 51.8)
        + Pos(-7.5, 0, 55.2) * Box(14.5, TAIL_W, 0.4))
MOTOR = (120.0, 16.0)                                   # medial arch, low plantar load
motor = Pos(MOTOR[0], MOTOR[1], 1.6) * Cylinder(5.0, 2.7)
foam = slab(0, FOAM_T) - Pos(MOTOR[0], MOTOR[1], 1.4) * Cylinder(5.3, 3.0)

# 7 to 12: heel pod clipped over the heel counter (counter outer face at X = -3.5, top at Z = 55)
X_OUT = -3.5
base = (Pos(X_OUT - 8.25, 0, 33) * Box(16.5, 38, 44)
        - Pos(X_OUT - 9.75, 0, 33) * Box(15.5, 34, 40)           # open tray, lid closes the outside
        + Pos(-5.0, 0, 56.9) * Box(13, 30, 3)                     # clip bridge over the counter top
        + Pos(1.0, 0, 47) * Box(2, 30, 19.8))                     # clip finger inside the counter
battery = Pos(X_OUT - 4.85, 0, 33) * Box(5.2, 25, 34)           # 502535 class, 400 mAh
controller = Pos(X_OUT - 9.25, 0, 42) * Box(3.5, 17.5, 21)       # ESP32-C3 module, USB-C at the top
imu = Pos(X_OUT - 8.75, 0, 20) * Box(2.5, 13, 11)                # 6-axis IMU breakout
buzzer = Pos(X_OUT - 12.7, 0, 30) * Rot(0, 90, 0) * Cylinder(6, 3)
lid = Pos(X_OUT - 17.5, 0, 33) * Box(2, 38, 44)

parts = [
    Part("Top cover, PU foam and textile", cover, "#8CC7C0", 1, (0, 0, 70)),
    Part("Force-sensing resistors (5)", fsrs, "#D4A017", 2, (0, 0, 48)),
    Part("Sensor laminate", laminate, "#C2410C", 3, (0, 0, 30)),
    Part("Flat flex tail and connector", tail, "#EA580C", 4, (-15, 0, 20)),
    Part("Coin vibration motor", motor, "#0F766E", 5, (0, 0, -45)),
    Part("Insole base, EVA foam", foam, "#374151", 6, (0, 0, 0)),
    Part("Heel pod base with clip", base, "#9CA3AF", 7, (-40, 0, 0)),
    Part("LiPo cell, 400 mAh", battery, "#B91C1C", 8, (-75, 0, 0)),
    Part("ESP32-C3 controller module", controller, "#0F766E", 9, (-110, 0, 5)),
    Part("6-axis IMU", imu, "#1D4ED8", 10, (-110, 0, -25)),
    Part("Piezo buzzer", buzzer, "#111827", 11, (-140, 0, 0)),
    Part("Heel pod lid", lid, "#D1D5DB", 12, (-175, 0, 0)),
]
INSOLE = ("Top cover, PU foam and textile", "Force-sensing resistors (5)", "Sensor laminate",
          "Coin vibration motor", "Insole base, EVA foam")

# Context for scale: a simplified shoe (outsole and heel counter), hero only
outsole = slab(-22, 22, grow=6)
inner = slab(-1, 60, grow=0.5)
counter = (slab(0, 55, grow=3.5) - inner) - Pos(170, 0, 30) * Box(260, 200, 70)
context = [Part("Shoe outsole and heel counter", outsole + counter, "#C8CDD3")]

if __name__ == "__main__":
    render_all(
        parts, project="StepCue", title="Cueing insole concept", dwg_no="STC-DWG-010",
        key_figures=["5 FSRs sampled at 100 Hz, plus 6-axis IMU",
                     "Freeze decision every 0.25 s on a 2 s window",
                     "Cue at the wearer's cadence, about 1.7 Hz",
                     "About 3 days per charge, 400 mAh (estimate)",
                     "About $106 in parts, one insole (indicative)"],
        scale_figure=False, context=context, cut_exclude=INSOLE,
        flow={"title": "closed-loop signal flow (all on the pod, no cloud)", "unit": "",
              "stages": [("Foot sensing", "5 FSRs + IMU, 100 Hz"),
                         ("Freeze detector", "every 0.25 s"),
                         ("Cue driver", "under 0.1 s (est.)"), ("Haptic or audio cue", "about 1.7 Hz (est.)"),
                         ("Walking resumes", "cue stops")]},
    )
