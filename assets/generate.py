"""Animated pixel-art 'agent office' SVG for the anshhoff GitHub profile README.
Original art. Usage: python3 pixel_office.py <out.svg>"""
import sys
import random

random.seed(7)
OUT = sys.argv[1]
W, H = 1200, 460

# ------------------------------------------------------------------ helpers
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "+": [".....", "....#", "...#.", "#.#..", ".#...", ".....", "....."],  # check mark
    " ": ["....."] * 7,
}


def runs(rows, x, y, u):
    """rows of chars -> {char: path-d} with horizontal runs merged."""
    out = {}
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            s = c
            while c < len(row) and row[c] == ch:
                c += 1
            out.setdefault(ch, []).append(f"M{x+s*u} {y+r*u}h{(c-s)*u}v{u}h{-(c-s)*u}z")
    return {k: "".join(v) for k, v in out.items()}


def sprite(rows, pal, x, y, u, cls=None, style=""):
    paths = runs(rows, x, y, u)
    body = "".join(f'<path d="{d}" fill="{pal[k]}"/>' for k, d in paths.items() if k in pal)
    attrs = (f' class="{cls}"' if cls else "") + (f' style="{style}"' if style else "")
    return f"<g{attrs}>{body}</g>"


def text(s, x, y, px, color):
    rows = [""] * 7
    for ch in s:
        g = FONT[ch]
        for i in range(7):
            rows[i] += g[i].replace("#", "x") + "."
    return sprite(rows, {"x": color}, x, y, px)


def text_w(s, px):
    return len(s) * 6 * px - px


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'


# ------------------------------------------------------------------ palette
INK = "#0b0b14"
EYE = "#ecfeff"
AG = {
    "cyan": ("#22d3ee", "#0e7490"),
    "pink": ("#f472b6", "#9d174d"),
    "lime": ("#a3e635", "#4d7c0f"),
    "orange": ("#fb923c", "#9a3412"),
    "violet": ("#a78bfa", "#5b21b6"),
}

HEAD = [
    "....y....",
    "....k....",
    ".bbbbbbb.",
    ".bfffffb.",
    ".bfffffb.",
    ".bffbffb.",
    ".bbbbbbb.",
    "..bbbbb..",
    ".bbbbbbb.",
    "..bbbbb..",
]
LEGS_STAND = ["..k...k..", ".kk...kk."]
LEGS_A = [".k.....k.", "kk.....kk"]
LEGS_B = ["...k.k...", "..kk.kk.."]


def agent(color, x, y, u=6, legs="stand", blink_delay=0.0, extra=""):
    b, k = AG[color]
    pal = {"b": b, "k": k, "f": INK, "y": b}
    base = [r.replace("y", ".") for r in HEAD]
    out = sprite(base, pal, x, y, u)
    out += sprite(["....y...."], pal, x, y, u, "ant", f"animation-delay:{blink_delay:.1f}s")
    eyes = [".........", ".........", ".........", ".........", "...e.e...."[:9]]
    out += sprite(eyes, {"e": EYE}, x, y, u, "blink", f"animation-delay:{blink_delay:.1f}s")
    ly = y + len(HEAD) * u
    if legs == "stand":
        out += sprite(LEGS_STAND, pal, x, ly, u)
    elif legs == "walk":
        out += sprite(LEGS_A, pal, x, ly, u, "fa")
        out += sprite(LEGS_B, pal, x, ly, u, "fb")
    return out + extra


def bubble(msg, x, y, delay, period=8, tail_x=None):
    px = 3
    tw = text_w(msg, px)
    w, h = tw + 24, 7 * px + 18
    tail_x = tail_x if tail_x is not None else x + 20
    g = (rect(x, y, w, h, INK) + rect(x + 3, y + 3, w - 6, h - 6, "#f8fafc")
         + rect(tail_x, y + h, 9, 3, INK) + rect(tail_x + 3, y + h - 3, 3, 3, "#f8fafc")
         + rect(tail_x + 3, y + h + 3, 3, 3, INK)
         + text(msg, x + 12, y + 9, px, INK))
    return f'<g class="bub" style="animation-delay:{delay}s;animation-duration:{period}s">{g}</g>'


# ------------------------------------------------------------------ scene
P = []
# wall + floor
P.append(rect(0, 0, W, 306, "#161729"))
for x in range(0, W, 48):
    P.append(rect(x, 0, 24, 300, "#191a2e"))
P.append(rect(0, 300, W, 8, "#2b2d4a"))
P.append(rect(0, 308, W, H - 308, "#231c36"))
for i, y in enumerate(range(308, H, 22)):
    P.append(rect(0, y, W, 2, "#1b1529"))
    off = (i * 70) % 140
    for x in range(off, W, 140):
        P.append(rect(x, y, 2, 22, "#1b1529"))

# window with night city
WX, WY, WW, WH = 40, 40, 216, 168
sky = [("#0f1033", 0), ("#171543", 40), ("#221a52", 80), ("#2e1f5e", 120)]
win = []
for col, dy in sky:
    win.append(rect(WX, WY + dy, WW, 48, col))
for _ in range(16):
    sx, sy = WX + random.randrange(8, WW - 8, 4), WY + random.randrange(6, 100, 4)
    d = random.random() * 3
    win.append(f'<rect class="tw" style="animation-delay:{d:.2f}s" x="{sx}" y="{sy}" width="4" height="4" fill="#fef9c3"/>')
moon = ["..mmm.", ".mmm..", "mmm...", "mmm...", ".mmm..", "..mmm."]
win.append(sprite(moon, {"m": "#fde68a"}, WX + 150, WY + 18, 5))
cloud = ["..cccc....", ".cccccccc.", "cccccccccc"]
win.append(f'<g class="cloud">{sprite(cloud, {"c": "#3b3470"}, WX - 60, WY + 40, 6)}</g>')
bx = WX
for bw, bh in [(26, 54), (20, 76), (30, 44), (18, 88), (28, 60), (22, 70), (34, 48), (26, 82), (32, 56)]:
    if bx >= WX + WW:
        break
    bw = min(bw, WX + WW - bx)
    win.append(rect(bx, WY + WH - bh, bw, bh, "#0a0a1f"))
    for wy in range(WY + WH - bh + 8, WY + WH - 6, 12):
        for wx in range(bx + 4, bx + bw - 4, 8):
            if random.random() < 0.45:
                d = random.random() * 6
                win.append(f'<rect class="lit" style="animation-delay:{d:.1f}s" x="{wx}" y="{wy}" width="4" height="5" fill="#fbbf24"/>')
    bx += bw + 2
P.append(f'<g clip-path="url(#win)">{"".join(win)}</g>')
P.append(rect(WX - 8, WY - 8, WW + 16, 8, "#34365a") + rect(WX - 8, WY + WH, WW + 16, 10, "#34365a")
         + rect(WX - 8, WY, 8, WH, "#34365a") + rect(WX + WW, WY, 8, WH, "#34365a")
         + rect(WX + WW // 2 - 3, WY, 6, WH, "#34365a") + rect(WX, WY + WH // 2 - 3, WW, 6, "#34365a"))

# neon sign
name, sub = "ANSH HARDAHA", "BUILDING AI AGENTS"
nx = 620 - text_w(name, 6) // 2
sx_ = 620 - text_w(sub, 3) // 2
P.append(f'<g class="neon" filter="url(#glow)">{text(name, nx, 46, 6, "#a3e635")}</g>')
P.append(f'<g class="neon2" filter="url(#glow)">{text(sub, sx_, 110, 3, "#67e8f9")}</g>')

# wall clock
CX, CY = 960, 92
clock = ["..wwww..", ".wffffw.", "wffffffw", "wffffffw", "wffffffw", "wffffffw", ".wffffw.", "..wwww.."]
P.append(sprite(clock, {"w": "#3f4270", "f": "#e2e8f0"}, CX - 24, CY - 24, 6))
P.append(f'<g class="hr" style="transform-origin:{CX}px {CY}px">{rect(CX - 2, CY - 12, 4, 14, INK)}</g>')
P.append(f'<g class="mn" style="transform-origin:{CX}px {CY}px">{rect(CX - 1.5, CY - 18, 3, 20, "#e11d48")}</g>')
P.append(rect(CX - 3, CY - 3, 6, 6, INK))

# hanging lamps + light cones
for lx in (386, 676):
    P.append(rect(lx - 1, 0, 2, 146, "#3f4270"))
    P.append(f'<polygon points="{lx-14},150 {lx+14},150 {lx+22},166 {lx-22},166" fill="#3f4270"/>')
    P.append(f'<polygon class="cone" points="{lx-22},166 {lx+22},166 {lx+90},276 {lx-90},276" fill="url(#cone)"/>')
    P.append(rect(lx - 6, 166, 12, 4, "#fde68a"))

# server rack
RX, RY = 1074, 128
P.append(rect(RX, RY, 84, 180, "#232542") + rect(RX + 6, RY + 6, 72, 168, "#0f1024"))
for i in range(6):
    yy = RY + 14 + i * 27
    P.append(rect(RX + 12, yy, 60, 18, "#1c1d38"))
    for j, col in enumerate(["#a3e635", "#22d3ee", "#f472b6"]):
        dur = 0.6 + random.random() * 1.4
        d = random.random()
        P.append(f'<rect class="led" style="animation-duration:{dur:.2f}s;animation-delay:{d:.2f}s" x="{RX+18+j*10}" y="{yy+7}" width="5" height="4" fill="{col}"/>')
    P.append(rect(RX + 52, yy + 6, 14, 2, "#2e3058") + rect(RX + 52, yy + 10, 14, 2, "#2e3058"))

# plant
leaves = ["..g.g..", ".ggggg.", "gg.g.gg", ".ggggg.", "..ggg..", "...g..."]
P.append(f'<g class="sway" style="transform-origin:892px 270px">{sprite(leaves, {"g": "#4ade80"}, 871, 228, 6)}</g>')
P.append(sprite(["ppppppp", ".ppppp.", ".ppppp.", ".ppppp."], {"p": "#b45309"}, 871, 266, 6))

# sleeping cat on cushion
P.append(rect(976, 294, 84, 12, "#7c3aed") + rect(970, 300, 96, 8, "#6d28d9"))
cat = ["o.o.........t", "ooo........tt", "ooooooooooot.", "oooooooooooo.", ".oooooooooo.."]
P.append(f'<g class="breath">{sprite(cat, {"o": "#f59e0b", "t": "#d97706"}, 984, 268, 5)}</g>')
P.append(sprite(["x.x", "..."], {"x": INK}, 984, 278, 5))
for i in range(3):
    P.append(f'<g class="zz" style="animation-delay:{i*0.9:.1f}s">{text("Z", 1000 + i * 8, 236 - i * 10, 2 if i < 2 else 3, "#c4b5fd")}</g>')

# desks with monitors and seated agents
for i, (dx, col, bubbles) in enumerate([(330, "cyan", [("TOOL CALL +", 0)]),
                                         (620, "pink", [("TESTS PASS!", 3), ("SHIP IT!", 7)])]):
    mx, my = dx + 16, 206
    P.append(rect(mx, my, 84, 56, "#2a2c48") + rect(mx + 6, my + 6, 72, 44, "#071a12"))
    P.append(rect(mx + 36, my + 56, 12, 6, "#2a2c48") + rect(mx + 24, my + 60, 36, 4, "#2a2c48"))
    for f in range(3):
        lines = []
        for li in range(5):
            w = random.choice([18, 24, 30, 36, 42, 54])
            ind = random.choice([0, 6, 12])
            c = random.choice(["#a3e635", "#67e8f9", "#f472b6", "#e2e8f0"])
            lines.append(rect(mx + 12 + ind, my + 11 + li * 8, w, 4, c))
        P.append(f'<g class="c{f+1}" style="animation-delay:{i*0.4}s">{"".join(lines)}</g>')
    # chair back
    P.append(rect(dx + 112, 228, 70, 40, "#2b2147"))
    ax = dx + 120
    P.append(f'<g class="type" style="animation-delay:{i*0.15}s">{agent(col, ax, 212, legs=None, blink_delay=i * 1.3)}</g>')
    # desk
    P.append(rect(dx, 266, 200, 12, "#8b5a3c") + rect(dx, 278, 200, 4, "#6e452d"))
    P.append(rect(dx + 8, 282, 10, 44, "#6e452d") + rect(dx + 182, 282, 10, 44, "#6e452d"))
    P.append(rect(dx + 112, 258, 60, 8, "#3f4270"))  # keyboard
    P.append(f'<rect class="mug-steam" x="{dx+186}" y="248" width="3" height="6" fill="#cbd5e1"/>' + rect(dx + 180, 254, 14, 12, "#e2e8f0"))
    for msg, d in bubbles:
        P.append(bubble(msg, ax - 40, 168, d, period=8, tail_x=ax + 18))

# ping-pong
TX, TY = 70, 362
P.append(rect(TX, TY, 190, 10, "#15803d") + rect(TX, TY + 10, 190, 4, "#0f5f2c") + rect(TX + 94, TY - 2, 2, 12, "#f8fafc"))
P.append(rect(TX + 92, TY - 16, 6, 16, "#e2e8f0"))
P.append(rect(TX + 10, TY + 14, 8, 40, "#0f5f2c") + rect(TX + 172, TY + 14, 8, 40, "#0f5f2c"))
paddle = ["rr", "rr", ".h"]
P.append(f'<g class="hitl">{agent("lime", 14, 336, blink_delay=0.7)}{sprite(paddle, {"r": "#ef4444", "h": "#7c2d12"}, 68, 376, 6)}</g>')
P.append(f'<g class="hitr">{agent("orange", 262, 336, blink_delay=2.1)}{sprite(paddle, {"r": "#ef4444", "h": "#7c2d12"}, 250, 376, 6)}</g>')
P.append(f'<g transform="translate(84,348)"><g class="ball">{rect(0, 0, 8, 8, "#f8fafc")}</g></g>')

# coffee machine at the end of the walk lane
CMX, CMY = 1104, 352
P.append(rect(CMX, CMY, 64, 96, "#334155") + rect(CMX + 6, CMY + 6, 52, 22, "#0f172a"))
P.append(text("COFFEE", CMX + 9, CMY + 11, 1.5, "#fbbf24"))
P.append(rect(CMX + 16, CMY + 40, 32, 30, "#0f172a") + rect(CMX + 28, CMY + 40, 8, 6, "#94a3b8"))
P.append(f'<rect class="drip" x="{CMX+31}" y="{CMY+48}" width="2" height="6" fill="#92400e"/>')
P.append(rect(CMX + 24, CMY + 58, 16, 12, "#f8fafc") + rect(CMX - 4, CMY + 92, 72, 8, "#1e293b"))
P.append(f'<rect class="led" style="animation-duration:.8s" x="{CMX+50}" y="{CMY+78}" width="6" height="6" fill="#a3e635"/>')

# walking agent with coffee (front lane)
mug = sprite(["s.s", ".s.", "mmmh", "mmmh", "mmm."], {"s": "#cbd5e1", "m": "#f8fafc", "h": "#f8fafc"}, 52, 374, 4)
walker = agent("violet", 0, 378, legs="walk", blink_delay=1.9) + f'<g class="steam">{mug}</g>'
P.append(f'<g transform="translate(330,0)"><g class="walk"><g class="flip"><g class="bob">{walker}</g></g></g></g>')

CSS = """
.ant{animation:ant 1.2s steps(1) infinite}@keyframes ant{50%{opacity:.15}}
.blink{animation:blink 4.2s steps(1) infinite}@keyframes blink{0%,91%{opacity:1}92%,95%{opacity:0}96%{opacity:1}}
.tw{animation:tw 2.6s steps(2) infinite}@keyframes tw{50%{opacity:.15}}
.lit{animation:lit 7s steps(1) infinite}@keyframes lit{0%,70%{opacity:1}71%,100%{opacity:.2}}
.cloud{animation:cloud 28s linear infinite}@keyframes cloud{from{transform:translateX(0)}to{transform:translateX(340px)}}
.neon{animation:neon 7s steps(1) infinite}@keyframes neon{0%,88%{opacity:1}89%{opacity:.35}90%{opacity:1}92%{opacity:.5}93%,100%{opacity:1}}
.neon2{animation:neon 9s steps(1) infinite 2s}
.hr{animation:spin 60s linear infinite}.mn{animation:spin 6s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
.cone{animation:cone 5s ease-in-out infinite}@keyframes cone{50%{opacity:.75}}
.led{animation:led 1s steps(1) infinite}@keyframes led{50%{opacity:.12}}
.sway{animation:sway 4s ease-in-out infinite}@keyframes sway{50%{transform:rotate(4deg)}}
.breath{animation:breath 3s steps(2) infinite}@keyframes breath{50%{transform:translateY(-2px)}}
.zz{opacity:0;animation:zz 2.7s linear infinite}@keyframes zz{0%{opacity:0;transform:translate(0,0)}25%{opacity:1}100%{opacity:0;transform:translate(14px,-26px)}}
.c1,.c2,.c3{animation-duration:1.5s;animation-timing-function:steps(1);animation-iteration-count:infinite}
.c1{animation-name:c1}.c2{animation-name:c2}.c3{animation-name:c3}
@keyframes c1{0%{opacity:1}33.3%{opacity:0}100%{opacity:0}}
@keyframes c2{0%{opacity:0}33.3%{opacity:1}66.6%{opacity:0}100%{opacity:0}}
@keyframes c3{0%{opacity:0}66.6%{opacity:1}100%{opacity:1}}
.type{animation:type .36s steps(1) infinite}@keyframes type{50%{transform:translateY(-3px)}}
.mug-steam{animation:steam 1.6s linear infinite}
.drip{animation:drip .9s linear infinite}@keyframes drip{0%{transform:translateY(0);opacity:1}100%{transform:translateY(8px);opacity:0}}
.bub{opacity:0;animation:bub 8s steps(1) infinite}@keyframes bub{0%{opacity:0}5%{opacity:1}40%{opacity:0}100%{opacity:0}}
.ball{animation:ball 1.6s linear infinite}
@keyframes ball{0%{transform:translate(0,0)}12.5%{transform:translate(40px,-34px)}25%{transform:translate(81px,-44px)}37.5%{transform:translate(122px,-34px)}50%{transform:translate(162px,0)}62.5%{transform:translate(122px,-34px)}75%{transform:translate(81px,-44px)}87.5%{transform:translate(40px,-34px)}100%{transform:translate(0,0)}}
.hitl{animation:hitl 1.6s steps(1) infinite}@keyframes hitl{0%,8%{transform:translateX(6px)}9%,100%{transform:none}}
.hitr{animation:hitr 1.6s steps(1) infinite}@keyframes hitr{50%,58%{transform:translateX(-6px)}59%,100%{transform:none}}
.walk{animation:walk 20s linear infinite}
@keyframes walk{0%{transform:translateX(0)}46%{transform:translateX(700px)}50%{transform:translateX(700px)}96%{transform:translateX(0)}100%{transform:translateX(0)}}
.flip{transform-box:fill-box;transform-origin:center;animation:flip 20s steps(1) infinite}
@keyframes flip{0%{transform:scaleX(1)}48%{transform:scaleX(-1)}98%{transform:scaleX(1)}}
.bob{animation:bob .5s steps(1) infinite}@keyframes bob{50%{transform:translateY(-3px)}}
.fa{animation:fa .5s steps(1) infinite}@keyframes fa{50%{opacity:0}}
.fb{animation:fb .5s steps(1) infinite}@keyframes fb{0%{opacity:0}50%{opacity:1}}
.steam path[fill="#cbd5e1"]{animation:steam 1.4s linear infinite}
@keyframes steam{0%{opacity:0;transform:translateY(0)}30%{opacity:.9}100%{opacity:0;transform:translateY(-12px)}}
"""

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-label="Ansh Hardaha: a pixel-art office where little AI agents code, ship, play ping-pong and drink coffee">
<title>Ansh Hardaha: building AI agents</title>
<defs>
<clipPath id="win"><rect x="{WX}" y="{WY}" width="{WW}" height="{WH}"/></clipPath>
<clipPath id="all"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<filter id="glow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fde68a" stop-opacity=".22"/><stop offset="1" stop-color="#fde68a" stop-opacity="0"/></linearGradient>
<style>{CSS}</style>
</defs>
<g clip-path="url(#all)">
{"".join(P)}
</g>
</svg>'''
open(OUT, "w").write(svg)
print(len(svg) // 1024, "KB")
