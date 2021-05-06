FROM mysql:8.0.23

ENV MYSQL_ROOT_PASSWORD=root
COPY init.sql /docker-entrypoint-initdb.d/
EXPOSE 3306