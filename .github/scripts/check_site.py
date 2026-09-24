#!/usr/bin/env python3
"""Pre-deploy check for avisrilab.org. Runs in CI before the deploy step, and locally:

    python3 .github/scripts/check_site.py

Exits non-zero, naming the file and the problem, if an edit would break the live site.
Python 3.9 standard library only.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PAGES = ['index.html', 'research.html', 'tools.html', 'publications.html', 'people.html', 'contact.html']
PILLARS = {'Measure', 'Quantify', 'Integrate', 'Apply'}
ROLES = {'Principal Investigator', 'Postdoctoral Researchers', 'Graduate Students', 'Research Assistants',
         'Rotation Students', 'Undergraduate Researchers', 'Visiting Scientists'}   # roleOrder in js/lab.js
LONG_DASH = '—'
errors = []


def err(where, msg):
    errors.append(f'{where}: {msg}')


def path(rel):
    return os.path.join(ROOT, rel)


def load(name):
    rel = f'data/{name}'
    try:
        with open(path(rel), encoding='utf-8') as f:
            text = f.read()
    except OSError as e:
        err(rel, f'cannot open ({e})')
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        err(rel, f'invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}')
        return None
    if LONG_DASH in text:
        line = text[:text.index(LONG_DASH)].count('\n') + 1
        err(rel, f'long dash at line {line}; use a comma, colon or period')
    return data


def need(rel, i, entry, keys):
    for k in keys:
        if k not in entry:
            err(rel, f'entry {i} ({entry.get("id") or entry.get("name") or entry.get("date") or "?"}) is missing "{k}"')


class TagBalance(HTMLParser):
    VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'wbr', 'source'}

    def __init__(self):
        super().__init__()
        self.stack, self.bad = [], None

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.bad = self.bad or f'unexpected </{tag}>'
        else:
            self.stack.pop()


def balanced(html):
    p = TagBalance()
    p.feed(html)
    p.close()
    if p.bad:
        return p.bad
    if p.stack:
        return f'unclosed <{p.stack[-1]}>'
    return None


def check_data():
    tools = load('tools.json')
    if isinstance(tools, list):
        for i, t in enumerate(tools):
            need('data/tools.json', i, t, ['id', 'name', 'kind', 'pillar', 'icon', 'tagline', 'summary',
                                           'docs', 'repo', 'paper', 'install', 'vignettes'])
            if t.get('pillar') not in PILLARS:
                err('data/tools.json', f'{t.get("id")}: pillar "{t.get("pillar")}" is not one of {sorted(PILLARS)}')
            if t.get('icon') and not os.path.exists(path(t['icon'])):
                err('data/tools.json', f'{t.get("id")}: icon {t["icon"]} does not exist')
            v = t.get('vignettes')
            if not isinstance(v, list):
                err('data/tools.json', f'{t.get("id")}: "vignettes" must be a list (use [] for none)')
            elif v:
                if not t.get('docs'):
                    err('data/tools.json', f'{t.get("id")}: has vignettes but no "docs" site')
                for j, g in enumerate(v):
                    for k in ('title', 'path', 'blurb'):
                        if k not in g:
                            err('data/tools.json', f'{t.get("id")}: vignette {j} is missing "{k}"')
            p = t.get('paper')
            if p is not None and not (isinstance(p, dict) and p.get('label') and p.get('url')):
                err('data/tools.json', f'{t.get("id")}: "paper" must be null or {{"label", "url"}}')

    papers = load('papers.json')
    if isinstance(papers, list):
        seen = set()
        for i, p in enumerate(papers):
            need('data/papers.json', i, p, ['id', 'title', 'authors', 'journal', 'year'])
            if p.get('id') in seen:
                err('data/papers.json', f'duplicate id "{p.get("id")}"')
            seen.add(p.get('id'))
            if not isinstance(p.get('year'), int):
                err('data/papers.json', f'{p.get("id")}: year must be a number, not {p.get("year")!r}')
            if p.get('doi') and not re.match(r'^10\.\d{4,9}/', p['doi']):
                err('data/papers.json', f'{p.get("id")}: doi "{p["doi"]}" should start 10.xxxx/ (no https://doi.org/)')
            if p.get('preview') and not os.path.exists(path(p['preview'])):
                err('data/papers.json', f'{p.get("id")}: preview {p["preview"]} does not exist')
            if not isinstance(p.get('authors'), list):
                err('data/papers.json', f'{p.get("id")}: authors must be a list')

    news = load('news.json')
    if isinstance(news, list):
        for i, n in enumerate(news):
            need('data/news.json', i, n, ['date', 'text'])
            if not re.match(r'^\d{4}-(0[1-9]|1[0-2])$', str(n.get('date', ''))):
                err('data/news.json', f'entry {i}: date "{n.get("date")}" must be YYYY-MM, e.g. 2026-10')
            bad = balanced(n.get('text', ''))
            if bad:
                err('data/news.json', f'entry {i} ({n.get("date")}): {bad} in the text')

    people = load('people.json')
    if isinstance(people, list):
        for i, p in enumerate(people):
            need('data/people.json', i, p, ['name', 'role', 'status'])
            if p.get('status') not in ('current', 'alumni'):
                err('data/people.json', f'{p.get("name")}: status must be "current" or "alumni"')
            if p.get('role') not in ROLES:
                err('data/people.json', f'{p.get("name")}: role "{p.get("role")}" is not one of {sorted(ROLES)}')
            if p.get('photo') and not os.path.exists(path(p['photo'])):
                err('data/people.json', f'{p.get("name")}: photo {p["photo"]} does not exist')


def block(html, start, end):
    i = html.find(start)
    return html[i:html.index(end, i)] if i >= 0 else None


def meta(html, attr, name):
    m = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', html)
    return m.group(1) if m else None


def check_pages():
    with open(path('sitemap.xml'), encoding='utf-8') as f:
        sitemap = f.read()
    navs, foots = {}, {}
    for page in PAGES:
        with open(path(page), encoding='utf-8') as f:
            html = f.read()
        navs[page] = block(html, '<ul class="nav__links"', '</ul>')
        foots[page] = block(html, '<ul class="footer__nav-links">', '</ul>')
        url = 'https://avisrilab.org/' + ('' if page == 'index.html' else page)
        canon = re.search(r'<link rel="canonical" href="([^"]*)"', html)
        if not canon or canon.group(1) != url:
            err(page, f'canonical link should be {url}')
        if meta(html, 'property', 'og:url') != url:
            err(page, f'og:url should be {url}')
        if meta(html, 'name', 'description') != meta(html, 'property', 'og:description'):
            err(page, 'description and og:description differ')
        if f'<loc>{url}</loc>' not in sitemap:
            err('sitemap.xml', f'missing {url}')
        text = re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S)
        if LONG_DASH in text:
            err(page, f'long dash at line {html[:html.index(LONG_DASH)].count(chr(10)) + 1}')
        for ref in re.findall(r'(?:href|src)="([^"#?]+)', html):
            if re.match(r'^(https?:|mailto:|tel:|data:|//)', ref) or ref.startswith('/Matisse/'):
                continue
            target = ref.lstrip('/') or 'index.html'
            if not os.path.exists(path(target)):
                err(page, f'link or file "{ref}" does not exist')
    for name, got in (('nav', navs), ('footer', foots)):
        first = got[PAGES[0]]
        for page in PAGES[1:]:
            if got[page] != first:
                err(page, f'{name} links differ from {PAGES[0]}; keep all six pages identical')


check_data()
check_pages()
if errors:
    print(f'Site check failed ({len(errors)} problem{"s" if len(errors) > 1 else ""}):')
    for e in errors:
        print('  ' + e)
    sys.exit(1)
print('Site check passed: data files, pages, nav, links and sitemap are consistent.')
