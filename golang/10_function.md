# Functions

Functions in Go are values, they are literally typed values, and that means that we can pass a function by its name anywhere we want in our program as long as type information is same, the function's signature.

## Panic

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