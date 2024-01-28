### Настройка Docker Compose
Технология автоматического развертывания набора контейнеров. Порядок и параметры развертывания определяются настроечным файлом docker-compose.yml.
Пример файла docker-compose.yml:
```docker
version: "3"
networks:
  external:
    driver: bridge
  internal:
    driver: bridge
volumes:
  drupal-data:/srv/drupal-ant-blog/data
  db-data:/srv/mysql/data
  - /srv/mysql/init.d:/docker-entrypoint-initdb.d
```
#### Общие параметры docker-compose.yml
- version: "3": версия docker-compose
- networks: раздел, определяющий список виртуальных сетей для связи между контейнерами.
- volumes: раздел, определяющий список томов хранения данных, используемых контейнерами.
- services: раздел, определяющий список запускаемых контейнеров.
#### Раздел networks
- external: название сети.
- driver: bridge: тип драйвера сети, возможные типы: bridge, host, overlay, macvlan
#### Раздел volumes
- drupal-data: название тома
- /srv/drupal-ant-blog/data: адрес в файловой системе хоста, куда будет монтироваться том.
- /srv/mysql/init.d:/docker-entrypoint-initdb.d: монтирование напрямую папки на хосте (1-ая позиция) в папку в контейнере (2-ая позиция).
В данном случае это специальная директория docker-entrypoint-initdb.d, в которой помещают скрипты инициализации БД. Они будут выполнены, если директория данных СУБД пуста. 
#### Выполнение произвольного скрипта при запуске контейнера.
