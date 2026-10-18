#!/usr/bin/env python3
"""Compile & run every runnable snippet in chapters; check 'out' quizzes against real output.
usage: verify.py [chapter ids...]"""
import os, re, sys, subprocess, tempfile, html, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, TMP, CXX
WRAP_HEAD = """#include <iostream>
#include <iomanip>
#include <string>
#include <string_view>
#include <cstdint>
#include <climits>
#include <cmath>
#include <cstring>
#include <memory>
#include <utility>
#include <limits>
"""
def wrap(code):
    inc, body = [], []
    for l in code.split('\n'): (inc if re.match(r'^\s*#', l) else body).append(l)
    return WRAP_HEAD + '\n'.join(inc) + '\nint main() {\n' + '\n'.join('    ' + l for l in body) + '\n    return 0;\n}\n'
def dedent(s):
    s = s.strip('\n').rstrip()
    ls = s.split('\n'); ind = min((len(l) - len(l.lstrip(' ')) for l in ls if l.strip()), default=0)
    return '\n'.join(l[ind:] for l in ls)
def run(code, stdin='', cxx=CXX):
    d = tempfile.mkdtemp(dir=TMP)
    src = os.path.join(d, 'main.cpp'); open(src, 'w').write(code)
    c = subprocess.run([cxx, '-std=c++20', '-w', src, '-o', os.path.join(d, 'a.out')], capture_output=True, text=True)
    if c.returncode: return 'CE', c.stderr
    try:
        r = subprocess.run([os.path.join(d, 'a.out')], input=stdin, capture_output=True, text=True, timeout=5)
        return r.returncode, r.stdout
    except subprocess.TimeoutExpired: return 'TL', ''
def norm(s): return '\n'.join(l.rstrip() for l in s.replace('\r\n', '\n').split('\n')).rstrip('\n')
ids = sys.argv[1:] or sorted(f[2:4] for f in os.listdir(os.path.join(ROOT, 'content')) if f.startswith('ch'))
fails = 0
for cid in ids:
    s = open(os.path.join(ROOT, 'content', f'ch{cid}.html'), encoding='utf-8').read()
    n = 0
    for m in re.finditer(r'<script type="text/x-cpp"([^>]*)>(.*?)</script>', s, re.S):
        attrs, code = m.group(1), dedent(m.group(2))
        if 'data-run' not in attrs: continue
        n += 1
        stdin = html.unescape(re.search(r'data-stdin="([^"]*)"', attrs).group(1)) if 'data-stdin' in attrs else ''
        full = wrap(code) if 'data-run="wrap"' in attrs else code
        rc, out = run(full, stdin)
        expect_ce = 'data-ce' in attrs
        if (rc == 'CE') != expect_ce or rc == 'TL':
            fails += 1; print(f'--- ch{cid} snippet #{n}: rc={rc} expectCE={expect_ce}\n{code[:300]}\n{out[:600]}')
    for m in re.finditer(r'<div class="qz" data-type="out"([^>]*)>(.*?)</div>\s*</div>', s, re.S):
        body = m.group(2); cm = re.search(r'<script type="text/x-cpp"[^>]*>(.*?)</script>', body, re.S)
        if not cm: continue
        pa = re.findall(r'<pre class="ans">(.*?)</pre>', body, re.S)
        ans = [html.unescape(a).lstrip('\n') for a in pa] if pa else html.unescape(re.search(r'data-ans="([^"]*)"', m.group(1)).group(1)).split('|')
        if any(a.strip() in ('CE', 'UB') for a in ans):
            rc, out = run(dedent(cm.group(1)))
            if ans[0].strip() == 'CE' and rc != 'CE': fails += 1; print(f'--- ch{cid} quiz expected CE but compiled')
            continue
        code = dedent(html.unescape(cm.group(1)) if False else cm.group(1))
        stdin_m = re.search(r'data-stdin="([^"]*)"', m.group(1))
        rc, out = run(code, html.unescape(stdin_m.group(1)) if stdin_m else '')
        if norm(out) not in [norm(a) for a in ans]:
            fails += 1; print(f'--- ch{cid} OUT-QUIZ mismatch: expected {ans!r} got {out!r} rc={rc}\n{code[:200]}')
    print(f'ch{cid}: {n} snippets checked')
print('FAILS:', fails)
