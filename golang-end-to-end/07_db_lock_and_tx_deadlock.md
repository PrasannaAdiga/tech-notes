# DB lock and transaction deadlock scenarions which needs to be avoided

Lets say we have a multiple transaction scenario through multiple goroutines, where we want to move money from one account to another account. 

One option is to get the account from DB, update it and then save it back. However the above one often done incorrectly without a proper locking mechanism

For example if we are running multiple go routines where each of them follows the above steps, then multiple get queries may result in old values before the update operation takes place.

That is why we need use the below SQL query(with begin and commit tx), so that all the get queries will be blocked until we commit
```
	BEGIN;
	SELECT * FROM accounts where id = 1 FOR update;
	COMMIT;
```
		
The above sql query also throws deadlock and hence we should use below one
```
	BEGIN;
	SELECT * FROM accounts where id = 1 FOR NO KEY update;
	COMMIT;
```

Also, instead of running 2 queries first to get the account by id and then add balance to that account by running update query, we can directly run update query by adding balance(AddAccountBalance function). This can eliminate the above mentioned deadlock issue.
```
-- name: AddAccountBalance :one
UPDATE accounts
set balance = balance + sqlc.arg(amount)
WHERE id = sqlc.arg(id)
RETURNING *;
```

Another place where deadlock might occur is the order of the update query. 

For example If one goroutine trying to transfer from account id 1 to 2 and another one is trying to tansfer from account id 2 to 1, then if we do the query like below, that will results in deadlock
```
	routine 1
		BEGIN transaction
		update account id 1 // holds the id 1 lock
		update account id 2 // needs id 2 lock
		COMMIT transaction
	routine 2
		BEGIN transaction
		update account id 2 // holds the id 2 lock
		update account id 1// needs id 1 lock
		COMMIT transaction
```

Intead we should have the order of the update like below

```
	routine 1
		BEGIN transaction
		update account id 1 // holds the id 1 lock
		update account id 2 // needs id 2 lock
		COMMIT transaction
	routine 2
		BEGIN transaction
		update account id 1 // waits for id 1 lock and gets it when the first routine commits
		update account id 2 // updtaes it since it will get the id 2 lock immediately
		COMMIT transaction
```
			