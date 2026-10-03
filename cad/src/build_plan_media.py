"""StepCue prototype build plan pictures (STC-BLD-001, STANDARDS section 18).

Run from the repo root:
    python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring] [item ...]
With no argument it draws everything; with a group and item numbers it draws only those
(for example `sheets 105` or `joints 05 06`), so pictures can be made one process at a time.
Every 3D picture is drawn from cad/src/model.py (build_parts), so the pictures and the model
never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/STC-DWG-101 to 107        making sketches for the made components
    docs/05-build-plan/insole-layout.png   the circuit on the carrier film, full-size figures
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as M  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
P1 = ("P1", "Making sketch for the prototype build plan", DATE, "AC")
OUTLINE_P2 = dict(rev="P2", history=(P1, ("P2", "Smooth spline insole outline", "2026-10-02", "AC")))
POD_P2 = dict(rev="P2", history=(P1, ("P2", "5 mm pod corners, parting-line groove", "2026-10-02", "AC")))
REPO = "github.com/BoujeeEnjinia1701/stepcue"
_C = {}


def C():
    if not _C:
        _C.update(M.build_parts())
        _C["shoe"] = M.shoe_context()
    return _C


def P():
    return C()["_p"]


COL = {"foam": "#374151", "film": "#D97706", "traces": "#9A3412", "patch": "#FCD34D", "fsrs": "#0F766E",
       "tail": "#EA580C", "motor": "#64748B", "spacer": "#7DD3FC", "cover": "#8CC7C0", "base": "#6B7280",
       "cell": "#B91C1C", "tape": "#FDE68A", "module": "#1D4ED8", "iface": "#16A34A", "zif": "#7C3AED",
       "cap": "#0F766E", "lid": "#D1D5DB", "screws": "#111827", "shoe": "#C8CDD3"}


def fuse(*keys):
    out = None
    for k in keys:
        s = C()[k]
        out = s if out is None else out + s
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def made():
    """The components in build order."""
    return {
        "foam": part("EVA base", C()["foam"], COL["foam"]),
        "film": part("Carrier film", C()["film"], COL["film"]),
        "traces": part("Copper traces and crossover patch", fuse("traces", "patch", "bridge"), COL["traces"]),
        "fsrs": part("Pressure sensors (5)", C()["fsrs"], COL["fsrs"]),
        "tail": part("Flex tail", C()["tail"], COL["tail"]),
        "motor": part("Vibration motor and leads", fuse("motor", "leads"), COL["motor"]),
        "spacer": part("Spacer foam", C()["spacer"], COL["spacer"]),
        "cover": part("Top cover", C()["cover"], COL["cover"]),
        "base": part("Pod base with clip", C()["base"], COL["base"]),
        "cell": part("Cell and its tape", fuse("cell", "cell_tape"), COL["cell"]),
        "module": part("Controller module and its tape", fuse("module", "module_tape"), COL["module"]),
        "iface": part("Interface board, connector, button cap", fuse("iface", "iface_tape", "zif", "cap"), COL["iface"]),
        "lid": part("Lid and four M2 screws", fuse("lid", "screws"), COL["lid"]),
    }


INSOLE = ("foam", "film", "traces", "fsrs", "tail", "motor", "spacer", "cover")


def win(shape, x0, x1, y0, y1, z0, z1):
    return shape & M._box(x0, x1, y0, y1, z0, z1)


# ----------------------------------------------------------------- overview
def overview():
    m = made()
    off = {"foam": (0, 0, 0), "film": (0, 0, 38), "traces": (0, 0, 76), "fsrs": (0, 0, 114), "tail": (0, 0, 152),
           "motor": (0, -95, -20), "spacer": (0, 0, 190), "cover": (0, 0, 228),
           "base": (-60, 0, 150), "cell": (-105, 0, 150), "module": (-145, 0, 150), "iface": (-185, 0, 150),
           "lid": (-230, 0, 150)}
    parts = []
    for k in m:
        p = m[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "StepCue prototype: every component, pulled apart",
                       subtitle="Numbered in build order: the insole (1 to 8) is built first, then the heel pod (9 to 13). "
                                "Seen from the front left and above",
                       elev=24, azim=-125, size=(11, 7.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheet(part_, neighbours, dwg_no, title, material, notes, views=("front", "top", "right"), view_shape=None,
          inset_view=(24, -58), rev="P1", history=()):
    """As build_views.component_sheet, but with a choice of views: a flat sheet part (an insole
    layer) is drawn in plan only, since its edge views are a fraction of a millimetre thick."""
    from drawing import Sheet, project_views
    work = DWG / f"_{dwg_no}_views"
    vs = project_views(view_shape if view_shape is not None else part_.shape, work)
    inset = bv.where_it_goes(part_, neighbours, work / "where.png", elev=inset_view[0], azim=inset_view[1])
    s = Sheet(project="StepCue", title=title, dwg_no=dwg_no, rev=rev, author="Amish Chadha",
              date=history[-1][2] if history else DATE,
              concept="BUILD PLAN SKETCH, PLAN NOT YET BUILT", scale=None, material=material,
              revisions=list(history) or [(rev, "Making sketch for the prototype build plan", DATE, "AC")])
    s.add_ortho(vs, list(views))
    s.add_image(str(inset), 276, 30, 140, 70, label="Where it goes", sublabel="This part in colour, its neighbours in grey")
    s.add_notes("How to make it and how it fits", notes, x=276, y=112, width=140)
    s.save(DWG / dwg_no)
    shutil.rmtree(work, ignore_errors=True)
    return DWG / f"{dwg_no}.png"


def sheets(which=None):
    from build123d import Pos
    p = P()
    m = made()
    grey_shoe = part("Shoe", C()["shoe"], COL["shoe"])
    out = []
    flat = dict(views=("top",), inset_view=(35, -60))
    mx, my = p["motor_xy"]
    S = {}
    S["101"] = lambda: sheet(
        m["foam"], [m["base"]], "STC-DWG-101", "StepCue EVA base: making sketch",
        "EVA foam sheet 2.5 mm, black or grey, cut to the insole outline", notes=[
            "Print the insole outline (one smooth curve, no corners) full size",
            "  from the insole layout picture; this model is about EU 42.",
            "Lay the print on the EVA and cut round it with a sharp knife on a",
            "  cutting mat: one pass with the blade upright, no sawing.",
            f"Motor hole: {2 * (p['motor_d'] / 2 + p['pocket_clear']):.1f} mm round, centred {mx:.0f} mm from the heel",
            f"  and {my:.0f} mm to the inner (big-toe) side of the centre line.",
            "  Punch it with an 11 mm hole punch or cut it with a knife.",
            "Lead notch: 4.4 mm wide, from the hole 4.5 mm toward the heel.",
            "Nothing else is cut. The hole goes right through: the motor",
            "  stands in it, 0.1 mm clear of the shoe's floor.",
            "Check: lay it in the shoe; it lies flat with no edge curling up",
            "  the side of the shoe. Trim the outline if it does.",
        ], **flat, **OUTLINE_P2)
    S["102"] = lambda: sheet(
        part("Carrier film with traces", fuse("film", "traces", "patch", "bridge"), COL["film"]),
        [m["foam"], m["fsrs"], m["tail"]], "STC-DWG-102", "StepCue carrier film and copper traces: making sketch",
        "125 um polyimide film with transfer adhesive; 6 mm copper tape cut to 1.5 mm", notes=[
            "Cut the film to the same outline as the EVA base, with the same",
            "  11 mm motor hole and lead notch. Polyimide, so it takes solder.",
            "Lay the film on the insole layout picture and mark the traces,",
            "  pads and sensor centres through it with a fine pen.",
            "Cut 6 mm copper tape into 1.5 mm strips with a steel rule and a",
            "  new blade. Lay each trace in one length, folding the tape at",
            "  corners rather than cutting it; burnish it flat.",
            "Eight tail pads 2 x 5 mm, 4 mm apart, 10 to 15 mm from the heel.",
            "Two tab pads at the end of each sensor tail, 2.54 mm apart.",
            "One crossover, beside the outer midfoot sensor: lay the outer",
            "  front-foot trace, cover it with an 8 x 8 mm polyimide patch,",
            "  then lay the midfoot supply branch over the patch.",
            "Check: a meter shows no connection between any two pads.",
        ], **flat, **OUTLINE_P2)
    S["103"] = lambda: sheet(
        m["spacer"], [m["film"], m["fsrs"], m["tail"]], "STC-DWG-103", "StepCue spacer foam: making sketch",
        "Closed-cell polyethylene foam 0.5 mm", notes=[
            "Cut the foam to the insole outline.",
            "Cut a window round each pressure sensor and its tail, 0.5 mm",
            "  clear all round: lay the sensors on the foam and trace round them.",
            "Cut a window at the heel, 16 mm long and 34 mm wide, for the tail",
            "  end and its eight pads, and a notch 11 mm wide at the heel edge.",
            "Cut a small window for the motor leads beside the motor, and a",
            "  10 x 10 mm window over the crossover patch.",
            "Do not cut over the motor: its top sticks to this foam.",
            "Fit: lay it over the carrier with the windows round the sensors;",
            "  its adhesive side down. Nothing in a window may stand proud of",
            "  the foam.",
            "Check: run a finger over it; no sensor edge or solder joint can",
            "  be felt above the foam.",
        ], **flat, **OUTLINE_P2)
    S["104"] = lambda: sheet(
        m["cover"], [m["spacer"], m["foam"]], "STC-DWG-104", "StepCue top cover: making sketch",
        "1.2 mm PU foam with textile face, cut from a thin commercial insole", notes=[
            "Cut a thin commercial insole to the same outline as the EVA base.",
            "Cut a notch 11 mm wide and 1.5 mm deep at the heel edge, on the",
            "  centre line, for the tail to turn up the heel counter.",
            "No other holes: the cover is the only layer the foot touches.",
            "Fit: bond it, textile face up, over the spacer with spray contact",
            "  adhesive suitable for footwear; roll it flat from the heel forward.",
            "Mark the five sensor centres lightly on the textile so the wearer",
            "  and tester can find them.",
            "Check: the finished insole is 4.5 mm thick (4.3 to 4.7 mm) at the",
            "  heel and the ball of the foot.",
        ], **flat, **OUTLINE_P2)
    base = C()["base"]
    S["105"] = lambda: sheet(
        m["base"], [m["cell"], m["module"], m["iface"], grey_shoe], "STC-DWG-105",
        "StepCue pod base with clip: making sketch", "PETG, 3D printed, 0.2 mm layers, 4 perimeters, 40 % infill",
        view_shape=Pos(0, 0, -p["pod_bot"]) * base, inset_view=(20, -150), **POD_P2, notes=[
            "Print lying on its side (a 37 mm side face on the bed), so the clip",
            "  bends along its layers and the largest span is 11.5 mm.",
            "Tray: 42 high, 37 wide, 13 deep, walls 1.5, open on the lid side;",
            "  corners rounded to 5 mm outside (3.5 mm inside). A groove 0.5",
            "  wide and 0.5 deep runs round the rim where the lid meets it.",
            "Clip: a 2 mm bridge over the counter top and a 1.5 mm finger",
            "  18 mm long, both curved to the heel counter (32 mm radius",
            "  inside). Fitted gap 3.8 mm; 2.8 mm as printed (1 mm grip).",
            "Round every edge of the finger to 0.5 mm: it rests on the heel.",
            "Tail slot 10 x 0.6 mm in the shoe-side wall, just under the roof.",
            "USB-C notch 9.4 mm wide in the bottom wall, open to the lid side.",
            "Four bosses 4 mm round, 5 mm deep, in the corners, 1.6 mm pilot",
            "  holes for the M2 screws.",
            "Check: the finger springs back after a 1 mm push; the slot passes",
            "  the tail; an M2 screw starts in each boss by hand.",
        ])
    S["106"] = lambda: sheet(
        part("Interface board, connector and cap", fuse("iface", "zif", "cap"), COL["iface"]),
        [m["base"], m["cell"], m["module"]], "STC-DWG-106", "StepCue interface board: making sketch",
        "Perfboard 2.54 mm pitch, cut to 20 x 12 mm; bought parts per bom/bom.csv line 10",
        view_shape=Pos(0, 0, -p["z_iface"][0]) * fuse("iface", "zif", "cap"), inset_view=(20, -150), notes=[
            "Cut perfboard to 20 x 12 mm (8 x 5 holes); file the edges.",
            "Front (lid side): the 12 mm tact switch, centred, with its 9.4 mm",
            "  round cap; the cap stands 1 mm out of the lid when fitted.",
            "Back: five 1 kohm divider resistors, the P-MOSFET that switches",
            "  the sensor supply, the motor N-MOSFET and its diode.",
            "Top edge: solder the tail connector's adapter board by its pin",
            "  row, standing up, latch to the lid side, opening upward.",
            "Wire it as the wiring picture shows, 30 AWG silicone wire, with",
            "  each wire 25 mm long so the board lifts out for checking.",
            "Fit: foam tape on the back; it sits on the cell above the module,",
            "  0.3 mm above it, with the cap through the lid's 10 mm hole.",
            "Check: the switch clicks through the cap; no joint stands more",
            "  than 2 mm off the back.",
        ])
    S["107"] = lambda: sheet(
        part("Lid", C()["lid"], COL["lid"]), [m["base"], m["iface"]], "STC-DWG-107", "StepCue pod lid: making sketch",
        "PETG, 3D printed flat, outer face down, 0.2 mm layers",
        view_shape=Pos(0, 0, -p["pod_bot"]) * C()["lid"], inset_view=(20, -150), **POD_P2, notes=[
            "Print flat, 42 x 37 x 2 mm with 5 mm round corners, outer face",
            "  on the bed (smooth face out).",
            f"Button hole 10 mm round, centred {p['z_button'] - p['pod_bot']:.1f} mm up from the lower edge.",
            f"LED window 3 mm round, {p['z_led'] - p['pod_bot']:.1f} mm up, 4.5 mm toward the outer side.",
            "Four screw holes 2.2 mm, countersunk 3.8 mm, at the corners: 3.3 mm",
            f"  in from the long sides and {p['bosses'][0][1] - p['pod_bot']:.1f} mm in from the short ends.",
            "Break the outer edges 0.5 mm so nothing catches on clothing.",
            "Fit: lies on the tray rim; the button cap passes through its hole",
            "  with 0.3 mm all round; four M2 x 6 countersunk thread-forming",
            "  screws into the bosses, heads flush.",
            "Check: the cap moves freely; the lid sits flat with no gap.",
        ])
    for k in (which or sorted(S)):
        out.append(S[k]())
    return out


# ----------------------------------------------------------------- the circuit layout on the carrier
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MPoly, Circle, Rectangle
    p = M.derived()
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    lay = M.trace_layout(p)
    fig = plt.figure(figsize=(14, 8.2), dpi=150)
    ax = fig.add_axes([0.03, 0.15, 0.94, 0.76]); ax.set_aspect("equal"); ax.set_axis_off()
    ol = M.outline(p)
    ax.add_patch(MPoly(ol, closed=True, fc="#FEF3C7", ec=INK, lw=1.0))
    mx, my = p["motor_xy"]
    hr = p["motor_d"] / 2 + p["pocket_clear"]
    ax.add_patch(Circle((mx, my), hr, fc="white", ec=INK, lw=0.8))
    ax.add_patch(Rectangle((mx - hr - 4.5, my - 2.2), 4.5 + 0.1, 4.4, fc="white", ec=INK, lw=0.8))
    for g in M.fsr_shapes2d(p):
        xs, ys = g.exterior.xy
        ax.fill(xs, ys, fc="none", ec=COL["fsrs"], lw=0.9, ls="--")
    colors = {"Lateral midfoot signal": "#B91C1C", "Fifth MTH signal": "#C2410C", "Heel signal": "#A16207",
              "First MTH signal": "#15803D", "Motor -": "#475569", "Motor +": "#0F172A", "Hallux signal": "#1D4ED8"}
    for k, g in lay["traces"].items():
        c = colors.get(k, "#7C3AED")
        xs, ys = g.exterior.xy
        ax.fill(xs, ys, fc=c, ec="none", alpha=0.9)
    for g in lay["pads"] + lay["tabs"] + lay["motor_pads"]:
        xs, ys = g.exterior.xy
        ax.fill(xs, ys, fc="#B45309", ec=INK, lw=0.3)
    xs, ys = lay["patch"].exterior.xy
    ax.fill(xs, ys, fc="#FDE68A", ec=INK, lw=0.6, alpha=0.8, zorder=3)
    xs, ys = lay["bridge"].exterior.xy
    ax.fill(xs, ys, fc="#7C3AED", ec="none", zorder=4)
    for g in M.strips2d(p):
        xs, ys = g.exterior.xy
        ax.fill(xs, ys, fc=COL["tail"], ec="none", zorder=4)
    ax.add_patch(Rectangle((-0.5, -p["tail_w"] / 2), p["slit_x"][0] + 0.5, p["tail_w"], fc=COL["tail"], ec="none", zorder=4))
    names = ("1 Heel", "2 Outer midfoot", "3 Ball, big-toe side", "4 Ball, little-toe side", "5 Big toe")
    spots = ((52, -50), (112, -52), (176, 60), (196, -60), (262, 56))
    lb = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9)
    for (x, y), n, (tx, ty) in zip(p["fsr_xy"], names, spots):
        ax.plot([x], [y], marker="+", color=COL["fsrs"], ms=7, mew=1.2)
        ax.annotate(f"{n}: {x:.0f}, {y:+.0f}", xy=(x, y), xytext=(tx, ty), fontsize=7.4, color=INK, ha="center",
                    va="center", bbox=lb, zorder=6, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    ax.annotate(f"Motor hole {2 * hr:.1f}: {mx:.0f}, {my:+.0f}", xy=(mx, my + hr), xytext=(112, 50), fontsize=7.4,
                color=INK, ha="center", va="center", bbox=lb, zorder=6, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    pc = M.crossing(p)
    ax.annotate("Crossover: an 8 x 8 patch over the little-toe-side\ntrace; the supply branch goes over the patch",
                xy=(pc[0] - 4, pc[1] - 4), xytext=(98, -70), fontsize=7.4, color=INK, ha="center", va="center", bbox=lb,
                arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6), zorder=6)
    ax.annotate("Tail end slit into 8 strips, each soldered to\na pad; pads 4 apart, 10 to 15 from the heel",
                xy=(9, -12), xytext=(-4, -62), fontsize=7.4, color=INK, ha="center", va="center", bbox=lb,
                arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6), zorder=6)
    # scales
    for x in range(0, 280, 20):
        ax.plot([x, x], [-76, -78], color=MUT, lw=0.6)
        ax.text(x, -80, f"{x}", ha="center", va="top", fontsize=6.8, color=MUT)
    ax.text(140, -87, "mm from the back of the heel", ha="center", va="top", fontsize=7.5, color=MUT)
    for y in range(-40, 60, 20):
        ax.plot([-26, -28], [y, y], color=MUT, lw=0.6)
        ax.text(-29, y, f"{y:+d}", ha="right", va="center", fontsize=6.8, color=MUT)
    ax.text(-42, 0, "mm from the centre line\n(+ toward the big toe)", rotation=90, ha="center", va="center", fontsize=7.2, color=MUT)
    ax.plot([-5, 285], [0, 0], color=MUT, lw=0.4, ls=(0, (8, 3, 2, 3)))
    ax.set_xlim(-50, 290); ax.set_ylim(-93, 66)
    fig.text(0.03, 0.965, "Insole circuit on the carrier film (right foot, seen from above)", fontsize=13, fontweight="bold",
             color=INK, va="top")
    fig.text(0.03, 0.925, "Positions in mm, taken from the model. Traces 1.5 wide, at least 0.8 apart and 1.5 inside the edge; "
             "dashed: the sensors and their tails, which sit on the tab pads at the tail ends. For a left foot, mirror it.",
             fontsize=8.5, color=MUT, va="top")
    key = [("#B91C1C", "Tail way 1: outer midfoot sensor"), ("#C2410C", "Way 2: ball, little-toe side"),
           ("#A16207", "Way 3: heel"), ("#7C3AED", "Way 4: sensor supply, to every sensor"),
           ("#15803D", "Way 5: ball, big-toe side"), ("#475569", "Way 6: motor -"), ("#0F172A", "Way 7: motor +"),
           ("#1D4ED8", "Way 8: big toe")]
    for i, (c, t) in enumerate(key):
        xk = 0.05 + (i % 4) * 0.235; yk = 0.105 - (i // 4) * 0.035
        fig.patches.append(Rectangle((xk, yk - 0.008), 0.018, 0.016, transform=fig.transFigure, fc=c, ec="none"))
        fig.text(xk + 0.024, yk, t, fontsize=8, color=INK, va="center")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "insole-layout.png", facecolor="white"); plt.close(fig)
    return OUT / "insole-layout.png"


def joint_at(parts, anchors, out, title, sub, elev, azim, size=(7, 5), dpi=160):
    """As build_views.joint, but each leader ends at a chosen 3D point and side, so labels in a
    tight section land on the right part. anchors: [(x, y, z, side)] in the same order as parts."""
    W, H = int(size[0] * dpi), int(size[1] * dpi * bv.PIC_HEIGHT)
    img, proj, verts = bv._raster([(p, p.color, p.alpha, (0, 0, 0)) for p in parts], elev, azim, W, H)
    fig, ax = bv._frame(size, dpi, title, sub)
    ax.imshow(img, interpolation="bilinear")
    for p, (x, y, z, side) in zip(parts, anchors):
        bv._label(ax, proj(__import__("numpy").array([x, y, z])), p.name, W, H, side=side)
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); bv.plt.close(fig)
    return out


# ----------------------------------------------------------------- joints
def joints(which=None):
    from build123d import Pos
    p = P()
    c = C()
    out = []
    zs = p["z_spacer"]
    mx, my = p["motor_xy"]
    pc = M.crossing(p)
    J = {}

    def j(n, parts, title, sub, **kw):
        return bv.joint([x for x in parts], OUT / f"joint-{n}.png", title, subtitle=sub, **kw)

    b1 = (82, 104, -33, -15, 2.0, 3.6)
    J["01"] = lambda: j("01", [
        part("Carrier film", win(c["film"], *b1), COL["film"]),
        part("Copper traces and tab pads", win(c["traces"], *b1), COL["traces"]),
        part("Sensor tail, lifted 3 mm to show the pads it is soldered to", Pos(0, 0, 3) * win(c["fsrs"], *b1), COL["fsrs"]),
        part("Spacer foam, window cut round the sensor", win(c["spacer"], *b1), COL["spacer"])],
        "Joint 1: a sensor's tail on its two tab pads (outer midfoot sensor)",
        "Seen from the outer side and above. Each of the two tabs is soldered to its pad; the spacer stands round the sensor",
        elev=38, azim=-120)
    b2 = (104, 132, my, my + 14, -0.6, 4.8)
    J["02"] = lambda: j("02", [
        part("EVA base", win(c["foam"], *b2), COL["foam"]),
        part("Carrier film", win(c["film"], *b2), COL["film"]),
        part("Motor lead on its pad", win(c["leads"] + c["traces"], *b2), COL["traces"]),
        part("Vibration motor", win(c["motor"], *b2), COL["motor"]),
        part("Spacer foam (motor stuck to its underside)", win(c["spacer"], *b2), COL["spacer"]),
        part("Top cover", win(c["cover"], *b2), COL["cover"])],
        "Joint 2: the motor in its hole, cut through its centre",
        "Seen from the inner side. The motor's top sticks to the spacer; it stands 0.1 mm clear of the shoe floor",
        elev=8, azim=-90)
    b3 = (-3, 19, -18, 18, 2.4, 3.4)
    J["03"] = lambda: j("03", [
        part("Carrier film", win(c["film"], *b3), COL["film"]),
        part("Tail pads (8)", win(c["traces"], *b3), COL["traces"]),
        part("Flex tail, end slit into 8 strips", win(c["tail"], *b3), COL["tail"]),
        part("Spacer foam (heel window)", win(c["spacer"], *b3), COL["spacer"])],
        "Joint 3: the tail end, slit and fanned onto its eight pads",
        "Seen from above at the heel. Each strip's bare end is soldered to its pad", elev=62, azim=-70)
    b4 = (pc[0] - 8, pc[0] + 8, pc[1] - 8, pc[1] + 8, 2.6, 3.3)
    J["04"] = lambda: j("04", [
        part("Carrier film", win(c["film"], *b4), COL["film"]),
        part("Little-toe-side trace (underneath)", win(c["traces"], *b4), COL["traces"]),
        part("Polyimide patch 8 x 8", win(c["patch"], *b4), COL["patch"]),
        part("Supply branch, over the patch", win(c["bridge"], *b4), "#7C3AED"),
        part("Spacer foam (window)", win(c["spacer"], *b4), COL["spacer"])],
        "Joint 4: the one place two traces cross",
        "Seen from above. The patch insulates the lower trace; the upper one bends over it", elev=40, azim=-60)
    b5 = (-8, 4.5, 0, 8, 32, 58.5)
    J["05"] = lambda: joint_at([
        part("Shoe heel counter (3.5 mm)", win(c["shoe"], *b5), COL["shoe"]),
        part("Flex tail, pressed on the counter", win(c["tail"], *b5), COL["tail"]),
        part("Pod: shoe-side wall and bridge over the top", win(c["base"], -8, 4.5, 0, 8, p["tail_top"], 58.5)
             + win(c["base"], -8, -0.6, 0, 8, 32, p["tail_top"]), COL["base"]),
        part("Clip finger, inside the counter", win(c["base"], -0.6, 4.5, 0, 8, 32, p["tail_top"] - 0.01), "#374151")],
        [(-1.75, 0, 44, "left"), (0.15, 0, 50, "right"), (-4.25, 0, 52, "left"), (1.05, 0, 40, "right")],
        OUT / "joint-05.png", "Joint 5: the clip over the heel counter, cut at the heel centre",
        "Seen from the inner side. The finger presses the tail on the counter; the bridge rides over both", elev=4, azim=-90)
    b6 = (-21, -1, 0, 20, 14, 58.5)
    J["06"] = lambda: j("06", [
        part("Pod base", win(c["base"], *b6), COL["base"]),
        part("Cell, taped to the wall", win(c["cell"] + c["cell_tape"], *b6), COL["cell"]),
        part("Controller module (USB-C down)", win(c["module"] + c["module_tape"], *b6), COL["module"]),
        part("Interface board", win(c["iface"] + c["iface_tape"], *b6), COL["iface"]),
        part("Tail connector", win(c["zif"], *b6), COL["zif"]),
        part("Flex tail, down into the connector", win(c["tail"], *b6), COL["tail"]),
        part("Button cap", win(c["cap"], *b6), COL["cap"]),
        part("Lid", win(c["lid"], *b6), COL["lid"])],
        "Joint 6: inside the pod, cut at the centre",
        "Seen from the inner side. The tail crosses over the cell and drops into the connector on the board",
        elev=4, azim=-90)
    by, bz = p["bosses"][3]
    b7 = (-19.5, -9, by, by + 4, bz - 4.5, bz + 3.5)
    J["07"] = lambda: joint_at([
        part("Pod base: corner boss", win(c["base"], *b7), COL["base"]),
        part("Lid", win(c["lid"], *b7), COL["lid"]),
        part("M2 x 6 countersunk screw", win(c["screws"], *b7), COL["screws"])],
        [(-12, by, bz - 1.8, "right"), (-17.5, by, bz - 3.5, "left"), (-14, by, bz, "right")],
        OUT / "joint-07.png", "Joint 7: a lid screw in its corner boss, cut through the screw",
        "Seen from the side, cut through the screw's centre. The screw forms its own thread in the 1.6 mm pilot hole",
        elev=12, azim=-80)
    b8 = (-20, -2, -12, 12, 14.0, 24)
    J["08"] = lambda: j("08", [
        part("Pod base: bottom wall and notch", win(c["base"], *b8), COL["base"]),
        part("Controller module, USB-C receptacle", win(c["module"], *b8), COL["module"]),
        part("Lid (closes the notch)", win(c["lid"], *b8), COL["lid"])],
        "Joint 8: the USB-C receptacle in the bottom wall, seen from below",
        "Looking up at the bottom wall: the receptacle mouth sits in the notch, 0.3 mm inside the outer face",
        elev=-80, azim=-110)
    for k in (which or sorted(J)):
        out.append(J[k]())
    return out


# ----------------------------------------------------------------- assembly steps
def steps(which=None):
    m = made()
    c = C()
    out = []
    S = {}

    def st(n, done, new, title, sub, **kw):
        return bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw)

    ins = dict(elev=32, azim=-62, size=(9, 5.6))
    pod = dict(elev=22, azim=-145)
    S[1] = lambda: st(1, [], [mv(m["foam"], (0, 0, 20))], "EVA base on the bench",
                      "Flat on a clean board, top face up; the motor hole is on the big-toe side", label_done=False, **ins)
    S[2] = lambda: st(2, [m["foam"]], [mv(m["film"], (0, 0, 25))], "carrier film onto the EVA base",
                      "Peel the backing; line up the two motor holes first, then roll the film flat from the heel", **ins)
    S[3] = lambda: st(3, [m["foam"], m["film"]], [mv(m["traces"], (0, 0, 25))], "copper traces, pads and the crossover patch",
                      "Lay each trace in one length as the insole layout shows; patch, then the branch over it",
                      label_done=False, **ins)
    S[4] = lambda: st(4, [m["foam"], m["film"], m["traces"]], [mv(m["fsrs"], (0, 0, 25))], "pressure sensors",
                      "Each sensor face up on its site, tail toward its two tab pads; solder each tab quickly",
                      label_done=False, **ins)
    S[5] = lambda: st(5, [m["foam"], m["film"], m["traces"], m["fsrs"]], [mv(m["tail"], (0, 0, 30))], "flex tail end onto its pads",
                      "Slit the last 10 mm into eight strips, fan them onto the pads and solder each; the tail runs off the heel",
                      label_done=False, **ins)
    S[6] = lambda: st(6, [m["foam"], m["film"], m["traces"], m["fsrs"], m["tail"]], [mv(m["motor"], (0, 0, 25))],
                      "vibration motor into its hole", "Adhesive face up, leads through the notch; solder each lead to its pad",
                      label_done=False, **ins)
    done7 = [m["foam"], m["film"], m["traces"], m["fsrs"], m["tail"], m["motor"]]
    S[7] = lambda: st(7, done7, [mv(m["spacer"], (0, 0, 25))], "spacer foam",
                      "Windows over the sensors, tail pads, leads and patch; press it down onto the motor's adhesive face",
                      label_done=False, **ins)
    S[8] = lambda: st(8, done7 + [m["spacer"]], [mv(m["cover"], (0, 0, 25))], "top cover",
                      "Spray contact adhesive; roll it on from the heel forward, notch over the tail",
                      label_done=False, **ins)
    S[9] = lambda: st(9, [m["base"]], [mv(m["cell"], (-30, 0, 0))], "cell into the pod base",
                      "Tape strip down the middle of the cell; press it flat on the shoe-side wall, lead at the bottom",
                      **pod)
    S[10] = lambda: st(10, [m["base"], m["cell"]], [mv(m["module"], (-30, 0, 0))], "controller module",
                       "Foam tape on its back; slide it in with the USB-C receptacle down into the notch", **pod)
    S[11] = lambda: st(11, [m["base"], m["cell"], m["module"]], [mv(m["iface"], (-30, 0, 0))],
                       "interface board with the connector and button cap",
                       "Foam tape on its back, above the module; connector on top with its latch open", **pod)
    pod_in = [m["base"], m["cell"], m["module"], m["iface"]]
    insole_parts = [m[k] for k in ("foam", "film", "traces", "fsrs", "spacer", "cover", "motor")]
    heel_box = (-30, 60, -60, 60, -1, 80)
    S[12] = lambda: st(12, [part("Finished insole (heel end shown)", win(fuse("foam", "film", "spacer", "cover"), *heel_box), COL["cover"])],
                       [mv(part("Flex tail (fitted at step 5)", c["tail"], COL["tail"]), (0, 0, 0)),
                        mv(part("Pod with its parts, lid off", fuse("base", "cell", "cell_tape", "module", "module_tape", "iface",
                                                                    "iface_tape", "zif", "cap"), COL["base"]), (-40, 0, 0))],
                       "tail into the pod and its connector",
                       "Lid off: feed the tail end through the slot under the roof, push it down into the connector, close the latch",
                       label_done=True, elev=22, azim=-135, size=(9, 5.6))
    S[13] = lambda: st(13, pod_in, [mv(m["lid"], (-30, 0, 0))], "lid and four screws",
                       "Button cap through its hole; four M2 x 6 countersunk screws, snug, heads flush", label_done=False, **pod)
    whole = part("Insole and pod, finished", fuse("foam", "film", "traces", "patch", "bridge", "fsrs", "tail", "motor",
                                                   "leads", "spacer", "cover", "base", "cell", "module", "iface", "zif",
                                                   "cap", "lid", "screws"), COL["base"])
    S[14] = lambda: st(14, [], [mv(whole, (0, 0, 75))], "into the shoe; clip over the heel counter",
                       "Insole flat in the shoe; tail up the inside of the heel; push the clip down over the counter top",
                       context=[part("Shoe", c["shoe"], COL["shoe"])], elev=24, azim=-125, size=(9, 5.6), label_done=False)
    for k in (which or sorted(S)):
        out.append(S[int(k)]())
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "StepCue prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules and a perfboard wired by hand; no circuit board is laid out. 30 AWG silicone wire in the pod; "
            "copper tape on the insole.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((2, 10), 28, 51, boxstyle="round,pad=0.4", fc="#FFFBEB", ec="#D97706", lw=1, ls="--"))
    ax.text(3.5, 59.8, "In the insole", fontsize=8, color=MUT, va="top")
    ax.add_patch(FancyBboxPatch((44, 10), 74, 51, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(45.5, 59.8, "In the heel pod", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.2, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        if sub:
            ax.text(x + w / 2, y + h - 3.9, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=1.6):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, BLK = "#B91C1C", "#1D4ED8", "#6B7280", "#111827"
    blk(4, 33, 16, 24, "Pressure sensors", "five FSR 402,\none tab of each to\nthe supply (way 4),\n"
        "the other to its own\nway (1, 2, 3, 5, 8)", "#0F766E")
    blk(4, 13, 16, 14, "Vibration motor", "coin, 3 V, 58 mA,\nways 6 (-) and 7 (+)", "#64748B")
    blk(33, 13, 9, 44, "", "", "#EA580C")
    ax.text(37.5, 35, "Flex tail, 8 ways, 1.0 mm pitch", rotation=90, ha="center", va="center", fontsize=8,
            fontweight="bold", color=INK)
    blk(47, 13, 11, 44, "", "", "#7C3AED")
    ax.text(52.5, 35, "Tail connector (ZIF)\non its adapter board", rotation=90, ha="center", va="center", fontsize=7.6,
            fontweight="bold", color=INK)
    blk(63, 13, 24, 44, "Interface board", "P-MOSFET: sensor supply on\nonly while sampling\n5 x 1 kohm from each sensor\n"
        "way to ground\nN-MOSFET and diode: motor\npause button to ground", "#16A34A")
    blk(92, 30, 24, 27, "Controller module", "XIAO nRF52840 Sense class\nIMU on board, charger,\nUSB-C (down), status LED\n\n"
        "suggested pins: A0 to A4\nsensors, D6 supply gate,\nD7 motor gate, D8 button", "#1D4ED8")
    blk(92, 13, 24, 12, "LiPo cell", "400 mAh, protected,\nleads to BAT+ and BAT-\npads under the module", "#B91C1C")
    for y in (36, 40, 44, 48, 52):
        wire([(20, y), (33, y)], BLU, 1.2)
    wire([(20, 55.5), (33, 55.5)], "#7C3AED", 1.4)
    lab(26.5, 44, "copper\ntraces", BLU, "center")
    wire([(20, 18), (33, 18)], GRY); wire([(20, 21), (33, 21)], RED)
    lab(26.5, 24.5, "motor -, +", GRY, "center")
    for y in range(16, 56, 5):
        wire([(42, y), (47, y)], "#EA580C", 2.4)
        wire([(58, y), (63, y)], GRY, 1.0)
    lab(44.5, 11.0, "push in, close latch", MUT, "center")
    lab(60.5, 11.0, "8 wires, 30 AWG", MUT, "center")
    wire([(87, 50), (92, 50)], BLU); lab(89.5, 52.3, "5 sensor\nlines", BLU, "center")
    wire([(87, 41), (92, 41)], GRY); lab(89.5, 43.3, "gates,\nbutton", GRY, "center")
    wire([(87, 34), (92, 34)], RED); lab(89.5, 36.3, "3.3 V,\nground", RED, "center")
    wire([(104, 25), (104, 30)], RED, 2.0); lab(104.8, 27.5, "cell leads", RED)
    ax.text(4, 7.2, "Safety: protected cell only, outside the shoe; never charge while worn or wet. Wire the cell last, "
            "after every other check (section 6 of the plan).", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(4, 4.2, "Tail ways, outer side first: 1 outer midfoot, 2 ball (little-toe side), 3 heel, 4 sensor supply, "
            "5 ball (big-toe side), 6 motor -, 7 motor +, 8 big toe. All circuits 4.2 V or less.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    if not args:
        for k, f in fns.items():
            print(k, "->", f())
    else:
        g, items = args[0], args[1:]
        f = fns[g]
        r = f(items) if items else f()
        print(g, items, "->", r)
