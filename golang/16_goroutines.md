# Goroutines
https://github.com/ardanlabs/gotraining/tree/master/topics/go/concurrency/goroutines

Goroutines are functions that are created and scheduled to be run independently by the Go scheduler. The Go scheduler is responsible for the management and execution of goroutines.

- Goroutines are functions that are scheduled to run independently.
- We must always maintain an account of running goroutines and shutdown cleanly.
- Concurrency is not parallelism.
    - Concurrency is about dealing with lots of things at once.
    - Parallelism is about doing lots of things at once.
- Parallelism is about physically doing two or more things at the same time. Concurrency is about undefined, out of order, execution.

## OS Scheduler Mechanism
When a program starts up on an operating system, the operating system create a process. Processes are the container for the resources that the running program is going to need. Processes maintains and managers all the resources which a running program needs. The 2 big key resources are memory and thread, which we call a main thread. When a main thread dies, the process will shut down. 

If a process is like a container for the resources, then the thread to be the path of execution. Our code turns into a machine code and that machine code is always gonna be executed in a linear fashion or in a linear path. And its the job of the thread to manage that linear path of execution. 

This path of execution can be in one of 3 states at any time. It can be in a **running(executing)** state, where it start executing instructions one by one until the OS decides to do context switch where it pull of the current running thread from the core and put a new thread on to it. The new thread which is on the core we call its in a **runnable** state. Now the Scheduler will select one of the thread from this runnable pool and assign it to the CPU which will make it to become running state. Context switch done by OS is really an expensive task. It needs to save and replace states of all these threads. Each of these OS threads will have 1 meg of stack space. The third state is called **Waiting** where thread is just created and it keeps wait for its turn to get it placed on a core by OS.

In the olden days, there were only one single core processor, where each of the core can execute one path of execution or thread at any given time. But to create a perception that everything is running at the same time, the OS Scheduler will provide a slice of time on the code for each of these thread. If there are less threads like 1K then each thread will get more CPU time. But if there are lots of thread like 10K then each thread will get less CPU time.

But now a days we have multi core processor, which means we wil be having multiple execution units where we can run not just one thread at a time but multiple threads. If its 2 core then 2 threads at a time and so. Which means we can run 2 thread parallely now and this brought parallelism in place. All the OS schedulers has been written again to take the advantages of these multi core processors. 

** program (our code) -> process (container for resources like memory and thread) -> thread (path of execution inside the process) **

## Go Scheduler Mechanism
When a Go program starts up, it is given a logical processor that we call `P`. This logical processor is given an `M` that stands for Machine, which represents a real-life operating system thread which the OS is still responsible to schedule on some core. Then there are 2 data structure here, there is the Global Run Queue(GRQ), and evry `P` has a Local Run Queue(LRQ). Now evry Goroutine also can be in any one of the state of runnable, running or waiting. 

When a Gorouitne like the main Goroutine when our Go program starts up, is start to executing in the above given logical processor `P` and other entire context. This main Goroutiine may have couple of more goroutines, which are ends up in a local run queue because they are in a runnable state. Sometimes a goroutine thats in a runnable state might find itself in the Global run queue, because a P has not taken in yet. If there are no other goroutine in the LRQ then `P` will take any available goroutine from the GRQ.

If there are multiple core in a system, then we need similar amout of thread to not to put more pressure on the OS, means single thread per core to executes thousands of goroutines. If we have 2 Core processor, then 2 goroutines can run in parallel. 

Go Scheduler is built into the the Go runtime, and the Go runtime is built into your Go application, the scheduler runs up in the user mode not the kernel mode. Since Go scheduler runs in user mode, it is called a cooperating sceduler not a preemptive scheduler, where the OS Scheduler are called preemptive scheduler. 

There are 3 classes of events that are gonna allow the scheduler to make a scheduling decision. First one is the use of keyword `go` infront of the function call, and this is how we create goroutine. Second one is the `GC`, anytime garbage collection kicks in there is lot of scheduling decision is been made. And the last one is `System calls`, which happens all the time in Go anytime we call log ot fmt.print thats a system call.

Lets say the above Goroutine makes a system call like open a file, it can take up few seconds of time. So if we allow this Goroutine to block its corresponding OS thread, then for that amout of time of latency, we are not getting any other work done. So Go has specail data structure here, that we call a `network poller`(it has its own thread as well), and when a goroutine wants to make a system call, what happens is, this goroutine context switched off of the M, and its placed over here in the network poller, and it will be in the waiting state, and we handle the system call asynchronously. This is great because we just freed up the `M`, to do more work. At this time, the other goroutine move from runnable to running state. Once the OS comes back with the system call, then the goroutine which was waiting, move back to the LRQ where it sits back into a runnable state through another context switch. 

There may be times when we are on an OS that does not support asynchronous system calls. When that happens the following things happens with the Scheduler. So a goroutine G1 which will get blocked on lets say M1, there is no way to do it asynchronously, there is no way to move it to the network poller, so the scheduler will detach this M1 and G1 off the P, and bring a new OS thread M2 where another goroutine will be scheduled to run by scheduler. We are continuing to process the goroutines from local run queue, even though that other thread is blocked. Once the blocking call is done, the goroutine M1 moves back to local run queue, and the thread M1 is put on the side for later use. 

If any of the P is idle at any time, it will search for goroutines from Global run queue and if it founds it will take it and start executing it. If other process is overloaded with goroutines in its local run queue, the idle processor can steal few of the goroutines from it and start executing it. This way we keep all the processor and OS threads busy all the times. 

Go Scheduler sits on top of OS Scheduler, and it turns I/O bound work(which OS thread does) into CPU bound work, so that from OS perceptive the OS thread always busy. Context switch in Go Scheduler are so fast compared to Context switch in OS. 

![stack_heap](images/goroutine.drawio.png "icon")

## Goroutines and Concurrency
Way to implement concurrency in Go. 

### Synchronization and Orchestration
When we have multiple Goroutines, then we need to have Synchronization and Orchestration between all of them in order not to have data races and other issues. To understand what are these Synchronization and Orchestration, lets consider we went to a Starbucks coffe shop and standing in the line of queue to get some coffe. Now we are in line, we are waiting to get our turn to get upto the counter. Anytime goroutines have to get in line, that is a synchronization issue. But once we get to the counter and start talking to the person at the register, we now have an Orchestration issue. We are having conversation, we are exchanging money, there is data going back and forth. This is Orchestration.

So Synchronization is about getting in line and taking a turn to run a goroutine and Orchestration is about the interaction.

### Goroutine Orchestration by using WaitGroup
Below is the example code to show how to create goroutines in Go and how to deal with Goroutine Orchetsration by using WaitGroup

```
// Sample program to show how to create goroutines and
// how the scheduler behaves.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func init() {

	// Allocate one logical processor for the scheduler to use.
	runtime.GOMAXPROCS(1)
}

func main() {

	// wg is used to manage concurrency.
	var wg sync.WaitGroup
	wg.Add(2)

	fmt.Println("Start Goroutines")

	// Create a goroutine from the lowercase function.
	go func() {
		lowercase()
		wg.Done()
	}()

	// Create a goroutine from the uppercase function.
	go func() {
		uppercase()
		wg.Done()
	}()

	// Wait for the goroutines to finish.
	fmt.Println("Waiting To Finish")
	wg.Wait()

	fmt.Println("\nTerminating Program")
}

// lowercase displays the set of lowercase letters three times.
func lowercase() {

	// Display the alphabet three times
	for count := 0; count < 3; count++ {
		for r := 'a'; r <= 'z'; r++ {
			fmt.Printf("%c ", r)
		}
	}
}

// uppercase displays the set of uppercase letters three times.
func uppercase() {

	// Display the alphabet three times
	for count := 0; count < 3; count++ {
		for r := 'A'; r <= 'Z'; r++ {
			fmt.Printf("%c ", r)
		}
	}
}

O/P:
Start Goroutines
Waiting To Finish
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n o p q r s t u v w x y z 
Terminating Program

```
We can use WaitGroup to wait for multiple goroutines to finish. So wait group is a great way to do Orchestration, when we dont need anything back from Go routine. Waitgroup provides 3 APIs Add, Wait and Done. 
In the above code we use the variable `wg` as a closure, both the inner gorouine functions remember this outer fuction variable. And we use the concept of IIFE (Immediately Invoked Function Expression) to declare and immediately run the unnamed function with `go` keyword infront of it. This will create a sepaarte path of execution or goroutine in Go. One thing to note here is, the order of the executions of these multiple goroutines are not predictable. It depends on the OS and Schedulers.

If we forget to add wg.wait() function call, then the main goroutine will terminate immediately without waiting for the sub goroutines to finish.

Built-in functions in the runtime package
- runtime.GOMAXPROCS(1): Allocate one logical processor for the scheduler to use, even though there are multiple cores available.
- runtime.Gosched() : Requesting a scheduler to move the running goroutine to wait state. Scheduler may accept this request and mmove the goroutine to wait state or it may reject it and continue it to run. Never use this in production.
- wg.Wait(): Demanding the Go Scheduler to move this running goroutine to wait state. Go Scheduler will move it to wait state immediately.

If we forget to add wg.Done() function call, then go runtime will through `fatal error: all goroutines are asleep - deadlock!`. The wait group no longer get to zero now, because we are not decrementing the counter which we set initially through wg.Add() function, the main goroutine has to wait continuously. But go runtime will detect this and through the above runtime error. Go runtime has a simple go deadlock detector, It can identify easily when every single goroutine is now in a waiting state and can never move back into a runnable state. 

If we do not set the counter value properly according to the number of goroutines, then there could be some unwanted things will happen. For example in the above code if we set counter to 1 (i.e wg.Add(1)), then only one goroutine will run and the other one will get skipped, since the main go routine will terminate before executing the second one.

## Goroutine time slicing
```
// Sample program to show how the goroutine scheduler
// will time slice goroutines on a single thread.
package main

import (
	"crypto/sha1"
	"fmt"
	"runtime"
	"strconv"
	"sync"
)

func init() {

	// Allocate one logical processor for the scheduler to use.
	runtime.GOMAXPROCS(1)
}

func main() {

	// wg is used to manage concurrency.
	var wg sync.WaitGroup
	wg.Add(2)

	fmt.Println("Create Goroutines")

	// Create the first goroutine and manage its lifecycle here.
	go func() {
		printHashes("A")
		wg.Done()
	}()

	// Create the second goroutine and manage its lifecycle here.
	go func() {
		printHashes("B")
		wg.Done()
	}()

	// Wait for the goroutines to finish.
	fmt.Println("Waiting To Finish")
	wg.Wait()

	fmt.Println("Terminating Program")
}

// printHashes calculates the sha1 hash for a range of
// numbers and prints each in hex encoding.
func printHashes(prefix string) {

	// print each has from 1 to 10. Change this to 50000 and
	// see how the scheduler behaves.
	for i := 1; i <= 10; i++ {

		// Convert i to a string.
		num := strconv.Itoa(i)

		// Calculate hash for string num.
		sum := sha1.Sum([]byte(num))

		// Print prefix: 5-digit-number: hex encoded hash
		fmt.Printf("%s: %05d: %x\n", prefix, i, sum)
	}

	fmt.Println("Completed", prefix)
}

O/P:
Create Goroutines
Waiting To Finish
B: 00001: 356a192b7913b04c54574d18c28d46e6395428ab
B: 00002: da4b9237bacccdf19c0760cab7aec4a8359010b0
B: 00003: 77de68daecd823babbb58edb1c8e14d7106e83bb
B: 00004: 1b6453892473a467d07372d45eb05abc2031647a
B: 00005: ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4
B: 00006: c1dfd96eea8cc2b62785275bca38ac261256e278
B: 00007: 902ba3cda1883801594b6e1b452790cc53948fda
B: 00008: fe5dbbcea5ce7e2988b8c69bcfdfde8904aabc1f
B: 00009: 0ade7c2cf97f75d009975f4d720d1fa6c19f4897
B: 00010: b1d5781111d84f7b3fe45a0852e59758cd7a87e5
Completed B
A: 00001: 356a192b7913b04c54574d18c28d46e6395428ab
A: 00002: da4b9237bacccdf19c0760cab7aec4a8359010b0
A: 00003: 77de68daecd823babbb58edb1c8e14d7106e83bb
A: 00004: 1b6453892473a467d07372d45eb05abc2031647a
A: 00005: ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4
A: 00006: c1dfd96eea8cc2b62785275bca38ac261256e278
A: 00007: 902ba3cda1883801594b6e1b452790cc53948fda
A: 00008: fe5dbbcea5ce7e2988b8c69bcfdfde8904aabc1f
A: 00009: 0ade7c2cf97f75d009975f4d720d1fa6c19f4897
A: 00010: b1d5781111d84f7b3fe45a0852e59758cd7a87e5
Completed A
Terminating Program
```

In the above code there are many context switch happens between A and B in the middle of A or B goroutine before they are completed, if we run the code with `i` value 50000. So Go scheduler will distributes the processor time between 2 goroutines, so that it gives a peception like both the goroutines are runnig at the same time. 

## Goroutines and parallelism
```
/ Sample program to show how to create goroutines and
// how the goroutine scheduler behaves with two contexts.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func init() {

	// Allocate two logical processors for the scheduler to use.
	runtime.GOMAXPROCS(2)
}

func main() {

	// wg is used to wait for the program to finish.
	// Add a count of two, one for each goroutine.
	var wg sync.WaitGroup
	wg.Add(2)

	fmt.Println("Start Goroutines")

	// Declare an anonymous function and create a goroutine.
	go func() {

		// Display the alphabet three times.
		for count := 0; count < 3; count++ {
			for r := 'a'; r <= 'z'; r++ {
				fmt.Printf("%c ", r)
			}
		}

		// Tell main we are done.
		wg.Done()
	}()

	// Declare an anonymous function and create a goroutine.
	go func() {

		// Display the alphabet three times.
		for count := 0; count < 3; count++ {
			for r := 'A'; r <= 'Z'; r++ {
				fmt.Printf("%c ", r)
			}
		}

		// Tell main we are done.
		wg.Done()
	}()

	// Wait for the goroutines to finish.
	fmt.Println("Waiting To Finish")
	wg.Wait()

	fmt.Println("\nTerminating Program")
}

O/P:
Start Goroutines
Waiting To Finish
a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n A B C D E F G H I J K L M N O P Q R S T U V W X Y Z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z A B C D E F G H I J K L M N O P Q R S T U V W X Y o p q r s t u v w x y z a b c d e f g h i j k l m n o p q r s t u v w x y z Z 
Terminating Program
```

In the above code we are using 2 core processor by setting the value to `runtime.GOMAXPROCS(2)`. So both of the goroutines run at the same time in the available 2 cores or 2 P's or 2 OS threads and we can see mix of output from both goroutines at the same time not one after the other. 

So now that we have went from one P(core) or thread to 2 thread or P, we are now a multi-threaded Go program. Go routines now can run in parallel and this is where synchronization, orchestration really become important.


## Goroutime Examples:
- Goroutines and concurrency: https://go.dev/play/p/4n6G3uRDc83
- Goroutine time slicing: https://go.dev/play/p/QtNVo1nb4uQ
- Goroutines and parallelism: https://go.dev/play/p/ybZ84UcLW81

