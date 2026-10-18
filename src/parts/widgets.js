/* ================= interactive widgets ================= */
const Widgets = {};
function vizBox(title, ...ctl) { const b = h('div', { class: 'viz' }); b.append(h('div', { class: 'vh' }, h('b', {}, title), h('span', { class: 'sp' }), ...ctl)); return b; }
function seg(items, cur, on) {
  const s = h('div', { class: 'seg', role: 'group' });
  for (const [v, l] of items) { const b = h('button', { type: 'button', class: v === cur ? 'on' : '' }, l); b.onclick = () => { $$('button', s).forEach(x => x.classList.remove('on')); b.classList.add('on'); on(v); }; s.append(b); }
  return s;
}

/* ---- bits: целые числа в памяти, дополнительный код, переполнение, битовые операции ---- */
const INT_T = { int8: [8, 1, 'signed char / int8_t'], uint8: [8, 0, 'unsigned char / uint8_t'], int16: [16, 1, 'short / int16_t'], uint16: [16, 0, 'unsigned short'], int32: [32, 1, 'int / int32_t'], uint32: [32, 0, 'unsigned int / uint32_t'] };
function bitsOf(u, n) { const a = []; for (let i = n - 1; i >= 0; i--) a.push(Math.floor(u / 2 ** i) % 2); return a; }
function sval(u, n, s) { return s && u >= 2 ** (n - 1) ? u - 2 ** n : u; }
function wrapU(x, n) { const m = 2 ** n; return ((x % m) + m) % m; }
Widgets.bits = (el, cfg) => {
  let type = cfg.type || 'int8', u = wrapU(cfg.value ?? 5, INT_T[type][0]), b2 = wrapU(cfg.b ?? 12, INT_T[type][0]), op = cfg.op || '&';
  const ops = !!cfg.ops;
  const box = vizBox(ops ? 'Битовые операции' : 'Целое число в памяти', seg(Object.keys(INT_T).filter(k => !cfg.only || cfg.only.includes(k)).map(k => [k, k]), type, v => { type = v; const n = INT_T[v][0]; u = wrapU(sval(u, 32, 0), n); b2 = wrapU(b2, n); draw(); }));
  const body = h('div'); box.append(body); el.replaceWith(box);
  const row = (val, n, clickable, onFlip, signed) => {
    const r = h('div', { class: 'bitrow' + (n > 16 ? ' sm' : '') });
    bitsOf(val, n).forEach((b, i) => {
      const idx = n - 1 - i;
      const d = h('div', { class: 'bit' + (b ? ' one' : '') + (signed && i === 0 ? ' sign' : '') + (i > 0 && i % 8 === 0 ? ' gap' : ''), title: 'бит ' + idx + ' (вес ' + (signed && i === 0 ? '−' : '') + '2^' + idx + ')' }, String(b));
      if (n <= 16 || i % 4 === 0) d.append(h('i', {}, String(idx)));
      if (clickable) { d.tabIndex = 0; d.setAttribute('role', 'button'); d.onclick = () => onFlip(idx); d.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onFlip(idx); } }; }
      r.append(d);
    });
    return r;
  };
  const hex = (x, n) => '0x' + x.toString(16).toUpperCase().padStart(n / 4, '0');
  function draw() {
    const [n, s] = INT_T[type]; body.innerHTML = '';
    const v = sval(u, n, s), min = s ? -(2 ** (n - 1)) : 0, max = s ? 2 ** (n - 1) - 1 : 2 ** n - 1;
    const flip = idx => { u = (Math.floor(u / 2 ** idx) % 2) ? u - 2 ** idx : u + 2 ** idx; draw(); };
    const inp = h('input', { class: 'qin', type: 'number', value: v, style: 'max-width:160px', 'aria-label': 'десятичное значение' });
    inp.onchange = () => { const x = Math.trunc(Number(inp.value)); if (!isFinite(x)) return; u = wrapU(x, n); draw(); };
    body.append(h('div', { class: 'vsmall', style: 'margin-bottom:16px' }, INT_T[type][2] + ` · ${n} бит · диапазон [${min}; ${max}] · кликай по битам`));
    body.append(row(u, n, true, flip, s));
    let flag = '';
    const step = d => { const raw = v + d; const out = raw < min || raw > max; u = wrapU(raw, n); draw(); if (out) toast(s ? `Переполнение знакового типа: в C++ это UB. Железо просто «прокрутило» значение.` : `Беззнаковый тип: арифметика по модулю 2^${n}, всё законно.`, 4200); };
    const ctl = h('div', { class: 'qrow', style: 'margin-top:12px' }, inp,
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => step(1) }, '+1'),
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => step(-1) }, '−1'),
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { u = wrapU(max, n); draw(); } }, 'max'),
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { u = wrapU(min, n); draw(); } }, 'min'),
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { u = 2 ** n - 1 - u; draw(); } }, '~x'),
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { u = wrapU(u * 2, n); draw(); } }, 'x << 1'),
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { u = s ? wrapU(Math.floor(v / 2), n) : Math.floor(u / 2); draw(); } }, 'x >> 1'));
    body.append(ctl);
    const kv = h('dl', { class: 'kv' });
    const add = (k, val) => kv.append(h('dt', {}, k), h('dd', { html: val }));
    add('десятичное', `<b>${v}</b>`); add('hex', hex(u, n));
    if (s) {
      add('старший бит', u >= 2 ** (n - 1) ? '1 → число отрицательное' : '0 → число неотрицательное');
      if (v < 0) {
        const absb = bitsOf(-v, n).join(''), inv = bitsOf(2 ** n - 1 - (-v), n).join('');
        add('как получилось', `|x| = ${-v} → <code>${absb.length > 16 ? absb.slice(-16) : absb}</code><br>инвертируем → <code>${inv.length > 16 ? '…' + inv.slice(-16) : inv}</code><br>+1 → <code>${bitsOf(u, n).join('').slice(-16)}</code> = дополнительный код`);
      }
      if (v === min) add('заметь', 'у минимального числа нет положительной пары: −(' + min + ') не влезает в тип');
    }
    body.append(kv);
    if (ops) {
      body.append(h('div', { style: 'margin:16px 0 6px', class: 'vsmall' }, 'Второй операнд b (тоже кликабельный):'));
      body.append(row(b2, n, true, idx => { b2 = (Math.floor(b2 / 2 ** idx) % 2) ? b2 - 2 ** idx : b2 + 2 ** idx; draw(); }, s));
      body.append(h('div', { style: 'margin:12px 0' }, seg([['&', 'a & b'], ['|', 'a | b'], ['^', 'a ^ b']], op, v2 => { op = v2; draw(); })));
      const r = op === '&' ? bitsOf(u, n).map((x, i) => x & bitsOf(b2, n)[i]) : op === '|' ? bitsOf(u, n).map((x, i) => x | bitsOf(b2, n)[i]) : bitsOf(u, n).map((x, i) => x ^ bitsOf(b2, n)[i]);
      const ru = r.reduce((acc, x) => acc * 2 + x, 0);
      body.append(h('div', { class: 'vsmall', style: 'margin:4px 0 16px' }, 'Результат:'), row(ru, n, false, null, s));
      body.append(h('p', { class: 'vsmall', html: `a = <b>${v}</b>, b = <b>${sval(b2, n, s)}</b>, a ${op} b = <b>${sval(ru, n, s)}</b>` }));
    }
  }
  draw();
};

/* ---- IEEE 754 float ---- */
Widgets.ieee = (el, cfg) => {
  const dv = new DataView(new ArrayBuffer(4)); let bits = 0;
  const set = x => { dv.setFloat32(0, x); bits = dv.getUint32(0); };
  set(cfg.value ?? -121.1);
  const presets = cfg.presets || [0.1, 0.2, 0.3, -121.1, 1, 0.5, 16777217, 1e30, 'Infinity', 'NaN'];
  const box = vizBox('IEEE 754 · float (32 бита)'); const body = h('div'); box.append(body); el.replaceWith(box);
  function exactDec(M, e) { // M * 2^e exactly
    if (e >= 0) return (BigInt(M) << BigInt(e)).toString();
    const k = -e; let s = (BigInt(M) * 5n ** BigInt(k)).toString().padStart(k + 1, '0');
    s = s.slice(0, s.length - k) + '.' + s.slice(s.length - k); return s.replace(/0+$/, '').replace(/\.$/, '');
  }
  function draw() {
    body.innerHTML = '';
    dv.setUint32(0, bits); const f = dv.getFloat32(0);
    const S = bits >>> 31, P = (bits >>> 23) & 255, Mf = bits & 0x7fffff;
    const inp = h('input', { class: 'qin', value: String(f), style: 'max-width:200px', 'aria-label': 'число' });
    inp.onchange = () => { const x = Number(inp.value.replace(',', '.')); if (inp.value.trim() === '' || (isNaN(x) && inp.value.trim().toLowerCase() !== 'nan')) return; set(x); draw(); };
    body.append(h('div', { class: 'qrow' }, inp, ...presets.map(p => h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { set(Number(p)); draw(); } }, String(p)))));
    const r = h('div', { class: 'bitrow sm', style: 'margin-top:22px' });
    for (let i = 31; i >= 0; i--) {
      const b = (bits >>> i) & 1, cls = i === 31 ? 'sign' : i >= 23 ? 'exp' : 'man';
      const d = h('div', { class: 'bit ' + cls + (b ? ' one' : '') + (i === 30 || i === 22 ? ' gap' : ''), tabIndex: 0, role: 'button', title: cls === 'sign' ? 'знак' : cls === 'exp' ? 'порядок' : 'мантисса' }, String(b));
      if (i === 31 || i === 30 || i === 22 || i === 0) d.append(h('i', {}, String(i)));
      d.onclick = () => { bits = (bits ^ (1 << i)) >>> 0; draw(); };
      d.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); d.click(); } };
      r.append(d);
    }
    body.append(r, h('div', { class: 'legend', style: 'margin-top:8px' },
      h('span', {}, h('i', { style: 'background:var(--red)' }), 'знак S (1 бит)'), h('span', {}, h('i', { style: 'background:var(--green)' }), 'порядок P (8 бит)'), h('span', {}, h('i', { style: 'background:var(--violet)' }), 'мантисса M (23 бита)')));
    const kv = h('dl', { class: 'kv' }); const add = (k, v) => kv.append(h('dt', {}, k), h('dd', { html: v }));
    add('hex', '0x' + bits.toString(16).toUpperCase().padStart(8, '0'));
    add('S', `${S} → ${S ? 'минус' : 'плюс'}`);
    if (P === 255) add('особый случай', Mf ? '<b>NaN</b> (порядок из единиц, мантисса ≠ 0)' : `<b>${S ? '−' : '+'}inf</b> (порядок из единиц, мантисса = 0)`);
    else if (P === 0) { add('P', '0 → денормализованное число (без неявной единицы)'); add('значение', `(−1)^${S} × 0.M × 2^(−126) = <b>${S ? '-' : ''}${exactDec(Mf, -149)}</b>`); }
    else {
      add('P', `${P} → истинный порядок E = P − 127 = <b>${P - 127}</b>`);
      add('1.M', '1.' + Mf.toString(2).padStart(23, '0').replace(/0+$/, '') + ' (двоичная)');
      add('хранится точно', `<b>${S ? '-' : ''}${exactDec(Mf + 2 ** 23, P - 127 - 23)}</b>`);
    }
    add('как float', String(f));
    body.append(kv);
  }
  draw();
};

/* ---- struct layout / выравнивание ---- */
const TY = { char: [1, 1], bool: [1, 1], short: [2, 2], int: [4, 4], float: [4, 4], long: [8, 8], double: [8, 8], 'int*': [8, 8], int64_t: [8, 8] };
const FCOL = ['var(--pen)', 'var(--green)', 'var(--violet)', 'var(--red)', 'var(--tk-type)', 'var(--tk-str)', 'var(--tk-pre)', 'var(--ink-2)'];
Widgets.align = (el, cfg) => {
  let fields = (cfg.fields || [['char', 'a'], ['long', 'c'], ['int', 'b']]).map(x => [...x]); let pack = false;
  const box = vizBox('Раскладка struct в памяти (64-бит Linux/macOS)'); const body = h('div'); box.append(body); el.replaceWith(box);
  function layout() {
    let off = 0, al = 1; const items = [];
    for (const [t, n] of fields) { const [sz, a0] = TY[t]; const a = pack ? 1 : a0; al = Math.max(al, a); const pad = (a - off % a) % a; if (pad) items.push({ pad }); off += pad; items.push({ t, n, sz, off }); off += sz; }
    const tail = (al - off % al) % al; if (tail) items.push({ pad: tail, tail: 1 }); return { items, size: off + tail, al };
  }
  function draw() {
    body.innerHTML = ''; const L = layout();
    const list = h('div', { class: 'fields' });
    fields.forEach((f, i) => {
      const sel = h('select', { class: 'qin', style: 'max-width:110px;min-width:0;flex:none;padding:3px 6px', 'aria-label': 'тип поля' }, ...Object.keys(TY).map(t => h('option', { value: t, selected: t === f[0] }, t)));
      sel.onchange = () => { f[0] = sel.value; draw(); };
      list.append(h('div', { class: 'fieldrow' }, h('i', { style: `width:12px;height:12px;border-radius:3px;background:${FCOL[i % 8]};display:inline-block` }), sel, h('span', {}, f[1] + ';'),
        h('button', { type: 'button', title: 'выше', 'aria-label': 'выше', onclick: () => { if (i) { [fields[i - 1], fields[i]] = [fields[i], fields[i - 1]]; draw(); } } }, '↑'),
        h('button', { type: 'button', title: 'ниже', 'aria-label': 'ниже', onclick: () => { if (i < fields.length - 1) { [fields[i + 1], fields[i]] = [fields[i], fields[i + 1]]; draw(); } } }, '↓'),
        h('button', { type: 'button', title: 'удалить', 'aria-label': 'удалить', onclick: () => { if (fields.length > 1) { fields.splice(i, 1); draw(); } } }, '×')));
    });
    body.append(h('div', { class: 'qrow' }, h('code', {}, 'struct S {'), h('span', { class: 'sp' })), list, h('code', {}, '};'));
    const by = h('div', { class: 'bytes' }); let k = 0;
    for (const it of L.items) {
      if (it.pad) for (let j = 0; j < it.pad; j++) by.append(h('div', { class: 'byte pad', title: it.tail ? 'хвостовой padding' : 'padding' }, '·'));
      else { const idx = fields.findIndex(f => f[1] === it.n); for (let j = 0; j < it.sz; j++) by.append(h('div', { class: 'byte', style: 'background:' + FCOL[idx % 8], title: it.n + ' (' + it.t + '), смещение ' + it.off }, j === 0 ? it.n : '')); }
      k++;
    }
    const useful = fields.reduce((a, f) => a + TY[f[0]][0], 0);
    body.append(by, h('p', { class: 'vsmall', html: `<b>sizeof(S) = ${L.size}</b>, alignof(S) = ${L.al}; полезных байт ${useful}, на «дырки» ушло ${L.size - useful}` }));
    body.append(h('div', { class: 'qrow' },
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { fields.sort((a, b) => TY[b[0]][1] - TY[a[0]][1]); draw(); } }, 'отсортировать по выравниванию'),
      h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { const names = 'abcdefghij'; const nm = names.split('').find(c => !fields.some(f => f[1] === c)) || 'z'; fields.push(['char', nm]); draw(); } }, '+ поле'),
      h('label', { class: 'vsmall', style: 'display:inline-flex;gap:6px;align-items:center' }, Object.assign(h('input', { type: 'checkbox', checked: pack }), { onchange: e => { pack = e.target.checked; draw(); } }), '#pragma pack(1)')));
  }
  draw();
};

/* ---- matrix fill patterns ---- */
const MX_CODE = {
  rows: `for (int i = 0; i < n; ++i)
    for (int j = 0; j < n; ++j)
        a[i][j] = ++k;`,
  cols: `for (int j = 0; j < n; ++j)
    for (int i = 0; i < n; ++i)
        a[i][j] = ++k;`,
  snake: `for (int i = 0; i < n; ++i)
    for (int j = 0; j < n; ++j)
        a[i][i % 2 == 0 ? j : n - 1 - j] = ++k;`,
  diag: `for (int s = 0; s <= 2 * (n - 1); ++s)   // s = i + j
    for (int i = 0; i < n; ++i) {
        int j = s - i;
        if (j >= 0 && j < n) a[i][j] = ++k;
    }`,
  spiral: `int top = 0, bottom = n - 1, left = 0, right = n - 1;
while (top <= bottom && left <= right) {
    for (int j = left; j <= right; ++j) a[top][j] = ++k;
    ++top;
    for (int i = top; i <= bottom; ++i) a[i][right] = ++k;
    --right;
    if (top <= bottom) {
        for (int j = right; j >= left; --j) a[bottom][j] = ++k;
        --bottom;
    }
    if (left <= right) {
        for (int i = bottom; i >= top; --i) a[i][left] = ++k;
        ++left;
    }
}`
};
function mxOrder(p, n) {
  const o = [];
  if (p === 'rows') for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) o.push([i, j]);
  if (p === 'cols') for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) o.push([i, j]);
  if (p === 'snake') for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) o.push([i, i % 2 === 0 ? j : n - 1 - j]);
  if (p === 'diag') for (let s = 0; s <= 2 * (n - 1); s++) for (let i = 0; i < n; i++) { const j = s - i; if (j >= 0 && j < n) o.push([i, j]); }
  if (p === 'spiral') { let t = 0, b = n - 1, l = 0, r = n - 1; while (t <= b && l <= r) { for (let j = l; j <= r; j++) o.push([t, j]); t++; for (let i = t; i <= b; i++) o.push([i, r]); r--; if (t <= b) { for (let j = r; j >= l; j--) o.push([b, j]); b--; } if (l <= r) { for (let i = b; i >= t; i--) o.push([i, l]); l++; } } }
  return o;
}
Widgets.matrix = (el, cfg) => {
  let p = cfg.pattern || 'spiral', n = cfg.n || 5, timer = null, k = 0;
  const box = vizBox('Заполнение матрицы', seg([['rows', 'по строкам'], ['cols', 'по столбцам'], ['snake', 'змейка'], ['diag', 'диагонали'], ['spiral', 'спираль']], p, v => { p = v; reset(); }));
  const grid = h('div', { class: 'mx' }); const codeBox = h('div', { class: 'code' }); const cp = h('pre'); codeBox.append(cp);
  const nIn = h('input', { type: 'range', min: 2, max: 8, value: n, 'aria-label': 'размер n' }); const nl = h('span', { class: 'vsmall' });
  nIn.oninput = () => { n = +nIn.value; reset(); };
  const play = h('button', { type: 'button', class: 'btn sm' }, '▶ заполнить');
  const stepB = h('button', { type: 'button', class: 'btn ghost sm' }, 'шаг');
  box.append(h('div', { class: 'qrow' }, play, stepB, h('label', { class: 'vsmall', style: 'display:inline-flex;gap:8px;align-items:center' }, 'n', nIn), nl), grid, codeBox);
  el.replaceWith(box);
  let order = [];
  function reset() {
    clearInterval(timer); timer = null; play.textContent = '▶ заполнить'; k = 0; order = mxOrder(p, n); nl.textContent = 'n = ' + n;
    grid.style.gridTemplateColumns = `repeat(${n}, minmax(0, 44px))`; grid.innerHTML = '';
    for (let i = 0; i < n * n; i++) grid.append(h('div'));
    highlight(cp, `int k = 0;\n${MX_CODE[p]}`);
  }
  function step() {
    if (k >= order.length) { clearInterval(timer); timer = null; play.textContent = '↺ заново'; return false; }
    $$('div.now', grid).forEach(d => d.classList.replace('now', 'on'));
    const [i, j] = order[k++]; const c = grid.children[i * n + j]; c.textContent = k; c.className = 'now'; return true;
  }
  play.onclick = () => {
    if (timer) { clearInterval(timer); timer = null; play.textContent = '▶ дальше'; return; }
    if (k >= order.length) reset();
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) { while (step()); return; }
    play.textContent = '⏸ пауза'; timer = setInterval(step, Math.max(90, 900 / n));
  };
  stepB.onclick = () => { if (k >= order.length) reset(); step(); };
  reset();
};

/* ---- tracer: пошаговое исполнение с памятью ---- */
Widgets.trace = (el, spec) => {
  const box = vizBox(spec.title || 'Пошаговый отладчик'); el.replaceWith(box);
  const codeEl = h('div', { class: 'tr-code' }); const lines = dedent(spec.code).split('\n');
  lines.forEach(l => { const d = h('div'); highlight(d, l || ' '); codeEl.append(d); });
  const mem = h('div', { class: 'tr-mem' }); const out = h('div', { class: 'tr-out' }); const note = h('div', { class: 'tr-note' });
  const hasOut = spec.steps.some(s => s.out != null);
  const left = h('div', {}, codeEl, hasOut ? h('div', { class: 'tr-col', style: 'margin-top:8px' }, h('h5', {}, 'Вывод'), out) : '');
  box.append(h('div', { class: 'tr' }, left, mem), note);
  let i = 0, timer = null; const N = spec.steps.length;
  const btn = (t, l, f) => h('button', { type: 'button', class: 'btn ghost sm', title: l, 'aria-label': l, onclick: f }, t);
  const n = h('span', { class: 'stepn' });
  const playB = btn('▶▶', 'автоплей', () => { if (timer) stop(); else { playB.textContent = '⏸'; timer = setInterval(() => { if (i < N - 1) go(i + 1); else stop(); }, 1300); } });
  const stop = () => { clearInterval(timer); timer = null; playB.textContent = '▶▶'; };
  box.append(h('div', { class: 'tr-ctl' }, btn('⏮', 'в начало', () => { stop(); go(0); }), btn('◀ назад', 'шаг назад', () => { stop(); go(Math.max(0, i - 1)); }), h('button', { type: 'button', class: 'btn sm', onclick: () => { stop(); go(Math.min(N - 1, i + 1)); } }, 'шаг ▶'), playB, n));
  box.tabIndex = 0; box.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { e.preventDefault(); go(Math.min(N - 1, i + 1)); } if (e.key === 'ArrowLeft') { e.preventDefault(); go(Math.max(0, i - 1)); } });
  const valMap = st => { const m = {}; (st.st || []).forEach((f, fi) => (f.v || []).forEach(v => m['s' + fi + ':' + v[0]] = JSON.stringify(v[2]))); (st.gl || []).forEach(v => m['g:' + v[0]] = JSON.stringify(v[2])); (st.hp || []).forEach(b => m['h:' + b.id] = JSON.stringify(b.c)); return m; };
  function cellsEl(vals, idBase, prevVals) {
    const c = h('div', { class: 'cells idx' });
    vals.forEach((v, k) => c.append(h('div', { class: 'cell' + (v === "'\\0'" ? ' term' : '') + (prevVals && prevVals[k] !== v ? ' chg' : ''), 'data-id': idBase + '.' + k }, String(v), h('sub', {}, String(k)))));
    return c;
  }
  function varEl(v, key, prev) {
    const [name, type, val, ex = {}] = v; const changed = prev && key in prev && prev[key] !== JSON.stringify(val);
    const id = ex.id || name;
    if (Array.isArray(val)) {
      let pv = null; try { pv = prev && prev[key] ? JSON.parse(prev[key]) : null; } catch (e) { }
      const d = h('div', { class: 'var' + (ex.dead ? ' dead' : ''), 'data-id': id, style: 'grid-template-columns:1fr' }, h('div', {}, h('span', { class: 'n' }, name), ' ', h('span', { class: 't' }, type), ex.a ? h('span', { class: 'a' }, '  @' + ex.a) : ''), cellsEl(val, id, pv));
      return d;
    }
    const d = h('div', { class: 'var' + (changed ? ' chg' : '') + (ex.dead ? ' dead' : ''), 'data-id': id },
      h('div', {}, h('span', { class: 'n' }, name), ' ', h('span', { class: 't' }, type)), h('span', { class: 'a' }, ex.a ? '@' + ex.a : ''), h('span', { class: 'v', 'data-from': ex.p || '' , 'data-dang': ex.dang ? '1' : '' }, String(val)));
    return d;
  }
  function go(k) {
    const prev = i !== k && k > 0 ? valMap(spec.steps[k - 1]) : null;
    i = k; const st = spec.steps[i]; n.textContent = `шаг ${i + 1} / ${N}`;
    [...codeEl.children].forEach((d, j) => d.classList.toggle('cur', j + 1 === st.l));
    const cur = codeEl.children[st.l - 1]; if (cur) { const top = cur.offsetTop - codeEl.clientHeight / 2; codeEl.scrollTop = Math.max(0, top); }
    note.innerHTML = st.n || ''; out.textContent = st.out ?? (i ? out.textContent : '');
    if (st.out == null) { let o = ''; for (let j = 0; j <= i; j++) if (spec.steps[j].out != null) o = spec.steps[j].out; out.textContent = o; }
    mem.innerHTML = '';
    if (st.gl && st.gl.length) { const c = h('div', { class: 'tr-col' }, h('h5', {}, 'Статическая память')); const f = h('div', { class: 'frame' }); st.gl.forEach(v => f.append(varEl(v, 'g:' + v[0], prev))); c.append(f); mem.append(c); }
    const sc = h('div', { class: 'tr-col' }, h('h5', {}, 'Стек ↓ (последний вызов сверху)'));
    const frames = st.st || []; frames.map((f, fi) => [f, fi]).reverse().forEach(([f, fi]) => {
      const fr = h('div', { class: 'frame' + (fi === frames.length - 1 ? ' top-f' : '') }, h('div', { class: 'fn' }, h('span', {}, f.f), h('span', { class: 'a' }, f.note || '')));
      (f.v || []).forEach(v => fr.append(varEl(v, 's' + fi + ':' + v[0], prev)));
      if (!(f.v || []).length) fr.append(h('div', { class: 'var' }, h('span', { class: 't' }, 'нет переменных')));
      sc.append(fr);
    });
    if (!frames.length) sc.append(h('div', { class: 'vsmall' }, 'пусто'));
    mem.append(sc);
    if (st.hp && st.hp.length) {
      const hc = h('div', { class: 'tr-col' }, h('h5', {}, 'Куча (динамическая память)'));
      st.hp.forEach(b => { let pv = null; try { pv = prev && prev['h:' + b.id] ? JSON.parse(prev['h:' + b.id]) : null; } catch (e) { } hc.append(h('div', { class: 'heapb' + (b.free ? ' freed' : ''), 'data-id': b.id }, h('div', { class: 'hl' }, h('span', {}, b.l), h('span', {}, b.a ? '@' + b.a : '')), b.c ? cellsEl(b.c, b.id, pv) : '')); });
      mem.append(hc);
    }
    requestAnimationFrame(arrows);
  }
  function arrows() {
    $$('svg.tr-svg', mem).forEach(s => s.remove());
    const srcs = $$('[data-from]', mem).filter(e => e.dataset.from); if (!srcs.length) return;
    const R = mem.getBoundingClientRect(); const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); svg.setAttribute('class', 'tr-svg');
    svg.setAttribute('width', R.width); svg.setAttribute('height', R.height);
    const defs = `<defs><marker id="ah${box._uid}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--pen)" stroke="none"/></marker></defs>`;
    let html = defs;
    for (const s of srcs) {
      const t = mem.querySelector(`[data-id="${CSS.escape(s.dataset.from)}"]`); if (!t) continue;
      const a = s.getBoundingClientRect(), b = t.getBoundingClientRect();
      const x1 = a.right - R.left + 2, y1 = a.top + a.height / 2 - R.top;
      const x2 = b.left - R.left - 2 + (b.width < 60 ? b.width / 2 + 2 : 0), y2 = b.width < 60 ? b.top - R.top - 1 : b.top + b.height / 2 - R.top;
      const bend = Math.max(40, Math.abs(y2 - y1) / 2);
      const d = b.width < 60 ? `M${x1},${y1} C${x1 + bend},${y1} ${x2},${y2 - bend} ${x2},${y2}` : `M${x1},${y1} C${x1 + bend},${y1} ${Math.max(x1 + bend, x2 + 40)},${y2} ${x2},${y2}`;
      html += `<path d="${d}" class="${s.dataset.dang ? 'dang' : ''}" marker-end="url(#ah${box._uid})"/>`;
    }
    svg.innerHTML = html; mem.append(svg);
  }
  box._uid = Math.random().toString(36).slice(2, 7);
  new ResizeObserver(() => requestAnimationFrame(arrows)).observe(mem);
  go(0);
};

function hydrateWidgets(root) {
  for (const el of $$('.viz-slot', root)) {
    const kind = el.dataset.viz; let cfg = {};
    try { cfg = JSON.parse(el.dataset.cfg || '{}'); } catch (e) { }
    try { Widgets[kind] ? Widgets[kind](el, cfg) : el.replaceWith(h('div', { class: 'c c-ub' }, 'Нет виджета ' + kind)); } catch (e) { console.error(e); }
  }
  for (const s of $$('div.trace', root)) {
    try {
      const spec = JSON.parse($('script[type="application/json"]', s).textContent);
      spec.code = $('script[type="text/x-cpp"]', s).textContent; spec.title = s.dataset.title || spec.title;
      Widgets.trace(s, spec);
    } catch (e) { console.error(e); s.replaceWith(h('div', { class: 'c c-ub' }, 'Битый трейс: ' + e.message)); }
  }
}
