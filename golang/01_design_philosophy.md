# Design Philosophy

## Integrity
We need to become very serious about reliability.

- Integrity is about every allocation, read and write of memory being accurate, consistent and efficient
- Integrity is about every data transformation being accurate, consistent and efficient.
- One simple way to reduce the number of bugs, and increase the integrity of your software, is to write less code.
- Write error handling everywhere

## Readability
We must structure our systems to be more comprehensible.

This is about writing simple code that is easier to read and understand without the need of mental exhaustion. Just as important, it's about not hiding the cost/impact of the code per line, function, package and the overall ecosystem it runs in.

## Simplicity
We must understand that simplicity is hard to design and complicated to build.

This is about hiding complexity. A lot of care and design must go into simplicity because this can cause more problems then good. It can create issues with readability and it can cause issues with performance.

## Performance
Perforamce in a software can come from 4 places

- Latency on networking, IO, disk IO
- Memory allocation and Garbage Collection
- How efficiently program will access data
- Algorithm efficiencies

Go can take the advantages of the hardware and it solves the first 3 perforamce issues. This gives us lot of performance built-in Go. 

Readability, writing clear and simple less code, testing, code reviews, re-factoring and good algorithms are the main blocks in Go to increase the performance from developers side.

## Best features of Go Programming language
- Compiled: Apps created in Go actually compile to native machine code and dont need any interpreter or virtual machine.
- Garbage collected
- Designed for multi core processor
- Easy to read codes
- Spend less time and money to develop an app
- Use Go for a range of apps: We can use Go for system and network programming, big data, machine learning, audio and video editing etc
- Worry less about the app crashing

## Install Go in Mac
- https://www.educative.io/answers/how-to-check-the-golang-version-on-mac
- Set below env variables:
    - export GOROOT=/usr/local/go 
    - export GOPATH=$HOME/go
    - export PATH=$GOPATH/bin:$GOROOT/bin:$PATH 



