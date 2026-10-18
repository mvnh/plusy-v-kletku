/* ================= core ================= */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k === 'html') el.innerHTML = v;
    else if (k === 'text') el.textContent = v;
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const kid of kids.flat()) if (kid != null && kid !== false) el.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
  return el;
}
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
let toastT;
function toast(msg, ms = 2600) {
  let t = $('.toast'); if (!t) { t = h('div', { class: 'toast', role: 'status' }); document.body.append(t); }
  t.textContent = msg; t.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => t.hidden = true, ms);
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
function plural(n, a, b, c) { n = Math.abs(n) % 100; const n1 = n % 10; if (n > 10 && n < 20) return c; if (n1 > 1 && n1 < 5) return b; if (n1 === 1) return a; return c; }
function normOut(s) { return String(s ?? '').replace(/\r\n/g, '\n').split('\n').map(l => l.replace(/[ \t]+$/, '')).join('\n').replace(/\n+$/, ''); }
function md(s) { // tiny markdown for AI answers: code fences, headings, inline code, bold, paragraphs, lists
  const parts = String(s).split(/```(\w*)\n?([\s\S]*?)```/g); let out = '';
  for (let i = 0; i < parts.length; i++) {
    if (i % 3 === 1) continue;
    if (i % 3 === 2) { out += '<pre>' + esc(parts[i].replace(/\n$/, '')) + '</pre>'; continue; }
    const blocks = parts[i].replace(/^#{1,6}[ \t]+.*$/gm, '\n$&\n').split(/\n{2,}/); // заголовок всегда в своём блоке, даже без пустых строк вокруг
    for (let b of blocks) {
      if (!b.trim()) continue;
      b = esc(b).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
      const hd = b.match(/^\s*#{1,6}[ \t]+(.*)$/);
      if (hd) out += '<p class="md-h">' + hd[1].trim() + '</p>';
      else if (/^\s*([-*]|\d+\.)\s/.test(b)) {
        const items = b.split(/\n(?=\s*(?:[-*]|\d+\.)\s)/).map(x => '<li>' + x.replace(/^\s*(?:[-*]|\d+\.)\s/, '').replace(/\n/g, '<br>') + '</li>').join('');
        out += /^\s*\d/.test(b) ? '<ol>' + items + '</ol>' : '<ul>' + items + '</ul>';
      } else out += '<p>' + b.replace(/\n/g, '<br>') + '</p>';
    }
  }
  return out;
}

/* ---------- progress store: localStorage cache + per-user cloud doc ---------- */
const Store = {
  key: 'pvk-progress-v1',
  data: { read: {}, quiz: {}, tasks: {}, pred: {}, cards: {}, exams: [], last: null, updated: 0 },
  cloud: null, saveT: null, saving: false, dirty: false,
  load() {
    try { const raw = localStorage.getItem(this.key); if (raw) Object.assign(this.data, JSON.parse(raw)); } catch (e) { }
  },
  touch() {
    this.data.updated = Date.now();
    try { localStorage.setItem(this.key, JSON.stringify(this.data)); } catch (e) { }
    this.dirty = true; clearTimeout(this.saveT); this.saveT = setTimeout(() => this.flush(), 2500);
    App.refreshProgress();
  },
  async flush() {
    if (!this.cloud || !this.dirty || this.saving) return;
    this.saving = true; this.dirty = false;
    try { await this.cloud.set({ json: JSON.stringify(this.data), updated: this.data.updated }); }
    catch (e) { if (e && e.code === 'invalid_argument') this.cloud = null; else this.dirty = true; }
    this.saving = false;
    if (this.dirty) { clearTimeout(this.saveT); this.saveT = setTimeout(() => this.flush(), 4000); }
  },
  merge(remote) { // union-ish merge: keep the "best" of both
    const a = this.data, b = remote;
    for (const k of ['read', 'quiz', 'pred']) a[k] = Object.assign({}, b[k] || {}, a[k] || {});
    a.tasks = a.tasks || {};
    for (const [id, t] of Object.entries(b.tasks || {})) {
      const m = a.tasks[id];
      if (!m) a.tasks[id] = t;
      else { m.solved = m.solved || t.solved; m.tries = Math.max(m.tries || 0, t.tries || 0); if (!m.code && t.code) m.code = t.code; }
    }
    for (const [id, c] of Object.entries(b.cards || {})) { const m = a.cards[id]; if (!m || (c.ts || 0) > (m.ts || 0)) a.cards[id] = c; }
    const seen = new Set((a.exams || []).map(e => e.ts)); for (const e of b.exams || []) if (!seen.has(e.ts)) a.exams.push(e);
    if (!a.last && b.last) a.last = b.last;
  },
  async initCloud() {
    try {
      if (!window.claude || !window.claude.use) return;
      const [db, user] = await Promise.all([claude.use('db'), claude.use('user')]);
      if (!db || !user) return;
      const id = await user.id(); if (!id) return;
      this.cloud = db.doc('data/users/' + id + '/progress');
      const snap = await this.cloud.get();
      if (snap.exists) {
        const d = snap.data(); try { this.merge(JSON.parse(d.json)); } catch (e) { }
        try { localStorage.setItem(this.key, JSON.stringify(this.data)); } catch (e) { }
        App.refreshProgress(); App.rerenderSoft();
      }
      this.dirty = true; this.flush();
      $('#sync').textContent = 'прогресс в облаке'; $('#sync').title = 'Прогресс сохраняется в твоём аккаунте и виден на всех устройствах';
    } catch (e) { /* stay local */ }
  }
};

/* ---------- content loading ---------- */
const Data = {
  manifest: null, chapters: {}, tasks: null, pred: null, cards: null, theory: null,
  async json(p) { const r = await fetch(p); if (!r.ok) throw new Error(p + ': ' + r.status); return r.json(); },
  async text(p) { const r = await fetch(p); if (!r.ok) throw new Error(p + ': ' + r.status); return r.text(); },
  async init() {
    this.manifest = await this.json('content/manifest.json');
    [this.tasks, this.pred, this.cards, this.theory] = await Promise.all([
      this.json('data/tasks.json').catch(() => []), this.json('data/predict.json').catch(() => []),
      this.json('data/cards.json').catch(() => []), this.json('data/theory.json').catch(() => [])]);
  },
  chapter(id) { return this.manifest.chapters.find(c => c.id === id); },
  async chapterHTML(id) { if (!this.chapters[id]) this.chapters[id] = await this.text('content/ch' + id + '.html'); return this.chapters[id]; },
  task(id) { return this.tasks.find(t => t.id === id); }
};
