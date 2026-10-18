/* ================= views ================= */
const LVL = { easy: 'лёгкая', medium: 'средняя', hard: 'сложная' };
const SRC = { sem: 'семинар', lect: 'из конспекта', lc: 'в стиле LeetCode', ai: 'от ИИ' };
const App = {
  view: null, ctxText: '',
  refreshProgress() {
    const m = Data.manifest; if (!m) return;
    const tot = m.chapters.length; const read = m.chapters.filter(c => Store.data.read[c.id] === 1).length;
    const solved = Object.values(Store.data.tasks).filter(t => t.solved).length;
    const pct = Math.round(100 * (read + solved * 0.3) / (tot + (Data.tasks.length || 1) * 0.3));
    $('#xpbar').style.width = pct + '%'; $('#xptext').textContent = pct + '%';
    for (const a of $$('.side a[data-ch]')) { const d = $('.dot', a); const r = Store.data.read[a.dataset.ch]; d.className = 'dot' + (r === 1 ? ' full' : r ? ' half' : ''); }
    const due = Cards.dueCount(); const b = $('#cards-badge'); b.textContent = due; b.hidden = !due;
  },
  rerenderSoft() { if (this.view === 'home') this.route(); },
  buildSide() {
    const s = $('#side'); s.innerHTML = '';
    const nav = (href, label, extra) => h('a', { href, 'data-nav': href }, label, extra || '');
    s.append(h('h4', {}, 'Тренажёр'),
      nav('#practice', h('span', {}, 'Задачи с автопроверкой')),
      nav('#seminars', h('span', {}, 'Что выведет? (семинары)')),
      nav('#cards', h('span', {}, 'Флешкарты'), h('span', { class: 'badge', id: 'cards-badge', hidden: true }, '0')),
      nav('#exam', h('span', {}, 'Пробный билет')),
      nav('#sandbox', h('span', {}, 'Песочница')));
    for (const g of Data.manifest.groups) {
      s.append(h('h4', {}, g.title));
      for (const c of Data.manifest.chapters.filter(c => c.group === g.id))
        s.append(h('a', { href: '#ch' + c.id, 'data-ch': c.id, 'data-nav': '#ch' + c.id }, h('span', { class: 'num' }, c.n), h('span', {}, c.title), h('span', { class: 'dot' })));
    }
    s.addEventListener('click', e => { if (e.target.closest('a')) s.classList.remove('open'); });
  },
  markNav(hash) { for (const a of $$('.side a')) a.classList.toggle('on', a.dataset.nav === hash || (hash.startsWith('#task-') && a.dataset.nav === '#practice')); },
  async route() {
    const hash = location.hash || '#home'; const main = $('#main'); main.innerHTML = '';
    this.markNav(hash); window.scrollTo(0, 0); Tutor.setCtx(null);
    try {
      if (hash.startsWith('#ch')) await this.chapter(hash.slice(3));
      else if (hash.startsWith('#task-')) this.task(hash.slice(6));
      else if (hash === '#practice') this.practice();
      else if (hash === '#seminars' || hash.startsWith('#sem')) this.seminars(hash.startsWith('#sem') && hash !== '#seminars' ? hash.slice(4) : null);
      else if (hash === '#cards') Cards.view();
      else if (hash === '#exam') Exam.view();
      else if (hash === '#sandbox') this.sandbox();
      else this.home();
    } catch (e) { console.error(e); main.append(h('div', { class: 'col' }, h('div', { class: 'c c-ub' }, 'Не загрузилось: ' + e.message))); }
  },

  home() {
    this.view = 'home'; const m = Data.manifest; const main = $('#main');
    const last = Store.data.last && Data.chapter(Store.data.last);
    const first = m.chapters.find(c => Store.data.read[c.id] !== 1) || m.chapters[0];
    const goto = last || first;
    const read = m.chapters.filter(c => Store.data.read[c.id] === 1).length;
    const solved = Object.values(Store.data.tasks).filter(t => t.solved).length;
    const predOk = Object.values(Store.data.pred).filter(x => x === 1).length;
    const col = h('div', { class: 'wide' });
    col.append(h('div', { class: 'hero' },
      h('div', { class: 'eyebrow' }, 'Программирование на C++ · модуль 1 · по «Великому конспекту»'),
      h('h1', { html: 'Весь конспект, только <em>не скучно</em>' }),
      h('p', {}, 'Те же 26 тем и та же строгость, но с отладчиком памяти, битами, которые можно потыкать, твоим настоящим компилятором под капотом и тьютором, который объяснит ещё раз, если не зашло.'),
      h('div', { class: 'qrow', style: 'margin-top:16px' },
        h('a', { class: 'btn', href: '#ch' + goto.id, style: 'text-decoration:none' }, (last ? 'Продолжить: ' : 'Начать: ') + goto.n + '. ' + goto.title),
        h('a', { class: 'btn ghost', href: '#exam', style: 'text-decoration:none' }, 'Проверить себя билетом'))));
    col.append(h('div', { class: 'stats' },
      h('div', { class: 'stat' }, h('b', {}, `${read}/${m.chapters.length}`), h('span', {}, 'глав прочитано')),
      h('div', { class: 'stat' }, h('b', {}, `${solved}/${Data.tasks.length}`), h('span', {}, 'задач решено')),
      h('div', { class: 'stat' }, h('b', {}, `${predOk}/${Data.pred.length}`), h('span', {}, '«что выведет» отгадано')),
      h('div', { class: 'stat' }, h('b', {}, String(Cards.dueCount())), h('span', {}, 'карточек к повторению'))));
    for (const g of m.groups) {
      col.append(h('h2', { class: 'grp-h' }, g.title));
      const map = h('div', { class: 'map' });
      for (const c of m.chapters.filter(c => c.group === g.id)) {
        const nt = Data.tasks.filter(t => t.ch === c.id), ns = nt.filter(t => Store.data.tasks[t.id]?.solved).length;
        const p = Store.data.read[c.id] === 1 ? (nt.length ? 50 + 50 * ns / nt.length : 100) : Store.data.read[c.id] ? 15 : 0;
        map.append(h('a', { class: 'mcard', href: '#ch' + c.id }, h('span', { class: 'n' }, 'Глава ' + c.n), h('span', { class: 't' }, c.title), h('span', { class: 'vsmall' }, c.blurb || ''), h('span', { class: 'p' }, h('i', { style: `width:${p}%` }))));
      }
      col.append(map);
    }
    main.append(col);
  },

  async chapter(id) {
    this.view = 'chapter'; const c = Data.chapter(id); if (!c) { location.hash = '#home'; return; }
    const main = $('#main'); main.append(h('div', { class: 'col empty' }, h('span', { class: 'spin' }), ' загружаю главу…'));
    let html;
    try { html = await Data.chapterHTML(id); }
    catch (e) { main.innerHTML = ''; main.append(h('div', { class: 'col' }, h('div', { class: 'eyebrow' }, 'Глава ' + c.n), h('h1', {}, c.title), h('div', { class: 'c c-hist', 'data-l': 'Скоро' }, 'Эта глава ещё пишется. Загляни чуть позже.'))); return; }
    main.innerHTML = '';
    Store.data.last = id; if (!Store.data.read[id]) Store.data.read[id] = 0.5; Store.touch();
    const col = h('div', { class: 'col' }); const art = h('article');
    art.innerHTML = html;
    const idx = Data.manifest.chapters.indexOf(c), prev = Data.manifest.chapters[idx - 1], next = Data.manifest.chapters[idx + 1];
    const head = h('header', { class: 'ch-head' }, h('div', { class: 'eyebrow' }, `Глава ${c.n} · ${Data.manifest.groups.find(g => g.id === c.group).title}`), h('h1', {}, c.title),
      h('div', { class: 'meta' }, h('span', {}, `≈ ${c.min || 15} мин`), h('span', {}, `стр. ${c.pages || ''} конспекта`)));
    if (c.lead) head.append(h('p', { class: 'lead', html: c.lead }));
    const toc = h('nav', { class: 'toc-mini', 'aria-label': 'Разделы главы' });
    $$('section', art).forEach((s, i) => { const t = $('h2', s); if (!t) return; s.id = s.id || 's' + i; toc.append(h('a', { href: '#ch' + id, onclick: e => { e.preventDefault(); s.scrollIntoView({ behavior: 'smooth' }); } }, t.textContent.replace(/\s+/g, ' ').trim())); });
    head.append(toc);
    col.append(head, art); main.append(col);
    hydrateQuizzes(art, id); hydrateWidgets(art); hydrateCode(art);
    // AI buttons per section
    for (const s of $$('section', art)) {
      const t = $('h2', s); if (!t) continue;
      const btn = h('button', { type: 'button', class: 'ai-mini', title: 'Попросить ИИ объяснить раздел проще' }, '✦ объясни проще');
      t.append(h('span', { class: 'sec-tools' }, btn));
      btn.onclick = () => Tutor.explainSection(s, c);
    }
    // chapter practice
    const tasks = Data.tasks.filter(t => t.ch === id), preds = Data.pred.filter(p => p.ch === id), cards = Data.cards.filter(x => x.ch === id);
    if (tasks.length || preds.length || cards.length) {
      const pr = h('div', { class: 'chapter-practice' }, h('h3', {}, 'Закрепим главу'));
      const ul = h('div', { class: 'tlist' });
      tasks.forEach(t => ul.append(taskItem(t)));
      pr.append(ul);
      const links = h('div', { class: 'qrow', style: 'margin-top:10px' });
      if (preds.length) links.append(h('a', { class: 'btn ghost sm', href: '#seminars', style: 'text-decoration:none', onclick: () => { App._predFilter = id; } }, `«Что выведет» по главе: ${preds.length}`));
      if (cards.length) links.append(h('a', { class: 'btn ghost sm', href: '#cards', style: 'text-decoration:none', onclick: () => { Cards.deck = id; } }, `Флешкарты главы: ${cards.length}`));
      pr.append(links); col.append(pr);
    }
    const doneBtn = h('button', { type: 'button', class: 'btn ' + (Store.data.read[id] === 1 ? 'ok' : '') }, Store.data.read[id] === 1 ? '✓ Глава пройдена' : 'Отметить главу пройденной');
    doneBtn.onclick = () => { Store.data.read[id] = 1; Store.touch(); doneBtn.className = 'btn ok'; doneBtn.textContent = '✓ Глава пройдена'; };
    col.append(h('div', { class: 'read-mark' }, doneBtn));
    const np = h('nav', { class: 'next-prev' });
    if (prev) np.append(h('a', { href: '#ch' + prev.id }, h('small', {}, '← назад'), prev.n + '. ' + prev.title));
    if (next) np.append(h('a', { href: '#ch' + next.id, style: 'text-align:right' }, h('small', {}, 'дальше →'), next.n + '. ' + next.title));
    col.append(np);
    const end = h('div'); col.append(end);
    new IntersectionObserver((en, ob) => { if (en.some(e => e.isIntersecting)) { if (Store.data.read[id] !== 1) { Store.data.read[id] = 1; Store.touch(); doneBtn.className = 'btn ok'; doneBtn.textContent = '✓ Глава пройдена'; } ob.disconnect(); } }).observe(end);
    Tutor.setCtx(() => `Глава ${c.n} «${c.title}» конспекта. Текст главы (сокращённо):\n` + art.innerText.slice(0, 9000));
  },

  practice() {
    this.view = 'practice'; const main = $('#main'); const col = h('div', { class: 'wide' });
    col.append(h('div', { class: 'eyebrow' }, 'Тренажёр'), h('h1', {}, 'Задачи с автопроверкой'),
      h('p', { class: 'vsmall', style: 'font-size:16px;max-width:70ch' }, 'Пишешь код — компилятор на твоём компьютере собирает его и гоняет по тестам. Задачи из семинаров, из примеров конспекта и в стиле LeetCode.'));
    const f = App._pf || (App._pf = { ch: '', lvl: '', src: '', st: '' });
    const chSel = h('select', { 'aria-label': 'глава' }, h('option', { value: '' }, 'все главы'), ...Data.manifest.chapters.map(c => h('option', { value: c.id, selected: f.ch === c.id }, c.n + '. ' + c.title)));
    const lvSel = h('select', { 'aria-label': 'сложность' }, h('option', { value: '' }, 'любая сложность'), ...Object.entries(LVL).map(([k, v]) => h('option', { value: k, selected: f.lvl === k }, v)));
    const srSel = h('select', { 'aria-label': 'источник' }, h('option', { value: '' }, 'любой источник'), ...Object.entries(SRC).filter(([k]) => k !== 'ai').map(([k, v]) => h('option', { value: k, selected: f.src === k }, v)));
    const stSel = h('select', { 'aria-label': 'статус' }, h('option', { value: '' }, 'все'), h('option', { value: 'todo', selected: f.st === 'todo' }, 'нерешённые'), h('option', { value: 'done', selected: f.st === 'done' }, 'решённые'));
    const list = h('div', { class: 'tlist' });
    const draw = () => {
      Object.assign(f, { ch: chSel.value, lvl: lvSel.value, src: srSel.value, st: stSel.value });
      list.innerHTML = '';
      const items = Data.tasks.filter(t => (!f.ch || t.ch === f.ch) && (!f.lvl || t.lvl === f.lvl) && (!f.src || t.src === f.src) && (!f.st || (f.st === 'done') === !!Store.data.tasks[t.id]?.solved));
      items.forEach(t => list.append(taskItem(t)));
      if (!items.length) list.append(h('div', { class: 'empty' }, 'Под фильтр ничего не попало.'));
    };
    [chSel, lvSel, srSel, stSel].forEach(s => s.onchange = draw);
    const gen = h('button', { type: 'button', class: 'btn ai sm' }, '✦ Сгенерировать новую задачу');
    gen.onclick = () => AITask.generate(chSel.value);
    col.append(h('div', { class: 'filters' }, chSel, lvSel, srSel, stSel, gen), list);
    main.append(col); draw();
  },

  task(id) {
    this.view = 'task'; const t = Data.task(id) || AITask.get(id); const main = $('#main');
    if (!t) { main.append(h('div', { class: 'col empty' }, 'Задача не найдена. ', h('a', { href: '#practice' }, 'К списку'))); return; }
    const st = Store.data.tasks[id] || (Store.data.tasks[id] = { solved: false, tries: 0 });
    const ch = Data.chapter(t.ch);
    const left = h('div', { class: 'panel' });
    left.append(h('a', { href: '#practice', class: 'vsmall' }, '← все задачи'),
      h('h1', {}, t.title),
      h('div', { class: 'tags' }, h('span', { class: 'tag ' + t.lvl }, LVL[t.lvl] || t.lvl), h('span', { class: 'tag sem' }, SRC[t.src] || t.src), ch ? h('a', { class: 'tag', href: '#ch' + ch.id, style: 'text-decoration:none' }, 'гл. ' + ch.n + ' ' + ch.title) : '', st.solved ? h('span', { class: 'tag done' }, '✓ решено') : ''),
      h('div', { class: 'qq', html: t.text, style: 'margin-top:12px' }));
    if (t.in) left.append(h('h3', {}, 'Ввод'), h('div', { html: t.in }));
    if (t.out) left.append(h('h3', {}, 'Вывод'), h('div', { html: t.out }));
    if (t.mode === 'func') left.append(h('div', { class: 'c c-tip', html: 'Напиши только то, что просят (функцию/класс). Свой <code>main</code> не нужен — проверяющий <code>main</code> допишется сам. Для отладки используй «Запустить», там твой код запускается вместе с проверочным <code>main</code>.' }));
    const shown = t.tests.slice(0, t.show ?? 2);
    if (shown.length) {
      left.append(h('h3', {}, 'Примеры'));
      shown.forEach((x, i) => left.append(h('div', { class: 'tw' }, h('table', {}, h('tr', {}, h('th', {}, 'Ввод #' + (i + 1)), h('th', {}, 'Вывод')), h('tr', {}, h('td', {}, h('pre', { class: 'mono', style: 'margin:0' }, x.i || '(пусто)')), h('td', {}, h('pre', { class: 'mono', style: 'margin:0' }, x.o)))))));
    }
    const aiBox = h('div');
    const hintB = h('button', { type: 'button', class: 'btn ai sm' }, '✦ Подсказка');
    const solB = h('button', { type: 'button', class: 'btn ghost sm' }, 'Показать решение');
    const solBox = h('div');
    solB.onclick = () => {
      if (!st.solved && (st.tries || 0) < 2 && !solB._sure) { solB._sure = true; solB.textContent = 'Точно? Сначала попробуй хотя бы 2 раза. Нажми ещё раз'; return; }
      solBox.innerHTML = ''; const c = h('div', { class: 'code' }); const p = h('pre'); highlight(p, t.sol); c.append(h('div', { class: 'bar' }, h('span', {}, 'эталонное решение'), h('span', { class: 'sp' }), h('button', { type: 'button', onclick: () => ed.setValue(t.sol) }, 'вставить в редактор')), p);
      solBox.append(c); if (t.solNote) solBox.append(h('div', { class: 'why', html: t.solNote }));
    };
    left.append(h('div', { class: 'qrow', style: 'margin-top:16px' }, hintB, solB), aiBox, solBox);
    if (t.hint) { const hb = h('button', { type: 'button', class: 'btn ghost sm' }, 'Подсказка из конспекта'); hb.onclick = () => { aiBox.prepend(h('div', { class: 'why', html: t.hint })); hb.remove(); }; $('.qrow', left).prepend(hb); }

    const right = h('div', { class: 'panel' });
    const draftKey = 'draft-' + id; let draft = null; try { draft = localStorage.getItem(draftKey); } catch (e) { }
    const host = h('div', { class: 'edwrap' }); right.append(host);
    const ed = makeEditor(host, draft || st.code || t.starter || '', { height: '420px', onRun: () => runB.click() });
    let dt; ed.on && ed.on('change', () => { clearTimeout(dt); dt = setTimeout(() => { try { localStorage.setItem(draftKey, ed.getValue()); } catch (e) { } }, 500); });
    const stdin = h('textarea', { class: 'qin', placeholder: 'свой ввод для «Запустить»', spellcheck: 'false', 'aria-label': 'свой ввод', style: 'width:100%' }); stdin.value = shown[0]?.i || '';
    const out = h('pre', { class: 'out', style: 'border:1px solid var(--line);border-radius:8px;background:var(--code-bg)' }, h('span', { class: 'dim' }, 'Тут появится вывод. Ctrl/⌘+Enter — запустить.'));
    const runB = h('button', { type: 'button', class: 'btn ghost' }, '▶ Запустить');
    const subB = h('button', { type: 'button', class: 'btn' }, '✓ Проверить на тестах');
    const revB = h('button', { type: 'button', class: 'btn ai' }, '✦ Ревью кода');
    const tests = h('div', { class: 'tests' });
    const full = () => t.mode === 'func' ? ed.getValue() + '\n\n// ---- проверяющий main ----\n' + t.harness : ed.getValue();
    runB.onclick = async () => {
      runB.disabled = true; out.innerHTML = '<span class="dim"><span class="spin"></span> ' + 'компилирую…' + '</span>';
      try { renderOutput(out, await Runner.run(full(), stdin.value)); } catch (e) { out.textContent = e.message; }
      runB.disabled = false;
    };
    let lastReport = '';
    subB.onclick = async () => {
      subB.disabled = true; tests.innerHTML = ''; out.innerHTML = '<span class="dim"><span class="spin"></span> ' + 'компилирую…' + '</span>';
      st.tries = (st.tries || 0) + 1; st.code = ed.getValue();
      try {
        const comp = await Runner.compile(full());
        if (!comp.ok) { renderOutput(out, { stage: 'compile', log: comp.log }); lastReport = 'Ошибка компиляции:\n' + comp.log; subB.disabled = false; Store.touch(); return; }
        out.innerHTML = ''; out.append(h('span', { class: 'dim' }, comp.log ? comp.log + '\n' : ''), h('span', { class: 'dim' }, 'Компиляция ок. Гоняю тесты…'));
        let pass = 0; const rep = [];
        for (let i = 0; i < t.tests.length; i++) {
          const x = t.tests[i]; const r = await Runner.exec(comp, x.i || '');
          const ok = !r.timeout && !r.trap && compareOut(r.stdout, x.o, t.check);
          if (ok) pass++;
          const hidden = i >= (t.show ?? 2);
          const d = h('details', { class: 'test ' + (ok ? 'pass' : 'fail') }, h('summary', {}, `${ok ? '✓' : '✗'} тест ${i + 1}${hidden ? ' (скрытый)' : ''}${r.timeout ? ' — TL' : r.trap ? ' — RE' : ''}`));
          if (!ok || !hidden) d.append(h('pre', {}, `ввод:\n${x.i || '(пусто)'}\nожидалось:\n${x.o}\nполучено:\n${r.stdout}${r.stderr ? '\nstderr:\n' + r.stderr : ''}${r.trap ? '\nпадение: ' + r.trap : ''}`));
          tests.append(d);
          if (!ok) rep.push(`тест ${i + 1}: ввод «${x.i}», ожидалось «${x.o}», получено «${r.stdout}»${r.timeout ? ' (превышено время)' : ''}${r.trap ? ' (падение ' + r.trap + ')' : ''}`);
          if (!ok && !t.allTests) break;
        }
        const all = pass === t.tests.length;
        out.innerHTML = ''; out.append(h('span', { class: all ? 'ok' : 'err' }, all ? `Все ${pass} тестов пройдены. Красава 🎉` : `Пройдено ${pass} из ${t.tests.length}. Первый упавший тест развернут ниже.`));
        lastReport = all ? 'Все тесты пройдены.' : rep.join('\n');
        if (all && !st.solved) { st.solved = true; toast('Задача решена! +1 в копилку'); }
        Store.touch();
      } catch (e) { out.textContent = e.message; }
      subB.disabled = false;
    };
    hintB.onclick = () => Tutor.hint(t, ed.getValue(), lastReport, aiBox);
    revB.onclick = () => Tutor.review(t, ed.getValue(), lastReport, aiBox, left);
    right.append(h('div', { class: 'ed-tools' }, runB, subB, revB, h('span', { class: 'compiler-state', id: 'cstate' }, Runner.status())),
      h('details', {}, h('summary', { class: 'vsmall', style: 'cursor:pointer' }, 'свой ввод для «Запустить»'), stdin), out, tests);
    main.append(h('div', { class: 'wide' }, h('div', { class: 'pgrid' }, left, right)));
    Tutor.setCtx(() => `Задача «${t.title}».\nУсловие: ${h('div', { html: t.text + (t.in || '') + (t.out || '') }).textContent}\n\nТекущий код студента:\n${ed.getValue()}\n\nПоследний результат проверки: ${lastReport || 'ещё не проверял'}`);
  },

  seminars(sem) {
    this.view = 'seminars'; const main = $('#main'); const col = h('div', { class: 'col' });
    col.append(h('div', { class: 'eyebrow' }, 'Тренажёр'), h('h1', {}, 'Что выведет?'),
      h('p', { class: 'vsmall', style: 'font-size:16px' }, 'Вопросы из семинаров: угадай вывод, найди UB, объясни. Любой код можно реально запустить и сравнить со своей догадкой.'));
    const sems = [...new Set(Data.pred.map(p => p.sem))].sort((a, b) => a - b);
    const chFilter = App._predFilter; App._predFilter = null;
    let cur = sem ? +sem : chFilter ? null : sems[0];
    const tabs = h('div', { class: 'filters' });
    const list = h('div');
    const draw = () => {
      tabs.innerHTML = '';
      for (const s of sems) {
        const items = Data.pred.filter(p => p.sem === s); const ok = items.filter(p => Store.data.pred[p.id] === 1).length;
        const b = h('button', { type: 'button', class: 'btn sm ' + (s === cur ? '' : 'ghost') }, `Семинар ${s} · ${ok}/${items.length}`);
        b.onclick = () => { cur = s; draw(); }; tabs.append(b);
      }
      list.innerHTML = '';
      const items = Data.pred.filter(p => cur ? p.sem === cur : p.ch === chFilter);
      const title = cur ? (Data.manifest.seminars || {})[cur] : 'Вопросы по главе ' + (Data.chapter(chFilter)?.n || '');
      if (title) list.append(h('h2', { style: 'font-size:20px;margin:18px 0 0' }, title));
      for (const p of items) list.append(predCard(p));
    };
    col.append(tabs, list); main.append(col); draw();
  },

  sandbox(code, stdin) {
    this.view = 'sandbox'; const main = $('#main'); const col = h('div', { class: 'wide' });
    let saved = null; try { saved = localStorage.getItem('sandbox'); } catch (e) { }
    const init = code || App._sb?.code || saved || '#include <iostream>\n\nint main() {\n    std::cout << "Hello, world!\\n";\n    return 0;\n}\n';
    const sin = stdin ?? App._sb?.stdin ?? ''; App._sb = null;
    col.append(h('div', { class: 'eyebrow' }, 'Песочница'), h('h1', { style: 'margin:4px 0 12px' }, 'Пиши что хочешь'));
    const host = h('div', { class: 'edwrap' });
    const ta = h('textarea', { class: 'qin', placeholder: 'stdin', spellcheck: 'false', 'aria-label': 'ввод программы', style: 'width:100%;min-height:90px' }); ta.value = sin;
    const out = h('pre', { class: 'out', style: 'border:1px solid var(--line);border-radius:8px;background:var(--code-bg);min-height:120px' }, h('span', { class: 'dim' }, 'Ctrl/⌘+Enter — запустить'));
    const run = h('button', { type: 'button', class: 'btn' }, '▶ Запустить');
    const flags = h('select', { class: 'qin', style: 'max-width:180px;flex:none', 'aria-label': 'оптимизация' }, h('option', { value: '-O0' }, '-O0 (как в отладке)'), h('option', { value: '-O2' }, '-O2 (как в релизе)'), h('option', { value: '-O0 san' }, '-O0 + санитайзеры (ловят UB)'));
    const grid = h('div', { class: 'pgrid' }, h('div', { class: 'panel' }, host), h('div', { class: 'panel' }, h('div', { class: 'ed-tools' }, run, flags, h('span', { class: 'compiler-state' }, Runner.status())), h('div', { class: 'vsmall' }, 'Ввод (stdin)'), ta, h('div', { class: 'vsmall', style: 'margin-top:8px' }, 'Вывод'), out));
    col.append(grid); main.append(col);
    const ed = makeEditor(host, init, { height: '62vh', onRun: () => run.click() });
    ed.on && ed.on('change', () => { try { localStorage.setItem('sandbox', ed.getValue()); } catch (e) { } });
    run.onclick = async () => { run.disabled = true; out.innerHTML = '<span class="dim"><span class="spin"></span> ' + 'компилирую…' + '</span>'; try { renderOutput(out, await Runner.run(ed.getValue(), ta.value, { opt: flags.value })); } catch (e) { out.textContent = e.message; } run.disabled = false; };
    Tutor.setCtx(() => 'Студент экспериментирует в песочнице. Его код:\n' + ed.getValue() + '\nПоследний вывод:\n' + out.textContent.slice(0, 3000));
  },
  openSandbox(code, stdin) { App._sb = { code, stdin }; if (location.hash === '#sandbox') this.route(); else location.hash = '#sandbox'; }
};

function compareOut(got, exp, mode) {
  if (mode === 'tokens' || mode === 'float') {
    const a = String(got).trim().split(/\s+/).filter(Boolean), b = String(exp).trim().split(/\s+/).filter(Boolean);
    if (a.length !== b.length) return false;
    return a.every((x, i) => mode === 'float' && !isNaN(+x) && !isNaN(+b[i]) ? Math.abs(+x - +b[i]) <= 1e-6 * Math.max(1, Math.abs(+b[i])) : x === b[i]);
  }
  return normOut(got) === normOut(exp);
}
function taskItem(t) {
  const s = Store.data.tasks[t.id];
  return h('a', { class: 'titem', href: '#task-' + t.id },
    h('span', { class: 'chk' + (s?.solved ? ' on' : '') }, s?.solved ? '✓' : ''),
    h('span', { style: 'flex:1;min-width:0' }, h('div', { class: 'tt' }, t.title), h('div', { class: 'ts' }, `гл. ${Data.chapter(t.ch)?.n ?? '?'} · ${SRC[t.src] || ''}`)),
    h('span', { class: 'tag ' + t.lvl }, LVL[t.lvl] || ''));
}
function predCard(p) {
  const wrap = h('div', { id: 'p-' + p.id });
  const q = buildQuiz({ ...p, q: `<b class="mono" style="color:var(--pen)">${p.n}</b> ${p.q}` }, 'pred-' + p.id, { noStore: true, label: p.type === 'out' ? 'Что выведет?' : 'Вопрос', onAnswer: ok => { if (ok || Store.data.pred[p.id] !== 1) Store.data.pred[p.id] = ok ? 1 : 0; Store.touch(); } });
  if (Store.data.pred[p.id] === 1) $('.st', q).textContent = '✓ решено';
  if (p.code && p.run !== false) {
    const full = p.wrap === 'inc' ? WRAP_HEAD + dedent(p.code) : p.wrap ? wrapMain(dedent(p.code)) : dedent(p.code);
    const out = h('pre', { class: 'out', hidden: true, style: 'border:1px dashed var(--line);border-radius:8px;margin-top:8px' });
    const b = h('button', { type: 'button', class: 'btn ghost sm' }, '▶ запустить по-настоящему');
    b.onclick = async () => { out.hidden = false; b.disabled = true; out.innerHTML = '<span class="dim"><span class="spin"></span> компилирую…</span>'; try { const r = await Runner.run(full, p.stdin || ''); renderOutput(out, r); if (p.ub) out.append(h('span', { class: 'err' }, '\n⚠ Тут UB: этот вывод — лишь один из возможных, на другом компиляторе/флагах будет иначе.')); } catch (e) { out.textContent = e.message; } b.disabled = false; };
    const tb = h('button', { type: 'button', class: 'btn ai sm' }, '✦ разобрать с ИИ');
    tb.onclick = () => Tutor.open(`Разбери, пожалуйста, вопрос с семинара ${p.n}: ${h('div', { html: p.q }).textContent}\n\nКод:\n${dedent(p.code || '')}\n\nОбъясни пошагово, что происходит и почему.`);
    q.append(h('div', { class: 'qrow', style: 'margin-top:8px' }, b, tb), out);
  }
  wrap.append(q); return wrap;
}
