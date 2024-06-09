# Web chat

## Создание окружения    
Установка poetry и необходимых пакетов:
``` Bash
pip install poetry

cd .\src\
poetry install
```

Параметры БД находятся в ```src/core/config.py```   

Применение миграций:
``` Bash
poetry run alembic upgrade head
```

Локальный запуск сервиса:
``` Bash
poetry run py main.py
```

## Прекоммит:
``` Bash
poetry run ruff --fix
poetry run ruff format
poetry run mypy .
```

docker compose -f .\docker-compose.chat.yaml up --build -d