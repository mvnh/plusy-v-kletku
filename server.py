#!/usr/bin/env python3
"""«Плюсы в клетку» — локальный сервер платформы.

Запуск:  python3 server.py            (откроет браузер на http://127.0.0.1:8737)
Опции:   --port 8737  --cxx g++-14  --no-browser
ИИ-тьютор (по желанию): задай переменную окружения ANTHROPIC_API_KEY
         (и, если хочешь, ANTHROPIC_MODEL, по умолчанию claude-sonnet-5-5)
         или OPENAI_API_KEY (OPENAI_MODEL, по умолчанию gpt-4.1; OPENAI_BASE_URL — другой
         OpenAI-совместимый сервер). Если заданы оба ключа, выбери AI_PROVIDER=openai|anthropic.

Только стандартная библиотека Python 3.8+. Нужен компилятор C++: g++ или clang++.
Сервер слушает только 127.0.0.1: код, который ты запускаешь, выполняется на твоём
компьютере с твоими правами — не открывай порт наружу.
"""
import argparse, hashlib, http.server, json, os, platform, shutil, signal, socketserver
import subprocess, sys, tempfile, threading, time, urllib.error, urllib.parse, urllib.request, webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(tempfile.gettempdir(), 'pvk-cpp')
IS_WIN = os.name == 'nt'
EXE = '.exe' if IS_WIN else ''
OUT_CAP = 200_000
SIGNALS = {
    'SIGSEGV': 'SIGSEGV — обращение к памяти, которая тебе не принадлежит (nullptr, выход за границы, висячий указатель)',
    'SIGBUS': 'SIGBUS — некорректное обращение к памяти',
    'SIGABRT': 'SIGABRT — программа аварийно завершена (abort, assert, исключение не поймано, санитайзер нашёл ошибку)',
    'SIGFPE': 'SIGFPE — арифметическая ошибка (целочисленное деление на ноль?)',
    'SIGILL': 'SIGILL — недопустимая инструкция (часто так компилятор оформляет UB)',
    'SIGTRAP': 'SIGTRAP — ловушка (часто UB, например функция без return)',
    'SIGKILL': 'SIGKILL — процесс убит',
}
WIN_CODES = {0xC0000005: 'ACCESS_VIOLATION — обращение к чужой памяти', 0xC0000094: 'деление на ноль',
             0xC00000FD: 'STACK_OVERFLOW — переполнение стека (бесконечная рекурсия?)', 0xC0000409: 'аварийное завершение (abort / проверка буфера)'}


class Compiler:
    def __init__(self, cxx=None):
        self.cxx = cxx or os.environ.get('CXX') or next((c for c in ('g++', 'clang++', 'c++') if shutil.which(c)), None)
        self.std, self.version, self.error = None, '', None
        if not self.cxx or not shutil.which(self.cxx):
            self.error = 'Не нашёл компилятор C++ (g++/clang++). ' + (
                'На macOS выполни в терминале: xcode-select --install' if sys.platform == 'darwin' else
                'Установи g++ (Linux: sudo apt install g++; Windows: MSYS2/MinGW и добавь в PATH).')
            return
        try:
            v = subprocess.run([self.cxx, '--version'], capture_output=True, text=True, timeout=20)
            self.version = (v.stdout or v.stderr).strip().splitlines()[0]
        except Exception as e:
            self.error = f'{self.cxx} не запускается: {e}'
            return
        os.makedirs(WORK, exist_ok=True)
        probe = os.path.join(WORK, 'probe.cpp')
        with open(probe, 'w') as f:
            f.write('#include <iostream>\nint main(){}\n')
        for std in ('c++23', 'c++2b', 'c++20', 'c++17'):
            r = subprocess.run([self.cxx, f'-std={std}', '-fsyntax-only', probe], capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                self.std = std
                break
        if not self.std:
            self.error = f'{self.cxx} не компилирует даже пустую программу: {r.stderr[:500]}'
        self.san = None  # lazily probed

    def sanitizers_ok(self):
        if self.san is None:
            src = os.path.join(WORK, 'probe_san.cpp')
            with open(src, 'w') as f:
                f.write('int main(){}\n')
            out = os.path.join(WORK, 'probe_san' + EXE)
            r = subprocess.run([self.cxx, '-fsanitize=address,undefined', src, '-o', out], capture_output=True, text=True, timeout=120)
            self.san = r.returncode == 0
        return self.san

    def compile(self, src, opt):
        if self.error:
            return {'ok': False, 'log': self.error}
        flags = ['-O2'] if '-O2' in opt else ['-O0']
        san = 'san' in opt
        if san:
            if not self.sanitizers_ok():
                return {'ok': False, 'log': 'Санитайзеры (-fsanitize=address,undefined) не поддерживаются этим компилятором/системой. Выбери обычный режим.'}
            flags += ['-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-fno-sanitize-recover=undefined']
        key = hashlib.sha256((self.cxx + self.std + ' '.join(flags) + '\0' + src).encode()).hexdigest()[:20]
        d = os.path.join(WORK, key)
        exe = os.path.join(d, 'main' + EXE)
        logf = os.path.join(d, 'log.txt')
        if os.path.exists(exe) and os.path.exists(logf):
            return {'ok': True, 'log': open(logf, encoding='utf-8', errors='replace').read(), 'id': key}
        os.makedirs(d, exist_ok=True)
        cpp = os.path.join(d, 'main.cpp')
        with open(cpp, 'w', encoding='utf-8') as f:
            f.write(src)
        cmd = [self.cxx, f'-std={self.std}', *flags, '-Wall', '-Wextra', '-fdiagnostics-color=never', 'main.cpp', '-o', 'main' + EXE]
        try:
            r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
        except subprocess.TimeoutExpired:
            return {'ok': False, 'log': 'Компиляция заняла больше 60 секунд — что-то пошло не так.'}
        log = (r.stderr + r.stdout).strip()
        if r.returncode != 0:
            return {'ok': False, 'log': log or 'Ошибка компиляции.'}
        with open(logf, 'w', encoding='utf-8') as f:
            f.write(log)
        return {'ok': True, 'log': log, 'id': key}


def run_binary(key, stdin, timeout):
    d = os.path.join(WORK, key)
    exe = os.path.join(d, 'main' + EXE)
    if not key.isalnum() or not os.path.exists(exe):
        return {'stdout': '', 'stderr': '', 'code': None, 'trap': 'бинарник не найден, перезапусти'}
    cwd = tempfile.mkdtemp(prefix='run-', dir=WORK)  # свежая папка: файлы программы не мешают друг другу
    env = dict(os.environ, ASAN_OPTIONS='detect_leaks=1:abort_on_error=0', UBSAN_OPTIONS='print_stacktrace=1')
    if sys.platform == 'darwin':
        env['ASAN_OPTIONS'] = 'detect_leaks=0'  # LeakSanitizer на macOS (arm64) не поддерживается
    kw = {'start_new_session': True} if not IS_WIN else {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP}
    t0 = time.time()
    p = subprocess.Popen([exe], cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, **kw)
    bufs = {'out': bytearray(), 'err': bytearray()}
    over = threading.Event()

    def kill():
        try:
            if IS_WIN:
                p.kill()
            else:
                os.killpg(p.pid, signal.SIGKILL)
        except Exception:
            pass

    def pump(stream, name):
        while True:
            chunk = stream.read1(65536) if hasattr(stream, 'read1') else stream.read(65536)
            if not chunk:
                break
            b = bufs[name]
            if len(bufs['out']) + len(bufs['err']) < OUT_CAP:
                b += chunk
            else:
                over.set()
                kill()
                break

    def feed():
        try:
            p.stdin.write(stdin.encode('utf-8'))
            p.stdin.close()
        except Exception:
            pass

    ts = [threading.Thread(target=pump, args=(p.stdout, 'out'), daemon=True),
          threading.Thread(target=pump, args=(p.stderr, 'err'), daemon=True),
          threading.Thread(target=feed, daemon=True)]
    for t in ts:
        t.start()
    timed_out = False
    try:
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill()
        p.wait()
    for t in ts[:2]:
        t.join(1)
    ms = int((time.time() - t0) * 1000)
    shutil.rmtree(cwd, ignore_errors=True)
    out = bufs['out'][:OUT_CAP].decode('utf-8', 'replace')
    err = bufs['err'][:OUT_CAP].decode('utf-8', 'replace').replace(d + os.sep, '')
    res = {'stdout': out, 'stderr': err, 'code': p.returncode, 'ms': ms}
    if over.is_set():
        res['stderr'] += '\n[вывод обрезан: больше 200 000 символов]'
        res['code'] = 0
        return res
    if timed_out:
        res.update(timeout=True, code=None)
        return res
    rc = p.returncode
    if rc is not None and rc < 0 and not IS_WIN:
        try:
            name = signal.Signals(-rc).name
        except Exception:
            name = f'сигнал {-rc}'
        res['trap'] = SIGNALS.get(name, name)
        res['code'] = None
    elif IS_WIN and rc is not None and (rc & 0xFFFFFFFF) in WIN_CODES:
        res['trap'] = WIN_CODES[rc & 0xFFFFFFFF]
        res['code'] = None
    return res


# Провайдеры ИИ: (переменная с ключом, переменная с моделью, модель по умолчанию).
# Страница говорит с сервером на формате Anthropic Messages; для OpenAI сервер переводит туда и обратно.
AI_ENV = {'anthropic': ('ANTHROPIC_API_KEY', 'ANTHROPIC_MODEL', 'claude-sonnet-5-5'),
          'openai': ('OPENAI_API_KEY', 'OPENAI_MODEL', 'gpt-4.1')}
OPENAI_STOP = {'length': 'max_tokens'}


def ai_provider():
    """AI_PROVIDER=anthropic|openai выбирает явно; иначе берётся тот, для которого задан ключ (Anthropic в приоритете)."""
    want = os.environ.get('AI_PROVIDER', '').strip().lower()
    for name in ([want] if want in AI_ENV else AI_ENV):
        if os.environ.get(AI_ENV[name][0]):
            return name
    return None


def ai_model(provider):
    _, var, default = AI_ENV[provider]
    return os.environ.get(var) or default


def _text(c):
    """Текст из строки или списка блоков Anthropic (нетекстовые блоки пропускаются)."""
    if isinstance(c, str):
        return c
    return '\n\n'.join(b.get('text', '') for b in c or [] if b.get('type') == 'text')


def openai_messages(system, messages):
    out = [{'role': 'system', 'content': _text(system)}] if system else []
    for m in messages:
        c = m['content']
        text = _text(c)
        if isinstance(c, str):
            out.append({'role': m['role'], 'content': text})
        elif m['role'] == 'assistant':
            msg = {'role': 'assistant', 'content': text or None}
            calls = [{'id': b['id'], 'type': 'function', 'function': {'name': b['name'], 'arguments': json.dumps(b.get('input') or {}, ensure_ascii=False)}}
                     for b in c if b.get('type') == 'tool_use']
            if calls:
                msg['tool_calls'] = calls
            out.append(msg)
        else:  # user: результаты инструментов идут отдельными сообщениями role=tool, сразу за tool_calls
            out += [{'role': 'tool', 'tool_call_id': b['tool_use_id'], 'content': _text(b.get('content'))} for b in c if b.get('type') == 'tool_result']
            if text:
                out.append({'role': 'user', 'content': text})
    return out


def openai_to_anthropic(d):
    ch = (d.get('choices') or [{}])[0]
    msg = ch.get('message') or {}
    blocks = []
    text = msg.get('content') or msg.get('refusal')
    if text:
        blocks.append({'type': 'text', 'text': text})
    for tc in msg.get('tool_calls') or []:
        f = tc.get('function') or {}
        try:
            args = json.loads(f.get('arguments') or '{}')
        except ValueError:
            args = {}
        blocks.append({'type': 'tool_use', 'id': tc['id'], 'name': f.get('name'), 'input': args})
    used_tools = any(b['type'] == 'tool_use' for b in blocks)
    return {'content': blocks, 'stop_reason': 'tool_use' if used_tools else OPENAI_STOP.get(ch.get('finish_reason'), 'end_turn')}


def openai_error(code, data):
    """Приводит ошибку OpenAI к типам, которые знает страница (authentication_error, rate_limit_error, overloaded_error)."""
    e = data.get('error') if isinstance(data, dict) else None
    if isinstance(e, str):
        e = {'message': e}
    elif not isinstance(e, dict):
        e = data if isinstance(data, dict) else {}  # шлюзы отдают {"code": ..., "message": ...} без обёртки error
    kind = e.get('type')
    if code == 401:  # 403 не трогаем: это и «регион не поддерживается», и блокировка шлюза — текст ошибки важнее
        kind = 'authentication_error'
    elif code == 429 and str(e.get('code')).lower() != 'insufficient_quota':  # «кончились деньги» — не «подожди минутку»
        kind = 'rate_limit_error'
    elif code in (503, 529):
        kind = 'overloaded_error'
    return {'error': {'type': kind or 'http', 'message': e.get('message') or f'HTTP {code}'}}


def ai_call(body):
    provider = ai_provider()
    if not provider:
        return 503, {'error': {'type': 'no_key', 'message': 'ИИ выключен: перезапусти сервер с переменной ANTHROPIC_API_KEY или OPENAI_API_KEY.'}}
    key = os.environ[AI_ENV[provider][0]]
    max_tokens = int(body.get('max_tokens') or 4096)
    if provider == 'openai':
        payload = {'model': ai_model(provider), 'max_completion_tokens': max_tokens,
                   'messages': openai_messages(body.get('system'), body['messages'])}
        if body.get('tools'):
            payload['tools'] = [{'type': 'function', 'function': {'name': t['name'], 'description': t.get('description', ''),
                                                                   'parameters': t.get('input_schema') or {'type': 'object', 'properties': {}}}}
                                for t in body['tools']]
        base = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1').rstrip('/')  # Azure, OpenRouter, Ollama и т.п.
        code, data = ai_post(base + '/chat/completions', {'Authorization': 'Bearer ' + key}, payload)
        return (code, openai_to_anthropic(data)) if code == 200 else (code, openai_error(code, data))
    payload = {
        'model': ai_model(provider),
        'max_tokens': max_tokens,
        'messages': body['messages'],
    }
    for k in ('system', 'tools'):
        if body.get(k):
            payload[k] = body[k]
    return ai_post('https://api.anthropic.com/v1/messages', {'x-api-key': key, 'anthropic-version': '2023-06-01'}, payload)


def ai_post(url, headers, payload):
    # Свой User-Agent: Cloudflare перед сторонними шлюзами режет стандартный «Python-urllib» ответом 403 (error code: 1010)
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method='POST',
                                 headers={'User-Agent': 'plusy-v-kletku/1.0', **headers, 'content-type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return 200, json.loads(r.read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except Exception:  # не JSON (страница Cloudflare, прокси): покажем начало тела, чтобы было видно причину
            return e.code, {'error': {'type': 'http', 'message': f'{e} — {raw[:200].decode("utf-8", "replace").strip()}'}}
    except Exception as e:
        msg = f'{urllib.parse.urlsplit(url).netloc}: {e}'  # по одному «nodename nor servname» не понять, до какого хоста не достучались
        if 'CERTIFICATE_VERIFY_FAILED' in msg:
            msg += ' — на macOS запусти «Install Certificates.command» из папки Python в Программах.'
        return 502, {'error': {'type': 'network', 'message': msg}}


class Handler(http.server.SimpleHTTPRequestHandler):
    compiler = None
    port = 0

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        pass

    def log_error(self, fmt, *args):
        sys.stderr.write('[server] ' + (fmt % args) + '\n')

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def guess_type(self, path):
        t = super().guess_type(path)
        if t.startswith('text/') or t in ('application/json', 'application/javascript'):
            t += '; charset=utf-8'
        return t

    def _host_ok(self):
        host = (self.headers.get('Host') or '').split(':')[0]
        return host in ('127.0.0.1', 'localhost', '[::1]')

    def do_GET(self):
        if not self._host_ok():
            return self.send_error(403)
        if self.path.split('?')[0] == '/api/info':
            c, prov = self.compiler, ai_provider()
            return self._json(200, {'ok': not c.error, 'error': c.error, 'cxx': c.cxx, 'std': c.std, 'version': c.version,
                                    'os': f'{platform.system()} {platform.machine()}',
                                    'ai': bool(prov), 'provider': prov, 'model': ai_model(prov) if prov else None})
        if self.path.startswith(('/server.py', '/src/')) or '/.' in self.path:
            return self.send_error(404)
        return super().do_GET()

    def do_POST(self):
        # Защита от чужих сайтов: нужен localhost в Host (DNS rebinding) и свой заголовок
        # (его нельзя послать кросс-доменно без preflight, а на preflight мы не отвечаем).
        if not self._host_ok() or self.headers.get('X-PVK') != '1':
            return self.send_error(403)
        try:
            n = int(self.headers.get('Content-Length') or 0)
            if n > 2_000_000:
                return self._json(413, {'error': 'слишком большой запрос'})
            body = json.loads(self.rfile.read(n) or b'{}')
        except Exception:
            return self._json(400, {'error': 'bad json'})
        p = self.path.split('?')[0]
        if p == '/api/compile':
            return self._json(200, self.compiler.compile(str(body.get('src', '')), str(body.get('opt', '-O0'))))
        if p == '/api/run':
            t = min(max(float(body.get('timeout') or 4), 0.5), 20)
            return self._json(200, run_binary(str(body.get('id', '')), str(body.get('stdin', '')), t))
        if p == '/api/ai':
            code, data = ai_call(body)
            return self._json(code, data)
        self.send_error(404)

    def do_OPTIONS(self):
        self.send_error(403)

    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    ap = argparse.ArgumentParser(description='Плюсы в клетку — локальный сервер')
    ap.add_argument('--port', type=int, default=int(os.environ.get('PORT', 8737)))
    ap.add_argument('--cxx', help='компилятор (по умолчанию g++, затем clang++)')
    ap.add_argument('--no-browser', action='store_true')
    a = ap.parse_args()
    if os.path.isdir(WORK):  # подчистить старые сборки
        for n in os.listdir(WORK):
            f = os.path.join(WORK, n)
            try:
                if time.time() - os.path.getmtime(f) > 86400:
                    shutil.rmtree(f, ignore_errors=True) if os.path.isdir(f) else os.remove(f)
            except OSError:
                pass
    c = Compiler(a.cxx)
    Handler.compiler = c
    try:
        srv = Server(('127.0.0.1', a.port), Handler)
    except OSError as e:
        print(f'Порт {a.port} занят ({e}). Запусти с другим: python3 server.py --port 8800')
        sys.exit(1)
    url = f'http://127.0.0.1:{a.port}/'
    print('━' * 60)
    print('  Плюсы в клетку')
    print(f'  {url}')
    print(f'  компилятор: {c.cxx} -std={c.std}  ({c.version})' if not c.error else f'  ⚠ {c.error}')
    prov = ai_provider()
    print(f'  ИИ-тьютор: {f"включён ({prov}, {ai_model(prov)})" if prov else "выключен (нет ANTHROPIC_API_KEY или OPENAI_API_KEY)"}')
    print('  остановить: Ctrl+C')
    print('━' * 60)
    if not a.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\nПока!')


if __name__ == '__main__':
    main()
