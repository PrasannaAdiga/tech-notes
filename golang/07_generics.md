# Generics

Consider the below example, where accepting any kind of value is too wide, and returning any type of value is too unspecific.

```
func add(a, b any) any {
	aInt, aIsInt := a.(int)
	bInt, bIsInt := b.(int)

	if aIsInt && bIsInt {
		return aInt + bInt
	}

	aFloat, aIsFloat := a.(float64)
	bFloat, bIsFloat := b.(float64)

	if aIsFloat && bIsFloat {
		return aFloat + bFloat
	}

	aString, aIsString := a.(string)
	bString, bIsString := b.(string)

	if aIsString && bIsString {
		return aString + bString
	}

	return nil
}
```

So if we have the code `result := add(1, 2)`, go does not understand the type of the variable result.
And working with this `result` varaible is too difficult since we Go does not know its type.

So we can turn the above function to a Generic function to solve the above problems.

We use Type Holder like `T` instead of `any` type, in place of receiving or return type of a function.

In the function name we use single or multiple Type Holder like `add[T any, K any]` and use these type holder in function definition like `func add[T any, K any](a, b T) K`

We can also list the posible types instead of `any` in the function declaration like `func add[T int|float|string]`

So the above program can be refectored to below one:

```
package main

import "fmt"

func main() {
	result := add(1, 2)
	fmt.Println(result)
}

func add[T int | float64 | string](a, b T) T {
	return a + b
}
```




