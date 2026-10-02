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

# Numbers match bom/bom.csv lines 1 to 11. Line 12 (hardware) is drawn with the lid, line 13 (tail
# connector) with the interface board and line 14 (spacer foam) as part of the sensor laminate.
parts = [
    Part("Top cover, PU foam and textile", m["cover"], "#8CC7C0", 1, (0, 0, 70)),
    Part("Force-sensing resistors (5)", m["fsrs"], "#D4A017", 2, (0, 0, 48)),
    Part("Sensor laminate (carrier, traces, spacer)", m["laminate"], "#C2410C", 3, (0, 0, 30)),
    Part("Flat flex tail and connector", m["tail"], "#EA580C", 4, (0, 0, -75)),
    Part("Coin vibration motor", m["motor"], "#0F766E", 5, (0, 0, -45)),
    Part("Insole base, EVA foam", m["foam"], "#374151", 6, (0, 0, 0)),
    Part("Heel pod base with clip", m["base"], "#9CA3AF", 7, (-45, 0, 70)),
    Part("LiPo cell, 400 mAh", m["cell"], "#B91C1C", 8, (-85, 0, 70)),
    Part("Controller module with IMU", m["module"], "#1D4ED8", 9, (-120, 0, 95)),
    Part("Interface board, connector and pause button", m["iface"] + m["zif"] + m["cap"], "#0F766E", 10, (-120, 0, 45)),
    Part("Heel pod lid and screws", m["lid"] + m["screws"], "#D1D5DB", 11, (-160, 0, 70)),
]
INSOLE = ("Top cover, PU foam and textile", "Force-sensing resistors (5)", "Sensor laminate (carrier, traces, spacer)",
          "Coin vibration motor", "Insole base, EVA foam")

# Context for scale: a simplified shoe (outsole and heel counter), hero only
context = [Part("Shoe outsole and heel counter", model.shoe_context(), "#C8CDD3")]

KEY_FIGURES = ["5 FSRs plus 6-axis IMU, sampled at 104 Hz",
               "Freeze decision every 0.25 s on a 2 s window",
               "Haptic cue at the wearer's cadence, 60 to 130 per min",
               "About 12 days per charge, 400 mAh (7 conservative)",
               "About $90 in parts, one insole (STC-CAL-001)"]
FLOW = {"title": "closed-loop signal flow (all on the pod, no cloud)", "unit": "",
        "stages": [("Foot sensing", "5 FSRs + IMU, 104 Hz"),
                   ("Freeze detector", "every 0.25 s"),
                   ("Cue driver", "about 41 ms (est.)"), ("Haptic cue", "about 1.75 Hz (est.)"),
                   ("Walking resumes", "cue stops")]}


def one(item):
    """Render one concept image per process when memory is tight:
    python cad/src/concept_media.py hero|cutaway|exploded|web|flow|sheet"""
    import concept as K
    md = ROOT / "media"
    if item == "hero":
        K._render(parts + context, md / "hero.png", title="StepCue",
                  note="Seen from the front right and above, 24 deg elevation. Grey: Shoe outsole and heel counter for scale")
    elif item == "cutaway":
        K._render(K.cutaway_parts([p for p in parts if p.name not in INSOLE]), md / "cutaway.png", azim=-90, elev=18,
                  title="StepCue: cutaway", note="Front half removed; seen from the front and above, 18 deg elevation")
    elif item == "exploded":
        K._render(parts, md / "exploded.png", offsets=True, labels=True, title="StepCue: exploded view",
                  note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv")
    elif item == "web":
        K.export_web_model(parts, "media", title="StepCue: Cueing insole concept")
    elif item == "flow":
        K.flow_diagram(FLOW["stages"], md / "flow.png", f"StepCue: {FLOW['title']}", FLOW["unit"], ())
    elif item == "sheet":
        import datetime
        from drawing import Sheet, project_views
        from build123d import Compound
        date = datetime.date.today().isoformat()
        views = project_views(Compound(children=[p.shape for p in parts]), md / "_views")
        views["iso"] = project_views(Compound(children=[p.shape for p in parts + context]), md / "_views_fig")["iso"]
        sh = Sheet(project="StepCue", title="Cueing insole concept", dwg_no="STC-DWG-010", rev="P1", author="Amish Chadha",
                   date=date, theme="blueprint", material="Massing model for concept communication",
                   revisions=[("P1", "Concept sheet", date, "AC")])
        sh.add_ortho(views)
        sh.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale; grey is for scale")
        sh.add_notes("Key figures", KEY_FIGURES, x=276, y=168, width=140)
        sh.save(md / "concept-blueprint")
        import shutil
        shutil.rmtree(md / "_views", ignore_errors=True); shutil.rmtree(md / "_views_fig", ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for it in sys.argv[1:]:
            one(it)
        sys.exit(0)
    render_all(
        parts, project="StepCue", title="Cueing insole concept", dwg_no="STC-DWG-010",
        key_figures=KEY_FIGURES, scale_figure=False, context=context, cut_exclude=INSOLE, flow=FLOW,
    )
