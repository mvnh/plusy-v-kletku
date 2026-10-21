# Серверная версия «Плюсов в клетку». Запускать через deploy/docker-compose.yml:
# там контейнер изолирован (без сети, только чтение, лимиты), потому что он выполняет чужой код.
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends g++ \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --uid 1000 --create-home pvk
WORKDIR /app
COPY --chown=root:root . .

ENV PVK_HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER 1000:1000
EXPOSE 8737
CMD ["python3", "server.py", "--no-browser"]
