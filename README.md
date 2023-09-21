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

6. Выполнить миграции на уровне проекта:

   ```python
   # для OS Lunix и MacOS
   cd backend && python3 manage.py makemigrations && python3 manage.py migrate

   # для OS Windows
   cd backend && python manage.py makemigrations && python manage.py migrate
   ```

7. Cоздайте файл `.env` в директории `/backend/` с содержанием
   (файл можно создать командой "touch .env", а в директорию `/backend/`
   вы перешли предыдущей комнадно cd backend):

   ```python
   SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
   DEBUG=''
   ALLOWED_HOSTS='*' (или,ваши,хосты,через,запятые,без,пробелов)
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
