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

# API Folder Structure

![stack_heap](images/api_folder_structure.drawio.png "icon")


# Middleware

Middleware is like a checkpoint or a gatekeeper that stands between a client request and the final processing of that request by the server. It can inspect, modify, or log the request before it reaches the final destination, and it can do the same with the response before it is sent back to the client.

### It serves below various purposes:

- **Logging**: which records information about each request for monitoring or debugging.
- **Authentication and authorization**: ensuring the client is allowed to access certain resources.
- **Data validation**: that means checking if the data in the request meets certain criteria.
- **Error handling** as well for catching errors and sending proper responses back to the client.

### Some type of middlewares which are good to add in each application:
- Security Headers: 

Using this middleware, we are going to set some security headers onto our response that we are going to send back to the client.
- CORS: 

Cross-origin Resource Sharing, is a security feature implemented in web browsers that restricts web pages from making requests to a domain different from the one that served the web page. This is crucial for preventing malicious attacks, but it can be a limitation during development or when building APIs that need to be accessed from different origins.
- Response time: 

A response time middleware will calculate the time it took to process a request from a client and send a response
- Compression: 

Using compression middleware in go can be very beneficial for improving the performance of your web applications. Compression reduces the size of the response body sent over the network, which can significantly decrease loading times for your application. This is especially important for large assets like images, stylesheets, and JavaScript files.

- Rate Limiter:

We can implement  the rate limiter based on the number of requests per IP in a certain duration.

# Dockerfile
Create one for each microservicce

```
# The base go-image
FROM golang:1.18-alpine as builder

# create a directory for the app
RUN mkdir /app

# copy all files from the current directory to the app directory
COPY broker-service/. /app

# set working directory
WORKDIR /app

# build executable
RUN CGO_ENABLED=0 go build -o brokerApp ./cmd/api

RUN chmod +x /app/brokerApp

# create a tiny image for use
FROM alpine:latest
RUN mkdir /app

COPY --from=builder /app/brokerApp /app

# Run the server executable
CMD [ "/app/brokerApp" ]
```

# docker-compose file
Create at the root folder

```
version: '3'

services:

  broker-service:
    build:
      context: .
      dockerfile: ./broker-service.dockerfile # Provide the correct path of the docker file
    restart: always
    ports:
      - "8080:80"
    deploy:
      mode: replicated
      replicas: 1
    environment:
      RABBIT_URL: "amqp://guest:guest@rabbitmq"
```

# Makefile 
Create at the root folder

```
up:
	@echo "Starting docker images..."
	docker-compose up -d
	@echo "Docker images started!"

## down: stop docker compose
down:
	@echo "Stopping docker images..."
	docker-compose down
	@echo "Docker stopped!"
```

# Smaple go REST poject

![stack_heap](images/architecture.drawio.png "icon")

![stack_heap](images/apis.drawio.png "icon")

![stack_heap](images/authentication_authorization.drawio.png "icon")

### main.go

```
package main

import (
	"github.com/PrasannaAdiga/my-first-go/db"
	"github.com/PrasannaAdiga/my-first-go/routes"
	"github.com/gin-gonic/gin"
)

func main() {
	server := gin.Default()

	routes.RegisterRoutes(server)

	db.InitDB()

	server.Run(":8080")
}
```

### db.go

```
package db

import (
	"database/sql"

	_ "github.com/mattn/go-sqlite3" // This is not a direct import, database/sql use this under the hood
)

var DB *sql.DB

func InitDB() {
	var err error
	DB, err = sql.Open("sqlite3", "api.db") // driver name here is sqlite to use go-sqlite3(SQLite database) under the hood
	// data source name will be any local file name which will be created automatically instead of storing in a real db
	// All the data will be stored in this file and we can interact with it through sql queries.

	if err != nil {
		panic("Could not connect to database.")
	}

	DB.SetMaxOpenConns(10)
	DB.SetMaxIdleConns(5)

	createTables()
}

func createTables() {
	createUsersTable := `
	CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		email TEXT NOT NULL UNIQUE,
		password TEXT NOT NULL
	)
	`

	_, err := DB.Exec(createUsersTable)

	if err != nil {
		panic("Could not create users table.")
	}

	createEventsTable := `
	CREATE TABLE IF NOT EXISTS events (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		description TEXT NOT NULL,
		location TEXT NOT NULL,
		dateTime DATETIME NOT NULL,
		user_id INTEGER,
		FOREIGN KEY(user_id) REFERENCES users(id)
	)
	`

	_, err = DB.Exec(createEventsTable)

	if err != nil {
		panic("Could not create events table.")
	}

	createRegistrationsTable := `
	CREATE TABLE IF NOT EXISTS registrations (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		event_id INTEGER,
		user_id INTEGER,
		FOREIGN KEY(event_id) REFERENCES events(id),
		FOREIGN KEY(user_id) REFERENCES users(id)
	)
	`

	_, err = DB.Exec(createRegistrationsTable)

	if err != nil {
		panic("Could not create registrations table.")
	}
}

```

### routes.go

```
package routes

import (
	"github.com/PrasannaAdiga/my-first-go/middlewares"
	"github.com/gin-gonic/gin"
)

func RegisterRoutes(server *gin.Engine) {
	server.GET("/events", getEvents)    // GET, POST, PUT, PATCH, DELETE
	server.GET("/events/:id", getEvent) // /events/1, /events/5

	authenticated := server.Group("/")
	authenticated.Use(middlewares.Authenticate)
	authenticated.POST("/events", createEvent)
	authenticated.PUT("/events/:id", updateEvent)
	authenticated.DELETE("/events/:id", deleteEvent)
	authenticated.POST("/events/:id/register", registerForEvent)
	authenticated.DELETE("/events/:id/register", cancelRegistration)

	server.POST("/signup", signup)
	server.POST("/login", login)
}

```

### auth.go

```
package middlewares

import (
	"net/http"

	"github.com/PrasannaAdiga/my-first-go/utils"
	"github.com/gin-gonic/gin"
)

func Authenticate(context *gin.Context) {
	token := context.Request.Header.Get("Authorization")

	if token == "" {
		context.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"message": "Not authorized."})
		return
	}

	userId, err := utils.VerifyToken(token)

	if err != nil {
		context.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"message": "Not authorized."})
		return
	}

	context.Set("userId", userId)
	context.Next()
}

```

### utils.go

```
package utils

import (
	"errors"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt"
)

const secretKey = "supersecret"

// User the unique userId and email to generate a JWT token
// And sign the token by using a key
// Same key will be used to check the incoming token later
func GenerateToken(email string, userId int64) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"email":  email,
		"userId": userId,
		"exp":    time.Now().Add(time.Hour * 2).Unix(),
	})

	return token.SignedString([]byte(secretKey))
}

func VerifyToken(token string) (int64, error) {
	parsedToken, err := jwt.Parse(token, func(jwtToken *jwt.Token) (interface{}, error) {
		_, ok := jwtToken.Method.(*jwt.SigningMethodHMAC)

		if !ok {
			return nil, errors.New("Unexpected signing method")
		}

		return []byte(secretKey), nil
	})

	if err != nil {
		fmt.Println("Could not parse token")
		return 0, errors.New("Could not parse token.")
	}

	tokenIsValid := parsedToken.Valid

	if !tokenIsValid {
		return 0, errors.New("Invalid token!")
	}

	claims, ok := parsedToken.Claims.(jwt.MapClaims)

	if !ok {
		return 0, errors.New("Invalid token claims.")
	}

	// email := claims["email"].(string)
	userId := int64(claims["userId"].(float64))
	return userId, nil
}

```

### handlers.go

```
package routes

import (
	"net/http"

	"github.com/PrasannaAdiga/my-first-go/models"
	"github.com/PrasannaAdiga/my-first-go/utils"
	"github.com/gin-gonic/gin"
)

func signup(context *gin.Context) {
	var user models.User

	err := context.ShouldBindJSON(&user)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data."})
		return
	}

	err = user.Save()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not save user."})
		return
	}

	context.JSON(http.StatusCreated, gin.H{"message": "User created successfully"})
}

func login(context *gin.Context) {
	var user models.User

	err := context.ShouldBindJSON(&user)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data."})
		return
	}

	err = user.ValidateCredentials()

	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": "Could not authenticate user."})
		return
	}

	token, err := utils.GenerateToken(user.Email, user.ID)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not authenticate user."})
		return
	}

	context.JSON(http.StatusOK, gin.H{"message": "Login successful!", "token": token})
}

```

### model.go

```
package models

import (
	"errors"

	"github.com/PrasannaAdiga/my-first-go/db"
	"github.com/PrasannaAdiga/my-first-go/utils"
)

type User struct {
	ID       int64
	Email    string `binding:"required"`
	Password string `binding:"required"`
}

func (u User) Save() error {
	query := "INSERT INTO users(email, password) VALUES (?, ?)"
	stmt, err := db.DB.Prepare(query)

	if err != nil {
		return err
	}

	defer stmt.Close()

	hashedPassword, err := utils.HashPassword(u.Password)

	if err != nil {
		return err
	}

	result, err := stmt.Exec(u.Email, hashedPassword)

	if err != nil {
		return err
	}

	userId, err := result.LastInsertId()

	u.ID = userId
	return err
}

func (u *User) ValidateCredentials() error {
	query := "SELECT id, password FROM users WHERE email = ?"
	row := db.DB.QueryRow(query, u.Email)

	var retrievedPassword string
	err := row.Scan(&u.ID, &retrievedPassword)

	if err != nil {
		return errors.New("Credentials invalid")
	}

	passwordIsValid := utils.CheckPasswordHash(u.Password, retrievedPassword)

	if !passwordIsValid {
		return errors.New("Credentials invalid")
	}

	return nil
}

```

## Call another API from gin-gonic with context timeout

```
package main

import (
	"context"
	"io"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func fetchData(c *gin.Context) {
	// Set a timeout for the HTTP request
	timeout := 2 * time.Second
	ctx, cancel := context.WithTimeout(c.Request.Context(), timeout)
	defer cancel()

	// Create a new HTTP request with the context
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, "https://httpbin.org/delay/0", nil)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create request"})
		return
	}

	// Perform the HTTP request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		c.JSON(http.StatusRequestTimeout, gin.H{"error": "Request timed out"})
		return
	}
	defer resp.Body.Close()

	// Read and return the response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read response"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"response": string(body)})
}

func main() {
	r := gin.Default()
	r.GET("/fetch", fetchData)
	r.Run(":8080")
}

```

# Sample go GRPC poject
