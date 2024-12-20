# API BookMarket
### 📦 Зависимости:
1. [Python 3.13.0](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)
2. [PostgreSQL 17.0](https://sbp.enterprisedb.com/getfile.jsp?fileid=1259174)

### 📄 Описание:
API BookMarket - это небольшое API, созданное в рамках учебного задания,
которое соответствует минимальным требованиям.

Оно обладает следующим *функционалом*:
- Регистрация и авторизация пользователей;
- Управление системой контроля доступа пользователей через роли; 
- Размещение книг на продажу, отзывов к ним, а также заказов на приобретение книжных изделий;
- Осуществление поиска той или иной сущности через фильтры;
- Загрузка изображений для профилей пользователей, обложек книг, портретов авторов;
- Валидация пользовательского ввода;

и т.д.

### 🚀 Установка:
1. Установить необходимые библиотеки:
```
pip install -r requirements.txt
```
2. Создать и настроить *.env* файл:
```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
SECRET_KEY=
ALGORITHM=
ADMIN_USERNAME=
ADMIN_PASSWORD=
```
Пример заполнения *.env* файла:
```
DB_USER=postgres
DB_PASSWORD=changeme
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
SECRET_KEY=DX73p2hQtLM9vjxYulxHrSTsmDP1xN-3JzzMuqt2YPo6QHPnBg8BfhQqGLPhqU
ALGORITHM=HS256
ADMIN_USERNAME=admin@admin.com
ADMIN_PASSWORD=admin
```
**ADMIN_USERNAME** и **ADMIN_PASSWORD** отвечают за профиль администратора, который устанавливается по умолчанию в системе при первичном запуске или же при отсутствии пользователя в базе данных с ролью администратора.

Рассмотрим далее вариант с использованием `docker-compose`* файла, поскольку с предустановленной на машине PostgreSQL гораздо легче работать.

3. Совместно с **API** возможно использовать либо **PostgreSQL** установленный прямо на машину, либо **PostgreSQL**, который находится в docker-compose файле.
Запуск *docker-compose.yaml* происходит через команду в терминале, находясь по пути *"..\API-BookMarket"*:
```
docker compose up
```
4. В браузере необходимо ввести адрес:
```
localhost:8080
```
5. Попав на страницу, обращаем внимание на **Quick Links** и кнопку **Add New Server**, здесь появится окно:

![postgres_web](https://imgur.com/n3et7fC.png)

Заполняем нужными данными, которые будут занесены затем в *.env* файл, чтобы **API** могло обращаться к **Postgres**.
Однако во избежание потенциальных ошибок советую в разделе *Connection* и поле *Host name/address* указывать `postgres`, вместо `localhost` или иного значения, указанного в *.env* в поле *DB_HOST*, иначе база данных может просто не создаваться.

6. Затем в терминале директории проекта прописываем команду для миграции таблиц сущностей в БД:
```
alembic upgrade 423ab8fbc2e1
```
7. Запускаем сам **API**. Здесь можно указать свой порт:
```
uvicorn app.main:app --reload --port 8000
```
8. В браузере вводим адрес:
```
localhost:8000
```
И мы попадаем на главную страницу **API**:

![api_main](https://imgur.com/8215isc.png)

Далее для удобства просмотра всех возможных эндпоинтов можно ввести в адресной строке:
```
localhost:8000/docs
```
На данной странице можно будет протестировать все эндпоинты.
