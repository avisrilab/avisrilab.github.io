# Generates the dot-art illustrations (hero palette) for research pillars, tool tiles and page headers.
import math, random, sys
OUT = sys.argv[1]
TEAL, BLUE, VIOLET, GREEN, AMBER, GREY = '#48bec8', '#608cff', '#a478ff', '#5ad68c', '#ffb03c', '#6d7890'
def svg(w, h, body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>\n'
def dot(x, y, r, c, o=0.9): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{c}" fill-opacity="{o}"/>'
def cloud(rng, cx, cy, sx, sy, n, c, r=1.8, rot=0.0, o=0.85):
    out = []
    for _ in range(n):
        a, b = rng.gauss(0, sx), rng.gauss(0, sy)
        out.append(dot(cx + a*math.cos(rot) - b*math.sin(rot), cy + a*math.sin(rot) + b*math.cos(rot), r, c, o))
    return ''.join(out)

def measure():   # droplets, most empty, some holding one cell; a few barcoded beads
    rng = random.Random(1); b = []
    for i in range(9):
        for j in range(7):
            x, y = 40 + i*42 + (21 if j % 2 else 0), 36 + j*38
            if x > 390: continue
            b.append(f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="{TEAL}" stroke-opacity=".35" stroke-width="1.2"/>')
            if rng.random() < .45: b.append(cloud(rng, x, y, 2.2, 2.2, 7, TEAL, 1.5, o=.95))
            elif rng.random() < .15: b.append(dot(x, y, 3, AMBER, 1))
    return svg(400, 300, ''.join(b))

def quantify():  # reads stacking on exons, with junction arcs (sashimi-like)
    rng = random.Random(2); b = []
    ex = [(40, 100), (170, 230), (300, 370)]
    for x0, x1 in ex: b.append(f'<rect x="{x0}" y="236" width="{x1-x0}" height="14" rx="2" fill="{BLUE}" fill-opacity=".9"/>')
    b.append(f'<line x1="20" y1="243" x2="390" y2="243" stroke="{GREY}" stroke-width="1"/>')
    for (x0, x1), n in zip(ex, (34, 22, 30)):
        for k in range(n):
            y = 222 - k*4.2; s = rng.uniform(x0 - 6, x1 - 30); L = rng.uniform(24, 46)
            b.append(f'<line x1="{s:.1f}" y1="{y:.1f}" x2="{min(s+L, x1+4):.1f}" y2="{y:.1f}" stroke="{BLUE}" stroke-opacity=".75" stroke-width="2.2" stroke-linecap="round"/>')
    b.append(f'<path d="M100 232 Q135 150 170 232" fill="none" stroke="{VIOLET}" stroke-width="2.5"/>')
    b.append(f'<path d="M230 232 Q265 150 300 232" fill="none" stroke="{VIOLET}" stroke-width="2.5"/>')
    b.append(f'<path d="M100 232 Q200 40 300 232" fill="none" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="4 4"/>')
    return svg(400, 300, ''.join(b))

def integrate(): # a gene-level atlas (grey) and long-read cells (violet) mapped onto it
    rng = random.Random(3); b = []
    centres = [(120, 90), (270, 100), (110, 215), (285, 215), (200, 160)]
    for cx, cy in centres: b.append(cloud(rng, cx, cy, 26, 18, 70, GREY, 1.6, o=.6))
    for cx, cy in centres:
        for _ in range(6):
            x, y = cx + rng.gauss(0, 18), cy + rng.gauss(0, 12)
            b.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+rng.uniform(-6,6):.1f}" y2="{y-rng.uniform(10,20):.1f}" stroke="{VIOLET}" stroke-opacity=".35"/>')
            b.append(dot(x, y, 2.6, VIOLET, .95))
    return svg(400, 300, ''.join(b))

def apply():     # two programmes: tumour states and immune states, each with a rare state
    rng = random.Random(4); b = []
    b.append(cloud(rng, 120, 140, 40, 30, 220, GREEN, 1.7, .5))
    b.append(cloud(rng, 150, 200, 12, 10, 40, AMBER, 2, o=.95))
    b.append(cloud(rng, 285, 110, 30, 22, 150, TEAL, 1.7, -.4))
    b.append(cloud(rng, 300, 205, 28, 18, 120, BLUE, 1.7, .3))
    b.append(cloud(rng, 250, 160, 9, 8, 30, AMBER, 2, o=.95))
    return svg(400, 300, ''.join(b))

def header():    # wide, faint cluster field for page headers
    rng = random.Random(5); b = []
    for (cx, cy, sx, sy, n, c, rot) in [(820, 90, 70, 26, 260, TEAL, .4), (650, 150, 34, 55, 200, BLUE, -.3),
                                       (990, 170, 60, 30, 230, VIOLET, .9), (800, 230, 64, 22, 200, GREEN, -.2),
                                       (930, 250, 20, 18, 90, AMBER, 0)]:
        b.append(cloud(rng, cx, cy, sx, sy, n, c, 1.6, rot, .7))
    return svg(1120, 320, ''.join(b))

def glyph(kind): # 120x120 tile icons
    rng = random.Random(6); b = []
    if kind == 'benchdrop':
        for (x, y) in [(38, 40), (82, 40), (60, 78), (30, 88), (92, 88)]:
            b.append(f'<circle cx="{x}" cy="{y}" r="17" fill="none" stroke="{TEAL}" stroke-opacity=".6" stroke-width="1.5"/>')
        for (x, y) in [(38, 40), (60, 78), (92, 88)]: b.append(cloud(rng, x, y, 3, 3, 9, TEAL, 1.8, o=1))
        b.append(dot(82, 40, 3.5, AMBER, 1))
    else:
        b.append(f'<rect x="12" y="84" width="26" height="9" rx="2" fill="{BLUE}"/><rect x="50" y="84" width="20" height="9" rx="2" fill="{BLUE}"/><rect x="84" y="84" width="24" height="9" rx="2" fill="{BLUE}"/>')
        b.append(f'<path d="M38 82 Q44 52 50 82" fill="none" stroke="{VIOLET}" stroke-width="2.5"/><path d="M70 82 Q77 52 84 82" fill="none" stroke="{VIOLET}" stroke-width="2.5"/>')
        b.append(f'<path d="M38 82 Q61 14 84 82" fill="none" stroke="{AMBER}" stroke-width="2" stroke-dasharray="3 3"/>')
    return svg(120, 120, ''.join(b))

# The four pillar illustrations it once drew were retired in b48108e; the functions stay for reference.
files = {'header-dots.svg': header(), 'benchdrop.svg': glyph('benchdrop'), 'bagpiper.svg': glyph('bagpiper')}
for name, s in files.items():
    open(f'{OUT}/{name}', 'w').write(s)
    print(name, len(s))
