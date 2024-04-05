# Functions

Functions in Go are values, they are literally typed values, and that means that we can pass a function by its name anywhere we want in our program as long as type information is same, the function's signature.

- A function can takes any number of arguments and it can return any number of values.
- Any variables or constants defined in a function, are scoped to that function and only available only in that function. We can also define variable and constant outside of any function so it will be available all the function of that file or package.

## Main function in Go
- There should be one `main` package which must have one `main` function, which is called by default by go runtime. This will be the entry point of Go runtime.
- The file name of this `main` package which has `main` function can be anything
- During development, we can have this atleast one `main` package with one `main` function and then we can execute it by `go run main.go`
- But in order to distribute our go application, we need to create an executable file. But to create an executable, we must have a go module, which is a collection of multiple packages or the go project which we are workin gon. We can create a module through `go mod init example.com/first-app`.
- This `go.mod` file has a `module` name and `go` version
- Once we have this go.mod and a single `main.go` file which has `main` package and a `main` function, we can create an executable through `go build` command. And then we can run this executable depending on the OS without need for the installation of Go.
- Also we can run this `main` function just by `go run .` without specifying function name, if we define a module.
- We can not have multiple `main` functin in a `main` package. There should be only one.
- But if we are building any third party utility function, not an application, then we no need to have this main package and function. Because these utility functions are not intended to run as a program, instead we just import it into a another application or go module, so that we can use its functions. 
- So only programs which needs to be executed needs this main package and function.

## Function example:
```
    func main() {
        fmt.Println("Hello user, please enter below values!")
        a := getUserInput("Enter A: ")
        b := getUserInput("Enter B: ")
        c := getUserInput("Enter C: ")
        res, err := calculateSum(a, b, c)
        if err != nil {
            fmt.Printf("Found an error: %s", err)
            return
        }
        fmt.Println("Result: ", res)
    }
    func getUserInput(text string) float64 {
        var a float64
        fmt.Print(text)
        fmt.Scan(&a)
        return a
    }
    func calculateSum(a, b, c float64) (float64, error) {
        var res float64
        var err error
        if a == 0 || b == 0 || c == 0 {
            return res, errors.New("please provide a non zero value")
        }
        res = a + b + c
        return res, err
    }
```
- A function can also return named values 
```
    func add(a int, b int) (res int, err error) {
        if (a == 0 || b == 0) {
            return res, errors.New("Failed")
        }
        res = a + b
        return
    }
```

## Passing function as parameter and custom function type

```
package main

import "fmt"

type transformFun func(int) int // It is a custom function type
// Use it whenver we have a lengthy function definition

func main() {
	numbers := []int{1, 2, 3, 4}
	//doubled := doubleNumbers(&numbers)
	doubled := transformNumbers(&numbers, double)
	trippled := transformNumbers(&numbers, triple)
	fmt.Println(doubled)
	fmt.Println(trippled)
}

// func doubleNumbers(numbers *[]int) []int {
// 	dNumbers := []int{}

// 	for _, val := range *numbers {
// 		dNumbers = append(dNumbers, double(val))
// 	}

// 	return dNumbers
// }

// Pass function as parameter values
func transformNumbers(numbers *[]int, transform transformFun) []int {
	dNumbers := []int{}

	for _, val := range *numbers {
		dNumbers = append(dNumbers, transform(val))
	}

	return dNumbers
}

func double(num int) int {
	return num * 2
}

func triple(num int) int {
	return num * 3
}

O/P:
[2 4 6 8]
[3 6 9 12]
```

## Return function as value
In the above example we can write another function like below which can return a function as value

```
// returning function as value
func getTransformerFunction(numbers *[]int) transformFun {
	if (*numbers)[0] == 1 {
		return double
	} else {
		return triple
	}
}
```

## Anonymous function

A function without any name. 
```
package main

import "fmt"

func main() {
	numbers := []int{1, 2, 3}

	transformed := transformNumbers(&numbers, func(number int) int { // This is an anonymous function without a name
		return number * 2
	})

	fmt.Println(transformed)
}

func transformNumbers(numbers *[]int, transform func(int) int) []int {
	dNumbers := []int{}

	for _, val := range *numbers {
		dNumbers = append(dNumbers, transform(val))
	}

	return dNumbers
}

```

## Clousre

```
package main

import "fmt"

func main() {
	numbers := []int{1, 2, 3}

	double := createTransformer(2)
	triple := createTransformer(3)

	transformed := transformNumbers(&numbers, func(number int) int {
		return number * 2
	})

	doubled := transformNumbers(&numbers, double)
	tripled := transformNumbers(&numbers, triple)

	fmt.Println(transformed)
	fmt.Println(doubled)
	fmt.Println(tripled)
}

func transformNumbers(numbers *[]int, transform func(int) int) []int {
	dNumbers := []int{}

	for _, val := range *numbers {
		dNumbers = append(dNumbers, transform(val))
	}

	return dNumbers
}

func createTransformer(factor int) func(int) int {
	// This inner function forms a closure
	// Which can remember its our lexical scope value
	// Which is factor
	return func(number int) int {
		return number * factor
	}
}
```

## Variadic function

```
package main

import "fmt"

func main() {
	numbers := []int{1, 10, 15}
	sum := sumup(1, 10, 15, 40, -5)
	anotherSum := sumup(1, numbers...) // This will take out all numbers and send

	fmt.Println(sum)
	fmt.Println(anotherSum)
}

// This function can take any number of integer values as a last parameter which is used as a collection
// First value will be assigned to startingValue
// Rest of the values will be assigned to numbers
func sumup(startingValue int, numbers ...int) int {
	sum := 0

	for _, val := range numbers {
		sum += val // sum = sum + val
	}

	return sum
}
```

## Panic
In Go error does not crash applications like in other languages where we need to wrap block of code inside try and catch block to handle errors and continue the program. 

But sometime we can not continue execution of programming, if some type of errors occured. In those cases we can stop execution with `return` statement which will immediately stops the current executing function.

Another way is to use `panic` statement wherever we want to stop the execution, which will crash the entire application.

Function can through a user defined panic or go runtime panic, which tells that the execution environemnt is unstable now. That means the function can no longer can execute because of some reason. So Go will immediately destroys this function and it returns the execution back to the function caller.

If the caller function does not have any way to recover from this panic, Go will destroy that function too up until the main function.

## Recover
If we have a way to recover from any panic, or we know how to restore the program to a stable execution environment, then we can use the recovery mechanism. Recovery mechanism works with `defer` function, where we can have our recovery mechanism in a differed function, so when a panic occurs this defered function will be called and which will takes the execution environment back to stable so that the caller function can continue. 

```
func main() {
    fmt.Println("main 1")
    func1()
    fmt.Println("main 1")

}
 
func func1() {
    fmt.Println("main 1")
    defer func() {
        fmt.Println(recover())
    }()
    panic("Panic triggered")
    fmt.Println("main 1")
} 
 ```

