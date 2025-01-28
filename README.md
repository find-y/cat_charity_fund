## Описание
Сервис для благотворительного фонда.

Основные возможности:
- создание благотворительных проектов
- создание донейшнов
- автоматическое распределение средств по проектам

В сервисе может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

## Технический стек
- Python 3.7.9
- FastAPI 0.78.0
- Alembic 1.7.7
- Pydantic 1.9.1
- Jinja2 3.1.4
- SQLAlchemy 1.4.36
- Uvicorn 0.17.6

## Шаблон наполнения env-файла
```
APP_TITLE=Название благотворительного фонда
APP_DESCRIPTION=Сервис для поддержки редких видов животных
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
FIRST_SUPERUSER_EMAIL=admin@admin.com
FIRST_SUPERUSER_PASSWORD=admin

```

## Запуск проекта

1. Создайте файл .env. По необходимости, внесите свои данные.
```
cp env_example .env
nano .env
```

2. Установите и активируйте виртуальное окружение

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

3. Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 

4. Создайте базу данных:
```
alembic revision --autogenerate -m "Initial migration"
```
```
alembic upgrade head
```

5. Запустите приложение:
```
uvicorn app.main:app
```
- режим отлаки:
```
uvicorn app.main:app --reload
```


## API документация

после локального запуска проекта  
http://127.0.0.1:8000/docs  
http://127.0.0.1:8000/redoc  
