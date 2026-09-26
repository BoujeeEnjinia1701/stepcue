"""StepCue parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl.

Coordinates (mm): X runs heel (0) to toe, Y points to the medial (big-toe) side of a
right insole, Z is up with the underside of the insole at Z = 0. The shoe heel counter
is a wall behind the heel: its inner face is at X = 0, its outer face at X = -counter_t,
and its top edge at Z = counter_h. The heel pod hangs on the outside of the counter and
clips over its top edge.

Detail level: correct interfaces (insole stack, sensor sites, motor pocket, flex tail
route, clip over the heel counter, USB-C and tail openings, pause button and LED
windows) and main dimensions. Not fabrication detail. PRELIMINARY, NOT FOR FABRICATION.

Decisions reflected (STC-DDR-001, 2026-09-25): one instrumented insole; XIAO nRF52840
Sense class controller with built-in IMU (no separate IMU, no multiplexer); haptic cue
by default with audio through a paired phone or earbuds (no piezo in the pod); commercial
FSRs; electronics in a clip-on heel pod. STC-DDR-002 (2026-09-25): 2.5 mm EVA base
with a relief for the motor in the underside of the sensor laminate (item O3).
"""
from pathlib import Path
import numpy as np

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Insole, about EU 42 (US men's 8.5)
    "insole_l": 272.0,        # heel to toe
    "foam_t": 2.5,            # EVA base (2.5 mm by decision O3, STC-DDR-002; was 3.0)
    "lam_t": 0.8,             # sensor laminate: 0.2 film and adhesive plus 0.46 FSR, rounded up
    "cover_t": 1.2,           # PU foam top cover
    # Force-sensing resistors (Interlink FSR 402: 18.3 dia, 14.68 active, 0.46 thick)
    "fsr_d": 18.3,
    "fsr_active_d": 14.68,
    "fsr_t": 0.46,
    # Sensor sites (x, y): heel, lateral midfoot, first MTH, fifth MTH, hallux
    "fsr_xy": ((34, 0), (110, -24), (185, 28), (178, -30), (246, 24)),
    # Coin ERM motor under the medial arch (Precision Microdrives 310-103 class, 10 x 2.7)
    "motor_d": 10.0,
    "motor_t": 2.7,
    "motor_xy": (120.0, 16.0),
    "pocket_clear": 0.3,      # radial clearance of the motor pocket
    "pocket_floor": 0.2,      # EVA left under the motor
    # Flat flex tail (8-way, 1.0 mm pitch)
    "tail_w": 12.0,
    "tail_t": 0.3,
    # Shoe heel counter (context and clip interface)
    "counter_t": 3.5,
    "counter_h": 55.0,
    # Heel pod body (outside the counter)
    "pod_x": 15.0,            # depth away from the shoe, including the lid
    "pod_y": 34.0,            # width across the heel
    "pod_z": 42.0,            # height
    "wall": 1.5,
    "lid_t": 2.0,
    # Clip over the counter top
    "bridge_t": 2.0,          # bridge thickness above the counter and tail
    "bridge_w": 26.0,         # bridge and finger width (Y)
    "finger_t": 1.5,          # finger inside the counter
    "finger_l": 18.0,         # finger length below the bridge
    "clip_interference": 1.0, # free-state gap is this much smaller than counter plus tail
    # Internal parts (envelopes)
    "cell": (5.2, 25.0, 35.0),        # 400 mAh LiPo, 502535 class: X (thick), Y, Z
    "module": (4.0, 17.8, 21.0),      # XIAO nRF52840 Sense class: X (with parts), Y, Z (USB-C up)
    "iface": (5.0, 20.0, 12.0),       # interface perfboard with MOSFETs, resistors and tact switch
    "usb_slot": (4.0, 10.0),          # opening in the top wall over the USB-C receptacle (X, Y)
    "button_d": 10.0,                 # pause button opening in the lid
    "led_d": 3.0,                     # status LED window in the lid
}


def outline(p, grow=0.0, n=40):
    """Right-foot insole outline as a list of (x, y) points, optionally grown outward."""
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


def _slab(p, z0, t, grow=0.0):
    from build123d import Face, Wire, Vector, Pos, extrude
    face = Face(Wire.make_polygon([Vector(x, y, 0) for x, y in outline(p, grow)], close=True))
    return Pos(0, 0, z0) * extrude(face, amount=t)


def derived(params=None):
    p = dict(params or PARAMS)
    p["stack"] = p["foam_t"] + p["lam_t"] + p["cover_t"]
    p["motor_relief"] = max(0.0, p["pocket_floor"] + p["motor_t"] - p["foam_t"])   # into the laminate underside
    p["tail_top"] = p["counter_h"] + p["tail_t"]                      # tail lies over the counter top
    p["pod_top"] = p["tail_top"] + p["bridge_t"]
    p["pod_bot"] = p["pod_top"] - p["pod_z"]
    p["pod_x1"] = -p["counter_t"]                                     # shoe-side face of the pod
    p["pod_x0"] = p["pod_x1"] - p["pod_x"]                            # outer face of the lid
    p["finger_x0"] = p["tail_t"]                                      # finger face against the tail
    p["clip_gap_fitted"] = p["counter_t"] + p["tail_t"]
    p["clip_gap_free"] = p["clip_gap_fitted"] - p["clip_interference"]
    p["cav_x"] = p["pod_x"] - p["wall"] - p["lid_t"]
    p["cav_y"] = p["pod_y"] - 2 * p["wall"]
    p["cav_z"] = p["pod_z"] - 2 * p["wall"]
    return p


def build_parts(params=None):
    """Return a dict of named build123d solids (fitted state, in the shoe)."""
    from build123d import Box, Cylinder, Pos, Rot
    p = derived(params)
    f, lam, cov = p["foam_t"], p["lam_t"], p["cover_t"]

    # 1 to 6: insole stack
    cover = _slab(p, f + lam, cov)
    fsrs = None
    for x, y in p["fsr_xy"]:
        d = Pos(x, y, f + lam - p["fsr_t"] / 2) * Cylinder(p["fsr_d"] / 2, p["fsr_t"])
        fsrs = d if fsrs is None else fsrs + d
    laminate = _slab(p, f, lam) - fsrs
    W, T = p["tail_w"], p["tail_t"]
    z_lam = f + lam
    tail_pad = Pos(4.0, 0, z_lam - T / 2) * Box(8.0, W, T)   # tail end bonded flush in the laminate
    laminate = laminate - tail_pad
    mx, my = p["motor_xy"]
    motor = Pos(mx, my, p["pocket_floor"] + p["motor_t"] / 2) * Cylinder(p["motor_d"] / 2, p["motor_t"])
    rel = p["motor_relief"]
    if rel > 0:   # 5: relief in the laminate underside where the motor stands proud of the EVA
        laminate = laminate - Pos(mx, my, f + rel / 2 - 0.05) * Cylinder(p["motor_d"] / 2 + p["pocket_clear"], rel + 0.1)
    pocket_h = f - p["pocket_floor"]
    foam = _slab(p, 0, f) - Pos(mx, my, p["pocket_floor"] + pocket_h / 2 + 0.05) * Cylinder(
        p["motor_d"] / 2 + p["pocket_clear"], pocket_h + 0.1)

    # 4: flat flex tail, bonded to the laminate at the heel rim, up the inside of the
    # counter (under the clip finger), over the counter top and into the pod
    tail = (Pos(4.0, 0, z_lam - T / 2) * Box(8.0, W, T)
            + Pos(T / 2, 0, (z_lam - T + p["counter_h"] + T) / 2) * Box(T, W, p["counter_h"] - z_lam + 2 * T)
            + Pos((T - p["counter_t"] - p["wall"]) / 2, 0, p["counter_h"] + T / 2)
            * Box(p["counter_t"] + p["wall"] + T, W, T))

    # 7: heel pod base, a tray open to the outside, with the clip
    x0, x1, zt, zb = p["pod_x0"], p["pod_x1"], p["pod_top"], p["pod_bot"]
    xl = x0 + p["lid_t"]                                   # tray rim, where the lid sits
    zc = (zt + zb) / 2
    base = Pos((xl + x1) / 2, 0, zc) * Box(x1 - xl, p["pod_y"], p["pod_z"])
    base -= Pos((xl + x1 - p["wall"]) / 2 - 0.05, 0, zc) * Box(x1 - xl - p["wall"] + 0.1, p["cav_y"], p["cav_z"])
    bx0, bx1 = x1, p["finger_x0"] + p["finger_t"]
    bridge = Pos((bx0 + bx1) / 2, 0, p["tail_top"] + p["bridge_t"] / 2) * Box(bx1 - bx0, p["bridge_w"], p["bridge_t"])
    finger = Pos(p["finger_x0"] + p["finger_t"] / 2, 0, p["tail_top"] - p["finger_l"] / 2) * Box(
        p["finger_t"], p["bridge_w"], p["finger_l"])
    base = base + bridge + finger
    # tail slot through the shoe-side wall, just under the top wall
    base -= Pos(x1 - p["wall"] / 2, 0, p["counter_h"] + T / 2) * Box(p["wall"] + 0.2, W + 1.0, 1.0)

    # Internal envelopes, from the shoe-side wall outward
    cxx, cyy, czz = p["cell"]
    cx = x1 - p["wall"] - 0.3 - cxx / 2
    cell = Pos(cx, 0, zc) * Box(cxx, cyy, czz)
    mxx, myy, mzz = p["module"]
    lx = cx - cxx / 2 - 0.5 - mxx / 2
    mz = zt - p["wall"] - mzz / 2
    module = Pos(lx, 0, mz) * Box(mxx, myy, mzz)
    ixx, iyy, izz = p["iface"]
    iz = zb + p["wall"] + 0.5 + izz / 2
    ix = cx - cxx / 2 - 0.5 - ixx / 2
    iface = Pos(ix, 0, iz) * Box(ixx, iyy, izz)
    # USB-C opening in the top wall over the module
    ux, uy = p["usb_slot"]
    base -= Pos(lx, 0, zt - p["wall"] / 2) * Box(ux, uy, p["wall"] + 0.2)

    # 11: lid with pause button and LED windows
    lid = Pos(x0 + p["lid_t"] / 2, 0, zc) * Box(p["lid_t"], p["pod_y"], p["pod_z"])
    lid -= Pos(x0 + p["lid_t"] / 2, 0, iz) * Rot(0, 90, 0) * Cylinder(p["button_d"] / 2, p["lid_t"] + 1)
    lid -= Pos(x0 + p["lid_t"] / 2, -myy / 4, mz) * Rot(0, 90, 0) * Cylinder(p["led_d"] / 2, p["lid_t"] + 1)

    p.update({"cell_c": (cx, 0, zc), "module_c": (lx, 0, mz), "iface_c": (ix, 0, iz)})
    return {"cover": cover, "fsrs": fsrs, "laminate": laminate, "tail": tail, "motor": motor,
            "foam": foam, "base": base, "cell": cell, "module": module, "iface": iface,
            "lid": lid, "_p": p}


def shoe_context(params=None):
    """Simplified shoe (outsole and heel counter), for scale only."""
    from build123d import Box, Pos
    p = derived(params)
    outsole = _slab(p, -22, 22, grow=6)
    inner = _slab(p, -1, 80, grow=0.0)
    counter = (_slab(p, 0, p["counter_h"], grow=p["counter_t"]) - inner) - Pos(170, 0, 30) * Box(260, 200, 90)
    return outsole + counter


INSOLE_KEYS = ("cover", "fsrs", "laminate", "tail", "motor", "foam")
POD_KEYS = ("base", "cell", "module", "iface", "lid")


def build(params=None, keys=INSOLE_KEYS + POD_KEYS):
    """Assembly (insole, tail and heel pod) as one compound."""
    from build123d import Compound
    parts = build_parts(params)
    return Compound(children=[parts[k] for k in keys])


def export(out=None):
    from build123d import export_step, export_stl
    out = Path(out) if out else Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    asm = build()
    export_step(asm, str(out / "step" / "stepcue-assembly.step"))
    export_stl(asm, str(out / "stl" / "stepcue-assembly.stl"))
    pod = build(keys=POD_KEYS)
    export_step(pod, str(out / "step" / "stepcue-heel-pod.step"))
    parts = build_parts()
    for name in ("base", "lid", "foam", "laminate", "cover"):
        export_step(parts[name], str(out / "step" / f"stepcue-{name}.step"))
        export_stl(parts[name], str(out / "stl" / f"stepcue-{name}.stl"))
    return parts


if __name__ == "__main__":
    parts = export()
    p = parts["_p"]
    print(f"Insole stack {p['stack']:.2f} mm (foam {p['foam_t']}, laminate {p['lam_t']}, cover {p['cover_t']}); "
          f"motor relief {p['motor_relief']:.1f} mm in the laminate")
    print(f"Pod body {p['pod_z']:.1f} high x {p['pod_y']:.1f} wide x {p['pod_x']:.1f} deep mm; "
          f"with clip {p['pod_x'] + p['counter_t'] + p['tail_t'] + p['finger_t']:.1f} deep")
    for k in ("base", "lid", "foam", "laminate", "cover"):
        print(f"{k:9s} volume {parts[k].volume / 1000:.2f} cm3")
    print("Wrote cad/step/stepcue-*.step and cad/stl/stepcue-*.stl")
