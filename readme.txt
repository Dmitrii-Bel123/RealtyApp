Настройка docker для django на mysql
https://habr.com/ru/articles/519912/

# Запустить контейнеры и сгенерить:
docker-compose up --build -d

# Пересобрать конкретный контейнер
docker-compose up realty --build -d

# Остановить контейнеры:
docker-compose kill

# Остановить контейнеры и удалить:
docker-compose down -v

# рестарт контейнеров:
docker-compose restart

# создание суперпользователя для интерфейса администратора
docker-compose exec -it realty python manage.py createsuperuser

# создание миграций для изменений в БД
docker-compose exec -it realty python manage.py makemigrations

# выполнение миграций в БД
docker-compose exec -it realty python manage.py migrate

# выполнение sql запросов в БД
docker-compose exec -it db bash -c "mysql -p realty < /code/init.sql"

