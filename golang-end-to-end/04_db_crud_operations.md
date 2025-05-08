# Generating DB models and CRUD operations in GO, by using SQLC go plugin

There are multiple plugins to connect postgres db from golang. Plugins like db/query, gorm, sqlx and sqlc

![stack_heap](images/04.drawio.png "icon")

We use sqlc from this repo: https://github.com/sqlc-dev/sqlc?tab=readme-ov-file

## sqlc installation

`brew install sqlc`

## Initialize sqlc, configure sqlc.yaml file with database/sql library

`database/sql`` is a plugin to connect to postgres DB


`sqlc init` -> generates sqlc.yaml file

Update the default sqlc.yaml file with below contents:

```
version: "2"
cloud:
    organization: ""
    project: ""
    hostname: ""
servers: []
sql:
  - engine: "postgresql"
    queries: "./db/query/" -> looks for the query file where we define all CRUD queries, so this plugin create corresponding crun functions in go along with transactions
    schema: "./db/migration/" -> looks for all the schema files where we define create table queries. So this plugin creates the corresponding Go structs.
    gen:
      go:
        package: "db" -> same package where we have migrations files
        out: "./db/sqlc" 
        sql_package: "database/sql"
overrides:
    go: null
plugins: []
rules: []
options: {}

```

## Create Account function

Add a new `account.sql` under `db/query` folder, where we also have migration files with below data

```
-- name: CreateAccount :one ---> It generates a go function named CreateAccount which returns created single account object along with transactions
INSERT INTO accounts (
  owner,
  balancer,
  currency
) VALUES (
  $1, $2, $3
)
RETURNING *; ---> Returns all columns after inserting an account into DB
```

Now run the command `sqlc generate` which will generates bunch of files under `db/sqlc` folder. Like a model file which contains the corresponding golang struct for the corresponding DB table. It also create the corresponding `CreateAccount` function in go for creating a new Account.   

## Get and List Account functions 

Add below data into `account.sql` file which generates the corresponding `get` and `list` functions
```
-- name: GetAccount :one ---> returns one account
SELECT * FROM accounts
WHERE id = $1 LIMIT 1;

-- name: ListAccounts :many ---> returns many account
SELECT * FROM accounts
ORDER BY id --> Order by ID
LIMIT $1 --> Number of rows to get in one pagination
OFFSET $2; --> to tell postgres to skip these many records before starting to return result
```

## Update Account function

```
-- name: UpdateAccount :exec --> Just update one row in DB and does not return anything
UPDATE accounts
set balance = $2
WHERE id = $1;
```

## Delete Account function

```
-- name: DeleteAccount :exec
DELETE FROM accounts
WHERE id = $1;
```