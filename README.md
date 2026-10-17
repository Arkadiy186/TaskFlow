# TaskFlow

## Запуск

```bash
cp .env.example .env
docker compose up --build
```

Windows PowerShell: `Copy-Item .env.example .env`

После запуска:
- API: http://localhost:8000
- Документация: http://localhost:8000/docs
- Проверка: http://localhost:8000/health

## Миграции вручную

```bash
docker compose run --rm api alembic upgrade head
docker compose run --rm api alembic downgrade base
docker compose run --rm api alembic upgrade head
```

## Примеры запросов

Создать проект:

```bash
curl -X POST http://localhost:8000/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Website", "description": "Test project"}'
```

Получить задачи проекта со статусом open:

```bash
curl "http://localhost:8000/v1/tasks?project_id=1&status=open"
```

Проверка работоспособности:

```bash
curl http://localhost:8000/health
```
