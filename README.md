# personal-training-and-nutrition-backend

## Описание

### Технологии
 - _[Python 3.11.5](https://docs.python.org/3/)_
 - _[Django 4.2.4](https://docs.djangoproject.com/en/4.1/releases/3.2.16/)_
 - _[Django REST framework 3.12.4](https://www.django-rest-framework.org/)_
 - _[Djoser 2.2.0](https://djoser.readthedocs.io/en/latest/)_
 - _[SQLite3](https://www3.sqlite.org/index.html)_


### Установка

1. Клонировать репозиторий (открываешь терминал в нужной папке и вставляешь эту строчку,
   и нажимаешь "ENTER", в директории появится папка с названием проекта):

   ```python
   git clone git@github.com:Personal-training-and-nutrition/personal-training-and-nutrition-backend.git
   ```
2. Переходишь в ветку develop:

   ```python
   cd personal-training-and-nutrition-backend && git checkout develop
   ```

3. Установить виртуальное окружение для проекта (там же набираешь одну из этих команд
   и нажимаешь "ENTER", в директории появится папка env):

   ```python
   # для OS Lunix и MacOS
   python3 -m venv venv

   # для OS Windows и MacOS
   python -m venv venv
   ```

4. Активировать виртуальное окружение для проекта (там же набираешь одну из этих команд
   и нажимаешь "ENTER", в терминал слева появится (venv) - значит ты в виртуально окружении)):

   ```python
   # для OS Lunix и MacOS
   source venv/bin/activate

   # для OS Windows
   source venv/Scripts/activate
   ```

5. Установить зависимости (так же в той же директории):

      ```python
   # для OS Lunix и MacOS
   python3 -m pip install --upgrade pip && pip install -r requirements.txt

   # для OS Windows
   python -m pip install --upgrade pip && pip install -r requirements.txt
   ```

6. Cоздайте файл `.env` в директории `/backend/`:

   ```python
   cd backend && nano .env

   В открывшийся редактор вставьте ключи ниже и после закройте командой "Ctrl + X"

   SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
   DEBUG=''
   ALLOWED_HOSTS='*' (или,ваши,хосты,через,запятые,без,пробелов)
   DEVELOPMENT=True (если хотите работать на sqlite, иначе - False)

   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DB=
   DB_HOST=
   DB_PORT=

   SOCIAL_AUTH_MAILRU_KEY=
   SOCIAL_AUTH_MAILRU_SECRET=
   SOCIAL_AUTH_VK_OAUTH2_KEY=
   SOCIAL_AUTH_VK_OAUTH2_SECRET=
   SOCIAL_AUTH_YANDEX_KEY=
   SOCIAL_AUTH_YANDEX_SECRET=

   EMAIL_HOST_USER=
   EMAIL_HOST_PASSWORD=
   ```

7. Выполнить миграции на уровне проекта из директории `/backend/`
   (если не вы перешли на нее предыдущей комнадно cd backend,
   то выполните команду cd backend):

   ```python
   # для OS Lunix и MacOS
   python3 manage.py makemigrations && python3 manage.py migrate

   # для OS Windows
   python manage.py makemigrations && python manage.py migrate
   ```

8. Запускаешь проект локально:

   ```python
   # для OS Lunix и MacOS
   python3 manage.py runserver

   # для OS Windows
   python manage.py runserver
   ```

### Работа с документацией и Postman после запуска проекта

1. Открываешь документацию по одной из ссылок:

   - _[Swagger UI](http://127.0.0.1:8000/api/schema/swagger-ui/)_
   - _[ReDoc (более аутентичный и простой интерфейс)](http://127.0.0.1:8000/api/schema/redoc/)_


2. Чтобы импортировать коллекцию в Postman и использовать ее для тестирования:

   - Откройте Postman и нажмите на кнопку "Import" в верхнем левом углу.
   - В разделе "Link" вставьте ссылку http://127.0.0.1:8000/api/schema/ и нажмите на кнопку "Continue".
   - В появившемся окне у вас будет возможность выбрать каталог, в который нужно импортировать.


3. Если не понимаешь, то смотришь видео по ссылкам:

   - _[Запись вебинара от ментора СА по OpenApi и Postman](https://disk.yandex.ru/i/IphJiDoH4ruBEA)_
   - _[Видео по работе с Postman от Никиты](https://disk.yandex.ru/d/ej4OW0Am5hfSow)_


### Вход в админку

1. ввести команду 'python manage.py createsuperuser', там придумаешь почту и пароль

   ```python
   # для OS Lunix и MacOS
   python3 manage.py createsuperuser

   # для OS Windows
   python manage.py createsuperuser
   ```
2. Запускаешь проект локально:

   ```python
   # для OS Lunix и MacOS
   python3 manage.py runserver

   # для OS Windows
   python manage.py runserver
   ```

3. Заходишь по адресу http://127.0.0.1:8000/admin со своим почтой и паролем


# Запускаем через docker-compose с Frontend'ом

### Важно! Для локального запуска, .env-файл берем у https://github.com/AlexanderPAI. Когда начнем настраивать деплой через docker-compose - необходимо будет в docker-compose.yml откорректировать название базы данных через параметр`environment`.

#### 1. Склонировать репозиторий:
```bash
git clone git@github.com:Personal-training-and-nutrition/personal-training-and-nutrition-backend.git
```

#### 2. Перейти в ветку `infra/docker_front_and_back`:
```bash
git checkout infra/docker_front_and_back
git pull
```
#### 3. Разметить актульный .env-файл в корне приложения `personal-training-and-nutrition-backend/`
#### 4. Собрать и запустить контейнеры приложения из корневого каталога приложения:
```bash
cd personal-training-and-nutrition-backend/
docker-compose up --build
```
#### 5. Открыть второй терминал. В нем открыть терминал контейнера `backend`:
```bash
docker exec -it backend bash
```
В командной строке должно появиться что-то типа:
```bash
root@4506fce0b38e:/app#
```

#### 6. В терминале контейнера `backend`(важно) собрать статику, создать миграции, применить их, создать суперпользователя для админки:
```bash
# Собираем статику:
python manage.py collectstatic

# Создаем миграции. Так как в репе нет файлов миграции 
# нужно создавать миграции для каждого отдельного приложения 
# с флагом --no-input
python manage.py makemigrations diets --no-input
python manage.py makemigrations users --no-input
python manage.py makemigrations workouts --no-input

# Применяем миграции:
python manage.py migrate

# Создаем суперпользователя:
python manage.py createsuperuser
```
#### 7. Закрыть терминал контейнера `backend`, нажав сочетание клавиш `Ctrl` + `D`

## Проект запускается на 9000 порту `http://127.0.0.1:9000/`
