## Описание
Сервис для благотворительного фонда, учебный проект


## Шаблон наполнения env-файла
```
APP_TITLE=Кошачий благотворительный фонд
APP_DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
FIRST_SUPERUSER_EMAIL=admin@admin.com
FIRST_SUPERUSER_PASSWORD=admin

```

## Запуск проекта

- Установите и активируйте виртуальное окружение

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

- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 

- Создайте базу данных:
```
alembic revision --autogenerate -m "Initial migration"
```
```
alembic upgrade head
```

- запустите приложение:
```
uvicorn app.main:app
```
режим отлаки:
```
uvicorn app.main:app --reload
```


## API документация

после локального запуска проекта
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
