# Control Structure

- Go has conditional statements like `if, else if and else`. It also provides `switch` case.
- Go has looping statement like `for`. Go does not have `while` loop like other languages.
- We can use `continue` statement in for loop to skip the current iteration and continue to the next one
- Also we can use `break` statement in for loop to stop the for loop
- Go also has `conditional for loop` which will run some code blocks as long as the condition valuates to `true`
```
    for someCondition {
    // do something ...
    }
```
- We can use either if/else if/else code block inside for loop or switch case. We can use `continue` sattements inside if/else if/else or switch case to continue the for loop to next iteration. But we can not use `break` statement in switch case to stop the current iteration of for loop, insated we have to use `return` statement. But the same `break` statement we can use in if/else if/else blocks
- In `switch` cases we do not need `break` keyword to stop each case like in other languages. Also, the break sattement in switch case just stops that particular case, not any of the outer loop.
- Example code
```
func main() {
	accountBalance := 1000.0
	fmt.Println("Welcome to Go bank!")
	for {
		fmt.Println("What do you want to do?")
		fmt.Println("1. Check balance")
		fmt.Println("2. Deposit money")
		fmt.Println("3. Withdraw money")
		fmt.Println("4. Exit")

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
		default:
			fmt.Println("Goodbye!")
			return
		}
		===============================================
		 (OR WE CAN USE if/else if/else block as below) 
		===============================================
		if choice == 1 {
			fmt.Println("Account balance is: ", accountBalance)
		} else if choice == 2 {
			fmt.Print("Deposit amount? ")
			var depositAmount float64
			fmt.Scan(&depositAmount)
			if depositAmount <= 0 {
				fmt.Println("Invalid amount! Must be greater than zero")
				continue
			}
			accountBalance += depositAmount
			fmt.Println("Balance updated! New amount is:", accountBalance)
		} else if choice == 3 {
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
		} else {
			fmt.Println("Goodbye!")
			// return // This will stops the for loop and thus the main function, so this will not allow any function after this for loop
			break // This will breaks the for loop so it will allow any code after this loop.
		}
	}
```

# Reading and Writing to files

In the above example code, instead of saving accountBalance in memory, we can save and read it from file as shown below:

```
    const accountBalanceFile = "balance.txt"

    func getBalanceFromFile() (float64, error) {
        data, err := os.ReadFile(accountBalanceFile)
        if err != nil { // nil means absence of any value
            return 1000, errors.New("failed to find balance file")
        }
        balanceText := string(data)
        balance, err := strconv.ParseFloat(balanceText, 64)
        if err != nil {
            return 1000, errors.New("failed to parse stored balance value")
        }
        return balance, nil
    }

    func writeToFile(balance float64) {
        balanceText := fmt.Sprint(balance) // One way to convert float to string
        os.WriteFile(accountBalanceFile, []byte(balanceText), 0644)
    }

    func main() {
        accountBalance, err := getBalanceFromFile()
        if err != nil {
            fmt.Println("ERROR")
            fmt.Println(err)
            fmt.Println("--------------------------------")
            panic("Can not continue, sorry!")
        }
        fmt.Println("Welcome to Go bank!")
        for {
            fmt.Println("What do you want to do?")
            fmt.Println("1. Check balance")
            fmt.Println("2. Deposit money")
            fmt.Println("3. Withdraw money")
            fmt.Println("4. Exit")

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
                writeToFile(accountBalance)
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
                writeToFile(accountBalance)
            default:
                fmt.Println("Goodbye!")
                return
            }
        }    
    }

```

## Reading multiple words from terminal
The scan or scanln function does not work if we type multiple words in the terminal. For that we need to use the below approach

```
func main() {
	title := getUserInput("Note title:")
	content := getUserInput("Note content:")
	fmt.Println(title)
	fmt.Println(content)
}

func getUserInput(prompt string) string {
	fmt.Printf("%v ", prompt)
	reader := bufio.NewReader(os.Stdin)
	text, err := reader.ReadString('\n')
	if err != nil {
		return ""
	}
	text = strings.TrimSuffix(text, "\n")
	text = strings.TrimSuffix(text, "\r")
	return text
}
```