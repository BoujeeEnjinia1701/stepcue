"""StepCue product appearance model (build123d), TRL 3, constructable design.

Finished-product look for photoreal renders, built on the solids of cad/src/model.py so the
renders show the design as it will be built (STC-DDR-003, accepted 2026-10-02): the smooth spline
insole outline, the two-layer sensor laminate (amber carrier film with copper tape traces under a
light foam spacer), the five FSRs with visible active areas, the coin motor in its through-hole,
the 9 mm flex tail up the heel counter, and the 37 mm heel pod with 5 mm round corners, a
parting-line groove, the curved clip over the counter, four M2 lid screws, the pause button cap
through the lid and the USB-C receptacle in the bottom wall.
Appearance-only additions (decision of 2026-10-02, item 8): printed sensor-site rings and forefoot
perforations on the top cover, ribbed side grips, a lid bezel recess, a lit LED light pipe and a
cadence mark. Context (decision 10): a smooth clay shoe shell and a clay foot and lower leg. Pose
(decision 6): the insole is lifted 8 degrees at the toe for the renders; the flat fitted state in
model.py stays the reference.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
Research and educational prototype, not a medical device.

Axes as model.py: X runs heel (0) to toe, Y to the medial side of a right insole, Z up with the
underside of the insole at Z = 0 (before the lift). The heel pod clips over the heel counter at
negative X.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Compound, Cylinder, Ellipse, Face, Plane, Polyline, Pos,
                       Rot, Wire, extrude, fillet, loft, make_face)
from model import PARAMS, derived, build_parts, outline_edge, shoe_context  # noqa: F401

TITLE = "StepCue: pressure-sensing insole with a clip-on heel cue pod"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -140,
     "note": "Product render from the front left and above (about 30 deg elevation), looking along the insole "
             "from the heel: heel pod clipped over the clay shoe's heel counter in the foreground, insole lifted "
             "at the toe, clay foot and lower leg behind"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -135,
     "note": "Exploded view from the front left and above (about 28 deg elevation): textile top cover, spacer foam, "
             "force-sensing resistors, carrier film with copper traces, coin motor, EVA base and flex tail; heel pod "
             "lid and screws, button cap, interface board and tail connector, controller module, LiPo cell and pod "
             "base in the foreground"},
]

# Colours (restrained product palette; accent from the kit)
C_ACCENT = "#0F766E"
C_COVER = "#D9DBD6"        # light textile top cover
C_SPACER = "#E8EDF0"       # white closed-cell PE foam spacer
C_EVA = "#2B2F36"          # dark EVA base
C_FILM = "#C98A2B"         # amber polyimide film
C_COPPER = "#B8743F"
C_FSR_FILM = "#D8C99A"
C_FSR_ACTIVE = "#3A3F47"
C_TAIL = "#D08A2E"
C_POD = "#3A3F47"          # graphite pod base
C_LID = "#E6E8EB"          # light lid
C_DARK = "#1C1F24"
C_METAL = "#B8BEC6"
C_LED = "#34D399"
C_PCB = "#1A1D21"
C_PERF = "#166534"
C_POUCH = "#C9CDD2"
C_LABEL = "#1E40AF"
C_CLAY = "#A9ADB2"

# Appearance-only sizes (mm)
LIFT_DEG = 8.0             # insole tilted up at the toe about the top of the heel (render pose, decision 6)
FLOOR_Z = -22.0            # underside of the clay shoe sole


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _smooth_slab(p, z0, t, grow=0.0):
    """The model's smooth spline insole outline (model.outline_edge), extruded from z0 by t."""
    return Pos(0, 0, z0) * extrude(Face(Wire([outline_edge(p, grow)])), amount=t)


def _x_cyl(r, length, x0, y, z):
    """Cylinder along +X starting at x0."""
    return Pos(x0 + length / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, length)


def _lift(shape, pivot_z):
    """Render pose: tilt the insole toe-up by LIFT_DEG about the top edge of the heel (x = 0)."""
    return Pos(0, 0, pivot_z) * Rot(0, -LIFT_DEG, 0) * Pos(0, 0, -pivot_z) * shape


# ---------------------------------------------------------------- context
def _clay_shoe(p):
    """Smooth clay shoe shell: sole and a low upper wall rising to the heel counter (counter_h, counter_t)."""
    ct, ch = p["counter_t"], p["counter_h"]
    sole = _smooth_slab(p, FLOOR_Z, -FLOOR_Z, grow=6.0)
    sole = _fillet_try(sole, _bottom_edges(sole), [4.0, 2.5, 1.5])
    wall = _smooth_slab(p, -1.0, ch + 1.0, grow=ct) - _smooth_slab(p, -2.0, ch + 4.0, grow=0.0)
    # top line: flat at counter_h around the heel (the clip interface), falling to 24 mm at the forefoot
    prof = [(-40, -40), (-40, ch), (28, ch), (52, ch - 5), (80, ch - 17), (115, 27), (150, 24), (320, 24),
            (320, -40)]
    top = Plane.XZ * make_face(Polyline(*[(x, z) for x, z in prof], close=True))
    top = extrude(top, amount=120, both=True)
    wall = wall & top
    wall = _fillet_try(wall, wall.edges().filter_by(lambda e: e.center().Z > 20), [1.5, 1.0, 0.6])
    shoe = sole + wall
    shoe = _fillet_try(shoe, [e for e in shoe.edges() if abs(e.center().Z) < 0.5 and e.length > 100],
                       [2.0, 1.0])
    return shoe


def _ellipse_x(x, a, b, yc, zc):
    return Plane(origin=(x, yc, zc), x_dir=(0, 1, 0), z_dir=(1, 0, 0)) * Ellipse(a, b)


def _clay_foot(y0=150.0):
    """Smooth clay left foot and lower leg standing beside the shoe (context only)."""
    zf = FLOOR_Z
    # (x, half-width, half-height, medial shift): heel, arch, ball, toes; medial side of a left foot is -Y
    secs = [(-10, 12, 14, 0), (-2, 24, 22, 0), (14, 30, 29, 0), (40, 32, 35, -1), (75, 35, 33, -2),
            (115, 40, 26, -4), (160, 46, 19, -6), (195, 47, 15, -7), (228, 43, 11, -9), (252, 33, 8, -11),
            (265, 15, 5, -12)]
    foot = loft([_ellipse_x(x, a, b, y0 + yc, zf + b) for x, a, b, yc in secs])
    # (z, x centre, half-length in X, half-width in Y): ankle to lower calf
    leg_secs = [(zf + 30, 44, 38, 31), (zf + 75, 42, 33, 28), (zf + 125, 43, 36, 32)]
    leg = loft([Plane(origin=(xc, y0, z)) * Ellipse(a, b) for z, xc, a, b in leg_secs])
    leg = _fillet_try(leg, _top_edges(leg), [10.0, 6.0, 3.0])
    try:
        out = foot + leg
        if out.is_valid:
            return out
    except Exception:
        pass
    return Compound(children=[foot, leg])


# ---------------------------------------------------------------- parts
def product_parts(P=PARAMS):
    m = build_parts(P)
    p = m["_p"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    zc, cov = p["z_cover"], p["cover_t"]
    stack = p["stack"]
    lift = lambda s: _lift(s, stack)     # noqa: E731
    T = p["tail_t"]

    # ---- insole stack: the model's own layers, dressed
    cover = m["cover"]
    perf = None
    for i, x in enumerate(range(196, 262, 6)):
        for j in range(-6, 7):
            y = 4.0 * j + (2.0 if i % 2 else 0.0)
            px = Pos(x, y, zc + cov - 0.3) * Cylinder(0.6, 0.8)
            perf = px if perf is None else perf + px
    inside = _smooth_slab(p, zc, cov + 1, grow=-4.0)
    cover = cover - (perf & inside)
    add("Top cover (PU foam, textile face)", lift(cover), C_COVER, "fabric", 1, "shell", (0, 0, 70))
    rings = None
    for (x, y) in p["fsr_xy"]:
        r = Pos(x, y, zc + cov + 0.05) * (Cylinder(p["fsr_d"] / 2 + 1.2, 0.1) - Cylinder(p["fsr_d"] / 2 + 0.2, 0.2))
        rings = r if rings is None else rings + r
    add("Printed sensor-site rings", lift(rings), C_ACCENT, "painted", 1, "shell", (0, 0, 70))
    add("Spacer foam (closed-cell PE)", lift(m["spacer"]), C_SPACER, "rubber", 3, "internal", (0, 0, 52))

    zs = p["z_spacer"]
    fsr_active = None
    for (x, y) in p["fsr_xy"]:
        a = Pos(x, y, zs + p["fsr_t"] - 0.03) * Cylinder(p["fsr_active_d"] / 2, 0.06)
        fsr_active = a if fsr_active is None else fsr_active + a
    add("Force-sensing resistors (5)", lift(m["fsrs"] - fsr_active), C_FSR_FILM, "plastic", 2, "internal", (0, 0, 38))
    add("FSR active areas", lift(fsr_active), C_FSR_ACTIVE, "painted", 2, "internal", (0, 0, 38))

    add("Carrier film (polyimide)", lift(m["film"]), C_FILM, "plastic", 3, "internal", (0, 0, 22))
    add("Copper tape traces and crossover", lift(m["traces"] + m["bridge"]), C_COPPER, "metal", 3, "internal", (0, 0, 22))
    add("Crossover patch (polyimide tape)", lift(m["patch"]), "#E3B35A", "plastic", 3, "internal", (0, 0, 22))

    motor = _fillet_try(m["motor"], _top_edges(m["motor"]), [0.5, 0.3])
    add("Coin vibration motor", lift(motor + m["leads"]), C_METAL, "metal", 5, "internal", (0, 0, 11))
    foam = _fillet_try(m["foam"], _bottom_edges(m["foam"]), [0.8, 0.5])
    add("Insole base (EVA foam)", lift(foam), C_EVA, "rubber", 6, "shell", (0, 0, 0))

    # flex tail: the part bonded on the insole lifts with it, the run up the counter stays put
    tail = m["tail"]
    on_insole = tail & Pos(60, 0, 0) * Box(118, 80, 2 * (zs + T + 0.05))
    run = tail - Pos(60, 0, 0) * Box(118, 80, 2 * (zs + T + 0.05))
    add("Flat flex tail", lift(on_insole) + run, C_TAIL, "plastic", 4, "internal", (0, 0, 22))

    # ---- heel pod: the model's rounded base and lid, dressed
    x0, x1, xl = p["pod_x0"], p["pod_x1"], p["x_lid_in"]
    zt, zb, hy = p["pod_top"], p["pod_bot"], p["pod_y"] / 2
    base = m["base"]
    for k in range(7):                                         # ribbed side grips, 0.4 mm deep
        z = zb + 10.0 + 3.2 * k
        for s in (-1, 1):
            base = base - Pos((xl + x1) / 2 + 0.5, s * hy, z) * Box(x1 - xl - 4.0, 0.8, 1.2)
    add("Heel pod base with clip (PETG)", base, C_POD, "plastic", 7, "shell", (-35, 0, 30))
    lid = m["lid"]
    lid = lid - _x_cyl(p["button_d"] / 2 + 2.2, 0.5, x0 - 0.1, 0, p["z_button"])      # bezel recess round the button
    # no 0.3 to 0.5 mm fillet on the lid face: its tessellation left vertices closer than the renderer's
    # merge distance, which broke the face shading (dark streaks); the render bevel rounds the edge instead
    # countersinks filled and the M2 screws drawn as flush heads (0.15 mm proud): the 1 mm countersink cones
    # are too small for the renderer's edge bevel, which broke the lid face shading into dark streaks
    heads = None
    for (by, bz) in p["bosses"]:
        lid = lid + _x_cyl(p["csk_d"] / 2 + 0.05, p["lid_t"], x0, by, bz)
        h_ = _x_cyl(p["csk_d"] / 2 - 0.05, 0.25, x0 - 0.15, by, bz)
        heads = h_ if heads is None else heads + h_
    add("Heel pod lid (PETG)", lid, C_LID, "plastic", 11, "shell", (-110, 0, 30))
    add("M2 lid screws (4)", heads, C_METAL, "metal", 12, "shell", (-128, 0, 30))
    add("Pause button cap", m["cap"], C_ACCENT, "plastic", 10, "shell", (-96, 0, 30))
    myy = p["module"][1]
    led = _x_cyl(p["led_d"] / 2 - 0.1, p["lid_t"] + 0.2, x0 - 0.1, -myy / 4, p["z_led"])
    add("Status LED light pipe (lit)", led, C_LED, "emissive", 9, "shell", (-110, 0, 30))
    mark = None                                                # cadence mark: three bars, lengths rising
    for k, ln in enumerate((3.0, 5.0, 7.0)):
        b = Pos(x0 - 0.1, 6.0 + 2.0 * k, p["z_led"] - ln / 2 + 3.5) * Box(0.2, 1.0, ln)
        mark = b if mark is None else mark + b
    add("Lid cadence mark", mark, C_ACCENT, "painted", 11, "shell", (-110, 0, 30))

    # ---- pod internals: the model's envelopes, dressed
    cell = _fillet_try(m["cell"], m["cell"].edges().filter_by(Axis.X), [1.5, 1.0])
    add("LiPo cell, 400 mAh", cell, C_POUCH, "metal", 8, "internal", (-52, 0, 30))
    cx0 = p["x_cell"][0]
    label = Pos(cx0 - 0.05, 0, sum(p["z_cell"]) / 2) * Box(0.1, p["cell"][1] - 5.0, p["cell"][2] - 9.0)
    add("LiPo cell label", label, C_LABEL, "painted", 8, "internal", (-52, 0, 30))
    add("Controller module (nRF52840 with IMU, USB-C down)", m["module"], C_PCB, "plastic", 9, "internal", (-68, 0, 30))
    add("Interface board (perfboard)", m["iface"], C_PERF, "plastic", 10, "internal", (-82, 0, 30))
    add("Tail connector (8-way ZIF)", m["zif"], C_DARK, "plastic", 13, "internal", (-82, 0, 30))

    # ---- context: clay shoe and clay foot and lower leg (renders only, decision 10)
    add("Shoe shell (clay)", _clay_shoe(p), C_CLAY, "clay", None, "context", (0, 0, 0))
    add("Foot and lower leg (clay)", _clay_foot(), C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:50s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:7.2f} cm3")
