# personal-training-and-nutrition-backend

## Описание

### Технологии
 - _[Python 3.11.5](https://docs.python.org/3/)_
 - _[Django 4.2.4](https://docs.djangoproject.com/en/4.1/releases/3.2.16/)_
 - _[Django REST framework 3.12.4](https://www.django-rest-framework.org/)_
 - _[Djoser 2.2.0](https://djoser.readthedocs.io/en/latest/)_
 - _[SQLite3](https://www3.sqlite.org/index.html)_


### Установка

1. Клонировать репозиторий (открываешь терминал в нужной папке и вставляешь эту строчку, и нажимаешь ENTER,
   в директории появится папка с названием проекта):

   ```python
   git clone git@github.com:Personal-training-and-nutrition/personal-training-and-nutrition-backend.git
   ```

2. Установить виртуальное окружение для проекта (там же набираешь одну из этих команд и нажимаешь ENTER,
   в директории появится папка env):

   ```python
   # для OS Lunix
   python3 -m venv venv

   # для OS Windows и MacOS
   python -m venv venv
   ```

3. Активировать виртуальное окружение для проекта (там же набираешь одну из этих команд и нажимаешь ENTER,
   в терминал слева появится (venv) - значит ты в виртуально окружении)):

   ```python
   # для OS Lunix
   source venv/bin/activate

   # для OS Windows и MacOS
   venv\Scripts\activate
   ```

4. Установить зависимости (так же в той же директории):

      ```python
   # для OS Lunix
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt

   # для OS Windows и MacOS
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Выполнить миграции на уровне проекта (Переходишь в папку backend, для этого набираешь в терминале команду "cd backend",
   после этого увидишь, что в командной строке добавился /backend и последовательно выполняешь следующие две команды):

   ```python
   # для OS Lunix
   python3 manage.py makemigrations
   python3 manage.py migrate

   # для OS Windows и MacOS
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Запустить проект локально:

   ```python
   # для OS Lunix
   python3 manage.py runserver

   # для OS Windows и MacOS
   python manage.py runserver
   ```

7. Открываешь документацию по ссылке ниже:

      ```python
    http://127.0.0.1:8000/api/schema/redoc/
   ```
