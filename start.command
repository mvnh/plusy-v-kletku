#!/bin/bash
# Двойной клик в Finder: то же, что start.sh (поставит недостающее и запустит платформу).
cd "$(dirname "$0")" || exit 1
bash ./start.sh "$@"
status=$?
[ $status -ne 0 ] && { echo; read -r -p "Нажми Enter, чтобы закрыть окно…" _; }
exit $status
