# Продуктовый помощник
![Workflow](https://github.com/iliazaraysky/yamdb_final/actions/workflows/main.yml/badge.svg)

Это место где пользователи могут публиковать свои рецепты, подписываться друг на друга, а также создавать корзину покупок ингредиентов

## Возможности сервиса Foodgram
1. Пользователи могут зарегистрировать на сервисе, чтобы получить доступ в личный кабинет
2. Каждый зарегистрированный пользователь может создавать, редактировать, и удалять свои публикации
3. Зарегистрированные пользователи могут добавлять рецепты в избранное
4. Зарегистрированные пользователи могут подписываться друг на друга
5. У сервиса предусмотрена фильтрация по тегам
6. Каждый зарегистрированный пользователь имеет возможность добавить рецепт в список покупок, а затем его скачать

## Установка
1. Устанавливаем на своем компьютере docker и docker-compose
2. Клонируем репозиторий
```
git clone https://github.com/iliazaraysky/foodgram-project-react.git
```
3. Переходим в каталог ./foodgram-project-react/backend/
4. Создайте файл .env со следующим содержимым:

```
ENV_SECRET_KEY=7r7w5%g^&s2ff^g0#q+buhsicw@t2#48t41tv5v2%raeo5hh^)
DEBUG_STATUS=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

> Примечание. У вас могут быть свои параметры в переменных DB_NAME (Имя БД), POSTGRES_USER (пользователь БД), POSTGRES_PASSWORD (пароль пользователя БД), ENV_SECRET_KEY (можно сгенерировать на сайте [djecrety.ir](https://djecrety.ir/))
5. Переходим в каталог infra и запускаем создание контейнеров:
```
docker-compose up
```
> Примечание. Первый запуск создания контейнеров можно запустить без дополнительных настроек. Последующие пересборки необходимо совершать с параметром --build
```
docker-compose up --build
```
6. Чтобы проект начал функционировать полностью, необходимо произвести миграции и собрать статические файлы. Набираем команды:
```
docker-compose exec backend python manage.py makemigrations users recipes
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic
```
7. Создаем в проекте суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
