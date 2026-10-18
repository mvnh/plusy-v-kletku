/* ================= code blocks, quizzes ================= */
const WRAP_HEAD = `#include <iostream>
#include <stdexcept>
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
`;
function wrapMain(code) {
  const inc = [], body = [];
  for (const l of code.split('\n')) (/^\s*#/.test(l) ? inc : body).push(l);
  return WRAP_HEAD + inc.join('\n') + '\nint main() {\n' + body.map(l => '    ' + l).join('\n') + '\n    return 0;\n}\n';
}
function highlight(el, code) {
  el.classList.add('cm-s-k');
  if (window.CodeMirror && CodeMirror.runMode) { el.textContent = ''; CodeMirror.runMode(code, 'text/x-c++src', el); }
  else el.textContent = code;
}
function dedent(s) {
  s = s.replace(/^\n+/, '').replace(/\s+$/, '');
  const ind = Math.min(...s.split('\n').filter(l => l.trim()).map(l => l.match(/^ */)[0].length));
  return s.split('\n').map(l => l.slice(ind)).join('\n');
}
function makeEditor(host, code, opts = {}) {
  if (!window.CodeMirror) { const ta = h('textarea', { class: 'qin', style: 'width:100%;min-height:220px' }); ta.value = code; host.append(ta); return { getValue: () => ta.value, setValue: v => ta.value = v, refresh() { }, on() { }, focus() { ta.focus() } }; }
  const cm = CodeMirror(host, {
    value: code, mode: 'text/x-c++src', theme: 'k', lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
    matchBrackets: true, autoCloseBrackets: true, viewportMargin: Infinity, lineWrapping: false,
    extraKeys: { Tab: c => c.somethingSelected() ? c.indentSelection('add') : c.replaceSelection('    ', 'end'), 'Ctrl-Enter': () => opts.onRun && opts.onRun(), 'Cmd-Enter': () => opts.onRun && opts.onRun() }
  });
  cm.getWrapperElement().classList.add('cm-s-k');
  cm.setSize(null, opts.height || 'auto');
  setTimeout(() => cm.refresh(), 30);
  return cm;
}
function renderOutput(pre, res, expected) {
  pre.innerHTML = '';
  if (res.stage === 'compile') { pre.append(h('span', { class: 'err' }, 'Ошибка компиляции (CE):\n'), h('span', {}, res.log || '')); return; }
  if (res.error) { pre.append(h('span', { class: 'err' }, res.error)); return; }
  if (res.log && res.log.trim()) pre.append(h('span', { class: 'dim' }, res.log.trim() + '\n'));
  pre.append(h('span', {}, res.stdout || ''));
  if (res.stderr) pre.append(h('span', { class: 'err' }, (res.stdout && !res.stdout.endsWith('\n') ? '\n' : '') + res.stderr));
  const tail = res.timeout ? '\n⏱ Превышено время (бесконечный цикл?)' : res.trap ? `\n💥 Программа упала: ${res.trap}` : `\n— код возврата ${res.code}, ${res.ms} мс`;
  pre.append(h('span', { class: res.timeout || res.trap || res.code ? 'err' : 'dim' }, tail));
}
function hydrateCode(root) {
  for (const pre of $$('pre.cpp, script[type="text/x-cpp"]', root)) {
    const code = dedent(pre.textContent);
    const runAttr = pre.getAttribute('data-run');
    const runnable = runAttr != null;
    const box = h('div', { class: 'code' + (pre.hasAttribute('data-ce') ? ' ce' : '') });
    const bar = h('div', { class: 'bar' },
      h('span', { class: 'tag' }, pre.dataset.title || (pre.hasAttribute('data-ce') ? 'не скомпилируется' : pre.hasAttribute('data-ub') ? 'UB внутри' : 'C++')),
      h('span', { class: 'sp' }));
    const out = h('pre'); highlight(out, code);
    const copy = h('button', { type: 'button', title: 'Скопировать', onclick: async () => { try { await navigator.clipboard.writeText(code); toast('Скопировано'); } catch (e) { toast('Не вышло скопировать — выдели вручную'); } } }, 'копия');
    bar.append(copy);
    if (runnable) {
      const full = runAttr === 'wrap' ? wrapMain(code) : code;
      bar.append(h('button', { type: 'button', title: 'Открыть в песочнице', onclick: () => App.openSandbox(full, pre.dataset.stdin || '') }, 'в песочницу'));
      const runBtn = h('button', { type: 'button', class: 'run' }, '▶ запустить');
      runBtn.onclick = () => openInline(box, out, full, pre.dataset.stdin || '', runBtn, runAttr === 'wrap' ? code : null);
      bar.append(runBtn);
    }
    box.append(bar, out);
    pre.replaceWith(box);
  }
}
function openInline(box, staticPre, full, stdin, btn, shownBody) {
  if (box._open) { box._run(); return; }
  box._open = true;
  const host = h('div'); staticPre.replaceWith(host);
  const ed = makeEditor(host, full, { onRun: () => box._run() });
  const ta = h('textarea', { placeholder: 'stdin (ввод программы)', spellcheck: 'false', 'aria-label': 'Ввод программы' }); ta.value = stdin;
  const res = h('pre', { class: 'out' }, h('span', { class: 'dim' }, 'Ctrl/⌘+Enter — запустить'));
  box.append(h('div', { class: 'inline-run' }, h('div', { class: 'io' }, ta, res)));
  box._run = async () => {
    btn.disabled = true; res.innerHTML = '<span class="dim"><span class="spin"></span> ' + 'компилирую…' + '</span>';
    try { renderOutput(res, await Runner.run(ed.getValue(), ta.value)); } catch (e) { res.textContent = String(e.message || e); }
    btn.disabled = false;
  };
  box._run();
}

/* ---------- quizzes ---------- */
function normAns(s) { return String(s).trim().replace(/\s+/g, ' ').toLowerCase().replace(/[«»"]/g, ''); }
function buildQuiz(spec, qid, opts = {}) {
  const done = Store.data.quiz[qid];
  const box = h('div', { class: 'quiz' });
  const st = h('span', { class: 'st' }, done === 1 ? '✓ решено' : '');
  box.append(h('div', { class: 'qh' }, h('span', {}, opts.label || (spec.type === 'out' ? 'Что выведет?' : 'Проверь себя')), st));
  box.append(h('div', { class: 'qq', html: spec.q }));
  if (spec.code) { const c = h('div', { class: 'code' }); const p = h('pre'); highlight(p, dedent(spec.code)); c.append(p); box.append(c); }
  const why = h('div', { class: 'why', hidden: true });
  const verdict = ok => {
    why.hidden = false; why.className = 'why ' + (ok ? 'good' : 'bad');
    why.innerHTML = `<span class="v">${ok ? (spec.ok || 'В точку.') : (spec.no || 'Мимо.')}</span>` + (spec.why || '');
    if (!opts.noStore) { if (ok || Store.data.quiz[qid] !== 1) Store.data.quiz[qid] = ok ? 1 : 0; Store.touch(); }
    st.textContent = ok ? '✓ решено' : '✗ попробуй ещё';
    opts.onAnswer && opts.onAnswer(ok);
  };
  if (spec.type === 'open') {
    const ta = h('textarea', { class: 'qin', style: 'width:100%;font-family:var(--f-body)', placeholder: 'Ответь своими словами, потом сверься с эталоном' });
    const self = h('div', { class: 'qrow', hidden: true },
      h('span', { class: 'vsmall' }, 'Сам оцени:'),
      h('button', { type: 'button', class: 'btn ok sm', onclick: () => verdict(true) }, 'Ответил верно'),
      h('button', { type: 'button', class: 'btn warn sm', onclick: () => verdict(false) }, 'Не совсем'));
    const reveal = h('button', { type: 'button', class: 'btn sm' }, 'Сверить с эталоном');
    const aiB = h('button', { type: 'button', class: 'btn ai sm' }, '✦ Проверить с ИИ');
    const model = h('div', { class: 'why', hidden: true, html: '<span class="v">Эталон:</span>' + (spec.why || '') });
    reveal.onclick = () => { model.hidden = false; self.hidden = false; };
    aiB.onclick = async () => {
      if (!ta.value.trim()) { toast('Сначала напиши ответ'); return; }
      aiB.disabled = true;
      const out = await Tutor.inline(box, TUTOR_RULES + `\n\nПроверь ответ студента на вопрос как экзаменатор: что верно, что упущено, есть ли ошибки. 3–6 предложений, в конце вердикт «зачтено» или «не зачтено».\n\nВопрос: ${h('div', { html: spec.q }).textContent}\n${spec.code ? 'Код:\n' + spec.code + '\n' : ''}Эталон: ${h('div', { html: spec.why }).textContent}\n\nОтвет студента: ${ta.value}`, 'Проверка ответа');
      aiB.disabled = false; self.hidden = false;
    };
    box.append(ta, h('div', { class: 'qrow', style: 'margin-top:8px' }, reveal, aiB), self, model);
    return box;
  }
  if (spec.type === 'single' || spec.type === 'multi') {
    const wrap = h('div', { class: 'opts' }); const sel = new Set();
    spec.opts.forEach((o, i) => {
      const b = h('button', { type: 'button', class: 'opt', html: `<span class="k">${String.fromCharCode(65 + i)}</span><span>${o}</span>` });
      b.onclick = () => {
        if (spec.type === 'single') { $$('.opt', wrap).forEach(x => x.classList.remove('sel', 'right', 'wrong')); sel.clear(); sel.add(i); b.classList.add('sel'); check(); }
        else { sel.has(i) ? sel.delete(i) : sel.add(i); b.classList.toggle('sel'); $$('.opt', wrap).forEach(x => x.classList.remove('right', 'wrong')); why.hidden = true; }
      };
      wrap.append(b);
    });
    const check = () => {
      const ans = new Set([].concat(spec.ans)); const btns = $$('.opt', wrap);
      const ok = ans.size === sel.size && [...sel].every(i => ans.has(i));
      btns.forEach((b, i) => { if (sel.has(i)) b.classList.add(ans.has(i) ? 'right' : 'wrong'); else if (ok === false && spec.type === 'single' && false) b.classList.add('right'); });
      verdict(ok);
    };
    box.append(wrap);
    if (spec.type === 'multi') box.append(h('div', { class: 'qrow' }, h('button', { type: 'button', class: 'btn sm', onclick: check }, 'Проверить'), h('span', { class: 'vsmall' }, 'можно выбрать несколько')));
  } else {
    const multi = spec.type === 'out' && String([].concat(spec.ans)[0]).includes('\n');
    const inp = multi ? h('textarea', { class: 'qin', spellcheck: 'false', placeholder: 'вывод программы, построчно' }) : h('input', { class: 'qin', spellcheck: 'false', placeholder: spec.ph || (spec.type === 'out' ? 'вывод программы (или CE / UB)' : 'ответ') });
    const check = () => {
      const v = spec.type === 'out' ? normOut(inp.value) : normAns(inp.value);
      const ok = [].concat(spec.ans).some(a => spec.type === 'out' ? normOut(a) === v || normAns(a) === normAns(inp.value) : normAns(a) === v);
      verdict(ok);
    };
    if (!multi) inp.addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
    const show = h('button', { type: 'button', class: 'btn ghost sm', onclick: () => { why.hidden = false; why.className = 'why'; why.innerHTML = `<span class="v">Ответ:</span><code>${esc([].concat(spec.ans)[0])}</code> ` + (spec.why || ''); } }, 'Показать ответ');
    box.append(h('div', { class: 'qrow' }, inp, h('button', { type: 'button', class: 'btn sm', onclick: check }, 'Проверить'), show));
  }
  box.append(why);
  return box;
}
function qzSpec(el) { // <div class="qz" data-type="single|multi|text|out" data-ans="1"> .q, script x-cpp, ol>li, .why, pre.ans
  const t = el.dataset.type || 'single';
  const spec = { type: t, q: $('.q', el)?.innerHTML || '', why: $('.why', el)?.innerHTML || '' };
  const code = $('script[type="text/x-cpp"]', el); if (code) spec.code = code.textContent;
  if (t === 'single' || t === 'multi') { spec.opts = $$('ol > li', el).map(li => li.innerHTML); const a = el.dataset.ans.split(',').map(Number); spec.ans = t === 'single' ? a[0] : a; }
  else { const pa = $$('pre.ans', el).map(p => p.textContent.replace(/^\n/, '')); spec.ans = pa.length ? pa : el.dataset.ans.split('|'); }
  if (el.dataset.ph) spec.ph = el.dataset.ph;
  return spec;
}
function hydrateQuizzes(root, chId) {
  $$('script[type="text/x-quiz"], div.qz', root).forEach((s, i) => {
    let spec; try { spec = s.tagName === 'DIV' ? qzSpec(s) : JSON.parse(s.textContent); } catch (e) { s.replaceWith(h('div', { class: 'c c-ub' }, 'Битый квиз: ' + e.message)); return; }
    s.replaceWith(buildQuiz(spec, chId + '-q' + i));
  });
}
