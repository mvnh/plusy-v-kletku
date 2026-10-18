/* ================= boot ================= */
(async function boot() {
  Store.load(); AITask.load();
  $('#menu').onclick = () => $('#side').classList.toggle('open');
  $('#tutor-btn').onclick = () => Tutor.toggle();
  $('#tclose').onclick = () => Tutor.toggle(false);
  $('#tstop').onclick = () => Tutor.ctl && Tutor.ctl.abort();
  $('#tclear').onclick = () => { Tutor.turns = []; $('#msgs').innerHTML = ''; Tutor.addMsg('a', '<p>Начали с чистого листа. Спрашивай.</p>'); };
  $('#tform').onsubmit = e => { e.preventDefault(); Tutor.send(); };
  $('#tin').addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); Tutor.send(); } });
  for (const b of $$('#chips button')) b.onclick = () => { $('#tin').value = b.textContent + (App.view === 'chapter' ? ' (по текущей главе)' : ''); Tutor.send(); };
  try { await Data.init(); }
  catch (e) { $('#main').innerHTML = ''; $('#main').append(h('div', { class: 'col c c-ub' }, 'Не получилось загрузить данные: ' + e.message)); return; }
  App.buildSide(); App.refreshProgress();
  window.addEventListener('hashchange', () => App.route());
  App.route();
  Runner.boot().then(i => { if (!i.ok) toast('⚠ ' + i.error); }).catch(e => toast(e.message));
  Tutor.get().then(s => { if (!s) { $('#tutor-btn').title = 'ИИ-тьютор выключен: запусти сервер с ANTHROPIC_API_KEY или OPENAI_API_KEY'; } });
  window.addEventListener('pagehide', () => Store.flush());
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') Store.flush(); });
})();
