# Benchmarking
https://github.com/ardanlabs/gotraining/tree/master/topics/go/testing/benchmarks

Go has support for testing the performance of your code.

# WRK - a HTTP benchmarking tool
- Install WRK on mac or Linux
- Use the below command to test the performance or load on a particular API

```
wrk -t8 -c400 -d30s "http://localhost:8080/person?id=1"

-t = number of threads
-c = number of concurrent connections
-d = duration
```

## Basic Benchmarking

```
// go test -run none -bench . -benchtime 3s -benchmem

// Basic benchmark test.
package basic

import (
	"fmt"
	"testing"
)

var gs string

// BenchmarkSprint tests the performance of using Sprint.
func BenchmarkSprint(b *testing.B) {
	var s string

	for i := 0; i < b.N; i++ {
		s = fmt.Sprint("hello")
	}

	gs = s
}

// BenchmarkSprint tests the performance of using Sprintf.
func BenchmarkSprintf(b *testing.B) {
	var s string

	for i := 0; i < b.N; i++ {
		s = fmt.Sprintf("hello")
	}

	gs = s
}

O/P:
go test -run none -bench . -benchtime 3s -benchmem                                               ✔  04:24:14 PM  
goos: darwin
goarch: arm64
pkg: example.com/m/v2
BenchmarkSprint-8       108178939               33.61 ns/op            5 B/op          1 allocs/op
BenchmarkSprintf-8      122974902               28.79 ns/op            5 B/op          1 allocs/op
PASS
ok      example.com/m/v2        12.561s

```

Each benchmark tests are starting with the name Benachmark and its takes an argument of `b *testing.B` instead of `t *testing.T`(in case of unit tests). Initially the benchmark framework uses the value of `b.N` as `1` and then it is going to increase this over time. So framework will run this for enough iterations for about few seconds before showing the result. 

To run the benchmark use the command `go test -run none -bench . -benchtime 3s -benchmem`. Here we tell the framework that there are no test cases are written(-run none), then we use bench falg with `.` which means all the benchmarks, increase the benchtime to `3s`, also use the flag benchmem which provides the reports on memory allocations.

By looking at the output, the SprintF function runs faster than the Sprint function.

## Sub Benchmark

How we have sub tests in case of unit test, we aslo have a same concepts in benchmarking. 

```
import (
	"fmt"
	"testing"
)

var gs string

// BenchmarkSprint tests all the Sprint related benchmarks as
// sub benchmarks.
func BenchmarkSprint(b *testing.B) {
	b.Run("none", benchSprint)
	b.Run("format", benchSprintf)
}

// benchSprint tests the performance of using Sprint.
func benchSprint(b *testing.B) {
	var s string

	for i := 0; i < b.N; i++ {
		s = fmt.Sprint("hello")
	}

	gs = s
}

// benchSprintf tests the performance of using Sprintf.
func benchSprintf(b *testing.B) {
	var s string

	for i := 0; i < b.N; i++ {
		s = fmt.Sprintf("hello")
	}

	gs = s
}

O/P:
go test -run none -bench . -benchtime 3s -benchmem
goos: darwin
goarch: arm64
pkg: example.com/m/v2
BenchmarkSprint/none-8          107011941               33.42 ns/op            5 B/op       1 allocs/op
BenchmarkSprint/format-8        123807186               29.61 ns/op            5 B/op          1 allocs/op
PASS
ok      example.com/m/v2        12.501s

```

We can run the entire benchmarks or sub benchmark by following commands:

```
// go test -run none -bench . -benchtime 3s -benchmem
// go test -run none -bench BenchmarkSprint/none -benchtime 3s -benchmem
// go test -run none -bench BenchmarkSprint/format -benchtime 3s -benchmem

```

## Validate Becnhmarks
Refer the code: https://github.com/ardanlabs/gotraining/blob/master/topics/go/testing/benchmarks/validate/validate_test.go


