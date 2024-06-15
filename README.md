## Хранилища и базы данных. Лабораторные работы

Работу выполнили студенты:  
P4116 - Егошин Алексей, Кулинич Ярослав  
P4115 - Карасёва Мария  

## Инструкции по запуску

1. Создаем директорию и пустой файл базы данных самого airflow:
```bash
mkdir ./etc/data
touch ./etc/data/airflow.db
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
hostname: source
database: source
username: source
password: source
```