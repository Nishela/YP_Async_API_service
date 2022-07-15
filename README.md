# Проектная работа 4-5 спринтов

## Основные сервисы 
- api_service для Fast api + тесты для сервиса
- etl_service для запуска ETL pipeline
- nginx для проксирования запросов

## Доп сервисы
- база Postgres
- база Elasticsearch
- база Redis

# Инструкция по использованию

---
## Запуск и тестирование
### Запуск:
1. Создаем файл `.env` на примере `.env.example`
2. Выполняем сборку и запуск проекта:
```shell
$ make run
```
Запускаются: 
- база Postgres
- база Elasticsearch
- база Redis
- ETL сервис
- Fast API service
- сервер nginx

**Для тестирования сервиса и просмотра документации в swagger, перейдите по ссылке: 
http://0.0.0.0/api_service/openapi#**  

### Тестирование :
- сборка контейнера и запуск тестов c
последующим удалением всех контейнеров, в сборку входят: сами тесты, ES, REDIS 
(полезно для одноразовой проверки):
```shell
make tests_run
```
- сборка/пересборка контейнера с тестами и запуск тестов без удаления сборки
(полезно после рефакторинга кода, если не хочется удалять контейнеры с ES, Redis):
```shell
make tests_up
```

- удаление всей сборки
```shell
make tests_down
```

---
## Makefile функции: 

 - сборка проекта:
```shell
make build
```
- сброс сохраненного состояния(для загрузки всей базы заново):
```shell
make drop-state
```

 - запуск проекта:
```shell
make up
```

 - запуск контейнера с тестами:
```shell
make tests_run
```

 - удаление контейнера с тестами проекта:
```shell
make tests_down
```

- остановить и удалить контейнеры и другие ресурсы, созданные командой docker-compose up
```shell
 make down
```
- собрать и сразу запустить проект
```shell
make run
```
- остановить контейнеры проекта, но не удалять их
```shell
make stop
```
- запуск остановленных контейнеровп проекта
```shell
make start
```

- просмотр логов
```shell
make logs
```

---
