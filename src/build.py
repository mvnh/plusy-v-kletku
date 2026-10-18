#!/usr/bin/env python3
"""Собирает index.html (в корне платформы) из src/parts и проверяет content/ и data/."""
import os, shutil, json, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, SRC
DIST = ROOT
read = lambda f: open(os.path.join(SRC, 'parts', f), encoding='utf-8').read()
head = f'''<title>Плюсы в клетку</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Crect width=%2232%22 height=%2232%22 rx=%226%22 fill=%22%232b4fd8%22/%3E%3Ctext x=%2216%22 y=%2222%22 font-size=%2215%22 font-family=%22monospace%22 font-weight=%22700%22 text-anchor=%22middle%22 fill=%22white%22%3EC++%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Unbounded:wght@500;600;700;800&display=swap">
<style>
{read('style.css')}
{read('cm.css')}
</style>
'''
body = read('body.html')
scripts = f'''<script src="vendor/codemirror.min.js"></script>
<script>
{read('cmlite.js')}
</script>
<script>
"use strict";
{read('core.js')}
{read('runner.js')}
{read('render.js')}
{read('widgets.js')}
{read('views.js')}
{read('extras.js')}
{read('boot.js')}
</script>
'''
open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8').write('<!doctype html>\n<html lang="ru">\n<head>\n' + head + '</head>\n<body>\n' + body + scripts + '</body>\n</html>\n')
# validate json in data/ and manifest
bad = 0
for d in ('content', 'data'):
    for f in os.listdir(os.path.join(DIST, d)):
        if f.endswith('.json'):
            try: json.load(open(os.path.join(DIST, d, f), encoding='utf-8'))
            except Exception as e: print('BAD JSON', d, f, e); bad += 1
# validate embedded quiz / trace json in chapters
for f in sorted(os.listdir(os.path.join(DIST, 'content'))):
    if not f.endswith('.html'): continue
    s = open(os.path.join(DIST, 'content', f), encoding='utf-8').read()
    if s.count('<section') != s.count('</section>'): print('UNBALANCED section in', f); bad += 1
    for tag in ('div', 'aside', 'p', 'ul', 'ol', 'table', 'script'):
        o, c = len(re.findall(r'<%s[\s>]' % tag, s)), s.count('</%s>' % tag)
        if o != c: print('UNBALANCED', tag, o, c, 'in', f); bad += 1
    for m in re.finditer(r'<script type="(?:text/x-quiz|application/json)">(.*?)</script>', s, re.S):
        try: json.loads(m.group(1))
        except Exception as e: print('BAD json in', f, e, m.group(1)[:80]); bad += 1
    for m in re.finditer(r"data-cfg='(.*?)'", s, re.S):
        try: json.loads(m.group(1))
        except Exception as e: print('BAD cfg in', f, e); bad += 1
print('built', os.path.getsize(os.path.join(DIST, 'index.html')), 'bytes; problems:', bad)
sys.exit(1 if bad else 0)
