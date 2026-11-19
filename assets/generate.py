"""Generate animated SVGs for the anshhoff GitHub profile README (dark + light)."""
import os, sys
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
                 term="#0b0f14", chip="#1f2630", g1="#22d3ee", g2="#a78bfa", g3="#f472b6",
                 ok="#3fb950", warn="#d29922", glow=0.35),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e",
                  term="#0d1117", chip="#eaeef2", g1="#0891b2", g2="#7c3aed", g3="#db2777",
                  ok="#1a7f37", warn="#9a6700", glow=0.18),
}


def grad(t, gid="g", animate=True):
    anim = ('<animateTransform attributeName="gradientTransform" type="translate" '
            'values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/>') if animate else ""
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="2" y2="0" spreadMethod="reflect">'
            f'<stop offset="0" stop-color="{t["g1"]}"/><stop offset=".5" stop-color="{t["g2"]}"/>'
            f'<stop offset="1" stop-color="{t["g3"]}"/>{anim}</linearGradient>')


# ---------------------------------------------------------------- hero
TRACE = [
    ("muted", "$ agent.run  channel=voice  lang=hi-en"),
    ("text", "caller  › “Kal shaam 6 baje slot free hai?”"),
    ("g2", "  ↳ tool  check_availability(tomorrow, 18:00)"),
    ("g2", "  ↳ tool  create_booking()   consent ✓"),
    ("ok", "✓ silent caller released   ~1 s   (was 5–9 s)"),
    ("ok", "✓ dead model session ends  ~1 s   (was ~28 s)"),
    ("ok", "✓ en→hi→en switch failures  6 → 0"),
]


def hero(t, name):
    W, H = 1200, 420
    cycle = 16.0
    step, typing = 1.5, 0.9
    css = [f"""
.t{{font-family:{MONO};font-size:15px;}}
.l{{opacity:0;clip-path:inset(0 100% 0 0);}}
.cur{{animation:blink 1s steps(1) infinite;}}
@keyframes blink{{50%{{opacity:0}}}}
.orb{{animation:float 9s ease-in-out infinite;}}
.orb2{{animation:float 11s ease-in-out infinite reverse;}}
@keyframes float{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(30px,-18px)}}}}
.chip{{opacity:0;animation:pop .6s ease-out forwards;}}
@keyframes pop{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.fade{{opacity:0;animation:pop .9s ease-out forwards;}}
"""]
    lines = []
    for i, (col, txt) in enumerate(TRACE):
        s = i * step / cycle * 100
        e = (i * step + typing) / cycle * 100
        css.append(
            f"@keyframes k{i}{{0%,{s:.2f}%{{opacity:0;clip-path:inset(0 100% 0 0)}}"
            f"{s+0.01:.2f}%{{opacity:1}}{e:.2f}%{{clip-path:inset(0 0 0 0);opacity:1}}"
            f"94%{{opacity:1;clip-path:inset(0 0 0 0)}}98%,100%{{opacity:0;clip-path:inset(0 0 0 0)}}}}"
            f".l{i}{{animation:k{i} {cycle}s steps(28,end) infinite;}}")
        D = THEMES["dark"]  # terminal is always dark, so use dark-theme colours
        fill = D["muted"] if col == "muted" else D[col] if col != "text" else D["text"]
        if col == "text":
            fill = "#e6edf3"  # terminal is always dark
        lines.append(f'<text class="t l l{i}" x="0" y="{i*30}" fill="{fill}">{esc(txt)}</text>')

    chips = ["Voice AI agents", "Tool-calling LLMs", "Full-stack", "IIIT Dharwad ’27"]
    chip_svg, x = [], 64
    for i, c in enumerate(chips):
        w = 18 + len(c) * 8.2
        chip_svg.append(
            f'<g transform="translate({x:.0f},300)"><g class="chip" style="animation-delay:{0.9+i*0.15:.2f}s">'
            f'<rect width="{w:.0f}" height="32" rx="16" fill="{t["chip"]}" stroke="{t["border"]}"/>'
            f'<text x="{w/2:.0f}" y="21" text-anchor="middle" font-family="{SANS}" font-size="14" '
            f'fill="{t["text"]}">{esc(c)}</text></g></g>')
        x += w + 10

    tx, ty, tw, th = 640, 70, 520, 290
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ansh Hardaha, AI engineer who builds production LLM agents">
<title>Ansh Hardaha, AI engineer</title>
<defs>{grad(t)}
<radialGradient id="o1"><stop offset="0" stop-color="{t["g1"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["g1"]}" stop-opacity="0"/></radialGradient>
<radialGradient id="o2"><stop offset="0" stop-color="{t["g3"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["g3"]}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["border"]}" stroke-opacity=".45" stroke-width="1"/></pattern>
<clipPath id="r"><rect width="{W}" height="{H}" rx="20"/></clipPath>
<style>{"".join(css)}</style></defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<circle class="orb" cx="220" cy="80" r="260" fill="url(#o1)"/>
<circle class="orb2" cx="1050" cy="380" r="280" fill="url(#o2)"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{t["border"]}"/>
<g class="fade" style="animation-delay:.1s"><text x="64" y="118" font-family="{MONO}" font-size="18" fill="{t["muted"]}">hi, i’m</text></g>
<g class="fade" style="animation-delay:.3s"><text x="60" y="184" font-family="{SANS}" font-size="64" font-weight="800" fill="url(#g)" letter-spacing="-1.5">{esc(name)}</text></g>
<g class="fade" style="animation-delay:.55s">
<text x="64" y="228" font-family="{SANS}" font-size="21" fill="{t["text"]}">I build LLM agents that real customers talk to,</text>
<text x="64" y="258" font-family="{SANS}" font-size="21" fill="{t["text"]}">and make them fast and reliable enough to trust.</text></g>
{"".join(chip_svg)}
<g transform="translate({tx},{ty})"><g class="fade" style="animation-delay:.4s">
<rect width="{tw}" height="{th}" rx="14" fill="{t["term"]}" stroke="{t["border"]}"/>
<circle cx="22" cy="22" r="6" fill="#ff5f57"/><circle cx="42" cy="22" r="6" fill="#febc2e"/><circle cx="62" cy="22" r="6" fill="#28c840"/>
<text x="{tw/2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b949e">agent-trace — voice receptionist</text>
<line x1="0" y1="44" x2="{tw}" y2="44" stroke="#30363d"/>
<g transform="translate(22,78)">{"".join(lines)}
<rect class="cur" x="0" y="{len(TRACE)*30-14}" width="9" height="18" fill="{THEMES['dark']['g1']}"/></g>
</g></g>
</svg>'''


# ---------------------------------------------------------------- cards
def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


def card(t, c, wide=False):
    W = 1200 if wide else 600
    H = c.get("h", 250)
    pad = 32
    chars = 118 if wide else 58
    desc = wrap(c["desc"], chars)
    y = 112
    desc_svg = "".join(
        f'<text x="{pad}" y="{y+i*24}" font-family="{SANS}" font-size="16" fill="{t["muted"]}">{esc(l)}</text>'
        for i, l in enumerate(desc))
    y += len(desc) * 24 + 14
    stats = ""
    for i, s in enumerate(c.get("stats", [])):
        stats += (f'<g class="st" style="animation-delay:{0.3+i*0.2:.1f}s"><text x="{pad}" y="{y+i*26}" font-family="{MONO}" font-size="15" fill="{t["text"]}">'
                  f'<tspan fill="{t["ok"]}">▸ </tspan>{esc(s)}</text></g>')
    y += len(c.get("stats", [])) * 26 + 10
    tags, x = "", pad
    for tg in c["tags"]:
        w = 16 + len(tg) * 7.4
        tags += (f'<rect x="{x:.0f}" y="{H-50}" width="{w:.0f}" height="26" rx="13" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                 f'<text x="{x+w/2:.0f}" y="{H-32}" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{t["text"]}">{esc(tg)}</text>')
        x += w + 8
    badge = ""
    if c.get("badge"):
        bw = 20 + len(c["badge"]) * 7.6
        live = c["badge"].lower().startswith("live")
        dot = (f'<circle cx="{W-pad-bw}" cy="44" r="4" fill="{t["ok"]}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>'
               if live else "")
        off = 14 if live else 0
        badge = (f'<rect x="{W-pad-bw-off}" y="31" width="{bw+off}" height="26" rx="13" fill="none" stroke="{t["ok"] if live else t["border"]}"/>{dot}'
                 f'<text x="{W-pad-bw/2+ (3 if live else 0)}" y="49" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{t["ok"] if live else t["muted"]}">{esc(c["badge"])}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(c["title"])}: {esc(c["desc"])}">
<title>{esc(c["title"])}</title>
<defs>{grad(t, "g", animate=False)}
<style>.st{{opacity:0;animation:in .7s ease-out forwards}}@keyframes in{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
.bar{{animation:sweep 6s ease-in-out infinite}}@keyframes sweep{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}</style></defs>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>
<rect class="bar" x="1" y="1" width="{W-2}" height="4" rx="2" fill="url(#g)"/>
<text x="{pad}" y="54" font-family="{SANS}" font-size="24" font-weight="700" fill="{t["text"]}">{esc(c["title"])}</text>
<text x="{pad}" y="80" font-family="{MONO}" font-size="13.5" fill="{t["g2"]}">{esc(c["sub"])}</text>
{badge}{desc_svg}{stats}{tags}
</svg>'''


WORK = [
    dict(slug="hobbyfi", title="HobbyFi", sub="AI / Full-Stack Intern · Mar 2026 – now", badge="in production", h=290,
         desc="Co-built a WhatsApp AI receptionist that books, reschedules and takes UPI payments for venues, and own latency and call reliability on its Hindi–English voice agent (LiveKit + Gemini Live).",
         stats=["16 tools · Qdrant RAG · consent gate before every write",
                "silent caller released in ~1 s (was 5–9 s); dead model session ends in ~1 s (was ~28 s)",
                "296 Vitest cases across both agents"],
         tags=["TypeScript", "Mastra", "Gemini Live", "LiveKit", "Qdrant", "Vitest"]),
    dict(slug="burrito", title="Burrito AI", sub="Founding Engineer · Jul 2026 – now", badge="askburrito.com", h=290,
         desc="Primary engineer of a multi-tenant SaaS that turns a team’s GitHub work into social posts: a tool-using chat assistant with model failover, a Gemini image pipeline, and a scheduler for IG, FB, LinkedIn and X.",
         stats=["334 of 374 commits on main",
                "37 Postgres migrations with row-level security per workspace",
                "45 Playwright end-to-end suites"],
         tags=["Next.js", "TypeScript", "Supabase", "PostgreSQL", "Gemini", "Playwright"]),
]

PROJECTS = [
    dict(slug="canapply", title="CanApply", sub="github.com/anshhoff/canapply", badge="live", h=300,
         desc="Job search that only shows jobs you can actually get. An LLM reads hard requirements out of each posting; plain code decides if you qualify. Runs as a Telegram agent.",
         stats=["16,431 postings from 349 career pages", "hybrid search: full-text + pgvector + RRF"],
         tags=["Python", "Postgres", "pgvector", "Telegram"]),
    dict(slug="sahara", title="Sahara", sub="Razorpay AI Buildathon · Sep 2026", badge="hackathon", h=300,
         desc="Failed-payment recovery agent. Rules first, then an LLM classifies each failure; actions go through fixed policy tables with hash-chained audit logs.",
         stats=["69.2% vs 19.4% recovered (88 synthetic cases)", "241 Pytest tests"],
         tags=["Python", "FastAPI", "Groq", "Webhooks"]),
    dict(slug="pixelagents", title="Pixel Agents", sub="fork · VS Code extension", badge="fork", h=300,
         desc="Extended an open-source VS Code extension with an authenticated relay that streams AI-agent events from remote machines onto one shared board.",
         stats=["long-polled permission requests", "answered from the shared board"],
         tags=["TypeScript", "VS Code API", "Node.js"]),
    dict(slug="fitform", title="FitForm", sub="iOS · on-device computer vision", badge="iOS", h=300,
         desc="Real-time squat form checker. Apple Vision pose estimation, joint-angle analysis and a rep-counting state machine, with voice and haptic coaching.",
         stats=["live skeleton overlay", "rep counter with anti-double-counting"],
         tags=["Swift", "SwiftUI", "Vision", "AVFoundation"]),
]

for mode, t in THEMES.items():
    open(f"{OUT}/hero-{mode}.svg", "w").write(hero(t, "Ansh Hardaha"))
    for c in WORK:
        open(f"{OUT}/work-{c['slug']}-{mode}.svg", "w").write(card(t, c, wide=True))
    for c in PROJECTS:
        open(f"{OUT}/proj-{c['slug']}-{mode}.svg", "w").write(card(t, c))
print(sorted(os.listdir(OUT)))
