#!/usr/bin/env bash
# «Плюсы в клетку»: запуск с нуля.
#   bash start.sh            — проверить/поставить всё нужное и запустить платформу
#   bash start.sh --port 8800 --no-browser   — опции передаются в server.py
#
# Что ставится, если нет:
#   macOS   — Xcode Command Line Tools (clang++ и python3)
#   Linux   — g++ и python3 через пакетный менеджер (apt, dnf, yum, pacman, zypper, apk)
#   Windows — в MSYS2: gcc и python через pacman (для обычного Windows есть start.bat)
# Для установки может понадобиться пароль администратора (sudo).

if [ -z "${BASH_VERSION:-}" ]; then exec bash "$0" "$@"; fi
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

say()  { printf '\033[1;34m▸\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m✓\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31m✗\033[0m %s\n' "$*" >&2; exit 1; }
has()  { command -v "$1" >/dev/null 2>&1; }

[ -f server.py ] || die "Не вижу server.py рядом со скриптом. Запускай start.sh из папки платформы."

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if has sudo; then SUDO="sudo"; fi
fi
need_root() {
  if [ "$(id -u)" -ne 0 ] && [ -z "$SUDO" ]; then
    die "Нужны права администратора, а sudo нет. Запусти от root или поставь вручную: $*"
  fi
}

python_ok() {
  local py="$1"
  has "$py" && "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1
}
find_python() {
  for p in python3 python; do
    if python_ok "$p"; then PY="$p"; return 0; fi
  done
  return 1
}
find_cxx() {
  if [ -n "${CXX:-}" ] && has "$CXX"; then return 0; fi
  for c in g++ clang++ c++; do
    if has "$c"; then CXX="$c"; return 0; fi
  done
  return 1
}
# Компилятор считается рабочим, только если реально собирает программу с <iostream>.
cxx_works() {
  local tmp; tmp="$(mktemp -d)"
  printf '#include <iostream>\nint main(){ std::cout << "ok"; }\n' > "$tmp/t.cpp"
  if "$CXX" -std=c++17 "$tmp/t.cpp" -o "$tmp/t" >/dev/null 2>&1 && [ "$("$tmp/t")" = "ok" ]; then
    rm -rf "$tmp"; return 0
  fi
  rm -rf "$tmp"; return 1
}

# ---------------------------------------------------------------- macOS
install_macos() {
  if xcode-select -p >/dev/null 2>&1; then return 0; fi
  say "Ставлю Xcode Command Line Tools (clang++, python3). Это ~1–2 ГБ и несколько минут."
  # Тихая установка через softwareupdate (спросит пароль), если не выйдет — обычное окно установщика.
  local flag=/tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress label=""
  touch "$flag"
  label="$(softwareupdate -l 2>/dev/null | grep -E '\*.*Command Line Tools' | sed -E 's/^.*\*[[:space:]]*(Label:[[:space:]]*)?//' | sort -V | tail -n1 || true)"
  if [ -n "$label" ]; then
    say "Нашёл пакет: $label"
    sudo softwareupdate -i "$label" --verbose || warn "softwareupdate не справился, попробую через окно установщика."
  fi
  rm -f "$flag"
  if ! xcode-select -p >/dev/null 2>&1; then
    xcode-select --install >/dev/null 2>&1 || true
    say "Открылось окно установки — нажми «Установить» и дождись конца. Я подожду (до 60 минут)…"
    local i=0
    until xcode-select -p >/dev/null 2>&1; do
      sleep 10; i=$((i + 10))
      [ "$i" -ge 3600 ] && die "Command Line Tools так и не установились. Поставь вручную: xcode-select --install"
    done
  fi
  ok "Command Line Tools установлены"
}

# ---------------------------------------------------------------- Linux
install_linux() {
  if has apt-get; then
    need_root "g++ python3"
    say "Ставлю пакеты через apt…"
    $SUDO apt-get update -y
    $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y g++ python3
  elif has dnf; then
    need_root "gcc-c++ python3"; say "Ставлю пакеты через dnf…"
    $SUDO dnf install -y gcc-c++ python3
  elif has yum; then
    need_root "gcc-c++ python3"; say "Ставлю пакеты через yum…"
    $SUDO yum install -y gcc-c++ python3
  elif has pacman; then
    need_root "gcc python"; say "Ставлю пакеты через pacman…"
    $SUDO pacman -Sy --needed --noconfirm gcc python
  elif has zypper; then
    need_root "gcc-c++ python3"; say "Ставлю пакеты через zypper…"
    $SUDO zypper --non-interactive install gcc-c++ python3
  elif has apk; then
    need_root "g++ python3"; say "Ставлю пакеты через apk…"
    $SUDO apk add --no-cache g++ python3
  else
    die "Не знаю пакетный менеджер этой системы. Поставь вручную g++ и python3 (3.8+), потом запусти снова."
  fi
}

# ---------------------------------------------------------------- MSYS2 / Git Bash
install_msys() {
  if has pacman; then
    say "Ставлю gcc и python через pacman (MSYS2)…"
    pacman -Sy --needed --noconfirm mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-python
    export PATH="/ucrt64/bin:$PATH"
  else
    die "Это Git Bash без пакетного менеджера. Поставь MSYS2 (https://www.msys2.org) или используй start.bat — инструкция в README.md."
  fi
}

OS="$(uname -s)"
PY=""
say "Проверяю окружение ($OS $(uname -m))…"

need_install=0
find_python || need_install=1
if find_cxx; then cxx_works || need_install=1; else need_install=1; fi
if [ "$OS" = "Darwin" ] && ! xcode-select -p >/dev/null 2>&1; then need_install=1; fi

if [ "$need_install" -eq 1 ]; then
  case "$OS" in
    Darwin) install_macos ;;
    Linux) install_linux ;;
    MINGW*|MSYS*|CYGWIN*) install_msys ;;
    *) die "Система $OS не поддерживается этим скриптом. Нужны python3 (3.8+) и g++/clang++." ;;
  esac
  hash -r
  find_python || die "python3 (3.8+) так и не нашёлся после установки."
  find_cxx || die "Компилятор C++ так и не нашёлся после установки."
  cxx_works || die "$CXX есть, но не собирает даже hello world. Проверь установку компилятора."
fi

ok "Python: $("$PY" --version 2>&1)"
ok "Компилятор: $CXX ($("$CXX" --version 2>/dev/null | head -n1))"

if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -z "${OPENAI_API_KEY:-}" ]; then
  warn "ИИ-тьютор выключен. Чтобы включить: export ANTHROPIC_API_KEY=sk-ant-... (или OPENAI_API_KEY=sk-...) и запусти снова (необязательно)."
fi

exec "$PY" server.py --cxx "$CXX" "$@"
