# REST API

## Gin-gonic
One of the frameowrk which is avialble in Go for REST API implementation is gin-goinc: https://github.com/gin-gonic/gin

- To install it:  `go get -u github.com/gin-gonic/gin`

- To use it: `import "github.com/gin-gonic/gin"`

## Implement a simple Rest API

```
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	server := gin.Default()

	server.GET("/events", getEvents)

	server.Run(":8080") // localhost:8080

}

func getEvents(context *gin.Context) { // This context will be sent automatically by Gin
	// Since this functin is registered as a handler function in Gin
	context.JSON(http.StatusOK, gin.H{"message": "Hello!"})
	// JSON method is used to send any response back to user as a JOSN body
	// We have other methods like HTML to send back an html response body

}

```

- Here the gin.Default will setup a basic http server which comes up with Logger and Recovery middleware by default. Logger will logs an incoming request and Recovery will take crae of recovering our program from not being crash entirely. 

For more detailed REST API implementation refer the below github project
- https://github.com/PrasannaAdiga/my-first-go