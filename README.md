REST API для реализации Least Recently Used (LRU) cache с поддержкой Time-To-Live (TTL).

Эндпоинты для работы с ресурсами

- GET /cache/{key} получение значения по ключу
- PUT /cache/{key} добавление/обновление значения по ключу
- DELETE /cache/{key} удаление значение по ключу
- GET /cache/stats получение статистики cache (количество элементов, максимальный размер, список ключей)


Емкость LRU cache задает через переменную окружения: APP_CAPACITY_CACHE

### Стек технологий 
    - Python3.11
    - FastAPI - API
    - Docker
    - asyncio
    - pytest


Тесты на pytest реализованы для всех эндпоинтов API и логики LRU cache.


#### Запуск приложения

- Копируем код приложения в Вашу директорию.

`git clone https://github.com/KIchkinevVladislav/lru-cache-api_test.git`

- Вы можете задать максимальный размер кеша через изменения переменной окружения APP_CAPACITY_CACHE в docker-compose.yml

- Запускаем контейнеры

`docker compose up -d`

Приложение готово для тестирования:

http://127.0.0.1:8000/docs

#### Запуск тестов

`docker exec app python -m pytest`