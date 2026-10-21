#!/bin/sh
# Пользователи платформы (окно логина в браузере).
#   ./user.sh add ИМЯ   — добавить или сменить пароль
#   ./user.sh del ИМЯ   — удалить
#   ./user.sh list      — кто есть
# Логины и bcrypt-хэши лежат в users.txt, из него собирается auth.caddy.
set -e
cd "$(dirname "$0")"

# переезд со старого set-password.sh: забрать пользователя из auth.caddy
if [ ! -f users.txt ]; then
	touch users.txt && chmod 600 users.txt
	[ -f auth.caddy ] && grep -E '^\s+\S+ \$2' auth.caddy | sed 's/^\s*//' > users.txt || true
fi

build() {
	{
		echo 'basic_auth {'
		sed 's/^/\t/' users.txt
		echo '}'
	} > auth.caddy   # перезапись на месте: Caddy видит файл через bind mount
	if docker compose ps --status running --services 2>/dev/null | grep -qx caddy; then
		docker compose exec -T caddy caddy reload --config /etc/caddy/Caddyfile >/dev/null && echo 'Caddy перезагружен.'
	fi
}

case "$1" in
add)
	[ -n "$2" ] || { echo "Использование: $0 add ИМЯ"; exit 1; }
	case "$2" in *[!A-Za-z0-9._-]*) echo 'Имя: только латиница, цифры, точка, дефис, подчёркивание.'; exit 1;; esac
	stty -echo; printf 'Пароль для %s: ' "$2"; read -r pass; stty echo; echo
	[ -n "$pass" ] || { echo 'Пустой пароль.'; exit 1; }
	hash=$(docker run --rm caddy:2 caddy hash-password --plaintext "$pass")
	grep -v "^$2 " users.txt > users.tmp || true
	echo "$2 $hash" >> users.tmp
	cat users.tmp > users.txt && rm users.tmp
	build
	echo "Готово: $2"
	;;
del)
	[ -n "$2" ] || { echo "Использование: $0 del ИМЯ"; exit 1; }
	grep -q "^$2 " users.txt || { echo "Нет такого пользователя: $2"; exit 1; }
	[ "$(wc -l < users.txt)" -gt 1 ] || { echo 'Это последний пользователь: Caddy не запустится без единого логина. Сначала добавь другого.'; exit 1; }
	grep -v "^$2 " users.txt > users.tmp || true
	cat users.tmp > users.txt && rm users.tmp
	build
	echo "Удалён: $2"
	;;
list)
	cut -d' ' -f1 users.txt
	;;
*)
	sed -n '2,5p' "$0" | sed 's/^# \{0,1\}//'
	exit 1
	;;
esac
