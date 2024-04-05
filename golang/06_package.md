# Packages

- Every package in Go must go into its own sub folder in the project. We can not not have different packages in the same folder.
- Every folder of the package must have the same name as the packge. So folder name and package name must be same, where the file name can be different.
- To import our own custom packages in other package, we must add full path which includes our module path. Also, we need to define function and variables in upper case in order to import them in other packages.
- If we want to import any external packages we can use the command `go get <full_path>`, which will add an entry in the `go.mod` file with `require` field. Then we need to run `go mod tidy`, which will generate `go.sum` file which has the `sha` commit of the corresponding package.

## fmt package in Go

### Functions in Go to send and receive data to and from terminal
- We use `fmt` package for reading or writting data to and from terminal
- To read we use `fmt.Print("Hello!")` and other related functionalities
- To write we use `fmt.Scan(&name)` and other realted functionalities. `Scan` function can not take multi-word input values like string.

### fmt.Printf
- fmt.Printf("Value of counter is: %d\n", counter)

### fmt.Sprintf
- counter := fmt.Sprintf("Value of counter is: %d\n", counter)
  fmt.Print(counter)

### Package example

**main package**

```
bank.go

package main

import (
	"fmt"

	"example.com/bank/fileops"
	"github.com/Pallinder/go-randomdata"
)

const accountBalanceFile = "balance.txt"

func main() {
	accountBalance, err := fileops.GetFloatFromFile(accountBalanceFile)
	if err != nil {
		fmt.Println("ERROR")
		fmt.Println(err)
		fmt.Println("--------------------------------")
		//panic("Can not continue, sorry!")
	}
	fmt.Println("Welcome to Go bank!")
	fmt.Println("Reach us 24/7", randomdata.PhoneNumber())
	for {
		presentOptions()
		var choice int
		fmt.Print("Please select any one option: ")
		fmt.Scan(&choice)
		fmt.Println("Your choice: ", choice)
		switch choice {
		case 1:
			fmt.Println("Account balance is: ", accountBalance)
		case 2:
			fmt.Print("Deposit amount? ")
			var depositAmount float64
			fmt.Scan(&depositAmount)
			if depositAmount <= 0 {
				fmt.Println("Invalid amount! Must be greater than zero")
				continue
			}
			accountBalance += depositAmount
			fmt.Println("Balance updated! New amount is:", accountBalance)
			fileops.WriteFloatToFile(accountBalance, accountBalanceFile)
		case 3:
			fmt.Print("Withdraw amount? ")
			var withdrawAmount float64
			fmt.Scan(&withdrawAmount)
			if withdrawAmount <= 0 {
				fmt.Println("Invalid amount! Must be greater than zero")
				continue
			}
			if withdrawAmount > accountBalance {
				fmt.Println("Invalid amount! You can not withdraw more than you have.")
				continue
			}
			accountBalance -= withdrawAmount
			fmt.Println("Balance updated! New amount is:", accountBalance)
			fileops.WriteFloatToFile(accountBalance, accountBalanceFile)
		default:
			fmt.Println("Goodbye!")
			fmt.Println("Thanks for using bank App!")
			return
		}
	}
}

=========================================================================================

communication.go

package main

import "fmt"

func presentOptions() {
	fmt.Println("What do you want to do?")
	fmt.Println("1. Check balance")
	fmt.Println("2. Deposit money")
	fmt.Println("3. Withdraw money")
	fmt.Println("4. Exit")

}

```

**package fileops**


```
file fileops.go under fileops folder

package fileops

import (
	"errors"
	"fmt"
	"os"
	"strconv"
)

func GetFloatFromFile(fineName string) (float64, error) {
	data, err := os.ReadFile(fineName)
	if err != nil { // nil means absence of any value
		return 1000, errors.New("failed to find file")
	}
	valueText := string(data)
	value, err := strconv.ParseFloat(valueText, 64)
	if err != nil {
		return 1000, errors.New("failed to parse stored value")
	}
	return value, nil
}

func WriteFloatToFile(value float64, fileName string) {
	valueText := fmt.Sprint(value) // One way to convert float to string
	os.WriteFile(fileName, []byte(valueText), 0644)
}
```