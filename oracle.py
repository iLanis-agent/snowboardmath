import math, json

def plural(n, one, many):
    return one if n == 1 else many

def tenths(x):
    return math.floor(x * 10 + 0.5) / 10

def fixed1(x):
    return f"{tenths(x):.1f}"

KG = [40, 50, 60, 70, 80, 90, 100]
CM = [140, 147, 152, 156, 159, 162, 165]
STYLE = ["freestyle", "all-mountain", "freeride"]
OFFSET = [-3, 0, 2]

def chart_length(kg):
    if kg <= KG[0]:
        return CM[0] + (kg - KG[0]) * (CM[1] - CM[0]) / (KG[1] - KG[0])
    for i in range(len(KG) - 1):
        if kg <= KG[i + 1]:
            return CM[i] + (kg - KG[i]) * (CM[i + 1] - CM[i]) / (KG[i + 1] - KG[i])
    n = len(KG) - 1
    return CM[n] + (kg - KG[n]) * (CM[n] - CM[n - 1]) / (KG[n] - KG[n - 1])

def length_truth(kg, style):
    if not (kg > 0):
        raise ValueError("the rider weight must be above zero")
    base = chart_length(kg) + OFFSET[style]
    return f"At {kg} kg the {STYLE[style]} chart reads {fixed1(base - 2)} to {fixed1(base + 2)} cm; the chin test never asked your weight honestly."

def width_truth(us, waist):
    if not (us > 0):
        raise ValueError("the boot size must be above zero")
    if not (waist > 0):
        raise ValueError("the waist width must be above zero")
    sole = (us + 17) * 10 + 20
    need = sole - 30
    dm = tenths(waist - need)
    if dm > 0:
        verdict = f"clears the drag line by {fixed1(dm)} mm honestly"
    elif dm < 0:
        verdict = f"comes {fixed1(-dm)} mm short of the drag line honestly"
    else:
        verdict = "lands exactly on the drag line honestly"
    return f"A US {us} boot measures about {fixed1(sole)} mm over the sole; the {waist} mm waist {verdict}."

def stance_truth(height, ref):
    if not (height > 0):
        raise ValueError("the rider height must be above zero")
    if not (ref > 0):
        raise ValueError("the reference stance must be above zero")
    rn = tenths(height * 0.29)
    dm = tenths(ref - rn)
    if dm > 0:
        verdict = f"sits {fixed1(dm)} cm wider honestly"
    elif dm < 0:
        verdict = f"sits {fixed1(-dm)} cm narrower honestly"
    else:
        verdict = "matches exactly honestly"
    return f"At {height} cm the stance chart reads {rn:.1f} cm; the board's {fixed1(ref)} cm reference {verdict}."

FNS = {"lengthTruth": length_truth, "widthTruth": width_truth, "stanceTruth": stance_truth}

CASES = [
    ("lengthTruth", [75, 1]),
    ("lengthTruth", [40, 1]),
    ("lengthTruth", [100, 1]),
    ("lengthTruth", [75, 0]),
    ("lengthTruth", [75, 2]),
    ("lengthTruth", [55, 1]),
    ("lengthTruth", [110, 1]),
    ("lengthTruth", [0, 1]),
    ("lengthTruth", [-10, 1]),
    ("widthTruth", [10, 255]),
    ("widthTruth", [9, 258]),
    ("widthTruth", [12, 260]),
    ("widthTruth", [8, 250]),
    ("widthTruth", [10, 270]),
    ("widthTruth", [7, 240]),
    ("widthTruth", [13, 265]),
    ("widthTruth", [0, 255]),
    ("widthTruth", [10, 0]),
    ("stanceTruth", [178, 56]),
    ("stanceTruth", [160, 51]),
    ("stanceTruth", [190, 55]),
    ("stanceTruth", [172, 50]),
    ("stanceTruth", [165, 48]),
    ("stanceTruth", [200, 60]),
    ("stanceTruth", [150, 44]),
    ("stanceTruth", [183, 53]),
    ("stanceTruth", [0, 56]),
    ("stanceTruth", [178, 0]),
]

out = []
for fn, args in CASES:
    rec = {"fn": fn, "args": args}
    try:
        rec["out"] = FNS[fn](*args)
    except ValueError as e:
        rec["err"] = str(e)
    out.append(rec)
    print(fn, args, "->", rec.get("out") or ("ERR: " + rec["err"]))

with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(f"{len(out)} cases written to expected.json")
