#!/usr/bin/env python3
"""Tasks -> data/tasks.json. Expected outputs are produced by running the reference solution."""
import json, os, subprocess, tempfile, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, SRC, TMP, CXX
SCR = os.path.join(TMP, 'tasks')
os.makedirs(SCR, exist_ok=True)
T = []
def task(id, ch, title, lvl, src, text, sol, tests, inp=None, out=None, starter=None, mode='io', harness=None, hint=None, check=None, show=2, solNote=None):
    T.append(dict(id=id, ch=ch, title=title, lvl=lvl, src=src, text=text, sol=sol.strip('\n') + '\n', tests=tests, **{'in': inp}, out=out,
                  starter=(starter or '').strip('\n') + '\n' if starter else None, mode=mode, harness=(harness or '').strip('\n') + '\n' if harness else None,
                  hint=hint, check=check, show=show, solNote=solNote))

IO = '#include <iostream>\n\nint main() {\n    // твой код\n    return 0;\n}\n'
def io_starter(extra=''):
    return '#include <iostream>\n' + extra + '\nint main() {\n    // твой код\n    return 0;\n}\n'

def build(t):
    return t['sol'] + ('\n' + t['harness'] if t['mode'] == 'func' else '')

def compile_run(code, inputs):
    h = hashlib.md5(code.encode()).hexdigest()[:10]
    d = os.path.join(SCR, h); os.makedirs(d, exist_ok=True)
    src = os.path.join(d, 'm.cpp'); exe = os.path.join(d, 'a')
    open(src, 'w').write(code)
    c = subprocess.run([CXX, '-std=c++20', '-Wall', '-Wno-unused', src, '-o', exe], capture_output=True, text=True)
    if c.returncode: return None, c.stderr
    outs = []
    for i in inputs:
        r = subprocess.run([exe], input=i, capture_output=True, text=True, timeout=10, cwd=d)
        if r.returncode != 0: return None, f'rc={r.returncode} on input {i!r}: {r.stderr[:300]}'
        outs.append('\n'.join(l.rstrip() for l in r.stdout.split('\n')).rstrip('\n'))
    return outs, c.stderr

exec(open(os.path.join(SRC, 'tasks_def.py'), encoding='utf-8').read())

def main():
    only = sys.argv[1:]
    old = {}
    p = os.path.join(ROOT, 'data', 'tasks.json')
    if os.path.exists(p) and only:
        for x in json.load(open(p)): old[x['id']] = x
    res = []; bad = 0; ids = set()
    for t in T:
        assert t['id'] not in ids, t['id']; ids.add(t['id'])
        if only and t['id'] not in only and t['id'] in old:
            res.append(old[t['id']]); continue
        outs, log = compile_run(build(t), [x for x in t['tests']])
        if outs is None:
            print('FAIL', t['id'], log[:1500]); bad += 1; continue
        if 'warning' in log: print('WARN', t['id'], log[:600])
        item = {k: v for k, v in t.items() if v is not None and k != 'tests'}
        item['tests'] = [{'i': i, 'o': o} for i, o in zip(t['tests'], outs)]
        # starter must at least be present
        if 'starter' not in item: item['starter'] = IO
        res.append(item)
    json.dump(res, open(p, 'w'), ensure_ascii=False, indent=0)
    print(len(res), 'tasks; failures:', bad)
main()
