## Описание
Сервис для благотворительного фонда.

Основные возможности:
- создание благотворительных проектов
- создание донейшнов
- автоматическое распределение средств по проектам

В сервисе может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

## Технический стек
Python 3.7.9
Django 2.2.16
Django REST framework 3.12.4
Djoser 2.1.0

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
