import json, math

W, H = 512, 512
FR = 60
DURATION = 10 * FR  # 600 frames = 10s

def static_prop(k): return {"a": 0, "k": k}
def animated_prop(keyframes):
    return {"a": 1, "k": [{"t": t, "s": s, "i": {"x": [0.5], "y": [1]}, "o": {"x": [0.5], "y": [0]}} if i < len(keyframes)-1 else {"t": t, "s": s} for i, (t, s) in enumerate(keyframes)]}

def make_text_layer(name, text, size, x, y, fc, ip, opacity_kf):
    return {
        "ty": 5, "nm": name, "ip": ip, "op": DURATION, "st": 0,
        "ks": {
            "o": animated_prop(opacity_kf),
            "r": static_prop(0), "p": static_prop([x, y, 0]),
            "a": static_prop([0, 0, 0]), "s": static_prop([100, 100, 100])
        },
        "t": {
            "d": {"k": [{"s": {"s": size, "f": "Arial", "t": text, "j": 0, "tr": 0, "lh": size*1.2, "ls": 0, "fc": fc}, "t": 0}]},
            "p": {}, "m": {"g": 1, "a": static_prop([0, 0])}
        }
    }

def make_shape_layer(name, shapes, ip=0, opacity_kf=None):
    if opacity_kf is None:
        opacity_kf = [(0, [100]), (DURATION, [100])]
    return {
        "ty": 4, "nm": name, "ip": ip, "op": DURATION, "st": 0,
        "ks": {
            "o": animated_prop(opacity_kf),
            "r": static_prop(0), "p": static_prop([0, 0, 0]),
            "a": static_prop([0, 0, 0]), "s": static_prop([100, 100, 100])
        },
        "shapes": shapes
    }

def make_path(points, closed=False):
    # Simple bezier with straight lines (i/o tangents = 0)
    verts = []
    ins = []
    outs = []
    for p in points:
        verts.append(p)
        ins.append([0, 0])
        outs.append([0, 0])
    return {
        "ty": "sh",
        "ks": static_prop({"c": closed, "v": verts, "i": ins, "o": outs})
    }

def make_stroke(color, width, opacity=100):
    return {"ty": "st", "c": static_prop(color), "o": static_prop(opacity), "w": static_prop(width), "lc": 2, "lj": 2}

def make_fill(color, opacity=100):
    return {"ty": "fl", "c": static_prop(color), "o": static_prop(opacity)}

def make_group(name, items):
    items.append({"ty": "tr", "p": static_prop([0, 0]), "a": static_prop([0, 0]), "s": static_prop([100, 100]), "r": static_prop(0), "o": static_prop(100)})
    return {"ty": "gr", "nm": name, "it": items}

# Curved path helper (simple quadratic approximation)
def curve_points(start, cp1, cp2, end, segments=8):
    pts = [start]
    for i in range(1, segments):
        t = i / segments
        # Cubic bezier
        x = (1-t)**3 * start[0] + 3*(1-t)**2*t * cp1[0] + 3*(1-t)*t**2 * cp2[0] + t**3 * end[0]
        y = (1-t)**3 * start[1] + 3*(1-t)**2*t * cp1[1] + 3*(1-t)*t**2 * cp2[1] + t**3 * end[1]
        pts.append([round(x, 2), round(y, 2)])
    pts.append(end)
    return pts

# Path with animated trim (stroke draw-on)
def make_animated_path_layer(name, points, stroke_w, stroke_color, start_frame, draw_duration, ip=0):
    trim_end = animated_prop([
        (start_frame, [0]),
        (start_frame + draw_duration, [100])
    ])
    shapes = [make_group(name, [
        make_path(points),
        make_stroke(stroke_color, stroke_w),
        {"ty": "tm", "s": static_prop(0), "e": trim_end, "o": static_prop(0), "m": 1}
    ])]
    return make_shape_layer(name, shapes, ip=ip)

# Czerwone X (two crossed rectangles)
def make_x_layer(x, y, size, ip, appear_duration):
    s1 = make_group("x1", [
        {"ty": "rc", "p": static_prop([0, 0]), "s": static_prop([size, size/5]), "r": static_prop(0)},
        make_fill([0.93, 0.27, 0.27, 1]),
        {"ty": "tr", "p": static_prop([0, 0]), "a": static_prop([0, 0]), "s": static_prop([100, 100]), "r": static_prop(45), "o": static_prop(100)}
    ])
    s2 = make_group("x2", [
        {"ty": "rc", "p": static_prop([0, 0]), "s": static_prop([size, size/5]), "r": static_prop(0)},
        make_fill([0.93, 0.27, 0.27, 1]),
        {"ty": "tr", "p": static_prop([0, 0]), "a": static_prop([0, 0]), "s": static_prop([100, 100]), "r": static_prop(-45), "o": static_prop(100)}
    ])
    # Group both with position and animated scale
    opacity_kf = [(ip, [0]), (ip + appear_duration, [100])]
    scale_kf = [(ip, [0, 0]), (ip + appear_duration, [100, 100])]
    return {
        "ty": 4, "nm": name, "ip": ip, "op": DURATION, "st": 0,
        "ks": {
            "o": animated_prop(opacity_kf),
            "r": static_prop(0), "p": static_prop([x, y, 0]),
            "a": static_prop([0, 0, 0]), "s": animated_prop(scale_kf)
        },
        "shapes": [s1, s2]
    }

# Czerwona kropka (circle)
def make_dot_layer(x, y, r, ip, appear_duration):
    opacity_kf = [(ip, [0]), (ip + appear_duration, [100])]
    scale_kf = [(ip, [0, 0]), (ip + appear_duration, [120, 120])]
    return {
        "ty": 4, "nm": "red dot", "ip": ip, "op": DURATION, "st": 0,
        "ks": {
            "o": animated_prop(opacity_kf),
            "r": static_prop(0), "p": static_prop([x, y, 0]),
            "a": static_prop([0, 0, 0]), "s": animated_prop(scale_kf)
        },
        "shapes": [make_group("dot", [
            {"ty": "el", "p": static_prop([0, 0]), "s": static_prop([r*2, r*2])},
            make_fill([0.93, 0.27, 0.27, 1])
        ])]
    }

# CTA Button shape
def make_cta_layer(x, y, w, h, ip, appear_duration):
    opacity_kf = [(ip, [0]), (ip + appear_duration, [100])]
    pos_kf = [(ip, [x, y+20, 0]), (ip + appear_duration, [x, y, 0])]
    return {
        "ty": 4, "nm": "CTA", "ip": ip, "op": DURATION, "st": 0,
        "ks": {
            "o": animated_prop(opacity_kf),
            "r": static_prop(0), "p": animated_prop(pos_kf),
            "a": static_prop([0, 0, 0]), "s": static_prop([100, 100, 100])
        },
        "shapes": [make_group("cta", [
            {"ty": "rc", "p": static_prop([0, 0]), "s": static_prop([w, h]), "r": static_prop(6)},
            make_fill([0.93, 0.27, 0.27, 1])
        ])]
    }

# Background layer with slotted color
def make_bg_layer():
    return {
        "ty": 4, "nm": "bg", "ip": 0, "op": DURATION, "st": 0,
        "ks": {
            "o": static_prop(100), "r": static_prop(0),
            "p": static_prop([W/2, H/2, 0]), "a": static_prop([0, 0, 0]),
            "s": static_prop([100, 100, 100])
        },
        "shapes": [make_group("bg", [
            {"ty": "rc", "p": static_prop([0, 0]), "s": static_prop([W, H]), "r": static_prop(0)},
            {"ty": "fl", "c": {"sid": "bgColor"}, "o": static_prop(100)}
        ])]
    }

# Main path definitions
# Start from left center
SX, SY = 50, 256
CX, CY = 256, 256

# Path 0: main horizontal line
main_line = [[SX, SY], [CX-20, SY]]

# Path 1: upper branch (curved up-right)
p1 = curve_points([CX-20, SY], [300, 220], [360, 180], [430, 140], 10)

# Path 2: lower branch (curved down-right)
p2 = curve_points([CX-20, SY], [300, 292], [360, 340], [430, 380], 10)

# Path 3: middle branch (slight wave right)
p3 = curve_points([CX-20, SY], [320, 246], [400, 266], [480, 256], 10)

# Path 4: from upper branch, sub-branch up
p4 = curve_points([360, 180], [390, 130], [440, 100], [490, 80], 8)

# Path 5: from upper branch, sub-branch down-cross
p5 = curve_points([340, 200], [380, 240], [440, 260], [490, 290], 8)

# Path 6: from lower branch, sub-branch down
p6 = curve_points([360, 340], [400, 390], [450, 430], [490, 460], 8)

# Path 7: from lower branch, sub-branch up-cross
p7 = curve_points([340, 320], [380, 280], [440, 240], [490, 200], 8)

# Path 8: from middle, sub-branch slight up
p8 = curve_points([400, 256], [440, 226], [470, 210], [500, 190], 8)

# Path 9: from middle, sub-branch slight down
p9 = curve_points([400, 256], [440, 286], [470, 300], [500, 320], 8)

# Build layers (top to bottom order)
layers = []

# Logo text (fade in 0-1s)
layers.append(make_text_layer("logo", "SCALAC.AI", 18, 70, 50, [1, 1, 1], 0, [(0, [0]), (30, [100])]))

# Headline (appear 1.5-3s)
layers.append(make_text_layer("headline", "Your AI stack\ngrew faster\nthan your\narchitecture", 42, 60, 160, [1, 1, 1], 0, [(60, [0]), (90, [100])]))

# Red dot after "architecture" (bounce in at 3s)
layers.append(make_dot_layer(330, 295, 5, 180, 15))

# Subtitle (slide in 3-4s)
layers.append(make_text_layer("subtitle", "We help enterprise teams\nbring structure to\ngrowing AI systems.", 16, 60, 360, [0.7, 0.7, 0.7], 0, [(120, [0]), (150, [100])]))

# CTA button (4-4.5s)
layers.append(make_cta_layer(60, 420, 220, 40, 180, 15))
layers.append(make_text_layer("cta_text", "Book an architecture review  →", 14, 170, 440, [1, 1, 1], 0, [(195, [0]), (210, [100])]))

# Main line (draws 0-1.5s)
layers.append(make_animated_path_layer("main", main_line, 3, [1, 1, 1, 1], 0, 45, 0))

# Branches appear 4-6s, draw over 2s each
branches = [
    ("branch1", p1, 2.5, 4*FR, 2*FR),
    ("branch2", p2, 2.5, 4*FR, 2*FR),
    ("branch3", p3, 2.5, 4*FR+10, 2*FR),
    ("branch4", p4, 1.5, 5*FR, 1.5*FR),
    ("branch5", p5, 1.5, 5*FR+5, 1.5*FR),
    ("branch6", p6, 1.5, 5*FR+10, 1.5*FR),
    ("branch7", p7, 1.5, 5*FR+15, 1.5*FR),
    ("branch8", p8, 1.5, 6*FR, 1.5*FR),
    ("branch9", p9, 1.5, 6*FR+5, 1.5*FR),
]
for name, pts, w, sf, dd in branches:
    layers.append(make_animated_path_layer(name, pts, w, [1, 1, 1, 1], sf, dd, sf))

# Red X marks on some dead ends (appear 7-8.5s)
x_positions = [
    (490, 80),   # end of p4
    (490, 290),  # end of p5
    (490, 460),  # end of p6
    (490, 200),  # end of p7
]
for i, (x, y) in enumerate(x_positions):
    layers.append(make_x_layer(x, y, 10, 7*FR + i*10, 15))

# Background (last layer)
layers.append(make_bg_layer())

lottie = {
    "v": "5.7.0",
    "fr": FR,
    "ip": 0,
    "op": DURATION,
    "w": W,
    "h": H,
    "assets": [],
    "slots": {
        "bgColor": {"p": {"a": 0, "k": [0, 0, 0, 1]}}
    },
    "layers": layers
}

with open("public/lottie.json", "w") as f:
    json.dump(lottie, f)

# Also write controls.json
controls = {
    "controls": [
        {"sid": "bgColor", "label": "Background color"}
    ]
}
with open("public/controls.json", "w") as f:
    json.dump(controls, f)

print("Generated lottie.json with", len(layers), "layers")
