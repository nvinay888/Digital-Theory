#!/usr/bin/env python3
"""SEO / AEO / GEO audit across every .html file in the site."""
import os, re, json
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))

class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.in_title = False
        self.meta = {}
        self.og = {}
        self.tw = {}
        self.canonical = None
        self.robots = None
        self.lang = None
        self.h_tree = []  # (level, text)
        self.cur_h = None
        self.imgs = []  # (src, alt)
        self.json_ld = []
        self.in_script = False
        self.script_type = None
        self.script_buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        elif tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            n = attrs.get('name')
            p = attrs.get('property')
            c = attrs.get('content', '')
            if n == 'description': self.meta['description'] = c
            if n == 'robots': self.robots = c
            if n == 'viewport': self.meta['viewport'] = c
            if p and p.startswith('og:'): self.og[p[3:]] = c
            if n and n.startswith('twitter:'): self.tw[n[8:]] = c
        elif tag == 'link':
            if attrs.get('rel') == 'canonical': self.canonical = attrs.get('href')
        elif tag in ('h1','h2','h3','h4','h5','h6'):
            self.cur_h = (int(tag[1]), '')
        elif tag == 'img':
            self.imgs.append((attrs.get('src',''), attrs.get('alt')))
        elif tag == 'script':
            if attrs.get('type') == 'application/ld+json':
                self.in_script = True
                self.script_buf = []

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag in ('h1','h2','h3','h4','h5','h6') and self.cur_h:
            self.h_tree.append(self.cur_h)
            self.cur_h = None
        elif tag == 'script' and self.in_script:
            self.in_script = False
            try:
                self.json_ld.append(json.loads(''.join(self.script_buf)))
            except: pass

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title or '') + data
        if self.cur_h is not None:
            l, t = self.cur_h
            self.cur_h = (l, t + data)
        if self.in_script:
            self.script_buf.append(data)

def audit(path):
    with open(path) as f: html = f.read()
    p = TagCollector()
    p.feed(html)
    issues = []
    warns = []
    info = {}

    # Title
    title = (p.title or '').strip()
    info['title'] = title
    info['title_len'] = len(title)
    if not title: issues.append('MISSING <title>')
    elif len(title) < 30: warns.append(f'title short ({len(title)} chars)')
    elif len(title) > 65: warns.append(f'title long ({len(title)} chars)')

    # Meta description
    desc = p.meta.get('description', '').strip()
    info['desc_len'] = len(desc)
    if not desc: issues.append('MISSING meta description')
    elif len(desc) < 100: warns.append(f'desc short ({len(desc)} chars)')
    elif len(desc) > 170: warns.append(f'desc long ({len(desc)} chars)')

    # Canonical
    info['canonical'] = p.canonical
    if not p.canonical: issues.append('MISSING canonical')

    # Robots
    info['robots'] = p.robots
    if not p.robots: warns.append('no robots meta')

    # OG / Twitter
    info['og_keys'] = list(p.og.keys())
    info['tw_keys'] = list(p.tw.keys())
    for k in ('title','description','type','url','image','site_name'):
        if k not in p.og: warns.append(f'missing og:{k}')
    for k in ('card','title','description','image'):
        if k not in p.tw: warns.append(f'missing twitter:{k}')

    # Headings
    h1s = [t for l,t in p.h_tree if l==1]
    info['h1_count'] = len(h1s)
    info['h1s'] = [h.strip()[:80] for h in h1s]
    if len(h1s) == 0: issues.append('NO h1')
    elif len(h1s) > 1: issues.append(f'MULTIPLE h1 ({len(h1s)})')

    # Heading hierarchy skip check
    levels = [l for l,t in p.h_tree]
    for i in range(1, len(levels)):
        if levels[i] > levels[i-1] + 1:
            warns.append(f'heading skip {levels[i-1]}->{levels[i]}')
            break

    info['h2_count'] = sum(1 for l,_ in p.h_tree if l==2)
    info['h3_count'] = sum(1 for l,_ in p.h_tree if l==3)

    # Structured data
    info['json_ld_types'] = []
    for j in p.json_ld:
        if isinstance(j, dict) and '@type' in j:
            info['json_ld_types'].append(j['@type'])
        elif isinstance(j, list):
            info['json_ld_types'] += [x.get('@type','?') for x in j if isinstance(x, dict)]

    # Images alt
    imgs_no_alt = [s for s,a in p.imgs if a is None]
    imgs_empty_alt = [s for s,a in p.imgs if a == '']
    info['imgs_total'] = len(p.imgs)
    info['imgs_no_alt'] = len(imgs_no_alt)
    if imgs_no_alt: warns.append(f'{len(imgs_no_alt)} img without alt')

    # Lang
    info['lang'] = p.lang
    if not p.lang: warns.append('no <html lang>')

    return info, issues, warns

# Walk
pages = []
for base, dirs, files in os.walk(ROOT):
    # Skip .git, .claude, node_modules
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'assets']
    for f in files:
        if f.endswith('.html'):
            pages.append(os.path.join(base, f))

pages.sort()

# Summary
total = 0
missing_h1 = []
multi_h1 = []
missing_canonical = []
missing_desc = []
short_title = []
long_title = []
short_desc = []
long_desc = []
no_lang = []
no_faq_schema = []
low_h2 = []
imgs_alt = []
canonicals_by_path = {}

report_lines = []
for p in sorted(pages):
    total += 1
    rel = os.path.relpath(p, ROOT)
    info, iss, warns = audit(p)
    if info['h1_count'] == 0: missing_h1.append(rel)
    if info['h1_count'] > 1: multi_h1.append(rel)
    if not info['canonical']: missing_canonical.append(rel)
    if info['desc_len'] == 0: missing_desc.append(rel)
    if 0 < info['title_len'] < 30: short_title.append((rel, info['title_len']))
    if info['title_len'] > 65: long_title.append((rel, info['title_len']))
    if 0 < info['desc_len'] < 100: short_desc.append((rel, info['desc_len']))
    if info['desc_len'] > 170: long_desc.append((rel, info['desc_len']))
    if not info['lang']: no_lang.append(rel)
    if info['h2_count'] < 2: low_h2.append((rel, info['h2_count']))
    if info['imgs_no_alt'] > 0: imgs_alt.append((rel, info['imgs_no_alt']))
    canonicals_by_path.setdefault(info['canonical'], []).append(rel)
    if info['json_ld_types']: pass

    if iss or warns:
        report_lines.append(f'\n{rel}')
        for i in iss: report_lines.append(f'  ISSUE   {i}')
        for w in warns: report_lines.append(f'  WARN    {w}')

print('=' * 72)
print(f'SEO/AEO/GEO audit — {total} HTML pages')
print('=' * 72)
print()
print('CRITICAL')
print('-' * 40)
print(f'  Missing <h1>          : {len(missing_h1)}')
print(f'  Multiple <h1>         : {len(multi_h1)}')
print(f'  Missing canonical     : {len(missing_canonical)}')
print(f'  Missing description   : {len(missing_desc)}')
print()
print('LENGTH / QUALITY')
print('-' * 40)
print(f'  Short titles (<30)    : {len(short_title)}')
print(f'  Long titles (>65)     : {len(long_title)}')
print(f'  Short descs (<100)    : {len(short_desc)}')
print(f'  Long descs (>170)     : {len(long_desc)}')
print(f'  Low h2 count (<2)     : {len(low_h2)}')
print()
print('OTHER')
print('-' * 40)
print(f'  No html lang          : {len(no_lang)}')
print(f'  Pages with img missing alt: {len(imgs_alt)}')

# Duplicate canonicals
dup = {c:paths for c,paths in canonicals_by_path.items() if c and len(paths)>1}
print(f'  Duplicate canonicals  : {len(dup)}')
for c, paths in dup.items():
    print(f'    {c}')
    for p in paths: print(f'      · {p}')

# Structured data coverage
jl_pages = []
for p in sorted(pages):
    info, _, _ = audit(p)
    if info['json_ld_types']:
        jl_pages.append((os.path.relpath(p, ROOT), info['json_ld_types']))
print()
print('STRUCTURED DATA (JSON-LD)')
print('-' * 40)
print(f'  Pages with JSON-LD    : {len(jl_pages)} / {total}')
for rp, types in jl_pages:
    print(f'    {rp}: {types}')

# Detailed issues if any
if report_lines:
    print()
    print('DETAILED WARNINGS')
    print('-' * 40)
    for l in report_lines[:200]:
        print(l)
