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