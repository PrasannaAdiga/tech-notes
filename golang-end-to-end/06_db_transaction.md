# Data Base Transaction

A DB transaction is a single unit of work, Often made up of multiple db operations.

### Example

Transfer 10 USD from bank account 1 to bank account 2

**Steps**
1. Create a transfer record with amount = 10
2. Create an account entry for account 1 with amount = -10
3. Create an account entry for account 2 with amount= +10
4. Subtract 10 from the balance of account 1
5.  Add 10 to the balance of account 2


### Why do we need db transaction?
1. To provide a reliable and consistent unit of work, even in case of system failure
2. To provide isolation between programs that accessthedatabase concurrently

## How to run SQL transactions

Create a go file which embed existing Queries extends its with transaction functionality. It provides an `execTx` method which will accept any function and wrap it aroung transaction `begin`, `rollback` and `commit`

```
package db

import (
	"context"
	"database/sql"
	"fmt"
)

// Store provides all functions to execute db queries and transactions
// It extentds functionality of Queries by composing it
// And provides transactions functionalities
type Stroe struct {
	*Queries
	db *sql.DB
}

func NewStore(db *sql.DB) *Stroe {
	return &Stroe{
		db:      db,
		Queries: New(db), // here we are passing *sql.Db
	}
}

// ExecTx executes a function within a database transaction
func (s *Stroe) execTx(ctx context.Context, fn func(*Queries) error) error {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}

	q := New(tx) // here we are passing *sql.Tx

	err = fn(q) // call the function

	if err != nil {
		if rbErr := tx.Rollback(); rbErr != nil {
			return fmt.Errorf("tx err: %v, rb err: %v", err, rbErr)
		}
		return err
	}

	return tx.Commit()
}

// TransferTx performs a money transfer from one account to the other.
// It performs  the below steps
// 1. create the transfer (in transfer table)
// 2. add an account entries (for both from and to in entries table)
// 3. update accounts' balance  (for both from and to in accounts table)
// within a database transaction
func (s *Stroe) TransferTx(ctx context.Context, arg TransferTxParams) (TransferTxResult, error) {
	var result TransferTxResult

	err := s.execTx(ctx, func(q *Queries) error {
		var err error

		result.Transfer, err = q.CreateTransfer(ctx, CreateTransferParams{
			FromAccountID: arg.FromAccountID,
			ToAccountID:   arg.ToAccountID,
			Amount:        arg.Amount,
		})
		if err != nil {
			return err
		}

		result.FromEntry, err = q.CreateEntry(ctx, CreateEntryParams{
			AccountID: arg.FromAccountID,
			Amount:    -arg.Amount,
		})
		if err != nil {
			return err
		}

		result.ToEntry, err = q.CreateEntry(ctx, CreateEntryParams{
			AccountID: arg.ToAccountID,
			Amount:    arg.Amount,
		})
		if err != nil {
			return err
		}

		//TODO: Update account's balance

		return err
	})

	return result, err
}

// TransferTxParams contains the input parameters of the transfer transaction
type TransferTxParams struct {
	FromAccountID int64 `json:"from_account_id"`
	ToAccountID   int64 `json:"to_account_id"`
	Amount        int64 `json:"amount"`
}

// TransferTxResult is the result of the transfer transaction
type TransferTxResult struct {
	Transfer    Transfer `json:"transfer"`
	FromAccount Account  `json:"from_account"`
	ToAccount   Account  `json:"to_account"`
	FromEntry   Entry    `json:"from_entry"`
	ToEntry     Entry    `json:"to_entry"`
}


```

