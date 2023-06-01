# Embedding
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/embedding

Embedding types provide the final piece of sharing and reusing state and behavior between types. Through the use of inner type promotion, an inner type's fields and methods can be directly accessed by references of the outer type.

- Embedding types allow us to share state or behavior between types.
- The inner type never loses its identity.
- This is not inheritance.
- Through promotion, inner type fields and methods can be accessed through the outer type.
- The outer type can override the inner type's behavior.

```
// Sample program to show how what we are doing is NOT embedding
// a type but just using a type as a field.
package main

import "fmt"

// user defines a user in the program.
type user struct {
	name  string
	email string
}

// notify implements a method notifies users
// of different events.
func (u *user) notify() {
	fmt.Printf("Sending user email To %s<%s>\n",
		u.name,
		u.email)
}

// admin represents an admin user with privileges.
type admin struct {
	person user // NOT Embedding
	level  string
}

func main() {

	// Create an admin user.
	ad := admin{
		person: user{
			name:  "john smith",
			email: "john@yahoo.com",
		},
		level: "super",
	}

	// We can access fields methods.
	ad.person.notify()
}

O/P:
Sending user email To john smith<john@yahoo.com>
```
Here `admin` type which has a `person` which is a concrete type of 	`user` and calls `notify` function of `person` through its reference. No embedding in action here.

But in the below program we can see the Embedding in action
```
// Sample program to show how to embed a type into another type and
// the relationship between the inner and outer type.
package main

import "fmt"

// user defines a user in the program.
type user struct {
	name  string
	email string
}

// notify implements a method notifies users
// of different events.
func (u *user) notify() {
	fmt.Printf("Sending user email To %s<%s>\n",
		u.name,
		u.email)
}

// admin represents an admin user with privileges.
type admin struct {
	user  // Embedded Type
	level string
}

func main() {

	// Create an admin user.
	ad := admin{
		user: user{
			name:  "john smith",
			email: "john@yahoo.com",
		},
		level: "super",
	}

	// We can access the inner type's method directly.
	ad.user.notify()

	// The inner type's method is promoted.
	ad.notify()
}

O/P:
Sending user email To john smith<john@yahoo.com>
Sending user email To john smith<john@yahoo.com>
```

Here in the admin, we removed the person field and just embedded a user value inside of an admin value, which will create a relationship between inner type and outer type. Here user is the inner type and admin is the outer type.
So we embedd another type inside a type and access all of the things which inner type has through outer type.

When we do this, there is a concept of **inner type promotion*, everything related to the inner type can be promoted up to the outer type. This promotion will allow access to those things from inner type through the outer type. 

Consider below program:
```
// Sample program to show how embedded types work with interfaces.
package main

import "fmt"

// notifier is an interface that defined notification
// type behavior.
type notifier interface {
	notify()
}

// user defines a user in the program.
type user struct {
	name  string
	email string
}

// notify implements a method notifies users
// of different events.
func (u *user) notify() {
	fmt.Printf("Sending user email To %s<%s>\n",
		u.name,
		u.email)
}

// admin represents an admin user with privileges.
type admin struct {
	user
	level string
}

func main() {

	// Create an admin user.
	ad := admin{
		user: user{
			name:  "john smith",
			email: "john@yahoo.com",
		},
		level: "super",
	}

	// Send the admin user a notification.
	// The embedded inner type's implementation of the
	// interface is "promoted" to the outer type.
	sendNotification(&ad)
}

// sendNotification accepts values that implement the notifier
// interface and sends notifications.
func sendNotification(n notifier) {
	n.notify()
}

O/P:
Sending user email To john smith<john@yahoo.com>
```

Because of the type promotion(behaviour being promoted up) the our type admin also satisfies all the method set of `notifier` and we can pass the address of this  admin to sendNotification which expects any piece of code which implements `notifier`.

But if the outer type implements the same things as the inner type, then there is no promotion. The outer type will override the inner type's implementation. 

Also, what if we have 2 inner types that implement the same method, then nothing going to happen unless we try to make a method call that has the ambiguity. 

So Embedding looks like its part of this concept of type reuse in Go. But we never user it for type reuse, instead we use it for Composition. 

## Embedding examples:
-  Fields: https://go.dev/play/p/mT4iWg10YEp
- Embedding types: https://go.dev/play/p/avo8I21N-qq
- Embedded types and interfaces: https://go.dev/play/p/pdwB9dxD1MR
- Outer and inner type interface implementations: https://go.dev/play/p/soB4QujV4Sj


# Exporting
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/exporting
To get Package level or Type/Field level Encapuslation

Packages contain the basic unit of compiled code. They define a scope for the identifiers that are declared within them. Exporting is not the same as public and private semantics in other languages. But exporting is how we provide encapsulation in Go.

- Basic unit of compilation in Go is a package. A package in Go represents a folder.
- Encapsulation begins and ends at the folder level in Go. Every folder represents a static library. That is our smallest unit of compilation.
- Based on this basic unit of compilation, symbols are either exported or available outside of the code in this folder, or un-exported and only available to the code in this folder or package.
- Always match the folder name with the package name.
- Code in go is compiled into packages and then linked together.
- Identifiers are exported (or remain unexported) based on letter-case.
- If an identifier name start with capital leter it is exported to outside folders. Else, it is not exported.
- We can also use the same idea at the type level also. Types which has field with capital letters are exported and others are un-exported.
- We import packages to access exported identifiers.
- Any package can use a value of an unexported type, but this is annoying to use.

## Exporting examples:

- Declare and access exported identifiers - Pkg: https://go.dev/play/p/8Xzq-m9ez-I
- Declare and access exported identifiers - Main: https://go.dev/play/p/KrpX0CyIyYO

- Declare unexported identifiers and restrictions - Pkg: https://go.dev/play/p/9u1IQexx5gk
- Declare unexported identifiers and restrictions - Main: https://go.dev/play/p/A5FpmRpuOWJ

- Access values of unexported identifiers - Pkg: https://go.dev/play/p/NroO30yoNvh
- Access values of unexported identifiers - Main: https://go.dev/play/p/e5fg0uOEkkn

- Unexported struct type fields - Pkg: https://go.dev/play/p/KQ6x5z7E1pN
- Unexported struct type fields - Main: https://go.dev/play/p/6MznWaiGwr-

- Unexported embedded types - Pkg: https://go.dev/play/p/br-2rVc1VF1
- Unexported embedded types - Main: https://go.dev/play/p/p9pQo5gCB42

