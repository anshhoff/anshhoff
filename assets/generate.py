"""Animated SVGs for the anshhoff GitHub profile README (v2: less text, one accent).
Usage: python3 generate.py <out_dir>"""
import os, sys
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Inter',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(bg="#09090b", card="#0f0f12", border="#27272a", text="#fafafa", muted="#a1a1aa",
                 dim="#52525b", acc="#a3e635", acc2="#a3e635", glow=0.16, grid=0.5),
    "light": dict(bg="#fafafa", card="#ffffff", border="#e4e4e7", text="#09090b", muted="#52525b",
                  dim="#a1a1aa", acc="#65a30d", acc2="#3f6212", glow=0.14, grid=0.7),
}
TERM = dict(bg="#0b0b0e", border="#27272a", text="#fafafa", muted="#71717a", acc="#a3e635", tool="#d4d4d8")

BASE_CSS = """
.up{opacity:0;animation:up .8s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.pulse{animation:pulse 1.8s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.glow{animation:drift 10s ease-in-out infinite}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(-40px,20px)}}
"""


def frame(t, W, H, body, label, extra_css="", glow_xy=None, rx=18):
    gx, gy = glow_xy or (W * 0.85, 0)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">
<title>{esc(label)}</title>
<defs>
<radialGradient id="gl"><stop offset="0" stop-color="{t["acc"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["acc"]}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t["border"]}" fill-opacity="{t["grid"]}"/></pattern>
<clipPath id="r"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>
<style>{BASE_CSS}{extra_css}</style></defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{t["card"]}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<g class="glow"><circle cx="{gx}" cy="{gy}" r="{max(W, H) * 0.45:.0f}" fill="url(#gl)"/></g>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{rx}" fill="none" stroke="{t["border"]}"/>
{body}
</svg>'''


def up(inner, delay, x=0, y=0):
    """Animated group; transform lives on the outer <g> so CSS can't clobber it."""
    return f'<g transform="translate({x},{y})"><g class="up" style="animation-delay:{delay:.2f}s">{inner}</g></g>'


def txt(x, y, s, size, fill, font=SANS, weight=400, anchor="start", ls=0, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{esc(s)}</text>')


def pill(x, y, label, t, live=False):
    w = 30 + len(label) * 7.3 + (12 if live else 0)
    dot = f'<circle class="pulse" cx="{x+16}" cy="{y+13}" r="4" fill="{t["acc"]}"/>' if live else ""
    tx = x + (28 if live else 15)
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="none" stroke="{t["acc"] if live else t["border"]}" stroke-opacity="{0.6 if live else 1}"/>'
            f'{dot}{txt(tx, y+17.5, label, 12.5, t["acc2"] if live else t["muted"], MONO)}'), w


# ---------------------------------------------------------------- hero
TRACE = [
    ("muted", "$ agent.run --channel voice --lang hi-en"),
    ("text", "caller › “Kal shaam 6 baje slot free hai?”"),
    ("tool", "  ↳ check_availability → create_booking"),
    ("acc", "✓ silent caller released   ~1 s  (was 5–9 s)"),
    ("acc", "✓ dead session ends call   ~1 s  (was ~28 s)"),
]


def hero(t):
    W, H = 1200, 400
    cycle, step, typing = 13.0, 1.6, 0.9
    css = [f".t{{font-family:{MONO};font-size:15.5px}} .l{{opacity:0}}"
           ".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"]
    lines = []
    for i, (col, s) in enumerate(TRACE):
        a = i * step / cycle * 100
        b = (i * step + typing) / cycle * 100
        css.append(f"@keyframes k{i}{{0%,{a:.2f}%{{opacity:0;clip-path:inset(0 100% 0 0)}}{a+.01:.2f}%{{opacity:1}}"
                   f"{b:.2f}%,93%{{opacity:1;clip-path:inset(0 0 0 0)}}97%,100%{{opacity:0;clip-path:inset(0 0 0 0)}}}}"
                   f".l{i}{{animation:k{i} {cycle}s steps(30,end) infinite}}")
        lines.append(f'<text class="t l l{i}" x="0" y="{i*34}" fill="{TERM[col]}">{esc(s)}</text>')

    p, _ = pill(0, 0, "open to AI / FDE roles · can join now", t, live=True)
    left = (up(txt(0, 0, "ansh hardaha", 15, t["muted"], MONO, ls=2), .05, 64, 112)
            + up(txt(-3, 0, "I build AI agents", 54, t["text"], weight=750, ls=-1.6), .2, 64, 178)
            + up(txt(-3, 0, "that answer real calls.", 54, t["acc"], weight=750, ls=-1.6), .35, 64, 240)
            + up(txt(0, 0, "CS @ IIIT Dharwad ’27 · India", 16, t["muted"], MONO), .5, 64, 286)
            + up(p, .65, 64, 316))

    tw, th = 500, 250
    term = (f'<rect width="{tw}" height="{th}" rx="14" fill="{TERM["bg"]}" stroke="{TERM["border"]}"/>'
            f'<circle cx="22" cy="22" r="5.5" fill="#3f3f46"/><circle cx="40" cy="22" r="5.5" fill="#3f3f46"/><circle cx="58" cy="22" r="5.5" fill="#3f3f46"/>'
            + txt(tw - 20, 27, "voice-agent · live trace", 12.5, TERM["muted"], MONO, anchor="end")
            + f'<line x1="0" y1="44" x2="{tw}" y2="44" stroke="{TERM["border"]}"/>'
            f'<g transform="translate(22,82)">{"".join(lines)}'
            f'<rect class="cur" x="0" y="{len(TRACE)*34-14}" width="9" height="18" fill="{TERM["acc"]}"/></g>')
    body = left + up(term, .3, 650, 75)
    return frame(t, W, H, body, "Ansh Hardaha: I build AI agents that answer real calls.",
                 "".join(css), glow_xy=(1000, 380))


# ---------------------------------------------------------------- work tiles
def work(t, c):
    W, H = 1200, 210
    pb, _ = pill(0, 0, c["badge"], t, live=c.get("live", False))
    left = (up(txt(0, 0, c["name"], 30, t["text"], weight=750, ls=-.6), .05, 48, 92)
            + up(txt(0, 0, c["role"], 14, t["muted"], MONO), .15, 48, 122)
            + up(pb, .25, 48, 146))
    stats = ""
    colw = 230
    for i, (num, l1, l2) in enumerate(c["stats"]):
        x = 470 + i * colw
        block = (f'<line x1="0" y1="-48" x2="0" y2="40" stroke="{t["border"]}"/>'
                 + txt(26, 0, num, 46, t["acc"], weight=750, ls=-1.5)
                 + txt(26, 28, l1, 14, t["text"]) + txt(26, 48, l2, 14, t["muted"]))
        stats += up(block, .3 + i * .15, x, 102)
    return frame(t, W, H, left + stats, f'{c["name"]}, {c["role"]}', glow_xy=(380, 0))


WORK = [
    dict(slug="hobbyfi", name="HobbyFi", role="AI / full-stack intern · 2026–now",
         badge="in production", live=True,
         stats=[("~1 s", "silent-caller hang-up", "was 5–9 s"),
                ("16", "tools in a WhatsApp", "booking agent"),
                ("296", "test cases across", "voice + chat agents")]),
    dict(slug="burrito", name="Burrito AI", role="founding engineer · 2026–now",
         badge="askburrito.com",
         stats=[("334", "of 374 commits", "on main"),
                ("37", "Postgres migrations", "with row-level security"),
                ("45", "Playwright e2e", "suites")]),
]


# ---------------------------------------------------------------- project tiles
def proj(t, c):
    W, H = 600, 250
    pb, pw = pill(0, 0, c["badge"], t, live=c.get("live", False))
    body = (up(txt(0, 0, c["name"], 24, t["text"], weight=750, ls=-.4), .05, 36, 60)
            + up(pb, .1, W - 36 - pw, 41)
            + up(txt(0, 0, c["line"], 15.5, t["muted"]), .15, 36, 90)
            + up(txt(-2, 0, c["num"], 44, t["acc"], weight=750, ls=-1.4), .3, 36, 162)
            + up(txt(0, 0, c["label"], 14, t["text"]), .4, 36, 190)
            + up(txt(0, 0, c["tech"], 12.5, t["dim"], MONO, ls=.3), .5, 36, 222))
    return frame(t, W, H, body, f'{c["name"]}: {c["line"]}', glow_xy=(W, H))


PROJECTS = [
    dict(slug="canapply", name="CanApply", badge="live", live=True,
         line="Job search that only shows jobs you can get.",
         num="16,431", label="postings checked from 349 career pages",
         tech="python · postgres · pgvector · telegram"),
    dict(slug="sahara", name="Sahara", badge="hackathon",
         line="Agent that recovers failed payments.",
         num="69.2%", label="recovered vs 19.4% control (synthetic test)",
         tech="python · fastapi · groq · 241 tests"),
    dict(slug="pixelagents", name="Pixel Agents", badge="fork",
         line="Watch remote AI agents from one board.",
         num="N → 1", label="machines streamed to one shared board",
         tech="typescript · vs code api · node"),
    dict(slug="fitform", name="FitForm", badge="iOS",
         line="Checks your squat form in real time.",
         num="on-device", label="Apple Vision pose estimation, no server",
         tech="swift · swiftui · vision"),
]

for mode, t in THEMES.items():
    open(f"{OUT}/hero-{mode}.svg", "w").write(hero(t))
    for c in WORK:
        open(f"{OUT}/work-{c['slug']}-{mode}.svg", "w").write(work(t, c))
    for c in PROJECTS:
        open(f"{OUT}/proj-{c['slug']}-{mode}.svg", "w").write(proj(t, c))
print(len(os.listdir(OUT)), "files")
