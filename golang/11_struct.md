# Struct Type (user defined type)
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/struct_types

Struct types are a way of creating complex types that group fields of data together. 
- We can use the struct literal form to initialize a value from a struct type.
- The dot (.) operator allows us to access individual field values.
- We can create anonymous structs.
- Structs are copied by value hence it can be comparable with other struct.

```
package main

import "fmt"

// example represents a type with different fields.
type example struct {
	flag    bool
	counter int16
	pi      float32
}

func main() {
	// Declare a variable of type example set to its
	// zero value.
	var e1 example

	// Display the value.
	fmt.Printf("%+v\n", e1)

	// Declare a variable of type example and init using
	// a struct literal.
	e2 := example{
		flag:    true,
		counter: 10,
		pi:      3.141592,
	}

	// Display the field values.
	fmt.Println("Flag", e2.flag)
	fmt.Println("Counter", e2.counter)
	fmt.Println("Pi", e2.pi)
}

O/P
---
{flag:false counter:0 pi:0}
Flag true
Counter 10
Pi 3.141592
```

In the above code we have created a variable `e` with zero value and constructed a variable `e2` with some value by using **struct literal construction**.

We can also create struct for an inbuilt types like string, int, bool etc and add our own custom methods to it

```
type str string

func (s str) log() {
	fmt.Println(s)
}

func main() {
	var name str
	name = "Prasanna"
	name.log()
}

```

## Empty struct

We can also have an empty literal construction 'example{}' to create zero value struct which mainly used when we do not have the need to assign it to a variable, returning from a function or while passing it as a parameter to a function.

```
// example represents a type with different fields.
type example struct {
	flag    bool
	counter int16
	pi      float32
}

func main() {
	// Declare a variable of type example set to its
	// zero value.
	var e1 example

	e1 = example{}

	// Display the field values.
	fmt.Println("Flag", e1.flag)
	fmt.Println("Counter", e1.counter)
	fmt.Println("Pi", e1.pi)
}
O/P:
False
0
0.0
```

## Constructor function

We can use constructor function to create a value of struct. So that we can call this constructor function as many times as we want and from anywhere in the program. Also, it is better to return pointer of the created value from this construction function.

We can also do validations in constructor functions before creating any value.

We usually name constructor function as just `New` since we usually create a struct in its own package and import it in other places. So we can call constructor function like for example `user.New()`

```
type user struct {
	firstName string
	lastName  string
	birthDate string
	createdAt time.Time
}

func newUser(firstName string, lastName string, birthDate string) *user {
	return &user{
		firstName: firstName,
		lastName:  lastName,
		birthDate: birthDate,
		createdAt: time.Now(),
	}
}

func main() {
	userFirstName := getUserData("Please enter your first name: ")
	userLastName := getUserData("Please enter your last name: ")
	userBirthDate := getUserData("Please enter your birthdate (MM/DD/YYYY): ")

	appUser := newUser(userFirstName, userLastName, userBirthDate)

	fmt.Println(appUser.firstName)
}

func getUserData(data string) string {
	var userData string
	fmt.Print(data)
	fmt.Scan(&userData)
	return userData
}
```

## Anonymous Struct
```
package main

import "fmt"

func main() {

	// Declare a variable of an anonymous type set
	// to its zero value.
	var e1 struct {
		flag    bool
		counter int16
		pi      float32
	}

	// Display the value.
	fmt.Printf("%+v\n", e1)

	// Declare a variable of an anonymous type and init
	// using a struct literal.
	e2 := struct {
		flag    bool
		counter int16
		pi      float32
	}{
		flag:    true,
		counter: 10,
		pi:      3.141592,
	}

	// Display the values.
	fmt.Printf("%+v\n", e2)
	fmt.Println("Flag", e2.flag)
	fmt.Println("Counter", e2.counter)
	fmt.Println("Pi", e2.pi)
}

O/P
{flag:false counter:0 pi:0}
{flag:true counter:10 pi:3.141592}
Flag true
Counter 10
Pi 3.141592
```

## Implicit Conversion
Go does not provide any implicit conversion from one type to another.

```
type A struct {
    flag    bool
	counter int16
	pi      float32
}

type B struct {
    flag    bool
	counter int16
	pi      float32
}

var a A
var b B
b = a
fmt.Println(a, b)

O/P
Compilation error
```

But if we need such conversion, then we have to do explicit conversion by using conversion syntax

```
b = (B)a
fmt.Println(a, b)
O/P
No compilation error
```

**Note**: When the type is named, there is going to be no implicit conversion. But when the type is literal typed(unnamed) then Go will do the implicit conversion.
```
var b B
a := struct {
		flag    bool
		counter int16
		pi      float32
	}{
		flag:    true,
		counter: 10,
		pi:      3.141592,
	}
b = a
O/P
No compilation error    
```

## Struct Embedding

Build a new struct that builds upon an existing structs. Go/Structs does not have classes or inheritances. So we use Embedding to have all the fields and methods of an existing struct along with its own fields or methods.

```
type User struct {
	firstName string
	lastName  string
	birthDate string
	createdAt time.Time
}

type Admin struct {
	email    string
	password string
	User
}

func NewAdmin(email string, password string) *Admin {
	return &Admin{
		email:    email,
		password: password,
		User: User{
			firstName: "ADMIN",
			lastName:  "ADMIN",
			birthDate: "---",
			createdAt: time.Now(),
		},
	}
}

adminUser := user.NewAdmin("test@example.com", "admin")

```

## Memory allignment and Padding in Struct

**Qustion**: How much memory the above code takes?

1 byte bool + 2 byte int + 4 byte float =  7 byte.

But it actually takes 8 byte.

There is a concept of allignement in hardware, which basically fits each values in the same word boudaries instead of keeping it across 2 different boundaries. This is because of a value spread across multiple word boudaries, then hardware will take multiple instructions to read/write to it.
- Allignment for bool is 1 byte i.e 0, 1, 2, 3 etc
- Allignement for int16 is 2 bytes i.e is 0, 2, 4, 6 etc
- Allignement for int32 is 4 bytes i.e is 4, 8, 12 etc
- Allignement for float32 is 4, 8, 12 etc

0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 
--- | --- | --- | --- |--- | --- | --- | --- |
bool| -   | int | -   | float | - | - | - | - |

In the above table, the byte number 1 is called padding, since this memory will not be used for any value, to have the proper allignment of all these types within a word boundary, hardware just skiped the byte 1 here. This will casues many unused memory locations.

If we used int32 in the above example, then it would have created 3 bytes of padding instead of 1. And if used int64 then the padding would have increased to 7 bytes!

One way to overcome padding is to order the fields in Struct from largest to smallest.
```
type example struct {
    pi      float32
    counter int16
	flag    bool
}
```

But until and unless our profilling tool report about this memory issues, it is better to group all the fields in a Struct in a way which are related and better for the readability. 

## Struct complete example
```
main function in main package

package main

import (
	"fmt"

	"example.com/structs/user"
)

func main() {
	userFirstName := getUserData("Please enter your first name: ")
	userLastName := getUserData("Please enter your last name: ")
	userBirthDate := getUserData("Please enter your birthdate (MM/DD/YYYY): ")

	appUser, err := user.New(userFirstName, userLastName, userBirthDate)
	if err != nil {
		fmt.Println(err)
		return
	}

	adminUser := user.NewAdmin("test@example.com", "admin")

	appUser.OutputUserDetails()
	appUser.ClearUserName()
	appUser.OutputUserDetails()

	adminUser.OutputUserDetails()
}

func getUserData(data string) string {
	var userData string
	fmt.Print(data)
	fmt.Scanln(&userData)
	return userData
}

=======

user function in user package

package user

import (
	"errors"
	"fmt"
	"time"
)

type User struct {
	firstName string
	lastName  string
	birthDate string
	createdAt time.Time
}

type Admin struct {
	email    string
	password string
	User
}

func New(firstName string, lastName string, birthDate string) (*User, error) {
	if firstName == "" || lastName == "" || birthDate == "" {
		return nil, errors.New("first name, last name and birth date are required")
	}
	return &User{
		firstName: firstName,
		lastName:  lastName,
		birthDate: birthDate,
		createdAt: time.Now(),
	}, nil
}

func NewAdmin(email string, password string) *Admin {
	return &Admin{
		email:    email,
		password: password,
		User: User{
			firstName: "ADMIN",
			lastName:  "ADMIN",
			birthDate: "---",
			createdAt: time.Now(),
		},
	}
}

func (u *User) OutputUserDetails() {
	fmt.Println(u.firstName, u.lastName, u.birthDate, u.createdAt)
}

func (u *User) ClearUserName() {
	u.firstName = ""
	u.lastName = ""
}


```

### Struct examples

- Declare, create and initialize struct types: https://go.dev/play/p/djzGT1JtSwy
- Anonymous struct types: https://go.dev/play/p/09cxjnmfcdC
- Named vs Unnamed types: https://go.dev/play/p/ky91roJDjir

