# Writing unit tests for database CRUD operations with random data

In Golang, we write the test files in the same folder where the code exists with extension `_test.go`

Every unit test in Go must start with `Test` prefix. 

### TestMain function

`TestMain` is the special function which takes `*testing.M` as an argument. This is the main entry point of all unit tests inside one specific golang package, and is called only one time to initialize all the needed object like below:

```
package db

import (
	"database/sql"
	"log"
	"os"
	"testing"

	_ "github.com/lib/pq"
)
const (
	dbDriver = "postgres"
	dbSource = "postgresql://root:password@localhost:5432/simple_bank?sslmode=disable"
)
var testQueries *Queries

// Main entry function for all the tests inside a package
// i.e db package here
func TestMain(m *testing.M) {
	conn, err := sql.Open(dbDriver, dbSource)
	if err != nil {
		log.Fatal("cannot connect to db: ", err)
	}
	testQueries = New(conn)
	os.Exit(m.Run())
}
```

Since `database/sql` package just provides the generic interface around seequel database, it needs to be used in conjuction with database driver, in order to talk to specific database engine.  

Here we are using `lib/pq` driver of postgres and importing it through `_ "github.com/lib/pq"` without calling any of its function.

### Normal Unit test function

We use `github.com/stretchr/testify/require` package for testing the test results.

```
import (
	"context"
	"database/sql"
	"testing"
	"time"

	"github.com/PrasannaAdiga/go-simplebank/util"
	"github.com/stretchr/testify/require"
)

func createRandomAccount(t *testing.T) Account {
	arg := CreateAccountParams{
		Owner:    util.RandomOwner(),
		Balance:  util.RandomMoney(),
		Currency: util.RandomCurrency(),
	}

	acc, err := testQueries.CreateAccount(context.Background(), arg)
	require.NoError(t, err)
	require.NotEmpty(t, acc)

	require.Equal(t, arg.Owner, acc.Owner)
	require.Equal(t, arg.Balance, acc.Balance)
	require.Equal(t, arg.Currency, acc.Currency)

	require.NotZero(t, acc.ID)
	require.NotZero(t, acc.CreatedAt)

	return acc
}
```
