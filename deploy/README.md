# Развёртывание на сервере

Платформа запускается в Docker за Caddy на `https://plusy.dammit.dev`, вход по логину и паролю.

Контейнер платформы выполняет присланный код, поэтому он изолирован:
нет выхода в интернет, файлы только для чтения, не root, лимиты на процессы, память и CPU.
Из-за отсутствия интернета ИИ-тьютор на сервере выключен. Это сделано специально:
ключ API в контейнере, где выполняется чужой код, рано или поздно утечёт.

## 1. DNS

В Porkbun: DNS → добавить запись **A**, host `plusy`, answer — IP сервера.

## 2. Подготовка сервера (Ubuntu 24.04)

Зайти по SSH и выполнить:

```sh
apt update && apt upgrade -y
apt install -y docker.io docker-compose-v2 docker-buildx git tmux

# swap на 2 ГБ: g++ с санитайзерами любит память
fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# файрвол: только SSH и веб
ufw allow OpenSSH && ufw allow 80,443/tcp && ufw allow 443/udp && ufw --force enable
```

## 3. Запуск

```sh
git clone https://github.com/mvnh/plusy-v-kletku
cd plusy-v-kletku/deploy
./set-password.sh            # придумать логин и пароль для входа
docker compose up -d --build
```

Через минуту открыть `https://plusy.dammit.dev`. Сертификат Caddy получит сам.

Если `docker compose` падает с 403/timeout при скачивании `python` или `caddy` с Docker Hub,
подключи зеркало реестра: у многих российских хостеров оно есть, адрес — в их документации.
Его прописывают в `/etc/docker/daemon.json` как `{"registry-mirrors": ["https://адрес-зеркала"]}`,
затем `systemctl restart docker`.

## Обновление

```sh
cd ~/plusy-v-kletku && git pull && cd deploy && docker compose up -d --build
```

## Полезное

- Логи: `docker compose logs -f pvk` (или `caddy`)
- Сменить пароль: `./set-password.sh && docker compose restart caddy`
- Другой домен: поменять его в `Caddyfile` и в `PVK_ALLOWED_HOSTS` в `docker-compose.yml`
