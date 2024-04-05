# Variables
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/variables
 
- Variables are at the heart of the language and provide the ability to read from and write to memory. 
- In Go, access to memory is type safe. This means the compiler takes type seriously and will not allow us to use variables outside the scope of how they are declared.
- When variables are being declared to their zero value, use the keyword var.
- When variables are being declared and initialized, use the short variable declaration operator.
- Variables names should start with a letter or an underscore. Unicode letters are also ok.

## Declaration and Initialization
- var a string - **zero value** or **null value**decalaration
- a := "golang" - **Short variable** declaration operation, to declare and initialize at the same time

## Types
- Type is everything in Go. Without this we can not have Integrity. Types refers to the types of values, because every value in Go is of specific type.
- Go is a statically typed language not a dynamically typed language.
- Type provides 2 pieces of information. Size of the memory that is being allocated and what that memory represents.
- Go has built-in types like numeric, string and bool.
- **Numeric**: int can be 8, 16 or 64 bits depending on the underlying architecture
- **Float**: Float64
- **Bool**:  0 or 1
- int32 in Go is also called as `rune`

Go has 3 different Types
- Built-in types like numeric, float, bool, string, array and Error
- User defined type like Struct
- Reference types like slices, maps, interfaces, functions and channels. We consider all reference type as nil when we set it to zero value.

## Null value
All Go value types come with a so-called "null value" which is the value stored in a variable if no other value is explicitly set.
Here's a list of the null values for the different types:
- int => 0
- float64 => 0.0
- string => "" (i.e., an empty string)
- bool => false

## String 
- String is 2 word data structure with 1 byte of size where each word has 4 bit size. Here the first word is a pointer to the backing array and the second word is the total number of bytes.
- For a zero value string, the first word will be a `nil` pointer and there are no bytes in the second word since we do not have any backing array yet.
- For eaxmplae consider a string, a := "hello". Here the first word ponits to a backing array which has a value `h`, `e`, `l`, `l`, `o` and the second word has a number of byte value as `5`.
- Two ways to define a string.
    - interpreted string: ex: "this is a escape character: \n it creates a new line"
    - raw string: ex: `this is a escape character: \n it does not create a new line`

## Numeric
- Integrers(int32 or int64). Ex: 99, 0, -93
- Unassigned Integers(uint). Ex: 0, 15, 1732
- Floating point numbers(float32 or float64). Ex: 6.02e23, 0.25
- Complex Numbers(complex64 or complex128). Ex: 1 + 2i, 0.833i

## Boolean
- true or false value

## Errors 
```
type error interface {
    Error() string
}
```

## Explicit type assignment
We can explicitely assign a type to variable. Else, go will implicitely assigns a type.
- var count = 10 (here go will implicitely assign an `int` type to the variable `count`)
- var count float64 = 10 (here we explicitely assign `float` type to the variable `count`. By default Go will store the value as `10.0`)

## Type Conversion
Go does not have type casting, it has a type conversion instead. 
- Type casting is converting an existing type into a new type with the same memory location by extending or shrinking the memory size.
- Where as type conversion is to create a new brand memory location for the new type.
- Go support type conversion(explicit) to have the integrity in place over the cost of the memory.
- Go does not support any implicit type conversion instead it only supports explicit type conversion.
```
var i int = 32
var f float32

f = i // no implicit conversion
f = float32(i) // supports explicit type conversion
```

### Variable Examples

Below are the multiple ways to decaring a variables:
- var myName string // declare variable
- var myName string = "Mike" // declare and initialize
- var myName = "Mike" // initialize with inferred type
- myName := "Mike" // Short declaration syntax

- Declare and initialize variables: https://go.dev/play/p/xD_6ghgB7wm