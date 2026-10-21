# Развёртывание на сервере

Платформа запускается в Docker за Caddy на `https://plusy.dammit.dev`, вход по логину и паролю.

Работают два контейнера из одного образа:

- **pvk** выполняет присланный код, поэтому изолирован: нет выхода в интернет, нет ключей,
  файлы только для чтения, не root, лимиты на процессы, память и CPU;
- **ai** держит ключ API и ходит в нейросеть, но чужой код в нём не выполняется.

Caddy отправляет `/api/ai` и `/api/info` в `ai`, всё остальное — в `pvk`.

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

## ИИ-тьютор (по желанию)

```sh
cp ai.env.example ai.env && nano ai.env   # вписать ключ и модель
docker compose up -d
```

Без `ai.env` платформа работает, просто ИИ-кнопки выключены.
API Anthropic и OpenAI с российских IP недоступны, поэтому в примере — Yandex AI Studio
(OpenAI-совместимый API): ключ API и ID каталога берутся в консоли Yandex Cloud.
Подойдёт и любой другой OpenAI-совместимый сервис.

Поставь в консоли провайдера лимит расходов: тьютором пользуются все, кто знает пароль.

## Обновление

```sh
cd ~/plusy-v-kletku && git pull && cd deploy && docker compose up -d --build
```

## Полезное

- Логи: `docker compose logs -f pvk` (или `caddy`)
- Сменить пароль: `./set-password.sh && docker compose restart caddy`
- Другой домен: поменять его в `Caddyfile` и в `PVK_ALLOWED_HOSTS` в `docker-compose.yml`
