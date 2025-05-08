# DB migration support in Golang

We can use the golang-migrate library for this https://github.com/golang-migrate/migrate

It can works with many different databases

## Installation through CLI

`brew install golang-migrate`

### Create first migration file to initialize simplebank database schema

`migrate create -ext sql -dir db/migration -seq init_schema`

This will create 2 files, one is `up` and other one is `down`.  Up script is to make forward change to the schema and the down script is to revert the change made by up script.

So when we run `migrate up` command, the up script files inside the `db/migration` folder will be run seequentially by the order of their prefix version. Same way when we run `migrate down` command, the down scripts will be run in the reverse order of their prefix.

```
 ~/g/src/go-simplebank    main  migrate create -ext sql -dir db/migration -seq init_schema 
/Users/prasanna/go/src/go-simplebank/db/migration/000001_init_schema.up.sql
/Users/prasanna/go/src/go-simplebank/db/migration/000001_init_schema.down.sql
 ~/g/s/go-simplebank
```

Copy the content of previously generated postgres sql file into `000001_init_schema.up.sql` file

In the `000001_init_schema.down.sql` file, we should revert the changes made by up script.
```
DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS transfers;
DROP TABLE IF EXISTS accounts; 
```

### Create a new postgres DB for simplbank

- Login to postgres container through `docker exec -it postgres16 /bin/sh`
- Inside the postgres container shell, it provides some CLI commands to interact with postgres server directly. With these commands we can create a new DB.
```
createdb --username=root owner=root simple_bank
```
username = connecting as a root user, owner= the db we are going to create is belongs to root user.

- Connect to this DB through psql command

```
/ # createdb --username=root --owner=root simple_bank
/ #
/ #
/ #
/ # psql simple_bank
psql (16.4)
Type "help" for help.

simple_bank=#
```
- We can also delete the db through `dropdb simple_bank`

- Form outside of container we can directly create a new DB through the command `docker exec -it postgres16 createdb --username=root --owner=root simple_bank`
- Access the database console, without going through container shell `docker exec -it postgres16 psql -U root simple_bank`

### Create a Makefile

With make file we can create a task for up and running postgres container, create or drop a new DB inside of it like below:

```
postgres:
	docker run --name postgres16 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:16-alpine

createdb:
	docker exec -it postgres16 createdb --username=root --owner=root simple_bank

dropdb: 
	docker exec -it postgres16 dropdb simple_bank

migrateup:
  migrate -path db/migration -database "postgresql://root:password@localhost:5432/simple_bank?sslmode=disable" -verbose up

migratedown:
  migrate -path db/migration -database "postgresql://root:password@localhost:5432/simple_bank?sslmode=disable" -verbose down

.PHONY: postgres createdb dropdb migrateup migratedown
```

Below are the such commands:
- make postgres // Run postgres container from postgres image
- make createdb // creates simple_bank db in postgress
- make dropdb // drops the simple_bank db from postgress
- make migrateup // Creates all the tables in simple_bank as per the migrate file
- make migratedown // Drops all the previously ran sql scripts in simple_bank

### Run migration db against simplebank database through migration script

`migrate -path db/migration -database "postgresql://root:password@localhost:5432/simple_bank?sslmode=disable" -verbose up` 

```
migrate -path db/migration -database "postgresql://root:password@localhost:5432/simple_bank?sslmode=disable" -verbose up
2024/09/05 21:40:24 Start buffering 1/u init_schema
2024/09/05 21:40:24 Read and execute 1/u init_schema
2024/09/05 21:40:24 Finished 1/u init_schema (read 7.952958ms, ran 31.864875ms)
2024/09/05 21:40:24 Finished after 46.250375ms
2024/09/05 21:40:24 Closing source and database
```

This will run the sql queries written in `000001_init_schema.up.sql` file and also create `schema_migrations` table with version value as `1` and `dirty` value as `False`

