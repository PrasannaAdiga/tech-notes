# Rest API using Gin

```
package main

import "github.com/gin-gonic/gin"

type Person struct {
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
}

func rootHandler(c *gin.Context) {
	c.JSON(200, Person{
		FirstName: "Prasanna",
		LastName:  "Adiga",
	})
}

func main() {
	router := gin.Default()

	router.GET("/", rootHandler)

	router.Run(":8080")
}
```