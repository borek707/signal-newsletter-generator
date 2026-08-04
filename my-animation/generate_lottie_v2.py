import json, math

W, H = 512, 512
FR = 60
DURATION = 10 * FR

def static_prop(k): return {"a": 0, "k": k}
def animated_prop(keyframes):
    return {"a": 1, "k": [{"t": t, "s": s, "i": {"x": [0.5], "y": [1]}, "o": {"x": [0.5], "y": [0]}} if i < len(keyframes)-1 else {"t": t, "s": s} for i, (t, s) in enumerate(keyframes)]}

def make_shape_layer(name, shapes, ip=0, opacity_kf=None, pos=None):
    if opacity_kf is None:
        opacity_kf = [(0, [100]), (DURATION, [100])]
    ks = {
        "o": animated_prop(opacity_kf),
        "r": static_prop(0), "p": static_prop(pos if pos else [0, 0, 0]),
        "a": static_prop([0, 0, 0]), "s": static_prop([100, 100, 100])
    }
    return {"ty": 4, "nm": name, "ip": ip, "op": DURATION, "st": 0, "ks": ks, "shapes": shapes}

def make_path(points, closed=False):
    verts = points
    ins = [[0,0] for _ in points]
    outs = [[0,0] for _ in points]
    return {"ty": "sh", "ks": static_prop({"c": closed, "v": verts, "i": ins, "o": outs})}

def make_stroke(color, width, opacity=100):
    return {"ty": "st", "c": static_prop(color), "o": static_prop(opacity), "w": static_prop(width), "lc": 2, "lj": 2}

def make_fill(color, opacity=100):
    return {"ty": "fl", "c": static_prop(color), "o": static_prop(opacity)}

def make_group(name, items):
    items.append({"ty": "tr", "p": static_prop([0, 0]), "a": static_prop([0, 0]), "s": static_prop([100, 100]), "r": static_prop(0), "o": static_prop(100)})
    return {"ty": "gr", "nm": name, "it": items}

def curve_points(start, cp1, cp2, end, segments=8):
    pts = [start]
    for i in range(1, segments):
        t = i / segments
        x = (1-t)**3 * start[0] + 3*(1-t)**2*t * cp1[0] + 3*(1-t)*t**2 * cp2[0] + t**3 * end[0]
        y = (1-t)**3 * start[1] + 3*(1-t)**2*t * cp1[1] + 3*(1-t)*t**2 * cp2[1] + t**3 * end[1]
        pts.append([round(x, 2), round(y, 2)])
    pts.append(end)
    return pts

def make_animated_path_layer(name, points, stroke_w, stroke_color, start_frame, draw_duration, ip=0):
    trim_end = animated_prop([(start_frame, [0]), (start_frame + draw_duration, [100])])
    shapes = [make_group(name, [make_path(points), make_stroke(stroke_color, stroke_w), {"ty": "tm", "s": static_prop(0), "e": trim_end, "o": static_prop(0), "m": 1}])]
    return make_shape_layer(name, shapes, ip=ip)

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
    opacity_kf = [(ip, [0]), (ip + appear_duration, [100])]
    scale_kf = [(ip, [0, 0]), (ip + appear_duration, [100, 100])]
    return {"ty": 4, "nm": name, "ip": ip, "op": DURATION, "st": 0,
        "ks": {"o": animated_prop(opacity_kf), "r": static_prop(0), "p": static_prop([x, y, 0]), "a": static_prop([0, 0, 0]), "s": animated_prop(scale_kf)},
        "shapes": [s1, s2]}

def make_dot_layer(x, y, r, ip, appear_duration):
    opacity_kf = [(ip, [0]), (ip + appear_duration, [100])]
    scale_kf = [(ip, [0, 0]), (ip + appear_duration, [120, 120])]
    return {"ty": 4, "nm": "red dot", "ip": ip, "op": DURATION, "st": 0,
        "ks": {"o": animated_prop(opacity_kf), "r": static_prop(0), "p": static_prop([x, y, 0]), "a": static_prop([0, 0, 0]), "s": animated_prop(scale_kf)},
        "shapes": [make_group("dot", [{"ty": "el", "p": static_prop([0, 0]), "s": static_prop([r*2, r*2])}, make_fill([0.93, 0.27, 0.27, 1])])]}

def make_cta_layer(x, y, w, h, ip, appear_duration):
    opacity_kf = [(ip, [0]), (ip + appear_duration, [100])]
    pos_kf = [(ip, [x, y+20, 0]), (ip + appear_duration, [x, y, 0])]
    return {"ty": 4, "nm": "CTA", "ip": ip, "op": DURATION, "st": 0,
        "ks": {"o": animated_prop(opacity_kf), "r": static_prop(0), "p": animated_prop(pos_kf), "a": static_prop([0, 0, 0]), "s": static_prop([100, 100, 100])},
        "shapes": [make_group("cta", [{"ty": "rc", "p": static_prop([0, 0]), "s": static_prop([w, h]), "r": static_prop(6)}, make_fill([0.93, 0.27, 0.27, 1])])]}

def make_bg_layer():
    return {"ty": 4, "nm": "bg", "ip": 0, "op": DURATION, "st": 0,
        "ks": {"o": static_prop(100), "r": static_prop(0), "p": static_prop([W/2, H/2, 0]), "a": static_prop([0, 0, 0]), "s": static_prop([100, 100, 100])},
        "shapes": [make_group("bg", [{"ty": "rc", "p": static_prop([0, 0]), "s": static_prop([W, H]), "r": static_prop(0)}, {"ty": "fl", "c": {"sid": "bgColor"}, "o": static_prop(100)}])]}

# Text as shapes: simple bars approximating text lines
def make_text_bars_layer(name, bars, ip, fade_duration):
    groups = []
    for bar in bars:
        groups.append(make_group("bar", [
            {"ty": "rc", "p": static_prop([bar[2]/2, 0]), "s": static_prop([bar[2], bar[3]]), "r": static_prop(2)},
            make_fill(bar[4]),
            {"ty": "tr", "p": static_prop([bar[0], bar[1]]), "a": static_prop([0, 0]), "s": static_prop([100, 100]), "r": static_prop(0), "o": static_prop(100)}
        ]))
    opacity_kf = [(ip, [0]), (ip + fade_duration, [100])]
    return make_shape_layer(name, groups, ip=ip, opacity_kf=opacity_kf)

SX, SY = 50, 256
CX, CY = 256, 256

# Main line
main_line = [[SX, SY], [CX-20, SY]]

# Many branches
p1 = curve_points([CX-20, SY], [300, 220], [360, 180], [430, 140], 10)
p2 = curve_points([CX-20, SY], [300, 292], [360, 340], [430, 380], 10)
p3 = curve_points([CX-20, SY], [320, 246], [400, 266], [480, 256], 10)
p4 = curve_points([360, 180], [390, 130], [440, 100], [490, 80], 8)
p5 = curve_points([340, 200], [380, 240], [440, 260], [490, 290], 8)
p6 = curve_points([360, 340], [400, 390], [450, 430], [490, 460], 8)
p7 = curve_points([340, 320], [380, 280], [440, 240], [490, 200], 8)
p8 = curve_points([400, 256], [440, 226], [470, 210], [500, 190], 8)
p9 = curve_points([400, 256], [440, 286], [470, 300], [500, 320], 8)
p10 = curve_points([430, 140], [460, 110], [480, 90], [500, 70], 6)
p11 = curve_points([430, 380], [460, 410], [480, 430], [500, 450], 6)
p12 = curve_points([300, 220], [340, 190], [380, 160], [420, 140], 6)
p13 = curve_points([300, 292], [340, 320], [380, 350], [420, 370], 6)
p14 = curve_points([480, 256], [500, 236], [510, 220], [512, 200], 6)
p15 = curve_points([480, 256], [500, 276], [510, 290], [512, 310], 6)

layers = []

# Logo text as white bars
logo_bars = [[60, 42, 110, 10, [1,1,1,1]], [60, 56, 70, 6, [0.6,0.6,0.6,1]]]
layers.append(make_text_bars_layer("logo", logo_bars, 0, 30))

# Headline as white bars (approximate layout)
headline_bars = [
    [50, 90, 220, 14, [1,1,1,1]],   # Your AI stack
    [50, 112, 180, 14, [1,1,1,1]],  # grew faster
    [50, 134, 160, 14, [1,1,1,1]],  # than your
    [50, 156, 200, 14, [1,1,1,1]],  # architecture
]
layers.append(make_text_bars_layer("headline", headline_bars, 60, 30))

# Red dot after headline
layers.append(make_dot_layer(260, 162, 5, 120, 15))

# Subtitle bars
sub_bars = [
    [50, 320, 190, 8, [0.65,0.65,0.65,1]],
    [50, 334, 140, 8, [0.65,0.65,0.65,1]],
    [50, 348, 160, 8, [0.65,0.65,0.65,1]],
]
layers.append(make_text_bars_layer("subtitle", sub_bars, 120, 30))

# CTA button
layers.append(make_cta_layer(70, 390, 220, 36, 180, 15))

# CTA text bars
cta_bars = [[80, 400, 180, 8, [1,1,1,1]]]
layers.append(make_text_bars_layer("cta_text", cta_bars, 195, 15))

# Main line (draws 0-1.5s)
layers.append(make_animated_path_layer("main", main_line, 3, [1, 1, 1, 1], 0, 45, 0))

# Branches
branches = [
    ("b1", p1, 2.5, 4*FR, 2*FR), ("b2", p2, 2.5, 4*FR, 2*FR), ("b3", p3, 2.5, 4*FR+10, 2*FR),
    ("b4", p4, 1.5, 5*FR, 1.5*FR), ("b5", p5, 1.5, 5*FR+5, 1.5*FR), ("b6", p6, 1.5, 5*FR+10, 1.5*FR),
    ("b7", p7, 1.5, 5*FR+15, 1.5*FR), ("b8", p8, 1.5, 6*FR, 1.5*FR), ("b9", p9, 1.5, 6*FR+5, 1.5*FR),
    ("b10", p10, 1.2, 6*FR+10, 1.2*FR), ("b11", p11, 1.2, 6*FR+15, 1.2*FR), ("b12", p12, 1.2, 7*FR, 1.2*FR),
    ("b13", p13, 1.2, 7*FR+5, 1.2*FR), ("b14", p14, 1.0, 7*FR+10, 1.0*FR), ("b15", p15, 1.0, 7*FR+15, 1.0*FR),
]
for name, pts, w, sf, dd in branches:
    layers.append(make_animated_path_layer(name, pts, w, [1, 1, 1, 1], sf, dd, sf))

# Red X marks
x_positions = [(490, 80), (490, 290), (490, 460), (490, 200), (500, 70), (500, 450)]
for i, (x, y) in enumerate(x_positions):
    layers.append(make_x_layer(x, y, 10, 7*FR + i*8, 12))

# Background
layers.append(make_bg_layer())

lottie = {
    "v": "5.7.0", "fr": FR, "ip": 0, "op": DURATION, "w": W, "h": H,
    "assets": [],
    "slots": {"bgColor": {"p": {"a": 0, "k": [0, 0, 0, 1]}}},
    "layers": layers
}

with open("public/lottie.json", "w") as f:
    json.dump(lottie, f)

controls = {"controls": [{"sid": "bgColor", "label": "Background color"}]}
with open("public/controls.json", "w") as f:
    json.dump(controls, f)

print("Generated v2 with", len(layers), "layers")
