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

We can also have an empty literal construction 'example{}' to create zero value struct which mainly used when we do not have the need to assign it to a variable, returning from a function or while passing it as a parameter to a function.

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

### Struct examples

- Declare, create and initialize struct types: https://go.dev/play/p/djzGT1JtSwy
- Anonymous struct types: https://go.dev/play/p/09cxjnmfcdC
- Named vs Unnamed types: https://go.dev/play/p/ky91roJDjir