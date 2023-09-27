# Constants
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/constants

Constants are a way to create a named identifier whose value can never change. 
There are 2 varient of constants. Constants of kind and constants of type.

- Constants are not variables.
- They exist only at compilation. They never find themselves on a stack or on a heap.
- Literal values in Go are constant of kind. For example 2, -5, 2.34 etc
- Untyped constants or constants of a kind can be implicitly converted where typed constants or constants of type and variables can't.
- Constants of a kind can be implicitly converted by the compiler, which means we can not have **Enumerations** in Go.
- Think of untyped constants as having a Kind, not a Type.
- Unassigned constants recieve previous value
```
const (
	a = "foo"
	b  // Value is "foo"
)
```
- We can assign expression, or concatinate operations to a Constant, since these are executes during compile time. But we can not assign a function call to a constant.
```
const c = 2 * 5
const d = "hello" + "World"
const e = someFunc() // wrong
```

```
// Sample program to show how to declare constants and their
// implementation in Go.
package main

func main() {

	// Constants live within the compiler.
	// They have a parallel type system.
	// Compiler can perform implicit conversions of untyped constants.

	// Untyped Constants.
	const ui = 12345    // kind: integer
	const uf = 3.141592 // kind: floating-point

	// Typed Constants still use the constant type system but their precision
	// is restricted.
	const ti int = 12345        // type: int
	const tf float64 = 3.141592 // type: float64

	// ./constants.go:XX: constant 1000 overflows uint8
	// const myUint8 uint8 = 1000

	// Constant arithmetic supports different kinds.
	// Kind Promotion is used to determine kind in these scenarios.

	// Variable answer will of type float64.
	var answer = 3 * 0.333 // KindFloat(3) * KindFloat(0.333)

	// Constant third will be of kind floating point.
	const third = 1 / 3.0 // KindFloat(1) / KindFloat(3.0)

	// Constant zero will be of kind integer.
	const zero = 1 / 3 // KindInt(1) / KindInt(3)

	// This is an example of constant arithmetic between typed and
	// untyped constants. Must have like types to perform math.
	const one int8 = 1
	const two = 2 * one // int8(2) * int8(1)
}
```

Thorugh **Kind Promotion** in Go, a constant of kind int can be promoted to a constant of kind float. For example: const third = 1 / 3.0. Here constant of kind int 1 will be promoted to constant of kind float. So const third = 1.0/3.0

## IOTA
```
// Sample program to show how iota works.
package main

import "fmt"

func main() {

	const (
		A1 = iota // 0 : Start at 0
		B1 = iota // 1 : Increment by 1
		C1 = iota // 2 : Increment by 1
	)

	fmt.Println("1:", A1, B1, C1)

    const (
		A2 = iota // 0 : Start at 0
		B2        // 1 : Increment by 1
		C2        // 2 : Increment by 1
	)

	fmt.Println("2:", A2, B2, C2)

	const (
		A3 = iota + 1 // 1 : Start at 0 + 1
		B3            // 2 : Increment by 1
		C3            // 3 : Increment by 1
	)

	fmt.Println("2:", A3, B3, C3)
}

O/P:
1: 0 1 2
2: 0 1 2
3: 1 2 3
```

### Constants examples:

- Declare and initialize constants: https://go.dev/play/p/z251qax3MYa
- Parallel type system (Kind): https://go.dev/play/p/8a_tp97RHAf
- iota: https://go.dev/play/p/SLAYYNFIdUA
- Implicit conversion: https://go.dev/play/p/aB4NGcnZlw2