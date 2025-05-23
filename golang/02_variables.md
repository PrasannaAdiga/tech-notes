# Variables
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/variables
 
- Variables are at the heart of the language and provide the ability to read from and write to memory. 
- In Go, access to memory is type safe. This means the compiler takes type seriously and will not allow us to use variables outside the scope of how they are declared.
- When variables are being declared to their zero value, use the keyword var.
- When variables are being declared and initialized, use the short variable declaration operator.
- Variables names should start with a letter or an underscore. Unicode letters are also ok.
- Global variables can not be declared with short variable declaration operator. We have to declare it with var keyword.

## Declaration and Initialization
- var a string - **zero value** or **null value**decalaration
- a := "golang" - **Short variable** declaration operation, to declare and initialize at the same time

## Data Types
- Type is everything in Go. Without this we can not have Integrity. Types refers to the types of values, because every value in Go is of specific type.
- Go is a statically typed language not a dynamically typed language.
- Type provides 2 pieces of information. Size of the memory that is being allocated and what that memory represents.

**Go has 3 different Data Types**
- Built-in types
    - numeric/integer: int can be 8, 16 or 64 bits depending on the underlying architecture
    - float: Float32 or Float64
    - booleans
    - strings and runes
    - constants
    - arrayas
    - Error
- User defined type 
    - Struct
    - Enums
- Reference types. We consider all reference type as nil when we set it to zero value.
    - slices
    - maps
    - Pointers
    - functions 
    - method and interfaces
    - channels 

## Naming Convention
- PascalCase
    - Structs, interfaces, enums
    - Example: CalculateArea, UserInfo
- snake_case
    - variables and file names
    - Example: user_id, first_name
- UPPERCASE
    - constansts
- mixedCase
    - Variables or extenral libraries    

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

## Rune
- A rune is an alias for int32 and it represents a Unicode code point, a Unicode value.
- So it is not a character, it is an integer value.
- A rune is an integer value, and that value represents a Unicode code point and that will be converted into a character.
- Runes are used to represent individual characters in a string, and they facilitate working with Unicode characters efficiently.
- Runes are declared using single quotes, double quotes and backticks are for strings.

```
var ch rune = 'a'
fmt.Println(ch)
O/P:
97

To convert rune to string:
str := string(ch)
```

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

### String functions
- To convert int to string: `strconv.Itoa(10)`
- To convert string to slice
```
fruits := "apples, orange, banana"
parts := strings.split(fruits, ",") O/P: [apples orange banana]
```
- To Join string values
```
countries :=  []string{"Genrmany", "France", "India"}
joined := strings.join(countries, ",") O/P: Genrmany, France, India
```
- To find a text: `strings.Contains(str, "Go")`
- To replace a text: `strings.Replace(str, "Go", "Hello", 1)`
- To lowercase or uppercase: `strings.ToLower(str)` - `strings.ToUpper(str)`
- To repeat the same string: `strings.Repeat("foo ", 3)` O/P: foo foo foo
- To count number of occurance: `strings.Count("Hello", "He")` O/P 1
- To find has the prefix: `strings.HasPrefix("Hello", "He")` O/P yes
- To find has the suffix: `strings.HasSuffix("Hello", "lo")` O/P yes

