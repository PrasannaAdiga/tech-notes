Links
- https://github.com/ardanlabs/gotraining/tree/master/topics/go#prepare-your-mind

# Why Go?
- Go provides high perforamnce like C/C++
- Super efficient concurrency handling like Java
- Also ease of programming or fun code to code like Python


# Design Philosophy

## Integrity
We need to become very serious about reliability.

- Integrity is about every allocation, read and write of memory being accurate, consistent and efficient
- Integrity is about every data transformation being accurate, consistent and efficient.
- One simple way to reduce the number of bugs, and increase the integrity of your software, is to write less code.
- Write error handling everywhere

## Readability
We must structure our systems to be more comprehensible.

This is about writing simple code that is easier to read and understand without the need of mental exhaustion. Just as important, it's about not hiding the cost/impact of the code per line, function, package and the overall ecosystem it runs in.

## Simplicity
We must understand that simplicity is hard to design and complicated to build.

This is about hiding complexity. A lot of care and design must go into simplicity because this can cause more problems then good. It can create issues with readability and it can cause issues with performance.

## Performance
Perforamce in a software can come from 4 places

- Latency on networking, IO, disk IO
- Memory allocation and Garbage Collection
- How efficiently program will access data
- Algorithm efficiencies

Go can take the advantages of the hardware and it solves the first 3 perforamce issues. This gives us lot of performance built-in Go. 

Readability, writing clear and simple less code, testing, code reviews, re-factoring and good algorithms are the main blocks in Go to increase the performance from developers side.

# Variables
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/variables
 
- Variables are at the heart of the language and provide the ability to read from and write to memory. 
- In Go, access to memory is type safe. This means the compiler takes type seriously and will not allow us to use variables outside the scope of how they are declared.
- When variables are being declared to their zero value, use the keyword var.
- When variables are being declared and initialized, use the short variable declaration operator.

## Declaration and Initialization
- var a string - **zero value** decalaration
- a := "golang" - **Short variable** declaration operation, to declare and initialize at the same time

## Types
- Type is everything in Go. Without this we can not have Integrity.
- Type provides 2 pieces of information. Size of the memory that is being allocated and what that memory represents.
- Go has built-in types like numeric, string and bool.
- **Numeric**: int can be 8, 16 or 64 bits depending on the underlying architecture
- **Float**: Float64
- **Bool**:  0 or 1

## Type Conversion
Go does not have type casting, it has a type conversion instead. 
- Type casting is converting an existing type into a new type with the same memory location by extending or shrinking the memory size.
- Where as type conversion is to create a new brand memory location for the new type.
- Go support type conversion to have the integrity in place over the cost of the memory.

## String 
- String is 2 word data structure. Where the first word is a pointer to the backing array and the second word is the total number of bytes.
- For a zero value string, the first word will be a `nil` pointer and there are no bytes in the second word since we do not have any backing array yet.
- For eaxmplae consider a string, a := "hello". Here the first word ponits to a backing array which has a value `h`, `e`, `l`, `l`, `o` and the second word has a number of byte value as `5`.

# Struct Type (user defined type)
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/struct_types

Struct types are a way of creating complex types that group fields of data together. 
- We can use the struct literal form to initialize a value from a struct type.
- The dot (.) operator allows us to access individual field values.
- We can create anonymous structs.

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

We can also have an empty literal construction to create zero value struct which mainly used when we do not have the need to assign it to a variable, returning from a function or while passing it as a parameter to a function.

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


# Pointers

Everything in Go is pass by value.

## Pass By Value
Three areas of memeory which are important when Goroutine start executing functions one by one.
### 1. Data segments
Reserved for global variables and read-only values

### 2. Stacks
- A stack is a data structure or stack of memory that every OS level or Goroutine level threads are given. 
- At OS level 1 meg memory will be allocated for a Stack, where as 2K memory is allocated for each Goroutines. 
- When a Go program starts up, we get a Goroutine or a new path of execution for the main() function, which start executing every single instruction one by one.
- Everytime when a function is called, it takes a frame of memory off the stack and start executing the code written inside that function. 
- At any time, the goroutine only has direct access to the memory for the frame that it is opertaing on, it means all of the data that the goroutine needs to perform this data transforamtion has to be in here.
- Each of these stack frames creates a sandbox, a layer of isolation or a sense of immutibilty that the goroutine only mutate or cause problems in the same stack frame and nowhere else in our code.


Consider the below program:
```
// Sample program to show the basic concept of pass by value.
package main

func main() {

	// Declare variable of type int with a value of 10.
	count := 10

	// Display the "value of" and "address of" count.
	println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")

	// Pass the "value of" the count.
	increment(count)

	println("count:\tValue Of[", count, "]\tAddr Of[", &count, "]")
}

// increment declares count as a pointer variable whose value is
// always an address and points to values of type int.
//
//go:noinline
func increment(inc int) {

	// Increment the "value of" inc.
	inc++
	println("inc:\tValue Of[", inc, "]\tAddr Of[", &inc, "]")
}
```

- In the above code, when we call the function `increment` we copy the value of `count` and pass it to that function as a parameter. 
- Hence, even though we increment the value of this count inside the function increment, the value of this count variable inside the main stack frame does not change.
- Note that once the increment function is executed, we remove this stack frame and it's corresponding local variable and values. Then the goroutine will go back to the main stack frame and start continuing the execution until it completes.

![stack_heap](images/stack_heap.drawio.png "icon")

### Value and Pointer Semantics
- In case of value Semantics(What is there inside the box) we copy the value of a variable. It provides isolation, mutability, reduce side effects and better performance. But one of the cost of this semantics is, we will be having multiple copies of the same data throughout the program. It is difficult to update a data everywhere it needs to be. 
- In case of Pointer Semantics(Where is the box located in the memory) we copy the address of a variable.

### 3. Heaps












