/* Лёгкий режим C++ и runMode для CodeMirror 5 (чтобы платформа работала без CDN). */
(function () {
  if (!window.CodeMirror) return;
  const words = s => new Set(s.split(' '));
  const KW = words('alignas alignof and asm break case catch class concept const consteval constexpr constinit const_cast continue co_await co_return co_yield decltype default delete do dynamic_cast else enum explicit export extern for friend goto if inline mutable namespace new noexcept not operator or private protected public register reinterpret_cast requires return sizeof static static_assert static_cast struct switch template this thread_local throw try typedef typeid typename union using virtual volatile while xor override final');
  const TY = words('auto bool char char8_t char16_t char32_t double float int long short signed unsigned void wchar_t size_t ptrdiff_t int8_t int16_t int32_t int64_t uint8_t uint16_t uint32_t uint64_t std string string_view vector ostream istream ifstream ofstream fstream stringstream istringstream ostringstream unique_ptr shared_ptr weak_ptr nullptr_t');
  const AT = words('true false nullptr NULL');
  CodeMirror.defineMode('cpplite', () => ({
    startState: () => ({ com: false, pre: false, inc: false }),
    token(s, st) {
      if (s.sol()) { st.pre = false; st.inc = false; }
      if (st.com) { if (s.skipTo('*/')) { s.next(); s.next(); st.com = false; } else s.skipToEnd(); return 'comment'; }
      if (s.eatSpace()) return null;
      if (s.match('//')) { s.skipToEnd(); return 'comment'; }
      if (s.match('/*')) { st.com = true; return this.token(s, st) || 'comment'; }
      if (s.sol() || /^\s*$/.test(s.string.slice(0, s.start))) { const m = s.match(/^#\s*\w+/); if (m) { st.pre = true; st.inc = /include/.test(m[0]); return 'meta'; } }
      if (st.inc && s.match(/^<[^>]*>/)) return 'string';
      if (s.match(/^R"([^(]*)\(/)) { while (!s.eol()) { if (s.match(')"')) return 'string'; s.next(); } return 'string'; }
      const ch = s.peek();
      if (ch === '"' || ch === "'") { s.next(); let esc = false, c; while ((c = s.next()) != null) { if (c === ch && !esc) break; esc = !esc && c === '\\'; } return 'string'; }
      if (s.match(/^(0[xX][\da-fA-F']+|0[bB][01']+|(\d[\d']*)?\.?\d[\d']*([eE][+-]?\d+)?)[uUlLfFzZ]*/)) return 'number';
      const id = s.match(/^[A-Za-z_]\w*/);
      if (id) { const w = id[0]; if (st.pre) return 'meta'; if (KW.has(w)) return 'keyword'; if (TY.has(w)) return 'type'; if (AT.has(w)) return 'atom'; return 'variable'; }
      if (s.match(/^[+\-*/%=<>!&|^~?:]+/)) return 'operator';
      s.next(); return null;
    },
    lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/',
    electricChars: '{}', closeBrackets: '()[]{}\'\'""',
    indent(st, after, cx) { return CodeMirror.Pass; }
  }));
  CodeMirror.defineMIME('text/x-c++src', 'cpplite');
  if (!CodeMirror.runMode) CodeMirror.runMode = function (text, spec, el) {
    const mode = CodeMirror.getMode(CodeMirror.defaults, spec), st = CodeMirror.startState(mode);
    const lines = CodeMirror.splitLines(text);
    lines.forEach((line, i) => {
      if (i) el.appendChild(document.createTextNode('\n'));
      const s = new CodeMirror.StringStream(line, 4);
      if (!line && mode.blankLine) mode.blankLine(st);
      while (!s.eol()) {
        const style = mode.token(s, st), txt = s.current();
        if (style) { const sp = document.createElement('span'); sp.className = style.split(' ').map(x => 'cm-' + x).join(' '); sp.textContent = txt; el.appendChild(sp); }
        else el.appendChild(document.createTextNode(txt));
        s.start = s.pos;
      }
    });
  };
})();
