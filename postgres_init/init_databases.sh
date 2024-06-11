#/bin/bash
set -e

psql --username postgres --dbname postgres <<-EOSQL
  CREATE DATABASE source;
  CREATE ROLE source WITH ENCRYPTED PASSWORD 'source' LOGIN;
  GRANT ALL PRIVILEGES ON DATABASE source TO source;

  CREATE DATABASE dwh;
  CREATE ROLE dwh WITH ENCRYPTED PASSWORD 'dwh' LOGIN;
  GRANT ALL PRIVILEGES ON DATABASE dwh TO dwh;

  CREATE DATABASE api;
  CREATE ROLE api WITH ENCRYPTED PASSWORD 'api' LOGIN;
  GRANT ALL PRIVILEGES ON DATABASE api TO api;
EOSQL

psql --username postgres --dbname source <<-EOSQL
  GRANT ALL ON SCHEMA public TO source;
EOSQL

psql --username postgres --dbname dwh <<-EOSQL
  GRANT ALL ON SCHEMA public TO dwh;
EOSQL

psql --username postgres --dbname api <<-EOSQL
  GRANT ALL ON SCHEMA public TO api;
EOSQL

psql --username source --dbname source <<-EOSQL
  \i /scripts/init-source-tables.sql
EOSQL
