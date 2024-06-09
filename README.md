# pvr-map

Клонирование репозитория:
``` Bash
git clone -c http.sslVerify=false https://gitlab.bdd/grade/its-grade.git
```

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

alembic revision --autogenerate -m 'init'
docker compose -f .\docker-compose.chat.yaml up --build -d