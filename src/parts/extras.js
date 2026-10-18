/* ================= flashcards (Leitner) ================= */
const DAY = 864e5, BOX_INT = [0, 1, 2, 4, 8, 16, 32].map(d => d * DAY);
const Cards = {
  deck: '',
  state(id) { return Store.data.cards[id] || { box: 0, due: 0 }; },
  dueCount() { const now = Date.now(); return (Data.cards || []).filter(c => { const s = Store.data.cards[c.id]; return !s || s.due <= now; }).length; },
  view() {
    App.view = 'cards'; const main = $('#main'); const col = h('div', { class: 'col' });
    const deckSel = h('select', { class: 'qin', style: 'max-width:320px;flex:none', 'aria-label': 'колода' }, h('option', { value: '' }, 'все главы'), ...Data.manifest.chapters.filter(c => Data.cards.some(x => x.ch === c.id)).map(c => h('option', { value: c.id, selected: this.deck === c.id }, c.n + '. ' + c.title)));
    const modeSel = h('select', { class: 'qin', style: 'max-width:220px;flex:none', 'aria-label': 'режим' }, h('option', { value: 'due' }, 'только к повторению'), h('option', { value: 'all' }, 'все карточки подряд'));
    col.append(h('div', { class: 'eyebrow' }, 'Тренажёр'), h('h1', {}, 'Флешкарты'),
      h('p', { class: 'vsmall', style: 'font-size:16px' }, 'Определения, правила и ловушки из конспекта. Интервальное повторение: что помнишь — вернётся через 1, 2, 4, 8… дней, что забыл — сегодня же ещё раз.'),
      h('div', { class: 'qrow' }, deckSel, modeSel));
    const stage = h('div'); col.append(stage); main.append(col);
    let queue = [];
    const build = () => {
      this.deck = deckSel.value; const now = Date.now();
      queue = Data.cards.filter(c => (!this.deck || c.ch === this.deck) && (modeSel.value === 'all' || (this.state(c.id).due <= now)));
      queue.sort((a, b) => this.state(a.id).box - this.state(b.id).box || Math.random() - .5);
      next();
    };
    const next = () => {
      stage.innerHTML = '';
      if (!queue.length) { stage.append(h('div', { class: 'empty' }, h('p', { style: 'font-size:20px' }, '🎉 На сегодня всё.'), h('p', {}, 'Карточки вернутся, когда подойдёт срок. Можно переключиться на «все карточки подряд».'))); App.refreshProgress(); return; }
      const c = queue[0]; const s = this.state(c.id); const chn = Data.chapter(c.ch);
      const fc = h('div', { class: 'fc', tabIndex: 0, role: 'button', 'aria-label': 'перевернуть карточку' },
        h('div', { class: 'front' }, h('div', { class: 'lab' }, `гл. ${chn?.n} · коробка ${s.box} · осталось ${queue.length}`), h('div', { class: 'body', html: c.f }), h('div', { class: 'vsmall' }, 'клик или пробел — перевернуть')),
        h('div', { class: 'back' }, h('div', { class: 'lab' }, 'ответ'), h('div', { class: 'body', html: c.b })));
      const flip = () => fc.classList.toggle('flip');
      fc.onclick = flip; fc.onkeydown = e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); flip(); } };
      const grade = g => {
        const st = { ...s, ts: Date.now() };
        if (g === 0) { st.box = 0; st.due = Date.now(); queue.push(queue.shift()); }
        else if (g === 1) { st.box = Math.max(1, s.box); st.due = Date.now() + BOX_INT[st.box] / 2; queue.shift(); }
        else { st.box = Math.min(6, s.box + 1); st.due = Date.now() + BOX_INT[st.box]; queue.shift(); }
        Store.data.cards[c.id] = st; Store.touch(); next();
      };
      stage.append(h('div', { class: 'fc-wrap' }, fc), h('div', { class: 'fc-btns' },
        h('button', { type: 'button', class: 'btn warn', onclick: () => grade(0) }, 'Не помню'),
        h('button', { type: 'button', class: 'btn ghost', onclick: () => grade(1) }, 'С трудом'),
        h('button', { type: 'button', class: 'btn ok', onclick: () => grade(2) }, 'Помню')));
      if (c.ch) stage.append(h('p', { class: 'vsmall', style: 'text-align:center;margin-top:14px' }, h('a', { href: '#ch' + c.ch }, 'перечитать главу')));
      fc.focus({ preventScroll: true });
    };
    deckSel.onchange = build; modeSel.onchange = build; build();
  }
};

/* ================= пробный билет ================= */
const Exam = {
  view() {
    App.view = 'exam'; const main = $('#main'); const col = h('div', { class: 'col' }); main.append(col);
    col.append(h('div', { class: 'eyebrow' }, 'Тренажёр'), h('h1', {}, 'Пробный билет'));
    const past = Store.data.exams || [];
    col.append(h('p', {}, 'Билет собирается случайно: 1 теоретический вопрос (ответ оценит ИИ по конспекту), 3 «что выведет» и 1 задача на код с автотестами. 40 минут. Можно ограничить темы.'));
    const chs = Data.manifest.chapters;
    const fromSel = h('select', { class: 'qin', style: 'max-width:300px;flex:none', 'aria-label': 'темы до главы' }, ...chs.map(c => h('option', { value: c.n, selected: c.n === chs[chs.length - 1].n }, 'темы 1–' + c.n + ' (до «' + c.title + '»)')));
    const go = h('button', { type: 'button', class: 'btn' }, 'Тянуть билет');
    col.append(h('div', { class: 'qrow' }, fromSel, go));
    if (past.length) {
      col.append(h('h2', { style: 'font-size:20px;margin-top:30px' }, 'Прошлые попытки'));
      const tb = h('table', {}, h('tr', {}, h('th', {}, 'Когда'), h('th', {}, 'Темы'), h('th', {}, 'Баллы')));
      past.slice(-10).reverse().forEach(e => tb.append(h('tr', {}, h('td', {}, new Date(e.ts).toLocaleString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })), h('td', {}, '1–' + e.upto), h('td', {}, h('b', {}, e.score + ' / 100')))));
      col.append(h('div', { class: 'tw' }, tb));
    }
    go.onclick = () => this.start(+fromSel.value);
  },
  pick(arr, n) { const a = [...arr]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a.slice(0, n); },
  start(upto) {
    const ok = id => (Data.chapter(id)?.n ?? 99) <= upto;
    const th = this.pick(Data.theory.filter(t => ok(t.ch)), 1)[0];
    const pr = this.pick(Data.pred.filter(p => ok(p.ch) && p.type === 'out' && !p.ub), 3);
    const tk = this.pick(Data.tasks.filter(t => ok(t.ch) && t.lvl !== 'hard' && t.mode !== 'free'), 1)[0];
    const main = $('#main'); main.innerHTML = ''; const col = h('div', { class: 'col' }); main.append(col);
    const timer = h('span', { class: 'timer' }); const end = Date.now() + 40 * 60e3;
    const tick = () => { const left = Math.max(0, end - Date.now()); timer.textContent = String(Math.floor(left / 60e3)).padStart(2, '0') + ':' + String(Math.floor(left / 1e3) % 60).padStart(2, '0'); timer.classList.toggle('low', left < 5 * 60e3); if (!left) { clearInterval(this.iv); submit(); } };
    clearInterval(this.iv); this.iv = setInterval(tick, 1000); tick();
    col.append(h('div', { class: 'qrow', style: 'justify-content:space-between' }, h('h1', { style: 'margin:0' }, 'Билет'), timer));
    const res = { pred: {} };
    let thA = null;
    if (th) { col.append(h('h2', { style: 'font-size:20px' }, '1. Теория · 30 баллов'), h('div', { class: 'quiz' }, h('div', { class: 'qq', html: th.q }), thA = h('textarea', { class: 'qin', style: 'width:100%;min-height:180px;font-family:var(--f-body);margin-top:10px', placeholder: 'Ответь своими словами, как на устном. Примеры кода приветствуются.' }))); }
    col.append(h('h2', { style: 'font-size:20px' }, '2. Что выведет · 3 × 10 баллов'));
    pr.forEach(p => {
      const box = h('div', { class: 'quiz' }, h('div', { class: 'qq', html: p.q }));
      const c = h('div', { class: 'code' }); const pre = h('pre'); highlight(pre, dedent(p.code || '')); c.append(pre); box.append(c);
      const inp = String([].concat(p.ans)[0]).includes('\n') ? h('textarea', { class: 'qin', style: 'width:100%' }) : h('input', { class: 'qin', style: 'width:100%', placeholder: 'вывод (или CE / UB)' });
      box.append(inp); col.append(box); res.pred[p.id] = inp;
    });
    let ed = null;
    if (tk) {
      col.append(h('h2', { style: 'font-size:20px' }, '3. Код · 40 баллов'), h('div', { class: 'quiz' }, h('div', { class: 'qq' }, h('b', {}, tk.title)), h('div', { html: tk.text }), tk.in ? h('div', { html: '<b>Ввод:</b> ' + tk.in }) : '', tk.out ? h('div', { html: '<b>Вывод:</b> ' + tk.out }) : '', tk.mode === 'func' ? h('p', { class: 'vsmall' }, 'Свой main не нужен.') : ''));
      const host = h('div', { class: 'edwrap' }); col.append(host); ed = makeEditor(host, tk.starter || '', { height: '320px' });
    }
    const sub = h('button', { type: 'button', class: 'btn', style: 'margin-top:20px' }, 'Сдать билет');
    const report = h('div'); col.append(sub, report);
    const submit = async () => {
      if (sub.disabled) return; sub.disabled = true; clearInterval(this.iv);
      report.innerHTML = '<p class="vsmall"><span class="spin"></span> проверяю…</p>';
      let score = 0; const lines = [];
      for (const p of pr) {
        const v = res.pred[p.id].value; const ok = [].concat(p.ans).some(a => normOut(a) === normOut(v) || normAns(a) === normAns(v));
        if (ok) score += 10; lines.push(h('div', { class: 'why ' + (ok ? 'good' : 'bad'), html: `<span class="v">${p.n}: ${ok ? '+10' : '0'}</span> правильный ответ: <code>${esc([].concat(p.ans)[0])}</code>. ${p.why || ''}` }));
      }
      if (tk && ed) {
        let pass = 0, log = '';
        try {
          const full = tk.mode === 'func' ? ed.getValue() + '\n' + tk.harness : ed.getValue();
          const comp = await Runner.compile(full);
          if (comp.ok) for (const x of tk.tests) { const r = await Runner.exec(comp, x.i || ''); if (!r.timeout && !r.trap && compareOut(r.stdout, x.o, tk.check)) pass++; }
          else log = 'не скомпилировалось';
        } catch (e) { log = e.message; }
        const pts = Math.round(40 * pass / tk.tests.length); score += pts;
        lines.push(h('div', { class: 'why ' + (pts === 40 ? 'good' : 'bad'), html: `<span class="v">Код: +${pts}</span> тестов пройдено ${pass}/${tk.tests.length}. ${esc(log)} <a href="#task-${tk.id}">открыть задачу</a>` }));
      }
      if (th) {
        const g = await Tutor.gradeTheory(th, thA.value);
        score += g.score; lines.unshift(h('div', { class: 'why ' + (g.score >= 20 ? 'good' : 'bad') }, h('span', { class: 'v' }, `Теория: +${g.score}`), h('div', { html: md(g.feedback) }), h('details', {}, h('summary', {}, 'эталонный ответ по конспекту'), h('div', { html: th.key }))));
      }
      report.innerHTML = '';
      const mark = score >= 80 ? 'отл' : score >= 60 ? 'хор' : score >= 40 ? 'удовл' : 'неуд';
      report.append(h('div', { class: 'stat', style: 'margin-top:20px' }, h('div', { class: 'grade' }, score + ' / 100'), h('span', {}, `≈ «${mark}». ` + (score >= 80 ? 'На экзамен можно идти с чистой совестью.' : 'Глянь разбор ниже и перечитай главы, где посыпался.'))), ...lines);
      Store.data.exams.push({ ts: Date.now(), upto, score }); Store.touch();
    };
    sub.onclick = submit;
    Tutor.setCtx(() => 'Студент решает пробный билет. Не подсказывай ответы на билет, пока он не сдан — можно только объяснять теорию в общем виде.');
  }
};

/* ================= AI tutor ================= */
/* ================= LocalAI: Anthropic или OpenAI API через server.py (ключ живёт только на сервере) ================= */
const LocalAI = Object.assign(async function sample(input, opts = {}) {
  const msgs = typeof input === 'string' ? [{ role: 'user', content: input }] : input.map(m => ({ role: m.role, content: m.content }));
  const tools = opts.tools || [];
  const apiTools = tools.map(t => ({ name: t.name, description: t.description, input_schema: t.inputSchema || { type: 'object', properties: {} } }));
  let text = '';
  for (let round = 0; round < 6; round++) {
    if (opts.signal?.aborted) throw { code: 'cancelled', text };
    let r, j;
    try {
      r = await fetch('/api/ai', { method: 'POST', signal: opts.signal, headers: { 'Content-Type': 'application/json', 'X-PVK': '1' },
        body: JSON.stringify({ messages: msgs, tools: apiTools.length ? apiTools : undefined, max_tokens: opts.maxTokens || 4096 }) });
      j = await r.json();
    } catch (e) { throw { code: e.name === 'AbortError' ? 'cancelled' : 'network', message: e.message, text }; }
    if (!r.ok || j.error) throw { code: j?.error?.type || 'http', message: j?.error?.message || ('HTTP ' + r.status), text };
    const blocks = j.content || [];
    const t = blocks.filter(b => b.type === 'text').map(b => b.text).join('');
    if (t) { text += (text ? '\n\n' : '') + t; opts.onText && opts.onText({ text, delta: t }); }
    const calls = blocks.filter(b => b.type === 'tool_use');
    if (j.stop_reason !== 'tool_use' || !calls.length) return { text, truncated: j.stop_reason === 'max_tokens' };
    msgs.push({ role: 'assistant', content: blocks });
    const results = [];
    for (const c of calls) {
      const tool = tools.find(x => x.name === c.name);
      let out, isErr = false;
      try { out = tool ? await tool.execute(c.input || {}) : { error: 'нет такого инструмента' }; } catch (e) { out = { error: String(e.message || e) }; isErr = true; }
      results.push({ type: 'tool_result', tool_use_id: c.id, content: JSON.stringify(out).slice(0, 12000), is_error: isErr });
    }
    msgs.push({ role: 'user', content: results });
    if (opts.onText) opts.onText({ text: text + '\n\n⚙ запускаю код…', delta: '' });
  }
  return { text, truncated: true };
}, {
  async json(prompt, opts = {}) {
    const { text } = await LocalAI(prompt + '\n\nОтветь ТОЛЬКО валидным JSON, без пояснений и без ```.', opts);
    const s = text.replace(/^```(?:json)?\s*|\s*```\s*$/g, '').trim();
    try { return JSON.parse(s); } catch (e) { }
    const a = s.search(/[\[{]/), b = Math.max(s.lastIndexOf('}'), s.lastIndexOf(']'));
    if (a >= 0 && b > a) return JSON.parse(s.slice(a, b + 1));
    throw { code: 'bad_json', message: 'ИИ вернул не JSON' };
  }
});
const TUTOR_RULES = `Ты — тьютор по C++ для первокурсника ВШЭ (программа «Дизайн и разработка информационных продуктов»), который готовится к экзамену по «Великому конспекту по C++» М. Горденко. Студент — зумер, ему скучно читать сухой текст.
Правила:
- Отвечай по-русски, живо и коротко, можно с лёгким юмором и мемными сравнениями, но технически абсолютно точно (стандарт C++20/23; код студента компилируется его локальным g++/clang на 64-битной системе; если ответ зависит от платформы — sizeof(long), порядок байт, поведение при UB — упомяни это).
- Терминологию бери из конспекта: операция (operator) vs оператор (statement), lvalue/rvalue, UB, CE, области действия/видимости, классы памяти.
- Код оформляй в блоках \`\`\`cpp.
- Если студент решает задачу — не выдавай полное решение, пока он прямо не попросит. Давай наводящие подсказки.
- Если не уверен — так и скажи, не выдумывай.`;
const Tutor = {
  sample: undefined, turns: [], ctxFn: null, busy: false, ctl: null,
  async get() { if (this.sample === undefined) { try { const i = await Runner.boot(); this.sample = i.ai ? LocalAI : null; } catch (e) { this.sample = null; } } return this.sample; },
  errText(e) { return ({ no_key: 'ИИ выключен: запусти сервер с переменной ANTHROPIC_API_KEY или OPENAI_API_KEY (см. README).', rate_limit_error: 'Слишком много запросов подряд, подожди минутку.', overloaded_error: 'Модель перегружена, попробуй через минуту.', authentication_error: 'API-ключ не подошёл — проверь ANTHROPIC_API_KEY / OPENAI_API_KEY.', cancelled: 'Остановлено.' })[e?.code] || 'ИИ сейчас недоступен' + (e?.message ? ': ' + e.message : '.'); },
  setCtx(fn) { this.ctxFn = fn; const c = $('#tctx'); if (c) c.textContent = fn ? 'Контекст: ' + (App.view === 'chapter' ? 'текущая глава' : App.view === 'task' ? 'текущая задача и твой код' : App.view === 'sandbox' ? 'код в песочнице' : App.view === 'exam' ? 'билет (без подсказок)' : 'страница') : 'Контекст: общий вопрос'; },
  toggle(force) { const d = $('#drawer'); const open = force ?? !d.classList.contains('open'); d.classList.toggle('open', open); document.body.classList.toggle('tutor-open', open); if (open) $('#tin').focus(); },
  open(text) { this.toggle(true); if (text) { $('#tin').value = text; this.send(); } },
  tools() {
    return [{
      name: 'run_cpp', description: 'Скомпилировать (локальный компилятор студента, -O0) и запустить полную программу на C++. Возвращает stdout, stderr, код возврата или ошибки компиляции. Используй, чтобы проверить свои утверждения о выводе программы.',
      inputSchema: { type: 'object', properties: { code: { type: 'string', description: 'полный исходник с main' }, stdin: { type: 'string' } }, required: ['code'] },
      execute: async ({ code, stdin }) => { const r = await Runner.run(code, stdin || ''); return r.stage === 'compile' ? { compile_error: r.log.slice(0, 4000) } : { stdout: (r.stdout || '').slice(0, 4000), stderr: (r.stderr || '').slice(0, 2000), exit_code: r.code, timeout: !!r.timeout, crash: r.trap || null }; }
    }];
  },
  async ask(prompt, onText, opts = {}) {
    const s = await this.get(); if (!s) throw { code: 'no_key' };
    this.ctl = new AbortController();
    return s(prompt, { onText, signal: this.ctl.signal, tools: Runner.ok ? this.tools() : undefined, ...opts });
  },
  addMsg(role, text) { const m = h('div', { class: 'msg ' + (role === 'user' ? 'u' : 'a') }); if (role === 'user') m.textContent = text; else m.innerHTML = text; $('#msgs').append(m); $('#msgs').scrollTop = 1e9; return m; },
  async send() {
    const inp = $('#tin'); const text = inp.value.trim(); if (!text || this.busy) return;
    inp.value = ''; this.addMsg('user', text); const bubble = this.addMsg('a', '<span class="spin"></span> думаю…');
    this.turns.push({ role: 'user', content: text }); if (this.turns.length > 16) this.turns = this.turns.slice(-16);
    if (this.turns[0].role !== 'user') this.turns.shift();
    const ctx = this.ctxFn ? this.ctxFn() : '';
    const input = [{ role: 'user', content: TUTOR_RULES + (ctx ? '\n\nКонтекст страницы, которую студент сейчас открыл:\n' + ctx.slice(0, 14000) : '') }, ...this.turns];
    this.busy = true; $('#tstop').hidden = false;
    try {
      const { text: ans } = await this.ask(input, ({ text }) => { bubble.innerHTML = md(text); $('#msgs').scrollTop = 1e9; }, { cache: false });
      bubble.innerHTML = md(ans); this.turns.push({ role: 'assistant', content: ans });
    } catch (e) { bubble.innerHTML = md(e.text || '') + `<p class="vsmall">${esc(this.errText(e))}</p>`; this.turns.pop(); }
    this.busy = false; $('#tstop').hidden = true;
  },
  async inline(box, prompt, label) {
    const out = h('div', { class: 'ai-out' }, h('div', { class: 'who' }, label || 'ИИ-тьютор'), h('div', { html: '<span class="spin"></span> думаю… (первый ответ бывает до минуты)' }));
    box.append(out); const body = out.lastChild;
    try { const { text } = await this.ask(prompt, ({ text }) => body.innerHTML = md(text)); body.innerHTML = md(text); }
    catch (e) { body.innerHTML = md(e.text || '') + `<p class="vsmall">${esc(this.errText(e))}</p>`; }
    return out;
  },
  explainSection(sec, ch) {
    const old = $('.ai-out', sec); if (old) { old.remove(); return; }
    const text = sec.innerText.slice(0, 7000); const h2 = $('h2', sec);
    const holder = h('div'); h2.after(holder);
    this.inline(holder, TUTOR_RULES + `\n\nОбъясни проще раздел «${h2.textContent.replace('✦ объясни проще', '').trim()}» из главы «${ch.title}». Студенту не зашло. Сделай так: 1) суть в 2–3 предложениях человеческим языком; 2) бытовая аналогия; 3) маленький пример кода с комментариями; 4) одна типичная ловушка на экзамене. Не длиннее ~250 слов.\n\nТекст раздела:\n${text}`, 'Объясняю проще');
  },
  hint(t, code, report, box) {
    this.inline(box, TUTOR_RULES + `\n\nСтудент решает задачу и просит подсказку. НЕ пиши решение и не пиши готовый код функции целиком. Дай одну следующую наводящую подсказку (2–4 предложения), опираясь на его текущий код и результаты тестов. Если в коде конкретная ошибка — укажи, где искать, но не исправляй за него.\n\nЗадача «${t.title}»: ${h('div', { html: t.text + (t.in || '') + (t.out || '') }).textContent}\n\nКод студента:\n${code}\n\nРезультат проверки: ${report || 'ещё не проверял'}`, 'Подсказка');
  },
  review(t, code, report, box, scrollTo) {
    this.inline(box, TUTOR_RULES + `\n\nСделай код-ревью решения как строгий, но добрый семинарист. Структура: ✅ что хорошо; ⚠️ ошибки/UB/краевые случаи (укажи строки); 🧹 стиль (именование, const, ++i, лишние копии, глобальные переменные — как требует конспект); 💡 как сделать лучше (без полного переписывания). Если решение верное — так и скажи. Коротко.\n\nЗадача «${t.title}»: ${h('div', { html: t.text }).textContent}\n\nКод:\n${code}\n\nРезультат тестов: ${report || 'не запускал'}`, 'Ревью кода');
    scrollTo && box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  },
  async gradeTheory(th, answer) {
    if (!answer.trim()) return { score: 0, feedback: 'Ответа нет — 0 баллов.' };
    const s = await this.get();
    if (!s) return { score: 0, feedback: 'ИИ недоступен, оцени себя сам по эталону ниже (теория не засчитана).' };
    try {
      const r = await s.json(`Ты экзаменатор по C++ (1 курс). Оцени устный ответ студента на вопрос билета по эталону из конспекта. Будь справедлив: суть важнее формулировок, но ошибки в терминах и фактах снижают балл. Верни ТОЛЬКО JSON {"score": целое 0..30, "feedback": "2–5 предложений по-русски: что упущено/неверно, что хорошо"}.\n\nВопрос: ${h('div', { html: th.q }).textContent}\n\nЭталон: ${h('div', { html: th.key }).textContent}\n\nОтвет студента: ${answer.slice(0, 6000)}`, { modelTier: 'default' });
      return { score: Math.max(0, Math.min(30, Math.round(+r.score || 0))), feedback: String(r.feedback || '') };
    } catch (e) { return { score: 0, feedback: this.errText(e) + ' Теория не засчитана — сверь с эталоном.' }; }
  }
};

/* ================= AI-generated tasks with verified tests ================= */
const AITask = {
  list: [],
  load() { try { this.list = JSON.parse(localStorage.getItem('ai-tasks') || '[]'); } catch (e) { this.list = []; } },
  save() { try { localStorage.setItem('ai-tasks', JSON.stringify(this.list.slice(-30))); } catch (e) { } },
  get(id) { return this.list.find(t => t.id === id); },
  async generate(chId) {
    const s = await Tutor.get(); if (!s) { toast('ИИ выключен: нужен ANTHROPIC_API_KEY или OPENAI_API_KEY при запуске сервера'); return; }
    const ch = chId ? Data.chapter(chId) : null;
    const upto = ch ? Data.manifest.chapters.filter(c => c.n <= ch.n).map(c => c.title).join(', ') : Data.manifest.chapters.map(c => c.title).join(', ');
    const main = $('#main'); main.innerHTML = '';
    const col = h('div', { class: 'col' }, h('h1', {}, 'Генерирую задачу…'), h('p', { class: 'vsmall' }, 'ИИ придумывает задачу в стиле LeetCode по ' + (ch ? 'главе «' + ch.title + '»' : 'всему курсу') + ', потом эталонное решение прогоняется настоящим компилятором, и ожидаемые ответы берутся из него. Обычно 30–90 секунд.'));
    const log = h('pre', { class: 'out' }); col.append(log); main.append(col);
    try {
      const spec = await s.json(`Придумай одну НОВУЮ задачу по C++ уровня easy/medium в стиле LeetCode для первокурсника. Тема: ${ch ? '«' + ch.title + '»' : 'любая'}; можно использовать только темы: ${upto}. Не используй STL-контейнеры (vector, map и т.п.) и алгоритмы — только то, что есть в курсе (массивы, указатели, строки, функции, структуры/классы, если они в списке тем). Формат — консольный ввод/вывод (stdin/stdout).
Верни ТОЛЬКО JSON: {"title": "...", "lvl": "easy"|"medium", "text": "условие в HTML (<p>, <code>)", "in": "формат ввода (HTML)", "out": "формат вывода (HTML)", "starter": "заготовка: полная программа с main и TODO", "sol": "полное правильное решение на C++", "inputs": ["ввод теста 1", ... 6–8 тестов, включая краевые случаи]}`, { modelTier: 'default' });
      if (!spec || !spec.sol || !Array.isArray(spec.inputs)) throw new Error('ИИ вернул что-то не то');
      log.textContent = 'Задача придумана. Компилирую эталон…';
      const comp = await Runner.compile(spec.sol); if (!comp.ok) throw new Error('эталон не скомпилировался:\n' + comp.log);
      const tests = [];
      for (const i of spec.inputs.slice(0, 10)) { const r = await Runner.exec(comp, String(i)); if (!r.timeout && !r.trap && r.code === 0) tests.push({ i: String(i), o: normOut(r.stdout) }); }
      if (tests.length < 3) throw new Error('эталон упал на большинстве тестов, попробуй ещё раз');
      const t = { id: 'ai' + Date.now().toString(36), ch: chId || Data.manifest.chapters[0].id, title: spec.title, lvl: spec.lvl === 'medium' ? 'medium' : 'easy', src: 'ai', text: spec.text, in: spec.in, out: spec.out, starter: spec.starter || '', sol: spec.sol, tests, show: 2, mode: 'io' };
      this.list.push(t); this.save(); location.hash = '#task-' + t.id;
    } catch (e) { log.textContent = 'Не получилось: ' + (e.message || Tutor.errText(e)); col.append(h('button', { type: 'button', class: 'btn', onclick: () => this.generate(chId) }, 'Ещё раз')); }
  }
};
