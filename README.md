<h1 align="center">Сервис уведомлений</h1>

## Запуск проекта

[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) и [Docker Compose](https://docs.docker.com/compose/install/linux/) должны быть предварительно установлены. Склонируй репозиторий и перейди в папку с проектом:
```
git clone https://github.com/Tizoner/notification-service.git && cd notification-service
```
Затем запусти все сервисы проекта одной командой:
```
docker compose up
```
После этого по адресу /docs/ становится доступна документация разработанного API в формате OpenApi.
По адресу /admin/ можно попасть в админ панель. Аккаунт администратора будет создан автоматически на основе данных из .env файла.

## Использованные технологии
- Язык программирования [Python](https://www.python.org) &nbsp;`3.10`
- Веб-фреймворк [Django](https://www.djangoproject.com) &nbsp;`4.1`
- REST фреймворк [DRF](https://www.django-rest-framework.org) &nbsp;`3.14`
- СУБД [PostgreSQL](https://www.postgresql.org) &nbsp;`15`
- Распределенная очередь задач [Celery](https://docs.celeryq.dev) &nbsp;`5.2`
- Брокер сообщений [Redis](https://redis.io) &nbsp;`7.0`
- Платформа контейнеризации [Docker](https://www.docker.com) &nbsp;`20.10`

## Примечание
Файлы  .env, db.env содержат примеры значений используемых переменных окружения, поэтому эти файлы не были добавлены в .gitignore.

## Выполненные дополнительные задания
3\. подготовить docker-compose для запуска всех сервисов проекта одной командой  
5. сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API  
6. реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям
