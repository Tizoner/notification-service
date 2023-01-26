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
После этого по адресу /docs/ должна открываться документация разработанного API в формате OpenApi.
По адресу /admin/ можно попасть в админ панель. Аккаунт администратора будет создан автоматически на основе данных из .env файла.

## Использованные технологии
- [Python](https://www.python.org) &nbsp;`3.10`
- [Django](https://www.djangoproject.com) &nbsp;`4.1`
- [DRF](https://www.django-rest-framework.org) &nbsp;`3.14`
- [PostgreSQL](https://www.postgresql.org) &nbsp;`15`
- [Docker](https://www.docker.com) &nbsp;`20.10`

## Примечание
Файлы  .env, db.env содержат примеры значений используемых переменных окружения, поэтому эти файлы не были добавлены в .gitignore.

## Выполненные дополнительные задания
- 3. подготовить docker-compose для запуска всех сервисов проекта одной командой
- 5. сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API
- 6. реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям
