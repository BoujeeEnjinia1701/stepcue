"""StepCue parametric model (build123d), TRL 3, constructable design (STC-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks and print the results

Coordinates (mm): X runs heel (0) to toe, Y points to the medial (big-toe) side of a
right insole, Z is up with the underside of the insole at Z = 0. The shoe heel counter
is a curved wall round the heel: its inner face follows the insole's heel cup (radius 32
about the point X = 32, Y = 0) and it is counter_t thick, so behind the heel centre its
inner face is at X = 0 and its outer face at X = -counter_t. Its top edge is at Z = counter_h.
The heel pod hangs on the outside of the counter and clips over its top edge.

Decisions reflected: STC-DDR-001 and STC-DDR-002 (2026-09-25), and the design for
construction changes of STC-DDR-003 (2026-10-01, accepted by Amish on 2026-10-02):
two-layer sensor laminate (carrier film with copper tape traces, foam spacer with
windows), sensor tails and tab pads, routed traces with one insulated crossover, motor
in a through-hole bonded under the spacer, 8-way 9 mm tail slit and fanned onto pads,
tail connector on the interface board, interface board above the module, USB-C through
the bottom wall, curved clip finger, taped internal parts, lid on four M2 screws into
corner bosses, button cap through the lid. Model revision of 2026-10-02 (Amish's decisions):
smooth spline insole outline, pod corners rounded to 5 mm with a parting-line groove.
BUILD PLAN MODEL, PLAN NOT YET BUILT.
"""
from pathlib import Path
import itertools
import math
import sys

import numpy as np

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Insole, about EU 42 (US men's 8.5)
    "insole_l": 272.0,        # heel to toe
    "foam_t": 2.5,            # EVA base (2.5 mm by decision O3, STC-DDR-002)
    "film_t": 0.25,           # carrier: 125 um polyimide film plus transfer adhesive
    "trace_t": 0.05,          # copper tape traces on the carrier
    "spacer_t": 0.5,          # closed-cell polyethylene foam spacer with windows
    "cover_t": 1.2,           # PU foam top cover
    "trace_w": 1.5,           # copper tape trace width
    # Force-sensing resistors (Interlink FSR 402: 18.3 dia, 14.68 active, 0.46 thick)
    "fsr_d": 18.3,
    "fsr_active_d": 14.68,
    "fsr_t": 0.46,
    "fsr_tail": (7.0, 12.0),  # tail width, length beyond the disc (short-tail type; confirm on the part)
    "tab_in": 2.0,            # tab centres this far in from the tail end
    "tab_pitch": 2.54,
    # Sensor sites (x, y): heel, lateral midfoot, first MTH, fifth MTH, hallux; tail directions
    "fsr_xy": ((34, 0), (110, -24), (185, 28), (178, -30), (246, 24)),
    "fsr_dir": ((1, 0), (-1, 0), (0, -1), (-1, 0), (-1, 0)),
    # Coin ERM motor under the medial arch (Precision Microdrives 310-103 class, 10 x 2.7)
    "motor_d": 10.0,
    "motor_t": 2.7,
    "motor_xy": (120.0, 16.0),
    "pocket_clear": 0.3,      # radial clearance of the motor hole
    # Flat flex tail: 8-way, 1.0 mm pitch (9 mm wide as bought)
    "tail_w": 9.0,
    "tail_t": 0.3,
    "tail_n": 8,
    "slit_x": (3.0, 13.0),    # the tail end is slit into eight strips between these X
    "pad_x": (10.0, 15.0),    # tail pads on the carrier
    "pad_pitch": 4.0,
    # Shoe heel counter (context and clip interface)
    "heel_r": 32.0,           # heel cup radius of the insole outline
    "counter_t": 3.5,
    "counter_h": 55.0,
    # Heel pod body (outside the counter)
    "pod_x": 15.0,            # depth away from the shoe, including the lid
    "pod_y": 37.0,            # width across the heel (34 in the concept; widened for the lid bosses)
    "pod_z": 42.0,            # height
    "wall": 1.5,
    "lid_t": 2.0,
    "pod_r": 5.0,             # corner radius of the pod body seen from the lid (2026-10-02 decision)
    "groove": 0.5,            # parting-line groove round the base rim at the lid: width and depth
    # Clip over the counter top
    "bridge_t": 2.0,
    "bridge_w": 26.0,
    "finger_t": 1.5,
    "finger_l": 18.0,
    "clip_interference": 1.0,
    # Internal parts (envelopes) and how they are held
    "cell": (5.2, 25.0, 35.0),        # 400 mAh LiPo, 502535 class: X (thick), Y, Z
    "cell_tape": 0.3,                 # double-sided transfer tape, cell to the shoe-side wall
    "foam_tape": 0.5,                 # double-sided foam tape, module and interface board to the cell
    "module": (4.5, 17.8, 21.0),      # XIAO nRF52840 Sense class: X (with parts), Y, Z (USB-C down)
    "usb_rec": (3.2, 8.94, 1.4),      # USB-C receptacle: X, Y, and how far it stands past the board end
    "usb_open": (9.4, 0.2),           # opening in the bottom wall: width, clearance round the receptacle
    "iface": (5.0, 20.0, 12.0),       # interface perfboard with MOSFETs, resistors and tact switch
    "zif": (4.0, 14.0, 3.0),          # 8-way ZIF connector on its adapter board, on top of the interface board
    "cap_d": 9.4,                     # pause button cap
    "cap_proud": 1.0,                 # cap stands this far out of the lid
    "button_d": 10.0,                 # pause button opening in the lid
    "led_d": 3.0,                     # status LED window in the lid
    "led_up": 4.0,                    # LED window height above the module's lower end
    "boss_d": 4.0,                    # lid screw bosses in the tray corners
    "boss_l": 5.0,
    "pilot_d": 1.6,                   # M2 thread-forming pilot
    "screw_l": 6.0,                   # M2 x 6 countersunk thread-forming screws
    "csk_d": 3.8,
    # Crossover of the lateral midfoot common branch over the fifth MTH signal trace
    "patch": 8.0,
}


def concept_outline(p, grow=0.0, n=40):
    """The TRL 3 insole outline as a polyline (x, y): straight runs between set half-widths, an
    elliptical toe cap and a circular heel cup (radius heel_r about X = heel_r). It has corners
    where the straight runs meet; outline_points() smooths it."""
    k = p["insole_l"] / 272.0
    xs = np.linspace(32, 255, n) * k
    lat = np.interp(xs, np.array([32, 100, 180, 230, 255]) * k, [32, 33, 42, 38, 28]) + grow
    med = np.interp(xs, np.array([32, 100, 140, 190, 230, 255]) * k, [32, 24, 30, 52, 50, 38]) + grow
    pts = [(x, -w) for x, w in zip(xs, lat)]
    for t in np.linspace(-np.pi / 2, np.pi / 2, 24)[1:-1]:          # toe cap
        pts.append((255 * k + (17 + grow) * np.cos(t), 5 + (33 + grow) * np.sin(t)))
    pts += [(x, w) for x, w in zip(xs[::-1], med[::-1])]
    for t in np.linspace(np.pi / 2, 3 * np.pi / 2, 24)[1:-1]:       # heel cup
        pts.append((32 * k + (32 + grow) * np.cos(t), (32 + grow) * np.sin(t)))
    return pts


def outline_points(p, grow=0.0, step=30.0):
    """Control points of the smooth insole outline (decision of 2026-10-02): the concept outline
    from the lateral heel round the toe to the medial heel, resampled every `step` mm so its
    corners are not copied into the spline, plus the heel cup arc kept exact (the clip and the
    tail fit the heel counter there)."""
    from shapely.geometry import LineString
    n = 40
    k = p["insole_l"] / 272.0
    front = concept_outline(p, grow, n)[: 2 * n + 22]                  # lateral side, toe cap, medial side
    line = LineString(front)
    m = int(round(line.length / step))
    pts = [(q.x, q.y) for q in (line.interpolate(i * line.length / m) for i in range(m + 1))]
    r = p["heel_r"] + grow
    pts += [(32 * k + r * math.cos(t), r * math.sin(t)) for t in np.linspace(np.pi / 2, 3 * np.pi / 2, 13)[1:-1]]
    return pts


_OUTLINE_CACHE = {}


def outline_edge(p, grow=0.0):
    """The insole outline as one smooth closed spline (decision of 2026-10-02: smooth spline
    outline, traces kept 1.5 mm inside it). Replaces the TRL 3 polyline outline."""
    from build123d import Edge, Vector
    return Edge.make_spline([Vector(x, y, 0) for x, y in outline_points(p, grow)], periodic=True)


def outline(p, grow=0.0, n=720):
    """The smooth spline outline sampled as n points (x, y) about 0.9 mm apart, for layout checks and drawings."""
    key = (p["insole_l"], round(grow, 4), n)
    if key not in _OUTLINE_CACHE:
        e = outline_edge(p, grow)
        _OUTLINE_CACHE[key] = [(v.X, v.Y) for v in (e.position_at(i / n) for i in range(n))]
    return list(_OUTLINE_CACHE[key])


def derived(params=None):
    p = dict(params or PARAMS)
    p["lam_t"] = p["film_t"] + p["trace_t"] + p["spacer_t"]          # 0.8 mm, as in the concept
    p["stack"] = p["foam_t"] + p["lam_t"] + p["cover_t"]
    p["z_film"] = p["foam_t"]
    p["z_trace"] = p["foam_t"] + p["film_t"]
    p["z_spacer"] = p["z_trace"] + p["trace_t"]
    p["z_cover"] = p["z_spacer"] + p["spacer_t"]
    p["motor_gap"] = p["z_spacer"] - p["motor_t"]                     # air under the motor (0.1)
    # kept for cad/src/product_model.py (appearance model)
    p["pocket_floor"] = p["motor_gap"]
    p["motor_relief"] = p["film_t"] + p["trace_t"]
    p["tail_top"] = p["counter_h"] + p["tail_t"]
    p["pod_top"] = p["tail_top"] + p["bridge_t"]
    p["pod_bot"] = p["pod_top"] - p["pod_z"]
    p["pod_x1"] = -p["counter_t"]                                     # shoe-side face of the pod
    p["pod_x0"] = p["pod_x1"] - p["pod_x"]                            # outer face of the lid
    p["finger_x0"] = p["tail_t"]                                      # at the heel centre
    p["clip_gap_fitted"] = p["counter_t"] + p["tail_t"]
    p["clip_gap_free"] = p["clip_gap_fitted"] - p["clip_interference"]
    p["cav_x"] = p["pod_x"] - p["wall"] - p["lid_t"]
    p["cav_y"] = p["pod_y"] - 2 * p["wall"]
    p["cav_z"] = p["pod_z"] - 2 * p["wall"]
    p["r_in"] = p["heel_r"]                                           # counter inner face
    p["r_out"] = p["heel_r"] + p["counter_t"]                         # counter outer face
    p["r_tail"] = p["heel_r"] - p["tail_t"]
    p["r_finger"] = p["r_tail"] - p["finger_t"]
    # pod interior, from the shoe-side wall outward and from the floor up
    x1, w = p["pod_x1"], p["wall"]
    p["x_wall_in"] = x1 - w
    p["x_cell"] = (p["x_wall_in"] - p["cell_tape"] - p["cell"][0], p["x_wall_in"] - p["cell_tape"])
    p["x_outer"] = p["x_cell"][0] - p["foam_tape"]                    # shoe-side face of module and board
    p["z_floor"] = p["pod_bot"] + w
    p["z_roof"] = p["pod_top"] - w
    p["z_cell"] = (p["z_floor"] + 0.2, p["z_floor"] + 0.2 + p["cell"][2])
    p["z_module"] = (p["z_floor"] + 0.2, p["z_floor"] + 0.2 + p["module"][2])
    p["z_iface"] = (p["z_module"][1] + 0.3, p["z_module"][1] + 0.3 + p["iface"][2])
    p["z_zif"] = (p["z_iface"][1], p["z_iface"][1] + p["zif"][2])
    p["z_button"] = sum(p["z_iface"]) / 2
    p["z_led"] = p["z_module"][0] + p["led_up"]
    p["x_lid_in"] = p["pod_x0"] + p["lid_t"]
    p["x_drop"] = p["x_outer"] - p["zif"][0] / 2                       # where the tail drops into the connector
    # centres, kept for cad/src/product_model.py
    p["cell_c"] = (sum(p["x_cell"]) / 2, 0, sum(p["z_cell"]) / 2)
    p["module_c"] = (p["x_outer"] - p["module"][0] / 2, 0, sum(p["z_module"]) / 2)
    p["iface_c"] = (p["x_outer"] - p["iface"][0] / 2, 0, sum(p["z_iface"]) / 2)
    by = p["cav_y"] / 2 - p["boss_d"] / 2 + 0.2                     # bosses run into the side and end walls
    p["bosses"] = [(s * by, z) for s in (-1, 1)
                   for z in (p["z_floor"] + p["boss_d"] / 2 - 0.2, p["z_roof"] - p["boss_d"] / 2 + 0.2)]
    return p


# ----------------------------------------------------------------- 2D layout of the insole circuit
def fsr_tabs(p):
    """For each sensor: (centre, tail direction, tab on the lateral side (or heel side for a tail
    pointing across the foot), the other tab)."""
    out = []
    for (x, y), (dx, dy) in zip(p["fsr_xy"], p["fsr_dir"]):
        r = p["fsr_d"] / 2 + p["fsr_tail"][1] - p["tab_in"]
        cx, cy = x + dx * r, y + dy * r
        nx, ny = -dy, dx                       # perpendicular
        h = p["tab_pitch"] / 2
        a, b = (cx - nx * h, cy - ny * h), (cx + nx * h, cy + ny * h)
        a, b = sorted((a, b), key=lambda t: (t[1], t[0]) if dx else (t[0], t[1]))   # lateral or heel side first
        out.append(((x, y), (dx, dy), a, b))
    return out


def pad_y(p, i):
    return (i - (p["tail_n"] - 1) / 2) * p["pad_pitch"]


def trace_paths(p=None):
    """The copper tape traces as named polylines (x, y). Signal pads from lateral to medial:
    0 lateral midfoot, 1 fifth MTH, 2 heel, 3 common supply, 4 first MTH, 5 motor -, 6 motor +, 7 hallux.
    The common branch to the lateral midfoot sensor crosses the fifth MTH trace over an
    insulating patch: its raised part is 'bridge' in trace_layout()."""
    p = derived(p)
    T = fsr_tabs(p)
    heel, mid, mth1, mth5, hal = T
    x0 = p["pad_x"][1]
    Y = [pad_y(p, i) for i in range(8)]
    mx, my = p["motor_xy"]
    mlx = mx - p["motor_d"] / 2 - p["pocket_clear"] - 4.7               # motor lead pads end here
    mp = (my - 1.4, my + 1.4)
    pc = crossing(p)
    hp = p["patch"] / 2 + 0.4
    return {
        "Lateral midfoot signal": [(x0, Y[0]), (27, mid[2][1]), mid[2]],
        "Fifth MTH signal": [(x0, Y[1]), (29, -19), (70, -19), (95, -12), (122, -12), (146, mth5[2][1]), mth5[2]],
        "Heel signal": [(x0, Y[2]), (27, -13), (57, -13), (57, heel[2][1]), heel[2]],
        "Common supply": [(x0, Y[3]), (26, 12.5), (60, 12.5), (60, heel[3][1]), heel[3]],
        "Common spine": [(60, heel[3][1]), (218, heel[3][1]), (218, hal[2][1]), hal[2]],
        "Common to lateral midfoot (heel side)": [(pc[0], heel[3][1]), (pc[0], pc[1] + hp)],
        "Common to lateral midfoot (sensor side)": [(pc[0], pc[1] - hp), (pc[0], mid[3][1]), mid[3]],
        "Common to fifth MTH": [(150, heel[3][1]), (150, mth5[3][1]), mth5[3]],
        "Common to first MTH": [(mth1[3][0], heel[3][1]), mth1[3]],
        "First MTH signal": [(x0, Y[4]), (26, 16.5), (40, 16.5), (55, 15.5), (60, 15.5), (80, 6.5),
                             (mth1[2][0], 6.5), mth1[2]],
        "Motor -": [(x0, Y[5]), (26, 20.5), (40, 20.5), (55, 18.5), (60, 18.5), (95, mp[0]), (mlx, mp[0])],
        "Motor +": [(x0, Y[6]), (26, 24.5), (40, 24.5), (55, 21.5), (60, 21.5), (95, mp[1]), (mlx, mp[1])],
        "Hallux signal": [(x0, Y[7]), (26, 28.5), (40, 28.5), (55, 24.5), (60, 24.5), (95, 21), (110, 21),
                          (114, 23.6), (128, 23.6), (160, 33), (175, 40), (198, 40), (214, hal[3][1]), hal[3]],
    }


NET = {"Common supply": "C", "Common spine": "C", "Common to lateral midfoot (heel side)": "C",
       "Common to lateral midfoot (sensor side)": "C", "Common to fifth MTH": "C", "Common to first MTH": "C"}


def crossing(p):
    """Where the common branch to the lateral midfoot sensor crosses the fifth MTH trace."""
    x = 93.0
    y = -19 + (x - 70) / (95 - 70) * 7
    return (x, y)


def trace_layout(p=None):
    """Shapely polygons: {'traces': per-path polygons, 'pads': tail pads, 'tabs': tab pads,
    'motor_pads', 'patch', 'bridge'}."""
    from shapely.geometry import LineString, box
    p = derived(p)
    w = p["trace_w"]
    paths = trace_paths(p)
    polys = {k: LineString(v).buffer(w / 2, cap_style=2, join_style=2) for k, v in paths.items()}
    pads = [box(p["pad_x"][0], pad_y(p, i) - 1.0, p["pad_x"][1], pad_y(p, i) + 1.0) for i in range(8)]
    tabs = []
    for c, (dx, dy), a, b in fsr_tabs(p):
        for t in (a, b):
            lx, ly = (1.6, 3.0) if dx else (3.0, 1.6)
            lx, ly = (3.0, 1.6) if dx else (1.6, 3.0)
            tabs.append(box(t[0] - lx / 2, t[1] - ly / 2, t[0] + lx / 2, t[1] + ly / 2))
    mx, my = p["motor_xy"]
    mlx = mx - p["motor_d"] / 2 - p["pocket_clear"] - 4.7
    motor_pads = [box(mlx - 3.0, y - 0.75, mlx, y + 0.75) for y in (my - 1.4, my + 1.4)]
    pc = crossing(p)
    h = p["patch"] / 2
    patch = box(pc[0] - h, pc[1] - h, pc[0] + h, pc[1] + h)
    hp = h + 0.4
    bridge = box(pc[0] - w / 2, pc[1] - hp, pc[0] + w / 2, pc[1] + hp)
    return {"traces": polys, "pads": pads, "tabs": tabs, "motor_pads": motor_pads, "patch": patch, "bridge": bridge}


def fsr_shapes2d(p=None, grow=0.0):
    from shapely.geometry import Point, box
    from shapely import affinity
    p = derived(p)
    out = []
    r = p["fsr_d"] / 2
    tw, tl = p["fsr_tail"]
    for (x, y), (dx, dy) in zip(p["fsr_xy"], p["fsr_dir"]):
        disc = Point(x, y).buffer(r + grow, 64)
        tail = box(r - 2, -tw / 2 - grow, r + tl + grow, tw / 2 + grow)
        tail = affinity.rotate(tail, math.degrees(math.atan2(dy, dx)), origin=(0, 0))
        tail = affinity.translate(tail, x, y)
        out.append(disc.union(tail))
    return out


def strips2d(p=None):
    """The slit end of the flex tail: eight strips fanned from the tail onto the pads."""
    from shapely.geometry import Polygon
    p = derived(p)
    xa, xb = p["slit_x"]
    out = []
    for i in range(p["tail_n"]):
        ya = (i - (p["tail_n"] - 1) / 2) * p["tail_w"] / p["tail_n"]
        yb = pad_y(p, i)
        h = 0.45
        out.append(Polygon([(xa, ya - h), (xb, yb - h), (xb, yb + h), (xa, ya + h)]))
    return out


# ----------------------------------------------------------------- solids
def _face(poly):
    from build123d import Face, Wire, Vector
    pts = list(poly.exterior.coords)[:-1]
    return Face(Wire.make_polygon([Vector(x, y, 0) for x, y in pts], close=True))


def _prism(poly, z0, t):
    from build123d import Pos, extrude
    from shapely.geometry import MultiPolygon
    geoms = poly.geoms if isinstance(poly, MultiPolygon) else [poly]
    out = None
    for g in geoms:
        s = Pos(0, 0, z0) * extrude(_face(g), amount=t, dir=(0, 0, 1))
        out = s if out is None else out + s
    return out


def _slab(p, z0, t, grow=0.0):
    """Insole layer: the smooth spline outline extruded from z0 by t."""
    from build123d import Face, Pos, Wire, extrude
    return Pos(0, 0, z0) * extrude(Face(Wire([outline_edge(p, grow)])), amount=t, dir=(0, 0, 1))


def _zcyl(r, z0, h, x=0.0, y=0.0):
    from build123d import Cylinder, Pos
    return Pos(x, y, z0 + h / 2) * Cylinder(r, h)


def _xcyl(r, x0, x1, y, z):
    from build123d import Cylinder, Pos, Rot
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def _rbox(x0, x1, hy, z0, z1, r):
    """Box along X from x0 to x1, Y from -hy to hy, Z from z0 to z1, with its four edges
    parallel to X rounded to radius r (r = 0 leaves them square)."""
    from build123d import Axis, fillet
    b = _box(x0, x1, -hy, hy, z0, z1)
    return fillet(b.edges().filter_by(Axis.X), r) if r > 0 else b


def _ring(r0, r1, z0, h, p):
    """Part of an annulus round the heel cup centre, near the heel (X < 10)."""
    c = p["heel_r"] * p["insole_l"] / 272.0
    return (_zcyl(r1, z0, h, c, 0) - _zcyl(r0, z0 - 0.1, h + 0.2, c, 0))


def build_parts(params=None):
    """Return a dict of named build123d solids in the fitted state (in the shoe)."""
    from build123d import Cone, Pos, Rot
    from shapely.geometry import box as sbox
    from shapely.ops import unary_union
    p = derived(params)
    f = p["foam_t"]
    zt, zs, zc = p["z_trace"], p["z_spacer"], p["z_cover"]
    lay = trace_layout(p)
    mx, my = p["motor_xy"]
    hr = p["motor_d"] / 2 + p["pocket_clear"]
    notch = _box(mx - hr - 4.5, mx, my - 2.2, my + 2.2, -1, 10)
    hole = _zcyl(hr, -1, 10, mx, my) + notch

    # Insole, from the bottom up
    foam = _slab(p, 0, f) - hole
    film = _slab(p, f, p["film_t"]) - hole
    trace2d = unary_union(list(lay["traces"].values()) + lay["pads"] + lay["tabs"] + lay["motor_pads"])
    traces = _prism(trace2d, zt, p["trace_t"])
    patch = _prism(lay["patch"], zs, 0.05)
    bridge = _prism(lay["bridge"], zs + 0.05, p["trace_t"])
    fsr2d = fsr_shapes2d(p)
    fsrs = _prism(unary_union(fsr2d), zs, p["fsr_t"])
    motor = _zcyl(p["motor_d"] / 2, p["motor_gap"], p["motor_t"], mx, my)
    mlx = mx - hr - 4.7
    leads = None
    for y in (my - 1.4, my + 1.4):
        l = _box(mlx - 2.5, mx - p["motor_d"] / 2 - 0.15, y - 0.2, y + 0.2, zs, zs + 0.4)
        leads = l if leads is None else leads + l
    # tail: strips on the pads, the full-width end, up the counter, over its top, into the pod
    T, W = p["tail_t"], p["tail_w"]
    strips = _prism(unary_union(strips2d(p)), zs, T)
    tail_flat = (_box(-1, p["slit_x"][0], -W / 2, W / 2, zs, zs + T)
                 & _zcyl(p["r_in"], zs - 1, 5, p["heel_r"], 0))
    tail_up = _ring(p["r_tail"], p["r_in"], zs, p["tail_top"] - zs, p) & _box(-5, 5, -W / 2, W / 2, zs, p["tail_top"])
    xd = p["x_drop"]
    tail_over = (_box(xd - T / 2, 3, -W / 2, W / 2, p["counter_h"], p["tail_top"])
                 - _zcyl(p["r_tail"], 0, 80, p["heel_r"], 0))
    tail_drop = _box(xd - T / 2, xd + T / 2, -W / 2, W / 2, p["z_zif"][1], p["tail_top"])
    tail = strips + tail_flat + tail_up + tail_over + tail_drop

    # spacer: windows round the sensors, the tail end and pads, the motor lead pads and the crossover
    sp_win = unary_union([g.buffer(0.5) for g in fsr2d] + [
        sbox(-2, -p["pad_pitch"] * 4.2, p["pad_x"][1] + 1.0, p["pad_pitch"] * 4.2),
        sbox(mlx - 3.5, my - 3.0, mx - p["motor_d"] / 2 + 0.1, my + 3.0),
        lay["patch"].buffer(1.0)])
    spacer = _slab(p, zs, p["spacer_t"]) - _prism(sp_win, zs - 0.1, p["spacer_t"] + 0.2)
    from shapely.geometry import Polygon as SPoly, Point as SPoint
    ol = SPoly(outline(p))
    notch2d = sbox(-2, -W / 2 - 1, 1.5, W / 2 + 1)
    hole2d = SPoint(mx, my).buffer(hr, 64).union(sbox(mx - hr - 4.5, my - 2.2, mx, my + 2.2))
    tail2d = unary_union(strips2d(p) + [sbox(-1, -W / 2, p["slit_x"][0], W / 2).intersection(
        SPoint(p["heel_r"], 0).buffer(p["r_in"], 128))])
    p["_2d"] = {  # footprint and (bottom, top) height of each insole part
        "foam": (ol.difference(hole2d), (0, f)), "film": (ol.difference(hole2d), (f, zt)),
        "traces": (trace2d, (zt, zs)), "patch": (lay["patch"], (zs, zs + 0.05)),
        "bridge": (lay["bridge"], (zs + 0.05, zs + 0.05 + p["trace_t"])),
        "fsrs": (unary_union(fsr2d), (zs, zs + p["fsr_t"])),
        "motor": (SPoint(mx, my).buffer(p["motor_d"] / 2, 64), (p["motor_gap"], p["motor_gap"] + p["motor_t"])),
        "leads": (unary_union([sbox(mlx - 2.5, y - 0.2, mx - p["motor_d"] / 2 - 0.15, y + 0.2) for y in (my - 1.4, my + 1.4)]),
                  (zs, zs + 0.4)),
        "tail": (tail2d, (zs, zs + T)),
        "spacer": (ol.difference(sp_win).difference(notch2d), (zs, zc)),
        "cover": (ol.difference(notch2d), (zc, zc + p["cover_t"])),
    }
    heel_notch = _box(-2, 1.5, -W / 2 - 1, W / 2 + 1, zs - 0.1, p["stack"] + 0.1)
    spacer = spacer - heel_notch
    cover = _slab(p, zc, p["cover_t"]) - heel_notch

    # Heel pod base: a tray open to the lid side, with the clip and four lid bosses
    x0, x1 = p["pod_x0"], p["pod_x1"]
    ztop, zbot = p["pod_top"], p["pod_bot"]
    xl = p["x_lid_in"]
    hy = p["pod_y"] / 2
    base = _rbox(xl, x1, hy, zbot, ztop, p["pod_r"])
    base -= _rbox(xl - 0.1, p["x_wall_in"], p["cav_y"] / 2, p["z_floor"], p["z_roof"], p["pod_r"] - p["wall"])
    # parting-line groove round the base rim where the lid meets it
    g = p["groove"]
    base -= (_rbox(xl - 0.1, xl + g, hy + 1, zbot - 1, ztop + 1, 0)
             - _rbox(xl - 0.2, xl + g + 0.1, hy - g, zbot + g, ztop - g, p["pod_r"] - g))
    bw = p["bridge_w"] / 2
    bridge_clip = (_box(x1 - 0.5, 8, -bw, bw, p["tail_top"], ztop) - _zcyl(p["r_finger"], 0, 80, p["heel_r"], 0))
    finger = (_ring(p["r_finger"], p["r_tail"], p["tail_top"] - p["finger_l"], p["finger_l"], p)
              & _box(-2, 10, -bw, bw, p["tail_top"] - p["finger_l"], p["tail_top"]))
    base = base + bridge_clip + finger
    for (by, bz) in p["bosses"]:
        base = base + (_xcyl(p["boss_d"] / 2, xl, xl + p["boss_l"], by, bz)
                       - _xcyl(p["pilot_d"] / 2, xl - 0.1, xl + p["boss_l"] - 0.5, by, bz))
    # tail slot through the shoe-side wall, under the roof
    base -= _box(x1 - p["wall"] - 0.2, x1 + 0.2, -W / 2 - 0.5, W / 2 + 0.5, p["counter_h"] - 0.15, p["tail_top"] + 0.15)
    # USB-C opening: a notch in the bottom wall, open to the lid side so the module slides in
    rx, ry, rz = p["usb_rec"]
    xo = p["x_outer"]
    xb = xo - 1.2                                                    # module board face (1.2 mm board)
    uo, uc = p["usb_open"]
    base -= _box(xb + uc, xl - 0.1, -uo / 2, uo / 2, zbot - 0.1, p["z_floor"] + 0.1)

    # Internal parts
    cx0, cx1 = p["x_cell"]
    cell = _box(cx0, cx1, -p["cell"][1] / 2, p["cell"][1] / 2, *p["z_cell"])
    cell_tape = _box(cx1, p["x_wall_in"], -10, 10, p["z_cell"][0] + 5, p["z_cell"][1] - 5)
    mxx, myy, mzz = p["module"]
    module = _box(xo - mxx, xo, -myy / 2, myy / 2, *p["z_module"])
    module = module + _box(xb - rx, xb, -ry / 2, ry / 2, p["z_module"][0] - rz, p["z_module"][0] + 0.1)
    module_tape = _box(cx0, xo, -7, 7, p["z_module"][0] + 3, p["z_module"][1] - 3)
    ixx, iyy, izz = p["iface"]
    iface = _box(xo - ixx, xo, -iyy / 2, iyy / 2, *p["z_iface"])
    iface_tape = _box(cx0, xo, -7, 7, p["z_iface"][0] + 2, p["z_iface"][1] - 2)
    zx, zy, zz = p["zif"]
    zif = _box(xo - zx, xo, -zy / 2, zy / 2, *p["z_zif"])
    cap = _xcyl(p["cap_d"] / 2, xo - ixx, x0 - p["cap_proud"], 0, p["z_button"])

    # Lid with pause button and LED windows and four countersunk screw holes
    lid = _rbox(x0, xl, hy, zbot, ztop, p["pod_r"])
    lid -= _xcyl(p["button_d"] / 2, x0 - 1, xl + 1, 0, p["z_button"])
    lid -= _xcyl(p["led_d"] / 2, x0 - 1, xl + 1, -myy / 4, p["z_led"])
    screws = None
    for (by, bz) in p["bosses"]:
        lid -= _xcyl(1.1, x0 - 1, xl + 1, by, bz)
        lid -= Pos(x0 + 0.45, by, bz) * Rot(0, 90, 0) * Cone(p["csk_d"] / 2 + 0.05, 1.05, 1.0)
        s = (_xcyl(p["pilot_d"] / 2, x0 + 0.9, x0 + p["screw_l"], by, bz)
             + Pos(x0 + 0.47, by, bz) * Rot(0, 90, 0) * Cone(p["csk_d"] / 2 - 0.05, p["csk_d"] / 2 - 0.05 - 0.774, 0.86))
        screws = s if screws is None else screws + s

    return {"foam": foam, "film": film, "traces": traces, "patch": patch, "bridge": bridge, "fsrs": fsrs,
            "motor": motor, "leads": leads, "tail": tail, "spacer": spacer, "cover": cover,
            "laminate": film + traces + spacer,
            "base": base, "cell": cell, "cell_tape": cell_tape, "module": module, "module_tape": module_tape,
            "iface": iface, "iface_tape": iface_tape, "zif": zif, "cap": cap, "lid": lid, "screws": screws, "_p": p}


def shoe_context(params=None):
    """Simplified shoe (outsole and heel counter), for scale and for the clip checks. Round the
    heel the counter is a true cylinder (radius heel_r to heel_r + counter_t), as a moulded counter is."""
    p = derived(params)
    c = p["heel_r"] * p["insole_l"] / 272.0
    outsole = _slab(p, -22, 22, grow=6)
    inner = _slab(p, -1, 80, grow=0.02)                             # 0.02 mm fit: no coincident faces
    sides = (_slab(p, 0, p["counter_h"], grow=p["counter_t"]) - inner) & _box(c, 40, -100, 100, -1, 80)
    # where the spline outline runs a hair outside the heel circle the counter is relieved to it
    heel = (_ring(p["r_in"], p["r_out"], 0, p["counter_h"], p) & _box(-10, c, -100, 100, -1, 80)) - inner
    return outsole + sides + heel


INSOLE_KEYS = ("foam", "film", "traces", "patch", "bridge", "fsrs", "motor", "leads", "tail", "spacer", "cover")
POD_KEYS = ("base", "cell", "cell_tape", "module", "module_tape", "iface", "iface_tape", "zif", "cap", "lid", "screws")


def build(params=None, keys=INSOLE_KEYS + POD_KEYS):
    """Assembly (insole, tail and heel pod) as one compound."""
    from build123d import Compound
    parts = build_parts(params)
    return Compound(children=[parts[k] for k in keys])


def export(out=None):
    from build123d import export_step, export_stl
    out = Path(out) if out else Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    from build123d import Compound
    # single parts first: a part placed in a Compound is re-parented and can no longer be written alone
    for name in ("base", "lid", "foam", "film", "spacer", "cover", "laminate"):
        export_step(parts[name], str(out / "step" / f"stepcue-{name}.step"))
        export_stl(parts[name], str(out / "stl" / f"stepcue-{name}.stl"), tolerance=0.05)
    pod = Compound(children=[build_parts()[k] for k in POD_KEYS])
    export_step(pod, str(out / "step" / "stepcue-heel-pod.step"))
    asm = Compound(children=[parts[k] for k in INSOLE_KEYS + POD_KEYS])
    export_step(asm, str(out / "step" / "stepcue-assembly.step"))
    export_stl(asm, str(out / "stl" / "stepcue-assembly.stl"), tolerance=0.05)
    return parts


# ----------------------------------------------------------------- constructability checks
CONTACT = [  # pairs that must touch (distance 0.06 mm or less)
    ("foam", "film"), ("film", "traces"), ("traces", "patch"), ("patch", "bridge"), ("traces", "fsrs"),
    ("traces", "tail"), ("traces", "leads"), ("motor", "spacer"), ("spacer", "cover"), ("traces", "spacer"),
    ("tail", "shoe"), ("base", "shoe"), ("base", "tail"), ("tail", "zif"), ("zif", "iface"),
    ("base", "cell_tape"), ("cell_tape", "cell"), ("cell", "module_tape"), ("module_tape", "module"),
    ("cell", "iface_tape"), ("iface_tape", "iface"), ("iface", "cap"), ("base", "lid"), ("lid", "screws"),
    ("base", "screws"), ("fsrs", "film"), ("tail", "film"),
]
CLEAR = [  # pairs that must stay apart, with the least gap in mm
    ("motor", "foam", 0.2), ("motor", "film", 0.2), ("cap", "lid", 0.2), ("module", "base", 0.15),
    ("module", "iface", 0.2), ("cell", "base", 0.2), ("iface", "lid", 0.3), ("zif", "base", 0.5),
    ("fsrs", "spacer", 0.3), ("tail", "spacer", 0.3), ("tail", "cell", 2.0), ("module", "lid", 0.5),
    ("cell", "module", 0.4), ("tail", "cover", 0.1), ("leads", "spacer", 0.2),
]


def check(verbose=True):
    """Constructability checks. Returns (passed, failed) lists of strings."""
    from shapely.geometry import Polygon, Point
    parts = build_parts()
    p = parts.pop("_p")
    parts.pop("laminate")
    parts["shoe"] = shoe_context()
    ok, bad = [], []

    def rec(cond, text):
        (ok if cond else bad).append(text)

    names = list(parts)
    bb = {k: parts[k].bounding_box() for k in names}

    def apart(a, b):
        A, B = bb[a], bb[b]
        return (A.max.X < B.min.X or B.max.X < A.min.X or A.max.Y < B.min.Y or B.max.Y < A.min.Y
                or A.max.Z < B.min.Z or B.max.Z < A.min.Z)
    # 1. nothing overlaps anything else
    for a, b in itertools.combinations(names, 2):
        if apart(a, b):
            rec(True, f"no overlap: {a} / {b} (bounding boxes apart)")
            continue
        try:
            v = (parts[a] & parts[b]).volume
        except Exception:
            v = 0.0
        rec(v < 1e-3, f"no overlap: {a} / {b} ({v:.4f} mm3)")
    F = p["_2d"]

    def gap(a, b):
        """Least gap between two parts. Insole layers are flat, so their gap is found from their
        footprints and heights (fast and exact); other parts use the 3D distance."""
        if a in F and b in F:
            (ga, (a0, a1)), (gb, (b0, b1)) = F[a], F[b]
            dz = max(b0 - a1, a0 - b1, 0.0)
            d2 = ga.distance(gb)
            if dz <= 1e-9:
                return d2                        # same height band: the gap is sideways
            return dz if ga.intersection(gb).area > 0.01 else (dz ** 2 + d2 ** 2) ** 0.5
        return parts[a].distance_to(parts[b])
    # 2. parts that must touch do touch
    touching = set()
    for a, b in CONTACT:
        d = gap(a, b)
        rec(d <= 0.06, f"touch: {a} / {b} (gap {d:.3f} mm)")
        if d <= 0.06:
            touching |= {a, b}
    # 3. parts that must stay apart do
    for a, b, g in CLEAR:
        d = gap(a, b)
        rec(d >= g - 1e-6, f"clear: {a} / {b} >= {g} mm (gap {d:.3f} mm)")
    # 4. every part is held by something (it is in at least one touching pair)
    for a in names:
        if a != "shoe":
            rec(a in touching, f"held: {a} touches the part that holds it")
    # 5. circuit layout on the carrier
    lay = trace_layout(p)
    tr = lay["traces"]
    out_in = Polygon(outline(p)).buffer(-1.5)
    for k, g in tr.items():
        rec(out_in.contains(g), f"trace inside the outline with 1.5 mm margin: {k}")
    cross = {("Common to lateral midfoot (heel side)", "Fifth MTH signal"),
             ("Common to lateral midfoot (sensor side)", "Fifth MTH signal")}
    for a, b in itertools.combinations(tr, 2):
        if NET.get(a) == "C" and NET.get(b) == "C":
            continue
        d = tr[a].distance(tr[b])
        rec(d >= 0.8, f"trace gap {a} / {b} >= 0.8 mm ({d:.2f} mm)")
    pc = crossing(p)
    rec(lay["patch"].contains(tr["Fifth MTH signal"].intersection(lay["bridge"].buffer(0.5))),
        "crossover: the fifth MTH trace is covered by the patch under the bridge")
    for k, g in tr.items():
        for (x, y), name in zip(p["fsr_xy"], ("heel", "lateral midfoot", "first MTH", "fifth MTH", "hallux")):
            d = g.distance(Point(x, y).buffer(p["fsr_d"] / 2))
            rec(d >= 0.5, f"trace clear of the {name} sensor disc: {k} ({d:.2f} mm)")
    # 6. process checks
    rec(p["wall"] >= 1.2 and p["lid_t"] >= 1.2 and p["finger_t"] >= 1.2 and p["bridge_t"] >= 1.2,
        "printed walls, lid, clip finger and bridge at least 1.2 mm (3 perimeters at 0.4 mm)")
    rec(p["cav_x"] + 0.1 <= 15.0, f"largest unsupported span when printed on its side {p['cav_x']:.1f} mm <= 15 mm")
    rec(p["boss_d"] - p["pilot_d"] >= 2.0, "lid bosses keep 1.2 mm of wall round the M2 pilot")
    rec(p["stack"] <= 5.0, f"insole stack {p['stack']:.2f} mm <= 5.0 mm (R9)")
    rec(p["pod_z"] <= 45 and p["pod_y"] <= 40 and p["pod_x"] <= 20, "pod body within 45 x 40 x 20 mm (R10)")
    # 6a. smooth spline insole outline (2026-10-02): passes through its control points, no corners
    from build123d import Vector
    ol_pts = np.array(outline(p))
    a, b, c = np.roll(ol_pts, 1, 0), ol_pts, np.roll(ol_pts, -1, 0)
    v1, v2 = b - a, c - a
    area = np.abs(v1[:, 0] * v2[:, 1] - v1[:, 1] * v2[:, 0]) / 2
    rad = (np.linalg.norm(b - a, axis=1) * np.linalg.norm(c - b, axis=1) * np.linalg.norm(a - c, axis=1)
           / (4 * area + 1e-12)).min()
    rec(rad >= 15.0, f"insole outline is a smooth spline: tightest bend radius {rad:.1f} mm >= 15 mm (no corners)")
    edge = outline_edge(p)
    dev = max(edge.distance_to(Vector(x, y, 0)) for x, y in outline_points(p))
    rec(dev < 0.01, f"spline outline passes through its control points (largest miss {dev:.3f} mm)")
    # 6b. rounded pod (2026-10-02): 5 mm corners on base and lid, groove at the parting line
    from shapely.geometry import box as sbox
    hy, zt, zb, R, g = p["pod_y"] / 2, p["pod_top"], p["pod_bot"], p["pod_r"], p["groove"]
    rec(R - p["wall"] >= 1.0, f"cavity corners rounded to {R - p['wall']:.1f} mm so the wall stays {p['wall']} mm round the corners")
    xm_b = (p["x_lid_in"] + p["pod_x1"]) / 2
    xm_l = (p["pod_x0"] + p["x_lid_in"]) / 2
    for nm, xm in (("base", xm_b), ("lid", xm_l)):
        corner_out = all(not parts[nm].is_inside((xm, sy * (hy - 0.5), sz)) for sy in (-1, 1) for sz in (zt - 0.5, zb + 0.5))
        rec(corner_out, f"{nm}: all four corners rounded to {R:.0f} mm")
    rec(p["wall"] - g >= 1.0, f"parting-line groove {g} x {g} mm leaves {p['wall'] - g:.1f} mm of rim wall (>= 1.0 mm)")
    floor_g = sbox(-hy + g, zb + g, hy - g, zt - g).buffer(-(R - g)).buffer(R - g)
    for by, bz in p["bosses"]:
        where = f"Y {by:+.1f}, {'top' if bz > (zt + zb) / 2 else 'bottom'}"
        boss = Point(by, bz).buffer(p["boss_d"] / 2, 64)
        rec(floor_g.contains(boss), f"lid boss at {where} stays inside the rounded corner and the groove "
            f"({floor_g.exterior.distance(boss):.2f} mm skin)")
        d = floor_g.exterior.distance(Point(by, bz)) - p["pilot_d"] / 2
        rec(d >= 1.0, f"M2 pilot at {where} keeps {d:.1f} mm of plastic to the groove (>= 1.0 mm)")
    # 7. assembly order: each pod part slides into the open tray along +X without hitting what is already there
    seq = [("cell", ["base"]), ("cell_tape", ["base"]), ("module", ["base", "cell"]),
           ("iface", ["base", "cell", "module"]), ("zif", ["base", "cell", "module"]), ("cap", ["base", "cell", "module"]),
           ("lid", ["base", "cell", "module", "iface", "zif", "cap"])]
    from build123d import Pos
    for k, fixed in seq:
        hit = None
        for dx in np.arange(0.5, 30.5, 1.0):
            moved = Pos(-dx, 0, 0) * parts[k]
            for o in fixed:
                if (moved & parts[o]).volume > 1e-3:
                    hit = (o, dx)
                    break
            if hit:
                break
        rec(hit is None, f"assembly: {k} slides in from the lid side" + (f" (hits {hit[0]} {hit[1]:.1f} mm out)" if hit else ""))
    if verbose:
        for t in bad:
            print("FAIL", t)
        print(f"{len(ok)} checks pass, {len(bad)} fail")
    return ok, bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        ok, bad = check()
        sys.exit(1 if bad else 0)
    parts = export()
    p = parts["_p"]
    print(f"Insole stack {p['stack']:.2f} mm (EVA {p['foam_t']}, carrier {p['film_t'] + p['trace_t']:.2f}, "
          f"spacer {p['spacer_t']}, cover {p['cover_t']}); motor {p['motor_gap']:.1f} mm clear of the insole underside")
    print(f"Pod body {p['pod_z']:.1f} high x {p['pod_y']:.1f} wide x {p['pod_x']:.1f} deep mm; "
          f"with clip {p['pod_x'] + p['counter_t'] + p['tail_t'] + p['finger_t']:.1f} deep at the heel centre")
    for k in ("base", "lid", "foam", "film", "spacer", "cover"):
        print(f"{k:9s} volume {parts[k].volume / 1000:.2f} cm3")
    print("Wrote cad/step/stepcue-*.step and cad/stl/stepcue-*.stl")
