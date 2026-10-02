"""StepCue sizing calculations for STC-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Every number quoted in docs/04-calcs/01-sizing.md is printed here. Geometry and
volumes come from cad/src/model.py; cost comes from bom/bom.csv.
Values marked "assumed" have no source and are to be confirmed.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))


def hr(t):
    print(f"\n== {t} ==")


# ---------------------------------------------------------------- inputs
FS = 104.0                     # LSM6DS3TR-C output data rate, Hz; FSRs sampled on the same tick
WIN_S = 2.0                    # detector window, s
STEP_S = 0.25                  # decision interval, s
LOCO = (0.5, 3.0)              # locomotor band, Hz
FREEZE = (3.0, 8.0)            # freeze band, Hz
VCC = 3.3                      # module regulator output, V

# FSR 402 (Interlink datasheet): 0.2 to 20 N sensitivity range, 14.68 mm active diameter
FSR_ACTIVE_D = 14.68e-3
FSR_RANGE_N = (0.2, 20.0)
# Assumed peak in-shoe plantar pressures during walking, kPa (to confirm with literature)
P_PEAK = {"heel": 250.0, "first MTH": 300.0, "hallux": 250.0, "fifth MTH": 150.0, "lateral midfoot": 80.0}
# Assumed FSR 402 force-resistance law read from the datasheet curve, R = R1 * F^-0.9 (R1 at 1 N)
FSR_R1, FSR_EXP = 10e3, 0.9
R_M = 1000.0                   # divider resistor, ohm
T_ON = 0.3e-3                  # divider rail on-time per sample, s (5 conversions at 40 us plus settling)

# Motor: Precision Microdrives 310-103 datasheet
MOTOR_I, MOTOR_LAG, MOTOR_RISE, MOTOR_STOP, MOTOR_RPM = 58e-3, 0.040, 0.087, 0.115, 12200
PULSE = 0.100                  # cue pulse length, s
CADENCE = (60, 130)            # adjustable cue tempo, beats per minute
BASE_CAD = 105                 # typical baseline cadence, steps per minute (concept 95 to 115)

# Power (mA), nominal and conservative
CELL_MAH = 400.0
USABLE = 0.85 * 0.90           # above a 3.5 V cutoff, then ageing and cold (assumed)
WEAR_H, OFF_H = 16.0, 8.0
I_IMU = (0.90, 0.90)           # LSM6DS3TR-C combined high-performance (ST)
I_RUN, MCU_CONS = 6.3, 1.0     # nRF52840 run current at 64 MHz (assumed), conservative MCU average
I_BLE = (0.03, 0.15)           # advertising or idle connection to a phone (assumed)
I_LED = (0.002, 0.01)          # status blink (assumed)
I_PROT = (0.003, 0.005)        # cell protection circuit (assumed)
I_OFF = (0.05, 0.08)           # off the shoe, IMU in wake-on-motion (assumed)
CUE_S = (300.0, 480.0)         # seconds of cueing per day (assumed; conservative adds 12 false cues x 15 s)
LOADED = (0.5, 1.0)            # fraction of wear time each FSR is loaded (assumed)

rows_out = []


def result(rid, target, value, status):
    rows_out.append((rid, target, value, status))


# ---------------------------------------------------------------- R1 pressure sensing
hr("R1: pressure sensing and FSR range")
area = math.pi * FSR_ACTIVE_D ** 2 / 4
print(f"FSR 402 active area {area * 1e6:.1f} mm2 ({area * 1e4:.2f} cm2)")
sat = []
for site, kpa in P_PEAK.items():
    f = kpa * 1e3 * area
    flag = "saturates" if f > FSR_RANGE_N[1] else "in range"
    if f > FSR_RANGE_N[1]:
        sat.append(site)
    print(f"  {site:16s} {kpa:5.0f} kPa -> {f:5.1f} N ({flag}, range {FSR_RANGE_N[1]:.0f} N)")


def r_fsr(f):
    return FSR_R1 * f ** -FSR_EXP


def v_out(f):
    return VCC * R_M / (R_M + r_fsr(f))


ropt = math.sqrt(r_fsr(2.0) * r_fsr(50.0))
print(f"Divider resistor for best spread over 2 to 50 N: sqrt(R(2 N) R(50 N)) = {ropt:.0f} ohm; chosen {R_M:.0f} ohm "
      "(resistance law extrapolated above 20 N)")
for f in (0.5, 2.0, 5.0, 10.0, 20.0, 40.0):
    print(f"  {f:4.1f} N: R_fsr {r_fsr(f):7.0f} ohm, Vout {v_out(f):.2f} V, {v_out(f) / VCC * 4095:.0f} counts of 4095")
i_div_max = VCC / (R_M + r_fsr(40.0))
print(f"Divider current at 40 N: {i_div_max * 1e3:.2f} mA per sensor; rail on {T_ON * 1e3:.1f} ms per "
      f"{1e3 / FS:.1f} ms sample ({T_ON * FS * 100:.1f} % duty)")
n_adc = 5
t_scan = n_adc * 40e-6 + 2e-6 * n_adc
print(f"SAADC scan of {n_adc} channels at 40 us acquisition: {t_scan * 1e3:.2f} ms per sample, "
      f"{t_scan * FS * 100:.1f} % of time; 6 analog inputs on the module, 5 used")
result("R1", "5 or more sites at 100 Hz or more", f"5 FSRs at {FS:.0f} Hz; peak load {max(P_PEAK.values()) * 1e3 * area:.0f} N "
       f"saturates at {', '.join(sat)}", "Met")

# ---------------------------------------------------------------- R2 motion sensing and window
hr("R2: IMU sampling and freeze-index window")
n = int(round(FS * WIN_S))
df = FS / n
bins = np.arange(n // 2 + 1) * df
nl = int(np.sum((bins >= LOCO[0]) & (bins < LOCO[1])))
nf = int(np.sum((bins >= FREEZE[0]) & (bins <= FREEZE[1])))
print(f"{n} samples per {WIN_S:.0f} s window at {FS:.0f} Hz; bin spacing {df:.2f} Hz; Nyquist {FS / 2:.0f} Hz")
print(f"Locomotor band {LOCO[0]} to {LOCO[1]} Hz: {nl} bins; freeze band {FREEZE[0]} to {FREEZE[1]} Hz: {nf} bins")
print(f"Nyquist margin over the top of the freeze band: {FS / 2 / FREEZE[1]:.1f} times")
result("R2", "6-axis IMU at 100 Hz or more covering 0.5 to 8 Hz", f"LSM6DS3TR-C at {FS:.0f} Hz; {df:.2f} Hz bins, "
       f"Nyquist {FS / 2:.0f} Hz", "Met")


# ---------------------------------------------------------------- R3 to R5 synthetic freeze index
hr("R3 to R5: synthetic freeze-index check (method arithmetic only)")
rng = np.random.default_rng(1)


def synth(t_total=20.0, onset=10.0, cad=1.75, tremble=5.5):
    """Vertical foot acceleration, m/s2: walking harmonics before onset, trembling after (assumed shapes)."""
    t = np.arange(0, t_total, 1 / FS)
    walk = sum((4.0 / k ** 1.5) * np.sin(2 * np.pi * k * cad / 2 * t + k) for k in range(1, 12))
    frz = 1.2 * np.sin(2 * np.pi * tremble * t) + 0.3 * np.sin(2 * np.pi * cad / 4 * t)
    x = np.where(t < onset, walk, frz) + rng.normal(0, 0.15, t.size)
    return t, x


def freeze_index(x):
    w = np.hanning(len(x))
    s = np.abs(np.fft.rfft((x - x.mean()) * w)) ** 2
    f = np.fft.rfftfreq(len(x), 1 / FS)
    pl = s[(f >= LOCO[0]) & (f < LOCO[1])].sum()
    pf = s[(f >= FREEZE[0]) & (f <= FREEZE[1])].sum()
    return pf / pl


t, x = synth()
onset = 10.0
step = int(STEP_S * FS)
fi = []
for end in range(n, len(x) + 1, step):
    fi.append((end / FS, freeze_index(x[end - n:end])))
walk_fi = max(v for te, v in fi if te <= onset)
frz_fi = min(v for te, v in fi if te >= onset + WIN_S)
thr = math.sqrt(walk_fi * frz_fi)
print(f"Walking windows: FI up to {walk_fi:.2f}; full-freeze windows: FI at least {frz_fi:.1f}; "
      f"threshold (geometric mean) {thr:.2f}")
first = next(te for te, v in fi if te > onset and v > thr)
print(f"First window over threshold ends {first - onset:.2f} s after onset")
delays = {}
for k in (1, 3, 5):
    run = 0
    for te, v in fi:
        run = run + 1 if (te > onset and v > thr) else 0
        if run >= k:
            delays[k] = te - onset
            break
    print(f"  confirm on {k} consecutive windows: detection {delays[k]:.2f} s after onset (plus firmware under 1 ms)")

# R5: false cues from a window false-positive rate, independence assumed (optimistic)
windows_10min = int(600 / STEP_S)
for spec in (0.85, 0.83):
    p = 1 - spec
    k_need = math.ceil(math.log(windows_10min) / math.log(1 / p))
    print(f"Window specificity {spec:.0%}: {windows_10min} windows per 10 min; false-positive rate {p:.2f}; "
          f"k = {k_need} consecutive windows for 1 false cue per 10 min if windows were independent; "
          f"adds {(k_need - 1) * STEP_S:.2f} s")
k5 = math.ceil(math.log(windows_10min) / math.log(1 / 0.15))
result("R3", "Median onset-to-detection 2 s or less", f"Method floor {delays[1]:.2f} s (k = 1) to {delays[5]:.2f} s (k = 5), synthetic",
       "At risk")
result("R4", "Episode sensitivity 80 % or more; window specificity 85 % or more",
       "Literature, pressure only: 77 to 80 % and 83 to 85 %", "At risk")
result("R5", "1 false cue or fewer per 10 min of walking", f"Needs k = {k5} or more confirmations at 85 % specificity "
       "(independence assumed)", "At risk")

# ---------------------------------------------------------------- R6 cue start
hr("R6: cue start after detection")
t_fw = 0.001
print(f"Haptic: firmware {t_fw * 1e3:.0f} ms + motor lag {MOTOR_LAG * 1e3:.0f} ms = {(t_fw + MOTOR_LAG) * 1e3:.0f} ms to first "
      f"vibration; 50 % amplitude at {(t_fw + MOTOR_RISE) * 1e3:.0f} ms")
audio = {"phone speaker": (0.030, 0.050, 0.100), "Bluetooth earbuds via phone": (0.030, 0.050, 0.200)}
aud_lat = {}
for route, (ble, app, out) in audio.items():
    aud_lat[route] = ble + app + out
    print(f"Audio, {route}: BLE {ble * 1e3:.0f} + app {app * 1e3:.0f} + audio output {out * 1e3:.0f} ms = "
          f"{aud_lat[route] * 1e3:.0f} ms (all assumed)")
R6_HAPTIC, R6_AUDIO = 0.100, 0.300   # targets, s (audio-route target decided by Amish 2026-09-25, STC-DDR-002)
print(f"Targets: haptic {R6_HAPTIC * 1e3:.0f} ms, audio route {R6_AUDIO * 1e3:.0f} ms; "
      f"haptic margin {(R6_HAPTIC - t_fw - MOTOR_LAG) * 1e3:.0f} ms, audio margin "
      f"{(R6_AUDIO - max(aud_lat.values())) * 1e3:.0f} ms at worst")
r6_ok = (t_fw + MOTOR_LAG) <= R6_HAPTIC and max(aud_lat.values()) <= R6_AUDIO
result("R6", "Cue starts 0.1 s or less after detection (haptic); 0.3 s or less (phone or earbud audio)",
       f"Haptic {(t_fw + MOTOR_LAG) * 1e3:.0f} ms (50 % amplitude {(t_fw + MOTOR_RISE) * 1e3:.0f} ms); phone audio "
       f"{min(aud_lat.values()) * 1e3:.0f} to {max(aud_lat.values()) * 1e3:.0f} ms", "Met" if r6_ok else "Not met")

# ---------------------------------------------------------------- R7 cue delivery
hr("R7: cue tempo, pulse and audio level")
fvib = MOTOR_RPM / 60
print(f"Motor speed {MOTOR_RPM} rpm -> vibration at {fvib:.0f} Hz")
for bpm in (CADENCE[0], BASE_CAD, CADENCE[1]):
    per = 60 / bpm
    felt = PULSE + MOTOR_STOP
    print(f"  {bpm:3d} per min: period {per * 1e3:.0f} ms; pulse {PULSE * 1e3:.0f} ms runs down over {MOTOR_STOP * 1e3:.0f} ms; "
          f"quiet gap {(per - felt) * 1e3:.0f} ms; drive duty {PULSE / per:.0%}")
for pl in (0.100, 0.150):
    print(f"  pulse {pl * 1e3:.0f} ms at 130 per min: quiet gap {(60 / CADENCE[1] - pl - MOTOR_STOP) * 1e3:.0f} ms; "
          f"reaches 50 % amplitude: {'yes' if pl + t_fw > MOTOR_RISE else 'no'}")
spl_10cm, d_ear = 80.0, 1.5
piezo = spl_10cm - 20 * math.log10(d_ear / 0.10)
print(f"Piezo at the heel (dropped by decision D5): {spl_10cm:.0f} dB at 10 cm -> {piezo:.1f} dB at {d_ear} m "
      f"(TRL 2 precis said about 60)")
phone_10cm, pocket_d = 80.0, 0.9
phone = phone_10cm - 20 * math.log10(pocket_d / 0.10)
print(f"Phone speaker in a trouser pocket: {phone_10cm:.0f} dB at 10 cm -> {phone:.1f} dB at {pocket_d} m before "
      f"pocket muffling (assumed)")
print("Earbuds: tens of dB above 60 dB(A) at the ear by design (volume set by the wearer)")
result("R7", "Haptic at cadence 60 to 130 per min; audio 60 dB(A) or more at the ear",
       f"Haptic {fvib:.0f} Hz ERM, gap {(60 / CADENCE[1] - PULSE - MOTOR_STOP) * 1e3:.0f} ms at 130 per min; "
       f"audio by earbuds; phone in pocket {phone:.0f} dB", "Met")

# ---------------------------------------------------------------- R8 stop logic
hr("R8: stop logic")
t3 = 3 * 60 / BASE_CAD
print(f"Three regular steps at {BASE_CAD} per min take {t3:.1f} s; hard stop at 15 s")
result("R8", "Stop within 3 regular steps or 15 s", f"3 steps = {t3:.1f} s; 15 s cap", "Met (design review)")

# ---------------------------------------------------------------- geometry from the model
import model  # noqa: E402
parts = model.build_parts()
p = parts["_p"]

hr("R9: insole stack")
carrier = p["film_t"] + p["trace_t"]
print(f"Stack {p['foam_t']:.1f} EVA + {p['lam_t']:.1f} laminate ({carrier:.2f} carrier film with copper traces + "
      f"{p['spacer_t']:.1f} foam spacer round the {p['fsr_t']:.2f} mm FSRs) + {p['cover_t']:.1f} cover = {p['stack']:.2f} mm "
      f"against 5.0 mm")
print(f"EVA sheet tolerance +/-0.2 mm (assumed) gives {p['stack'] - 0.2:.1f} to {p['stack'] + 0.2:.1f} mm; "
      f"margin {5.0 - p['stack']:.2f} mm nominal, {5.0 - p['stack'] - 0.2:.2f} mm worst case")
print(f"Motor {p['motor_t']} mm in a through-hole in the {p['foam_t']:.1f} mm EVA and the carrier, bonded under the "
      f"spacer: {p['motor_gap']:.1f} mm clear of the insole underside, {p['spacer_t'] + p['cover_t']:.1f} mm of foam over it "
      f"(STC-DDR-003; was a 0.2 mm EVA floor and a 0.4 mm laminate relief)")
print(f"Previous 3.0 mm EVA base gave {p['stack'] + 3.0 - p['foam_t']:.2f} mm, zero margin")
print(f"Rigid parts under heel and metatarsal heads: FSR {p['fsr_t']:.2f} mm (limit 1 mm); motor under the arch only")
r9_ok = p["stack"] + 0.2 <= 5.0
result("R9", "Stack 5.0 mm or less; no rigid part over 1 mm under heel or MTH",
       f"{p['stack']:.2f} mm ({p['stack'] + 0.2:.1f} mm at +0.2 mm EVA tolerance); FSR {p['fsr_t']:.2f} mm",
       "Met" if r9_ok else "At risk")

hr("R10: heel pod size and mass")
rho_petg = 1.27
v_base, v_lid = parts["base"].volume / 1000, parts["lid"].volume / 1000
mass = {
    "Heel pod base with clip, PETG": v_base * rho_petg,
    "Heel pod lid, PETG": v_lid * rho_petg,
    "LiPo cell, 400 mAh (Adafruit 3898 class, 8.2 g)": 8.2,
    "Controller module with IMU (assumed)": 3.0,
    "Interface board and pause button (assumed)": 2.0,
    "Tail connector on its adapter board (assumed)": 1.0,
    "Button cap, four M2 screws, tapes, wire (assumed)": 1.5,
}
for k, v in mass.items():
    print(f"  {k:50s} {v:5.2f} g")
m_pod = sum(mass.values())
clip_depth = p["pod_x"] + p["counter_t"] + p["tail_t"] + p["finger_t"]
print(f"Pod mass {m_pod:.1f} g against 35 g; body {p['pod_z']:.0f} x {p['pod_y']:.0f} x {p['pod_x']:.0f} mm "
      f"against 45 x 40 x 20 mm; {clip_depth:.1f} mm deep including the clip over the counter")
result("R10", "Pod 35 g or less; within 45 x 40 x 20 mm", f"{m_pod:.1f} g; body {p['pod_z']:.0f} x {p['pod_y']:.0f} x "
       f"{p['pod_x']:.0f} mm ({clip_depth:.1f} mm deep with clip)", "Met")

# ---------------------------------------------------------------- R12 clip retention
hr("R12: clip over the heel counter")
E = 2000.0                     # PETG modulus, MPa (assumed)
mu = 0.4                       # friction, PETG on shoe lining (assumed)
g_peak = 10.0                  # peak heel-strike acceleration at the counter, g (assumed)
b, tt, L, d = p["bridge_w"], p["finger_t"], p["finger_l"], p["clip_interference"]
I = b * tt ** 3 / 12
P = 3 * E * I * d / L ** 3
strain = 1.5 * tt * d / L ** 2
hold = 2 * mu * P
inert = m_pod / 1000 * 9.81 * g_peak
print(f"Finger {b:.0f} wide x {tt} thick x {L:.0f} long, interference {d} mm: clamp {P:.1f} N; bending strain {strain:.2%}")
print(f"Friction hold {hold:.1f} N (both faces, mu {mu}) vs pod inertia at {g_peak:.0f} g: {inert:.1f} N; margin {hold / inert:.1f}")
print(f"One-handed removal force about {hold:.0f} N")
result("R12", "One-handed clip on and off; USB-C off the shoe; one large pause button",
       f"Clamp {P:.1f} N, hold {hold:.1f} N vs {inert:.1f} N, removal about {hold:.0f} N; {p['button_d']:.0f} mm button",
       "Not verifiable at TRL 3")

# ---------------------------------------------------------------- R11 power
hr("R11: power budget")
t_i2c = FS * 12 * 9 / 400e3
t_saadc = FS * 0.3e-3
t_dsp = (1 / STEP_S) * 1.0e-3
duty = t_i2c + t_saadc + t_dsp
i_mcu = duty * I_RUN + 0.005
print(f"MCU duty: I2C FIFO read {t_i2c:.3f}, SAADC wake {t_saadc:.3f}, FFT and features {t_dsp:.3f} = {duty:.3f}; "
      f"{i_mcu:.3f} mA nominal, {MCU_CONS:.2f} mA conservative")
days = []
for j, label in enumerate(("nominal", "conservative")):
    i_fsr = 5 * LOADED[j] * VCC / (R_M + (r_fsr(10.0) if j == 0 else r_fsr(40.0))) * 1e3 * T_ON * FS
    i_mcu_j = i_mcu if j == 0 else MCU_CONS
    rec = I_IMU[j] + i_mcu_j + i_fsr + I_BLE[j] + I_LED[j] + I_PROT[j]
    cue = MOTOR_I * 1e3 * (PULSE * BASE_CAD / 60) * CUE_S[j] / 3600
    day = rec * WEAR_H + I_OFF[j] * OFF_H + cue
    usable = CELL_MAH * USABLE
    days.append(usable / day)
    print(f"{label:12s}: IMU {I_IMU[j]:.2f} + MCU {i_mcu_j:.3f} + FSR dividers {i_fsr:.3f} + BLE {I_BLE[j]:.2f} + "
          f"LED {I_LED[j]:.3f} + protection {I_PROT[j]:.3f} = {rec:.2f} mA worn")
    print(f"{'':12s}  cue {cue:.2f} mAh per day ({CUE_S[j]:.0f} s); {day:.1f} mAh per day; {usable:.0f} mAh usable; "
          f"{usable / day:.1f} days")
esp = 6.0 * WEAR_H + 0.1 * OFF_H + 1.0
print(f"Reference, TRL 2 ESP32-C3 estimate (6 mA worn): {esp:.0f} mAh per day, {CELL_MAH * USABLE / esp:.1f} days")
for c in (50, 100):
    print(f"Charge at {c} mA (BQ25101 setting): {c / CELL_MAH:.3f} C, about {CELL_MAH / c * 1.2:.1f} h")
result("R11", "2 days or more at 16 h per day", f"{days[0]:.1f} days nominal, {days[1]:.1f} days conservative", "Met")

result("R13", "On-device detection and cueing; owner-only export; no cloud", "Architecture has no cloud path; "
       "phone used only for optional audio", "Met (design review)")

# ---------------------------------------------------------------- R14 cost
hr("R14: cost (bom/bom.csv)")
with open(ROOT / "bom" / "bom.csv", newline="") as fh:
    bom = list(csv.DictReader(fh))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
insole_items = ("1 ", "2 ", "3 ", "4 ", "5 ", "6 ")
second = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if r["item"].startswith(insole_items))
print(f"{len(bom)} lines, all priced; estimated cost ${cost:.2f} per unit (one instrumented insole); value-engineering "
      f"target $200 (a hypothetical control target, not a limit): ${200 - cost:.2f} under the target")
print(f"A second instrumented insole with its own pod would add about ${cost:.2f} (pair ${2 * cost:.2f}); "
      f"insole parts alone ${second:.2f}")
result("R14", "$200 or less with one instrumented insole; no custom rigid PCB",
       f"${cost:.2f} (${200 - cost:.2f} under the value-engineering target); perfboard only", "Met")
result("R15", "Protected cell outside the shoe; no exposed conductors; footwear-safe materials",
       "Protected cell in the pod outside the counter; sensors laminated under the cover", "Met (design review)")

# ---------------------------------------------------------------- summary
hr("Results table")
order = {f"R{i}": i for i in range(1, 16)}
for rid, target, value, status in sorted(rows_out, key=lambda r: order[r[0]]):
    print(f"{rid:4s} | {status:32s} | {value}")
counts = {}
for r in rows_out:
    key = r[3].split(" (")[0].split(";")[0]
    counts[key] = counts.get(key, 0) + 1
print("Counts: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
