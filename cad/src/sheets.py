"""StepCue drawing sheets.

Run from the repo root:  python cad/src/sheets.py
Builds STC-DWG-001 (general arrangement, Rev P2) in cad/drawings/ from cad/src/model.py.
STC-DWG-010 is the concept blueprint sheet made by cad/src/concept_media.py.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
from drawing import Sheet, project_views  # noqa: E402
import model  # noqa: E402

p = model.build_parts()["_p"]
asm = model.build()
work = ROOT / "cad" / "drawings" / "_views"
views = project_views(asm, work)
pod_views = project_views(model.build(keys=model.POD_KEYS), work / "pod")

s = Sheet(project="StepCue", title="Insole and heel pod general arrangement", dwg_no="STC-DWG-001", rev="P2",
          author="Amish Chadha", date="2026-09-25", scale=0.5, concept=True,
          material="Insole EVA, PET laminate, PU cover; pod PETG; bought parts per bom/bom.csv. "
                   "PRELIMINARY, NOT FOR FABRICATION",
          revisions=[("P1", "General arrangement for TRL 3 (STC-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "2.5 mm EVA base, 0.4 mm motor relief (STC-DDR-002)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(pod_views["iso"], 276, 32, 140, 74, label="Heel pod, isometric", sublabel="Not to scale; shoe omitted")
cx, cy, cz = p["cell"]
mx, my, mz = p["module"]
s.add_notes("Main dimensions (mm)", [
    f"Insole {p['insole_l']:.0f} long (EU 42); stack {p['foam_t']:.1f} EVA + {p['lam_t']:.1f} laminate "
    f"+ {p['cover_t']:.1f} cover = {p['stack']:.1f}",
    f"FSRs {p['fsr_d']:.1f} dia x {p['fsr_t']:.2f}, 5 sites: heel, lat. midfoot, MTH1, MTH5, hallux",
    f"Motor {p['motor_d']:.0f} dia x {p['motor_t']:.1f} under medial arch at X {p['motor_xy'][0]:.0f}, "
    f"Y {p['motor_xy'][1]:.0f}; {p['motor_relief']:.1f} relief in laminate underside",
    f"Flex tail {p['tail_w']:.0f} wide x {p['tail_t']:.1f}, up inside the counter, over its top",
    f"Pod body {p['pod_z']:.0f} high x {p['pod_y']:.0f} wide x {p['pod_x']:.0f} deep; "
    f"wall {p['wall']:.1f}, lid {p['lid_t']:.1f}",
    f"Clip: bridge {p['bridge_t']:.0f} thick, finger {p['finger_t']:.1f} x {p['finger_l']:.0f} long, "
    f"{p['bridge_w']:.0f} wide",
    f"Clip gap {p['clip_gap_fitted']:.1f} fitted (counter {p['counter_t']:.1f} + tail), "
    f"{p['clip_gap_free']:.1f} free",
    f"Cell {cx:.1f} x {cy:.0f} x {cz:.0f}; module {mx:.1f} x {my:.1f} x {mz:.0f}, USB-C up",
    f"Pause button opening {p['button_d']:.0f} dia; LED window {p['led_d']:.0f} dia",
], x=276, y=118, width=140)
s.add_notes("Parts list (items match bom/bom.csv)", [
    "1 Top cover, PU foam",
    "2 Force-sensing resistors (5)",
    "3 Sensor laminate",
    "4 Flat flex tail and connector",
    "5 Coin vibration motor",
    "6 Insole base, EVA foam",
], x=20, y=222, width=100)
s.add_notes("Parts list, continued", [
    "7 Heel pod base with clip, PETG",
    "8 LiPo cell, 400 mAh protected",
    "9 Controller module with IMU",
    "10 Interface board, pause button",
    "11 Heel pod lid, PETG",
    "Not a medical device. Never charge while worn.",
], x=124, y=222, width=100)
s.save(ROOT / "cad" / "drawings" / "STC-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("Wrote cad/drawings/STC-DWG-001.svg, .pdf and .png")
