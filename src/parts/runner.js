/* ================= C++ runner: local compiler via server.py ================= */
const API = async (path, body) => {
  const r = await fetch(path, body === undefined ? {} : { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-PVK': '1' }, body: JSON.stringify(body) });
  let j = null; try { j = await r.json(); } catch (e) { }
  if (!r.ok && !j) throw new Error(path + ': HTTP ' + r.status);
  return j;
};
const Runner = {
  ready: false, ok: true, info: null, loading: null, cache: new Map(),
  status() {
    if (!this.info) return this.loading ? 'проверяю компилятор…' : 'компилятор: сервер не отвечает';
    if (!this.info.ok) return '⚠ компилятор не найден';
    return (this.info.cxx || 'c++') + ' · -std=' + this.info.std;
  },
  setStatus() { for (const e of $$('.compiler-state')) { e.textContent = this.status(); if (this.info) e.title = this.info.version || this.info.error || ''; } },
  boot() {
    if (this.loading) return this.loading;
    this.loading = API('/api/info').then(i => { this.info = i; this.ready = !!i.ok; this.ok = !!i.ok; this.setStatus(); App.onInfo && App.onInfo(i); return i; })
      .catch(e => { this.ok = false; this.loading = null; this.setStatus(); throw new Error('Сервер платформы не отвечает. Запусти его: python3 server.py'); });
    return this.loading;
  },
  clean(log) { return String(log || '').replace(/\x1b\[[0-9;]*m/g, ''); },
  async compile(src, opt = '-O0') {
    const key = opt + '\n' + src; if (this.cache.has(key)) return this.cache.get(key);
    const i = await this.boot(); if (!i.ok) return { ok: false, log: i.error };
    const r = await API('/api/compile', { src, opt });
    const out = { ok: !!r.ok, log: this.clean(r.log), id: r.id };
    if (this.cache.size > 50) this.cache.delete(this.cache.keys().next().value);
    if (out.ok) this.cache.set(key, out);
    return out;
  },
  async exec(comp, stdin = '', { timeout = 4000 } = {}) {
    try { return await API('/api/run', { id: comp.id, stdin, timeout: timeout / 1000 }); }
    catch (e) { return { stdout: '', stderr: '', code: null, trap: 'сервер не ответил: ' + e.message }; }
  },
  async run(src, stdin = '', o = {}) {
    const c = await this.compile(src, o.opt || '-O0');
    if (!c.ok) return { stage: 'compile', log: c.log };
    const r = await this.exec(c, stdin); r.log = c.log; return r;
  }
};
