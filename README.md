# vorontsov39/infra_sp2
Проект YaMDb позволяет добавлять новых пользователей,
собирает отзывы пользователей на различные произведения.

### Авторы:
- Vorontsov Anton (Vorontsov39) https://github.com/Vorontsov39

## стек:
- Python
- Django
-  DRF
- Docker
- Nginx


## руководство по установке Docker
можно найти [здесь](https://docs.docker.com/engine/install/)


---

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/vorontsov39/infra_sp2.git
```

```bash
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

```bash
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Запустить приложение в контейнерах:

*из директории `infra/`*
```bash
docker-compose up -d --build
```

Выполнить миграции:

*из директории `infra/`*
```bash
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

*из директории `infra/`*
```bash
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

*из директории `infra/`*
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Остановить приложение в контейнерах:

*из директории `infra/`*
```bash
docker-compose down -v
```
