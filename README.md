## Хранилища и базы данных. Лабораторные работы

Работу выполнили студенты:  
P4116 - Егошин Алексей, Кулинич Ярослав  
P4115 - Карасёва Мария  

## Инструкции по запуску

1. Создаем директорию и пустой файл базы данных самого airflow:
```bash
mkdir ./etl/data
touch ./etl/data/airflow.db
chmod 777 ./etl/data/airflow.db
```
2. Запускаем контейнеры:
```bash
# Linux
docker compose up
# Mac OS
docker compose -f docker-compose.yml -f docker-compose-macos.yml up
```
3. Заходим в веб-морду AirFlow - `http://172.16.0.4:8080` (в случае Mac OS - `http://localhost:8080`) и авторизуемся.
```text
креды:
login: admin
password: <найти в логах и запомнить>
```
4. Admin -> Connections инициализируем коннекты к источникам данных
```text
ID: postgres_source
host: postgres
database: source
username: source
password: source

ID: postgres_dwh
host: postgres
database: dwh
username: dwh
password: dwh

ID: mongo_source
host: mongodb
database: mongo
username: mongo
password: mongo
```