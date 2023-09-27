# Error Handling
https://github.com/ardanlabs/gotraining/tree/master/topics/go/design/error_handling

Error handling is critical for making your programs reliable, trustworthy and respectful to those who depend on them. A proper error value is both specific and informative. It must allow the caller to make an informed decision about the error that has occurred. There are several ways in Go to create error values. This depends on the amount of context that needs to be provided.

Failure is always what we are coding against and error handling is everything. It is not about the execption handling, because exception handling hides context around errors. This is about looking at an error, when its happeninand Go errors are just values and they can be anything you need them to be.

Error handling is about showing respect to the user of your API, giving your user enough context to make an informed decision about the state of the application and giving them enough information to be able to either recover or make a decision to shut down.

There's two ways to shut down an application in Go. You can go to OS, the OS package, dot exit, and you can set a return code on that, that's the fastest way, or you can call the built in function panic. Now you'll choose one over the other depending on if you need a stack trace or not. So if you need the stack trace you're gonna call panic, if you don't you just call OS exit. But we've gotta design APIs and errors around the idea of giving the user enough context to make an informed decision.

- Use the default error value for static and simple formatted messages.
- Create and return error variables to help the caller identify specific errors.
- Create custom error types when the context of the error is more complex.
- Error Values in Go aren't special, they are just values like any other, and so you have the entire language at your disposal.
- Errors are values in Go, just like any other return value from a function. In Go we dont generally consider errors as exceptional events. 

**Ways to create an Error in Go**:
```
func main() {
	err := errors.New("this is an error")

	err2 := fmt.Errorf("this error wraps the first one: %w", err)
	fmt.Println(err2)
}
```

## Default Error Values
```
// Sample program to show how the default error type is implemented.
package main

import "fmt"

// http://golang.org/pkg/builtin/#error
type error interface {
	Error() string
}

// http://golang.org/src/pkg/errors/errors.go
type errorString struct {
	s string
}

// http://golang.org/src/pkg/errors/errors.go
func (e *errorString) Error() string {
	return e.s
}

// http://golang.org/src/pkg/errors/errors.go
// New returns an error that formats as the given text.
func New(text string) error {
	return &errorString{text}
}

func main() {
	if err := webCall(); err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Life is good")
}

// webCall performs a web operation.
func webCall() error {
	return New("Bad Request")
}

O/P:
Bad Request
```

When we call the New() function, we are getting back the error interface value, it has a pointer to an errorString and a pointer to the string `text`. 

**Nil Value**: Nil is always the zero value for either the pointers or for the reference types.

People liked the idea of exception handling because the idea was the try code had your happy path and your catch took care of all the negative path and you separated this for code readability. I get it, but I can't tell you how many times when I landed in the catch, I was lost, because the context of how I got there is lost. Was it this call, was it that call? And I used to spend too much time trying to figure out how I got inside of a catch, it doesn't work.

But you can still have this concept of happy path if you follow this basic design principle when writing code in Go. Use the if statement to handle your negative path logic and keep your path, your positive path logic on a straight line of sight. If this call to webCall succeeds, then I just move down the function to the next call.


## Error Variables
We use error variables, when a function returns more than one error.
```
// Sample program to show how to use error variables to help the
// caller determine the exact error being returned.
package main

import (
	"errors"
	"fmt"
)

var (
	// ErrBadRequest is returned when there are problems with the request.
	ErrBadRequest = errors.New("Bad Request")

	// ErrPageMoved is returned when a 301/302 is returned.
	ErrPageMoved = errors.New("Page Moved")
)

func main() {
	if err := webCall(true); err != nil {
		switch err {
		case ErrBadRequest:
			fmt.Println("Bad Request Occurred")
			return

		case ErrPageMoved:
			fmt.Println("The Page moved")
			return

		default:
			fmt.Println(err)
			return
		}
	}

	fmt.Println("Life is good")
}

// webCall performs a web operation.
func webCall(b bool) error {
	if b {
		return ErrBadRequest
	}

	return ErrPageMoved
}
```

In the baove code, we declared 2 error variables(global variables at the package level) ErrBadRequest and ErrPageMoved. And the function webCall returns anyone of these depending on value. 

Use the error string type and variables first untill we no longer get enough context from it. Else, we can go ahead and create our own custom error types. 

## Custom Error Types

### Type as Context
Think about networking issue, there are so many problems can happen on the network. So an error variable is not gonna be enough to say there was a network issue. We need to have more details about that network issue. 
```
// Sample program to show how to implement a custom error type
// based on the json package in the standard library.
package main

import (
	"fmt"
	"reflect"
)

// An UnmarshalTypeError describes a JSON value that was
// not appropriate for a value of a specific Go type.
type UnmarshalTypeError struct {
	Value string       // description of JSON value
	Type  reflect.Type // type of Go value it could not be assigned to
}

// Error implements the error interface.
func (e *UnmarshalTypeError) Error() string {
	return "json: cannot unmarshal " + e.Value + " into Go value of type " + e.Type.String()
}

// An InvalidUnmarshalError describes an invalid argument passed to Unmarshal.
// (The argument to Unmarshal must be a non-nil pointer.)
type InvalidUnmarshalError struct {
	Type reflect.Type
}

// Error implements the error interface.
func (e *InvalidUnmarshalError) Error() string {
	if e.Type == nil {
		return "json: Unmarshal(nil)"
	}

	if e.Type.Kind() != reflect.Ptr {
		return "json: Unmarshal(non-pointer " + e.Type.String() + ")"
	}
	return "json: Unmarshal(nil " + e.Type.String() + ")"
}

// user is a type for use in the Unmarshal call.
type user struct {
	Name int
}

func main() {
	var u user
	err := Unmarshal([]byte(`{"name":"bill"}`), u) // Run with a value and pointer.
	if err != nil {
		switch e := err.(type) {
		case *UnmarshalTypeError:
			fmt.Printf("UnmarshalTypeError: Value[%s] Type[%v]\n", e.Value, e.Type)
		case *InvalidUnmarshalError:
			fmt.Printf("InvalidUnmarshalError: Type[%v]\n", e.Type)
		default:
			fmt.Println(err)
		}
		return
	}

	fmt.Println("Name:", u.Name)
}

// Unmarshal simulates an unmarshal call that always fails.
func Unmarshal(data []byte, v interface{}) error {
	rv := reflect.ValueOf(v)
	// If rv is not a pointer or rv is Nil
	if rv.Kind() != reflect.Ptr || rv.IsNil() {
		return &InvalidUnmarshalError{reflect.TypeOf(v)}
	}

	return &UnmarshalTypeError{"string", reflect.TypeOf(v)}
}

O/P:
InvalidUnmarshalError: Type[main.user]
```

In the above code the type assertion `err.(type)` letting us do is type as context. What its saying is. type assert, what is inside of the error interface value? 

### Behavior as context

```
// Package example4 provides code to show how to implement behavior as context.
package example4

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net"
)

// client represents a single connection in the room.
type client struct {
	name   string
	reader *bufio.Reader
}

// TypeAsContext shows how to check multiple types of possible custom error
// types that can be returned from the net package.
func (c *client) TypeAsContext() {
	for {
		line, err := c.reader.ReadString('\n')
		if err != nil {
			switch e := err.(type) {
			case *net.OpError:
				if !e.Temporary() {
					log.Println("Temporary: Client leaving chat")
					return
				}

			case *net.AddrError:
				if !e.Temporary() {
					log.Println("Temporary: Client leaving chat")
					return
				}

			case *net.DNSConfigError:
				if !e.Temporary() {
					log.Println("Temporary: Client leaving chat")
					return
				}

			default:
				if err == io.EOF {
					log.Println("EOF: Client leaving chat")
					return
				}

				log.Println("read-routine", err)
			}
		}

		fmt.Println(line)
	}
}

// temporary is declared to test for the existence of the method coming
// from the net package.
type temporary interface {
	Temporary() bool
}

// BehaviorAsContext shows how to check for the behavior of an interface
// that can be returned from the net package.
func (c *client) BehaviorAsContext() {
	for {
		line, err := c.reader.ReadString('\n')
		if err != nil {
			switch e := err.(type) {
			case temporary:
				if !e.Temporary() {
					log.Println("Temporary: Client leaving chat")
					return
				}

			default:
				if err == io.EOF {
					log.Println("EOF: Client leaving chat")
					return
				}

				log.Println("read-routine", err)
			}
		}

		fmt.Println(line)
	}
}
```

In the above code instead of asking for what is the concete data inside of err, does that concrete data also implement our temporary interface. So error value not only can have a state but it can also have behaviors. 
And we can check against its data value or behavior.

## Errors vs Panics
- Errors result of an operation. Panic alters control flow, where the running function terminates immediately and the caller goes back to calling function.
- Errors are easy to discover. Panics are relies on docs and reading code.
- Errors implies that things didnt go as per the plan. Panic implies that program is in unstable state.
- Errors are used freequently whre as Panics are used rarely. 

## Error Handling Examples:

- Default Error Values: https://go.dev/play/p/beGEdO2QE4g
- Error Variables: https://go.dev/play/p/JQUJbS20MrE
- Type As Context: https://go.dev/play/p/BmiblC2Q7MC
- Behavior As Context: https://go.dev/play/p/sNRSXKtcJKM
- Find The Bug: https://go.dev/play/p/CBL-ADH-nSv | The Reason: https://go.dev/play/p/-f4PPcBGkDU
- Wrapping Errors With pkg/errors: https://go.dev/play/p/Zt1Z5k4HbDG
- Wrapping Errors With stdlib: https://go.dev/play/p/f5bw9G7OLog

