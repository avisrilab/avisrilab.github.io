#!/usr/bin/env python3
"""Redraw BenchDrop-seq Fig. 2D (HBA1, K562) in the site's own style.

    python3 .github/tools/retoken_fig.py /path/to/benchdrop_paper/figures/Fig2D.svg > out.svg

Reads the published IGV-style SVG by clip group and re-emits only the data: the canonical gene
model, both coverage tracks (each scaled to its own maximum) and the first ROWS alignments of each
pileup, split at their gaps. Colours come from CSS classes, so the figure follows the site theme.
Nothing identifying is carried over: no hover titles, no read ids, no barcodes or UMIs.
"""
import re
import sys

ROWS = 25            # molecules shown per track
PITCH, BAR = 10, 7   # row spacing and bar height, in figure units (sized for the half-width column)
GENE = 'ENST00000320868'   # canonical HBA1 transcript

src = open(sys.argv[1]).read()


def group(n):
    i = src.index(f'clip_path_{n}"><rect')
    return src[i:src.index('</g>', i)]


def r1(v):
    return f'{float(v):.1f}'.rstrip('0').rstrip('.')


out, y = [], 0

# gene model: thin UTR boxes, thick coding boxes, introns as a line
g = group(108)
boxes = re.findall(r'<rect x="([\d.]+)" y="[\d.]+" width="([\d.]+)" height="([\d.]+)" fill="#E89E9D" stroke="none" id="' + GENE, g)
xs = [float(x) for x, w, h in boxes] + [float(x) + float(w) for x, w, h in boxes]
out.append(f'<line class="hb-intron" x1="{r1(min(xs))}" x2="{r1(max(xs))}" y1="{y + 8}" y2="{y + 8}"/>')
for x, w, h in boxes:
    tall = float(h) > 6
    out.append(f'<rect class="hb-exon" x="{r1(x)}" y="{y + (2 if tall else 5)}" width="{r1(w)}" height="{12 if tall else 6}"/>')
y += 60


def coverage(n, cls, top):
    g = group(n)
    d = re.search(r'<path d="([^"]+)"', g).group(1)
    pts = [(float(a), float(b)) for a, b in re.findall(r'([\d.]+) ([\d.]+)', d)]
    base = max(p[1] for p in pts)
    peak = min(p[1] for p in pts)
    h = 56
    poly = ' '.join(f'{r1(x)},{r1(top + h - (base - yy) / (base - peak) * h)}' for x, yy in pts)
    return f'<polygon class="{cls}" points="{r1(pts[0][0])},{top + h} {poly} {r1(pts[-1][0])},{top + h}"/>', h


def pileup(n, cls, top):
    g = group(n)
    # each alignment starts with its body path; gaps and marks follow until the next body
    parts = re.split(r'(?=<path d="M [\d.]+ [\d.]+ L [\d.]+ [\d.]+ L [\d.]+ [\d.]+ L [\d.]+ [\d.]+ L [\d.]+ [\d.]+ z")', g)
    rows = {}
    for p in parts[1:]:
        m = re.match(r'<path d="M ([\d.]+) ([\d.]+) L ([\d.]+) ', p)
        x0, row, x1 = float(m.group(1)), float(m.group(2)), float(m.group(3))
        gaps = sorted((float(a), float(a) + float(w)) for a, w in re.findall(r'<rect x="([\d.]+)" y="[\d.]+" width="([\d.]+)" height="[\d.]+" fill="white"', p))
        marks = [float(a) for a, c in re.findall(r'<rect x="([\d.]+)" y="[\d.]+" width="[\d.]+" height="[\d.]+" fill="(blue|green|red|black|purple)"', p)]
        rows.setdefault(row, []).append((x0, x1, gaps, marks))
    body = []
    for k, row in enumerate(sorted(rows)[:ROWS]):
        yy = top + k * PITCH
        for x0, x1, gaps, marks in rows[row]:
            cur = x0
            for a, b in gaps + [(x1, x1)]:
                if a > cur:
                    body.append(f'<rect class="{cls}" x="{r1(cur)}" y="{yy}" width="{r1(a - cur)}" height="{BAR}"/>')
                if b > a:
                    body.append(f'<line class="hb-gap" x1="{r1(a)}" x2="{r1(b)}" y1="{yy + BAR / 2}" y2="{yy + BAR / 2}"/>')
                cur = max(cur, b)
            for a in marks:
                body.append(f'<rect class="hb-mark" x="{r1(a)}" y="{yy}" width="1.6" height="{BAR}"/>')
    return body, ROWS * PITCH


track_tops = {}
for name, cov, pile, cls, ccls in (('illumina', 110, 111, 'hb-ill', 'hb-cov-ill'), ('nanopore', 112, 113, 'hb-ont', 'hb-cov-ont')):
    y += 14
    track_tops[name] = y + 28   # middle of the coverage track, where its label sits
    poly, h = coverage(cov, ccls, y)
    out.append(poly)
    y += h + 6
    body, h = pileup(pile, cls, y)
    out.extend(body)
    y += h + 6

# 200 bp scale bar: 100 bp = 156.96 units on the published ruler (176,600 at 14.42, 176,700 at 171.38)
bar = 2 * (171.38 - 14.42)
out.append(f'<line class="hb-scale" x1="{r1(1590 - bar)}" x2="1590" y1="{y + 4}" y2="{y + 4}"/>')
y += 10

sys.stdout.write('<!-- label tops: gene {:.2f}%, '.format(8 / y * 100) + ', '.join(f'{k} {v / y * 100:.2f}%' for k, v in track_tops.items()) + ' -->\n')
sys.stdout.write(f'<svg class="hba1__svg" viewBox="0 0 1600 {y}" role="img" aria-labelledby="hba1Cap">' + ''.join(out) + '</svg>\n')
