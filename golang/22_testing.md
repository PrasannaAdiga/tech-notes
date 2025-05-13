# Testing
https://github.com/ardanlabs/gotraining/tree/master/topics/go/testing/tests

Testing is built right into the go tools and the standard library. Testing needs to be a vital part of the development process because it can save you a tremendous amount of time throughout the life cycle of the project. Benchmarking is also a very powerful tool tied to the testing functionality. Aspect of your code can be setup to be benchmarked for performance reviews. Profiling provides a view of the interations between functions and which functions are most heavily used.

- The Go toolset has support for testing and benchmarking.
- The tools are very flexible and give you many options.
- Write tests in tandem with development.
- Example code serve as both a test and documentation.
- Benchmark throughout the dev, qa and release cycles.
- If performance problems are observed, profile your code to see what functions to focus on.
- The tools can interfere with each other. For example, precise memory profiling skews CPU profiles, goroutine blocking profiling affects scheduler trace, etc. Rerun tests for each needed profiling mode.

## Basic Unit Test

```
package main

func main() {
	Add(1, 2)
}

func Add(a, b int) int {
	return a + b
}

```

```
package main

import (
	"fmt"
	"testing"
)

func TestAdd(t *testing.T) {
	tests := []struct {
		a, b, want int
	}{
		{2, 3, 5},
		{4, 5, 9},
		{0, 0, 0},
	}
	for _, tt := range tests {
		t.Run(fmt.Sprintf("%d+%d", tt.a, tt.b), func(t *testing.T) {
			got := Add(tt.a, tt.b)
			if got != tt.want {
				t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
			}
		})
	}
}

```


```
// Sample test to show how to write a basic unit test.
package example1

import (
	"net/http"
	"testing"
)

const succeed = "\u2713"
const failed = "\u2717"

// TestDownload validates the http Get function can download content.
func TestDownload(t *testing.T) {
	url := "https://www.ardanlabs.com/blog/index.xml"
	statusCode := 200

	t.Log("Given the need to test downloading content.")
	{
		testID := 0
		t.Logf("\tTest %d:\tWhen checking %q for status code %d", testID, url, statusCode)
		{
			resp, err := http.Get(url)
			if err != nil {
				t.Fatalf("\t%s\tTest %d:\tShould be able to make the Get call : %v", failed, testID, err)
			}
			t.Logf("\t%s\tTest %d:\tShould be able to make the Get call.", succeed, testID)

			defer resp.Body.Close()

			if resp.StatusCode == statusCode {
				t.Logf("\t%s\tTest %d:\tShould receive a %d status code.", succeed, testID, statusCode)
			} else {
				t.Errorf("\t%s\tTest %d:\tShould receive a %d status code : %d", failed, testID, statusCode, resp.StatusCode)
			}
		}
	}
}

O/P for the success case:
go test -v                                                                                       ✔  12:50:47 PM  
=== RUN   TestDownload
    hello_test.go:16: Given the need to test downloading content.
    hello_test.go:19:   Test 0: When checking "https://www.ardanlabs.com/blog/index.xml" for status code 200
    hello_test.go:25:   ✓       Test 0: Should be able to make the Get call.
    hello_test.go:30:   ✓       Test 0: Should receive a 200 status code.
--- PASS: TestDownload (0.37s)
PASS
ok      example.com/m/v2        0.536s

O/P for the failure case:
go test -v                                  ✔  12:54:46 PM  
=== RUN   TestDownload
    hello_test.go:16: Given the need to test downloading content.
    hello_test.go:19:   Test 0: When checking "https://www.ardanlabs.com/blog/index.xml" for status code 200
    hello_test.go:25:   ✓       Test 0: Should be able to make the Get call.
    hello_test.go:32:   ✗       Test 0: Should receive a 200 status code : 200
--- FAIL: TestDownload (0.50s)
FAIL
exit status 1
FAIL    example.com/m/v2        0.969s

```

It is nice to write unit test with given, when and should clauses. Given is why we are writing this test to begin with, when is what data we are using for the test, and should is what should happen. 

To run a go test, there are several options like:
- `go test`: runs all the test cases
- `go test -v`: Runs in verbose mode which gives more information on the tests
- `go test -run 'test_name'`: Runs one particular test case

## Table Unit Test

With this we do not have to write a whole bunch of test functions, we can leverage one test function with a table of inputs and outputs and run that test all the way through. 
```
// Sample test to show how to write a basic unit table test.
package example2

import (
	"net/http"
	"testing"
)

const succeed = "\u2713"
const failed = "\u2717"

// TestDownload validates the http Get function can download content and
// handles different status conditions properly.
func TestDownload(t *testing.T) {
	tt := []struct {
		url        string
		statusCode int
	}{
		{"https://www.ardanlabs.com/blog/index.xml", http.StatusOK},
		{"http://rss.cnn.com/rss/cnn_topstorie.rss", http.StatusNotFound},
	}

	t.Log("Given the need to test downloading different content.")
	{
		for testID, test := range tt {
			t.Logf("\tTest %d:\tWhen checking %q for status code %d", testID, test.url, test.statusCode)
			{
				resp, err := http.Get(test.url)
				if err != nil {
					t.Fatalf("\t%s\tTest %d:\tShould be able to make the Get call : %v", failed, testID, err)
				}
				t.Logf("\t%s\tTest %d:\tShould be able to make the Get call.", succeed, testID)

				defer resp.Body.Close()

				if resp.StatusCode == test.statusCode {
					t.Logf("\t%s\tTest %d:\tShould receive a %d status code.", succeed, testID, test.statusCode)
				} else {
					t.Errorf("\t%s\tTest %d:\tShould receive a %d status code : %v", failed, testID, test.statusCode, resp.StatusCode)
				}
			}
		}
	}
}

O/P:

go test -v                                1 ✘  12:59:55 PM  
=== RUN   TestDownload
    hello_test.go:22: Given the need to test downloading different content.
    hello_test.go:25:   Test 0: When checking "https://www.ardanlabs.com/blog/index.xml" for status code 200
    hello_test.go:31:   ✓       Test 0: Should be able to make the Get call.
    hello_test.go:36:   ✓       Test 0: Should receive a 200 status code.
    hello_test.go:25:   Test 1: When checking "http://rss.cnn.com/rss/cnn_topstorie.rss" for status code 404
    hello_test.go:31:   ✓       Test 1: Should be able to make the Get call.
    hello_test.go:36:   ✓       Test 1: Should receive a 404 status code.
--- PASS: TestDownload (1.14s)
PASS
ok      example.com/m/v2        1.619s

```

## Mocking WebServer Response
Refer this code: https://go.dev/play/p/SILnu117hak

Here we defined a Mock Server by using `*httptest.Server` package, which exposes a single GET API, and then we create an instance of this mock server and call the Get method. So by this way we can create our own mock server with different APIs exposed and each of the API returns some expected response and then we use this mock server in our test cases, instead of calling the real server.

## Testing Internal Endpoints
Refer this code: https://go.dev/play/p/CSK7SZEeWf3

Here we can define a webserver with multiple endpoints and then we can test these endpoints by writing test cases which will make a call to these endpoints and test against the responses.

## Example Tests
Example tests serves 2 purposes, they help with providing examples in the Go documentation that our code is producing and for a test. We write this type of test with word `Example` and the actual function name which we want to test.

```
// Sample to show how to write a basic example.
package handlers_test

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/http/httptest"
)

// ExampleSendJSON provides a basic example example.
func ExampleSendJSON() {
	r := httptest.NewRequest("GET", "/sendjson", nil)
	w := httptest.NewRecorder()
	http.DefaultServeMux.ServeHTTP(w, r)

	var u struct {
		Name  string
		Email string
	}

	if err := json.NewDecoder(w.Body).Decode(&u); err != nil {
		log.Println("ERROR:", err)
	}

	fmt.Println(u)
	// Output:
	// {Bill bill@ardanlabs.com}
}

```

## Sub Tests
Refer this code: https://go.dev/play/p/7PrkFU-qVdY

Sub Tests are really, really help when we start looking at table tests because one of the things that we have with table tests is the ability to do this data-driven testing. But if we wanna just filter out one piece of data over the other, historically, we had to comment out the data which meant we had to go in and do some code changes. What our subtests are gonna let us do is filter a piece of data at the command line-level. So each tests in a table test becomes a sub test and we can call one particular sub test through its name, without commenting any code. Also, we can run all of these sub tests in parallel so that all the unit test can run faster in the CI servers.

## Code Coverage
Making sure your tests cover as much of your code as possible is critical. Go's testing tool allows you to create a profile for the code that is executed during all the tests and see a visual of what is and is not covered.

```
go test -coverprofile cover.out
go tool cover -html=cover.out
```

