# Maps
https://github.com/ardanlabs/gotraining/tree/master/topics/go/language/maps

Maps provide a data structure that allow for the storage and management of key/value pair data.

- Maps provide a way to store and retrieve key/value pairs.
- Reading an absent key returns the zero value for the map's value type.
- Iterating over a map is always random.
- The map key must be a value that is comparable.
- Elements in a map are not addressable. We can cannot take the address of an element in a map. 
- Maps are a reference type. The value of maps are shared across the program boundary.
- Maps can not be used in the zero value state where as slices can be used. Maos has to be constructed.
- Maps also uses value semantics similar like slices
- We can create a map either by using make function literal construction similar way how we do in slices.

```
// Sample program to show how to initialize a map, write to
// it, then read and delete from it.
package main

import "fmt"

// user represents someone using the program.
type user struct {
	name    string
	surname string
}

func main() {

	// Declare and make a map that stores values
	// of type user with a key of type string.
	users := make(map[string]user)

	// Add key/value pairs to the map.
	users["Roy"] = user{"Rob", "Roy"}
	users["Ford"] = user{"Henry", "Ford"}
	users["Mouse"] = user{"Mickey", "Mouse"}
	users["Jackson"] = user{"Michael", "Jackson"}

	// Read the value at a specific key.
	mouse := users["Mouse"]

	fmt.Printf("%+v\n", mouse)

	// Replace the value at the Mouse key.
	users["Mouse"] = user{"Jerry", "Mouse"}

	// Read the Mouse key again.
	fmt.Printf("%+v\n", users["Mouse"])

	// Delete the value at a specific key.
	delete(users, "Roy")

	// Check the length of the map. There are only 3 elements.
	fmt.Println(len(users))

	// It is safe to delete an absent key.
	delete(users, "Roy")

    // Declare and initialize the map with values.
	users_literal := map[string]user{
		"Roy":     {"Rob", "Roy"},
		"Ford":    {"Henry", "Ford"},
		"Mouse":   {"Mickey", "Mouse"},
		"Jackson": {"Michael", "Jackson"},
	}

	// Iterate over the map printing each key and value.
	for key, value := range users_literal {
		fmt.Println(key, value)
	}

	fmt.Println("Goodbye.")
}

O/P:
{name:Mickey surname:Mouse}
{name:Jerry surname:Mouse}
3
Roy {Rob Roy}
Ford {Henry Ford}
Mouse {Mickey Mouse}
Jackson {Michael Jackson}
Goodbye.
```

### Map examples:

- Absent keys: https://go.dev/play/p/5KHMfmL2SyA
- Map key restrictions: https://go.dev/play/p/lfl967ocaKv 
- Map literals and range: https://go.dev/play/p/0KFlxby2a0z
- Sorting maps by key: https://go.dev/play/p/XADXCQqn2pJ
- Taking an element's address: https://go.dev/play/p/4phv1S1wZWh
- Maps are Reference Types: https://go.dev/play/p/7jEDn1yhg5v
