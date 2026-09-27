"""StepCue product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: smooth insole outline with a light textile top
cover (printed sensor-site rings and forefoot perforations), amber sensor laminate with copper
traces, FSRs with visible active areas, coin motor, flat flex tail, and a filleted two-part heel
pod with a parting line, ribbed side grips, teal pause button, lit status LED, USB-C port and lid
screws. Context: a smooth clay shoe shell (sole and heel counter) with the insole lifted a few
degrees at the toe, and a clay foot and lower leg standing beside it for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
Research and educational prototype, not a medical device.

Every main dimension and interface comes from PARAMS and derived() in model.py.
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

from build123d import (Axis, Box, Compound, Cylinder, Edge, Ellipse, Face, Plane, Polyline, Pos,
                       Rot, SlotOverall, Solid, Vector, Wire, extrude, fillet, loft, make_face)
from model import PARAMS, derived, build_parts, outline

TITLE = "StepCue: pressure-sensing insole with a clip-on heel cue pod"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -140,
     "note": "Product render from the front left and above (about 30 deg elevation), looking along the insole "
             "from the heel: heel pod clipped over the clay shoe's heel counter in the foreground, insole lifted "
             "at the toe, clay foot and lower leg behind"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -135,
     "note": "Exploded view from the front left and above (about 28 deg elevation): textile top cover, "
             "force-sensing resistors, sensor laminate with copper traces, coin motor, EVA base and flex "
             "tail; heel pod lid, button, interface board, controller module, LiPo cell and pod base in the foreground"},
]

# Colours (restrained product palette; accent from the kit)
C_ACCENT = "#0F766E"
C_COVER = "#D9DBD6"        # light textile top cover
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
LIFT_DEG = 8.0             # insole tilted up at the toe about the top of the heel (hero pose)
FLOOR_Z = -22.0            # underside of the clay shoe sole
POD_R = 5.0                # pod corner radius in the YZ plane
GROOVE = 0.5               # parting-line groove width and depth


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
    """Insole outline from model.outline(), as a smooth periodic spline, extruded from z0 by t."""
    pts = [Vector(x, y, 0) for x, y in outline(p, grow)]
    face = Face(Wire([Edge.make_spline(pts, periodic=True)]))
    return Pos(0, 0, z0) * extrude(face, amount=t)


def _x_cyl(r, length, x0, y, z):
    """Cylinder along +X starting at x0."""
    return Pos(x0 + length / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, length)


def _polyline_strip(pts, w, t, z0):
    """Flat strip of width w and thickness t along the XY polyline pts, bottom at z0."""
    out = None
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        a = math.degrees(math.atan2(y1 - y0, x1 - x0))
        seg = Pos((x0 + x1) / 2, (y0 + y1) / 2, z0 + t / 2) * Rot(0, 0, a) * Box(L, w, t)
        out = seg if out is None else out + seg
    for (x, y) in pts[1:-1]:
        out += Pos(x, y, z0 + t / 2) * Cylinder(w / 2, t)
    return out


def _lift(shape, pivot_z):
    """Hero pose: tilt the insole toe-up by LIFT_DEG about the top edge of the heel (x = 0)."""
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


# ---------------------------------------------------------------- heel pod
def _pod(p, m):
    """Two-part pod body: graphite base with clip and light lid, split at the model's lid plane."""
    x0, x1, zt, zb = p["pod_x0"], p["pod_x1"], p["pod_top"], p["pod_bot"]
    xl = x0 + p["lid_t"]
    zc = (zt + zb) / 2
    env = Pos((x0 + x1) / 2, 0, zc) * Box(x1 - x0, p["pod_y"], p["pod_z"])
    env = _fillet_try(env, env.edges().filter_by(Axis.X), [POD_R, 4.0, 3.0])
    env = _fillet_try(env, env.faces().sort_by(Axis.X)[0].edges(), [2.0, 1.5, 1.0])      # outer lid face
    env = _fillet_try(env, env.faces().sort_by(Axis.X)[-1].edges(), [0.8, 0.5])          # shoe-side face
    split = Pos(xl - 50, 0, zc) * Box(100, 100, 100)
    lid = env & split
    base = env - split
    # parting-line groove on the base rim
    ring = Pos(xl + GROOVE / 2, 0, zc) * Box(GROOVE, p["pod_y"] + 2, p["pod_z"] + 2)
    ring -= Pos(xl + GROOVE / 2, 0, zc) * Box(GROOVE + 1, p["pod_y"] - 2 * GROOVE, p["pod_z"] - 2 * GROOVE)
    base -= ring
    # cavity, tail slot and USB-C opening exactly as model.py
    base -= Pos((xl + x1 - p["wall"]) / 2 - 0.05, 0, zc) * Box(x1 - xl - p["wall"] + 0.1, p["cav_y"], p["cav_z"])
    T, W = p["tail_t"], p["tail_w"]
    base -= Pos(x1 - p["wall"] / 2, 0, p["counter_h"] + T / 2) * Box(p["wall"] + 0.2, W + 1.0, 1.0)
    lx = m["_p"]["module_c"][0]
    ux, uy = p["usb_slot"]
    base -= Pos(lx, 0, zt - p["wall"] / 2) * Rot(0, 0, 90) * extrude(SlotOverall(uy, ux), amount=p["wall"] + 0.4,
                                                                    both=True)
    # ribbed side grips (shallow grooves) for one-handed fitting
    for k in range(7):
        z = zb + 10.0 + 3.2 * k
        for s in (-1, 1):
            base -= Pos((xl + x1) / 2 + 0.6, s * p["pod_y"] / 2, z) * Box(x1 - xl - 5.0, 0.9, 1.2)
    # clip: bridge over the counter top and finger inside the counter, as model.py, filleted
    bx0, bx1 = x1, p["finger_x0"] + p["finger_t"]
    bridge = Pos((bx0 + bx1) / 2 - 0.5, 0, p["tail_top"] + p["bridge_t"] / 2) * Box(bx1 - bx0 + 1.0, p["bridge_w"],
                                                                                   p["bridge_t"])
    finger = Pos(p["finger_x0"] + p["finger_t"] / 2, 0, p["tail_top"] - p["finger_l"] / 2) * Box(
        p["finger_t"], p["bridge_w"], p["finger_l"])
    clip = bridge + finger
    clip = _fillet_try(clip, clip.edges().filter_by(Axis.Y), [0.6, 0.4])
    clip = _fillet_try(clip, clip.edges().filter_by(Axis.Y, reverse=True), [0.5, 0.3])
    base = base + clip

    # lid: pause button and LED windows exactly as model.py, bezel recess, screw countersinks
    iz = m["_p"]["iface_c"][2]
    mz = m["_p"]["module_c"][2]
    myy = p["module"][1]
    lid -= _x_cyl(p["button_d"] / 2, p["lid_t"] + 2, x0 - 1, 0, iz)
    lid -= _x_cyl(p["button_d"] / 2 + 2.2, 0.5, x0 - 0.1, 0, iz)          # shallow bezel ring recess
    lid -= _x_cyl(p["led_d"] / 2, p["lid_t"] + 2, x0 - 1, -myy / 4, mz)
    screws = [(s * 12.0, zc + t * 16.0) for s in (-1, 1) for t in (-1, 1)]
    for (y, z) in screws:
        lid -= _x_cyl(1.9, 0.9, x0 - 0.1, y, z)
        lid -= _x_cyl(1.1, p["lid_t"] + 2, x0 - 1, y, z)
    return base, lid, screws


# ---------------------------------------------------------------- parts
def product_parts(P=PARAMS):
    p = derived(P)
    m = build_parts(P)
    q = m["_p"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    f, lam, cov = p["foam_t"], p["lam_t"], p["cover_t"]
    z_lam = f + lam
    stack = p["stack"]
    lift = lambda s: _lift(s, stack)     # noqa: E731
    mx, my = p["motor_xy"]
    T, W = p["tail_t"], p["tail_w"]

    # ---- insole stack (smooth outline from the same points as model.py)
    cover = _smooth_slab(p, z_lam, cov)
    cover = _fillet_try(cover, _top_edges(cover), [0.6, 0.4, 0.2])
    perf = None
    for i, x in enumerate(range(196, 262, 6)):
        for j in range(-6, 7):
            y = 4.0 * j + (2.0 if i % 2 else 0.0)
            px = Pos(x, y, z_lam + cov - 0.3) * Cylinder(0.6, 0.8)
            perf = px if perf is None else perf + px
    inside = _smooth_slab(p, z_lam, cov + 1, grow=-4.0)
    cover -= perf & inside
    add("Top cover (PU foam, textile face)", lift(cover), C_COVER, "fabric", 1, "shell", (0, 0, 62))
    rings = None
    for (x, y) in p["fsr_xy"]:
        r = Pos(x, y, z_lam + cov + 0.05) * (Cylinder(p["fsr_d"] / 2 + 1.2, 0.1) - Cylinder(p["fsr_d"] / 2 + 0.2, 0.2))
        rings = r if rings is None else rings + r
    add("Printed sensor-site rings", lift(rings), C_ACCENT, "painted", 1, "shell", (0, 0, 62))

    fsr_film, fsr_active = None, None
    for (x, y) in p["fsr_xy"]:
        d = Pos(x, y, z_lam - p["fsr_t"] / 2) * Cylinder(p["fsr_d"] / 2, p["fsr_t"])
        a = Pos(x, y, z_lam - 0.03) * Cylinder(p["fsr_active_d"] / 2, 0.06)
        fsr_film = (d - a) if fsr_film is None else fsr_film + (d - a)
        fsr_active = a if fsr_active is None else fsr_active + a
    add("Force-sensing resistors (5)", lift(fsr_film), C_FSR_FILM, "plastic", 2, "internal", (0, 0, 42))
    add("FSR active areas", lift(fsr_active), C_FSR_ACTIVE, "painted", 2, "internal", (0, 0, 42))

    # copper traces from each sensor site to the tail pad at the heel (indicative routing)
    routes = [
        [(34 - p["fsr_d"] / 2, 0), (8, 0)],
        [(110 - 8.0, -24 + 3.0), (70, -14), (46, -14), (16, -14), (8, -4.5)],
        [(178 - 7.0, -30 + 5.5), (140, -11), (46, -11), (16, -11), (8, -2.5)],
        [(185 - 7.5, 28 - 5.0), (150, 10), (60, 10), (46, 14), (16, 14), (8, 4.5)],
        [(246 - 7.5, 24 - 5.0), (200, 6.5), (60, 6.5), (46, 11), (16, 11), (8, 2.5)],
    ]
    traces = None
    for r in routes:
        s = _polyline_strip(r, 1.2, 0.06, z_lam - 0.06)
        traces = s if traces is None else traces + s
    fsr_all = None
    for (x, y) in p["fsr_xy"]:
        d = Pos(x, y, z_lam - 0.5) * Cylinder(p["fsr_d"] / 2, 2.0)
        fsr_all = d if fsr_all is None else fsr_all + d
    traces -= fsr_all
    lamin = _smooth_slab(p, f, lam) - fsr_all
    lamin -= Pos(4.0, 0, z_lam - T / 2) * Box(8.0, W, T)                       # tail pad, as model.py
    rel = p["motor_relief"]
    if rel > 0:
        lamin -= Pos(mx, my, f + rel / 2 - 0.05) * Cylinder(p["motor_d"] / 2 + p["pocket_clear"], rel + 0.1)
    lamin -= traces
    add("Sensor laminate (polyimide film)", lift(lamin), C_FILM, "plastic", 3, "internal", (0, 0, 22))
    add("Copper tape traces", lift(traces), C_COPPER, "metal", 3, "internal", (0, 0, 22))

    # coin motor, a flat can with a slight chamfer and leads
    motor = Pos(mx, my, p["pocket_floor"] + p["motor_t"] / 2) * Cylinder(p["motor_d"] / 2, p["motor_t"])
    motor = _fillet_try(motor, _top_edges(motor), [0.5, 0.3])
    add("Coin vibration motor", lift(motor), C_METAL, "metal", 5, "internal", (0, 0, 11))

    pocket_h = f - p["pocket_floor"]
    foam = _smooth_slab(p, 0, f) - Pos(mx, my, p["pocket_floor"] + pocket_h / 2 + 0.05) * Cylinder(
        p["motor_d"] / 2 + p["pocket_clear"], pocket_h + 0.1)
    foam = _fillet_try(foam, _bottom_edges(foam), [0.8, 0.5])
    add("Insole base (EVA foam)", lift(foam), C_EVA, "rubber", 6, "shell", (0, 0, 0))

    # flat flex tail: bonded pad lifts with the insole, the run up the counter stays put
    pad = lift(Pos(4.0, 0, z_lam - T / 2) * Box(8.0, W, T))
    z_up0 = z_lam - T
    run = (Pos(T / 2, 0, (z_up0 + p["counter_h"] + T) / 2) * Box(T, W, p["counter_h"] - z_up0 + T)
           + Pos((T - p["counter_t"] - p["wall"]) / 2, 0, p["counter_h"] + T / 2)
           * Box(p["counter_t"] + p["wall"] + T, W, T))
    add("Flat flex tail", pad + run, C_TAIL, "plastic", 4, "internal", (0, 0, 22))
    conn = Pos(p["pod_x1"] - p["wall"] - 1.5, 0, p["counter_h"] - 0.5) * Box(3.0, W + 4.0, 2.4)
    add("Tail connector", conn, C_DARK, "plastic", 4, "internal", (-35, 0, 48))

    # ---- heel pod
    base, lid, screws = _pod(p, m)
    add("Heel pod base with clip (PETG)", base, C_POD, "plastic", 7, "shell", (-35, 0, 30))
    add("Heel pod lid (PETG)", lid, C_LID, "plastic", 11, "shell", (-110, 0, 30))
    x0 = p["pod_x0"]
    heads = None
    for (y, z) in screws:
        h = _x_cyl(1.8, 0.8, x0 - 0.05, y, z)
        h -= Pos(x0 - 0.1, y, z) * Box(0.6, 2.2, 0.5) + Pos(x0 - 0.1, y, z) * Box(0.6, 0.5, 2.2)
        h += _x_cyl(0.9, 6.0, x0 + 0.7, y, z)
        heads = h if heads is None else heads + h
    add("M2 lid screws (4)", heads, C_METAL, "metal", 12, "shell", (-128, 0, 30))

    iz = q["iface_c"][2]
    mz = q["module_c"][2]
    myy = p["module"][1]
    btn = _x_cyl(p["button_d"] / 2 - 0.4, p["lid_t"] + 1.2, x0 - 1.0, 0, iz)
    btn = _fillet_try(btn, btn.faces().sort_by(Axis.X)[0].edges(), [0.8, 0.5])
    btn += _x_cyl(p["button_d"] / 2 + 0.6, 0.6, x0 + p["lid_t"], 0, iz)       # retaining flange inside
    add("Pause button cap", btn, C_ACCENT, "plastic", 10, "shell", (-96, 0, 30))
    led = _x_cyl(p["led_d"] / 2 - 0.1, p["lid_t"] + 0.2, x0 - 0.1, -myy / 4, mz)
    add("Status LED light pipe (lit)", led, C_LED, "emissive", 9, "shell", (-110, 0, 30))
    # small raised cadence mark on the lid: three bars, lengths rising
    mark = None
    for k, ln in enumerate((3.0, 5.0, 7.0)):
        b = Pos(x0 - 0.1, 6.0 + 2.0 * k, mz - ln / 2 + 3.5) * Box(0.2, 1.0, ln)
        mark = b if mark is None else mark + b
    add("Lid cadence mark", mark, C_ACCENT, "painted", 11, "shell", (-110, 0, 30))

    # ---- pod internals (envelopes from model.py, dressed)
    cxx, cyy, czz = p["cell"]
    cx, _, cz = q["cell_c"]
    cell = Pos(cx, 0, cz) * Box(cxx, cyy, czz)
    cell = _fillet_try(cell, cell.edges().filter_by(Axis.X), [1.5, 1.0])
    cell = _fillet_try(cell, cell.edges(), [0.6, 0.3])
    add("LiPo cell, 400 mAh", cell, C_POUCH, "metal", 8, "internal", (-52, 0, 30))
    label = Pos(cx - cxx / 2 - 0.05, 0, cz) * Box(0.1, cyy - 5.0, czz - 9.0)
    add("LiPo cell label", label, C_LABEL, "painted", 8, "internal", (-52, 0, 30))

    mxx, myy_, mzz = p["module"]
    lx = q["module_c"][0]
    pcb_t = 1.0
    pcb = Pos(lx + mxx / 2 - pcb_t / 2, 0, mz) * Box(pcb_t, myy_, mzz)
    pcb = _fillet_try(pcb, pcb.edges().filter_by(Axis.X), [1.0, 0.6])
    add("Controller module PCB (nRF52840 with IMU)", pcb, C_PCB, "plastic", 9, "internal", (-68, 0, 30))
    shield = Pos(lx + mxx / 2 - pcb_t - 0.75, 0, mz - 2.5) * Box(1.5, 12.0, 11.0)
    usb = Pos(lx + mxx / 2 - pcb_t - 1.6, 0, mz + mzz / 2 - 3.6) * Box(3.2, 9.0, 7.2)
    usb = _fillet_try(usb, usb.edges().filter_by(Axis.Z), [1.4, 1.0])
    add("Controller shield can and USB-C", shield + usb, C_METAL, "metal", 9, "internal", (-68, 0, 30))

    ixx, iyy, izz = p["iface"]
    ix = q["iface_c"][0]
    perfb = Pos(ix + ixx / 2 - 0.8, 0, iz) * Box(1.6, iyy, izz)
    add("Interface board (perfboard)", perfb, C_PERF, "plastic", 10, "internal", (-82, 0, 30))
    sw = Pos(ix - 0.5, 0, iz) * Box(3.4, 12.0, 11.5)
    sw = _fillet_try(sw, sw.edges().filter_by(Axis.X), [0.8, 0.5])
    parts = sw + Pos(ix + ixx / 2 - 2.2, 7.5, iz + 3.0) * Box(1.2, 3.0, 1.6)
    parts += Pos(ix + ixx / 2 - 2.2, -7.5, iz + 3.0) * Box(1.2, 3.0, 1.6)
    add("Tact switch and MOSFETs", parts, C_DARK, "plastic", 10, "internal", (-82, 0, 30))

    # ---- context: clay shoe and clay foot and lower leg
    add("Shoe shell (clay)", _clay_shoe(p), C_CLAY, "clay", None, "context", (0, 0, 0))
    add("Foot and lower leg (clay)", _clay_foot(), C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:7.2f} cm3")
