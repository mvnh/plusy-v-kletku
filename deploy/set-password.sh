#!/bin/sh
# Создаёт auth.caddy с логином и bcrypt-хэшем пароля для входа на платформу.
set -e
cd "$(dirname "$0")"
printf 'Логин: '; read -r user
stty -echo; printf 'Пароль: '; read -r pass; stty echo; echo
hash=$(docker run --rm caddy:2 caddy hash-password --plaintext "$pass")
printf 'basic_auth {\n\t%s %s\n}\n' "$user" "$hash" > auth.caddy
chmod 644 auth.caddy
echo "Готово: auth.caddy. Если Caddy уже запущен: docker compose restart caddy"
