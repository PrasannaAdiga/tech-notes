# SOLID Principle

## Single Responsibilty principle

The Single Responsibility Principle states that a class or module should have only one reason to change. In other words, a type should have a single responsibility, making the code easier to understand and maintain.
Consider an example where we have a struct User and two methods, GetFullName() and Save():

```
type User struct {
    FirstName string
    LastName  string
}

func (u *User) GetFullName() string {
    return u.FirstName + " " + u.LastName
}

func (u *User) Save() error {
    // Save user to the database
    // ...
}
```

In this case, the User struct has two responsibilities: managing user data and saving it to the database. To adhere to the Single Responsibility Principle, we should separate these concerns:

```
type User struct {
    FirstName string
    LastName  string
}

func (u *User) GetFullName() string {
    return u.FirstName + " " + u.LastName
}

type UserRepository struct {
    // Database connection or other storage-related fields
}

func (r *UserRepository) Save(u *User) error {
    // Save user to the database
    // ...
}
```
Now, the User struct is only responsible for managing user data, while the UserRepository handles database operations.


**Applying SRP to Functions**

```
func ParseAndSave(filename string, db *EmployeeDB) {
 // 1. Read the file
 // 2. Parse the file content to get employee details
 // 3. Save the parsed data into the database
}
```

```
func ReadFile(filename string) []byte {
 // Code to read the file
}
func ParseEmployee(data []byte) *Employee {
 // Code to parse the data to get employee details
}
func (db *EmployeeDB) SaveEmployee(e *Employee) {
 // Code to save employee details into a database
}
```

## Open/Closed Principle

The Open/Closed Principle states that software entities (classes, modules, functions, etc.) should be open for extension but closed for modification. This principle encourages developers to write code that is flexible and can be extended without the need for significant modifications.
Suppose we have a simple function that calculates the area of a rectangle:

```
type Rectangle struct {
    Width  float64
    Height float64
}

func Area(rectangle *Rectangle) float64 {
    return rectangle.Width * rectangle.Height
}
If we need to add support for calculating the area of a circle, the current implementation would require modification:
type Circle struct {
    Radius float64
}

func Area(shape interface{}) float64 {
    switch s := shape.(type) {
    case *Rectangle:
        return s.Width * s.Height
    case *Circle:
        return math.Pi * math.Pow(s.Radius, 2)
    default:
        return 0
    }
}
```

To follow the Open/Closed Principle, we can define an interface and implement it for each shape:

```
type Shape interface {
    Area() float64
}

func (r *Rectangle) Area() float64 {
    return r.Width * r.Height
}

func (c *Circle) Area() float64 {
    return math.Pi * math.Pow(c.Radius, 2)
}
```

Now, our code is open for extension (we can add new shapes) but closed for modification (we don’t need to change the Area() function).

## Liskov Substitution Principle (LSP)

The Liskov Substitution Principle states that objects of a derived class should be able to replace objects of the base class without affecting the correctness of the program. In Golang, this principle applies to interfaces and their implementations, ensuring that the code remains consistent and reliable.

Consider an example with a simple Bird interface:

```
type Bird interface {
    Fly() string
}

type Pigeon struct{}

func (p *Pigeon) Fly() string {
    return "Pigeon is flying."
}

type Penguin struct{}

func (p *Penguin) Fly() string {
    return "Penguin is flying."
}
```

In this case, both Pigeon and Penguin implement the Bird interface. However, penguins cannot fly, so the Penguin implementation violates the Liskov Substitution Principle. To fix this, we can refactor our code to separate the concerns:

```
type Bird interface {
    MakeSound() string
}

type FlyingBird interface {
    Bird
    Fly() string
}

type Pigeon struct{}

func (p *Pigeon) MakeSound() string {
    return "Coo"
}

func (p *Pigeon) Fly() string {
    return "Pigeon is flying."
}

type Penguin struct{}

func (p *Penguin) MakeSound() string {
    return "Squawk"
}
```

Now, the Penguin type correctly implements the Bird interface without violating the LSP, and we've introduced a new FlyingBird interface for birds that can fly.

## Interface Segregation pattern

The Interface Segregation Principle states that clients should not be forced to depend on interfaces they do not use. This principle encourages creating smaller, more focused interfaces rather than large, monolithic ones.
Suppose we have a Document interface with methods for reading, writing, and printing:

```
type Document interface {
    Read() string
    Write(content string)
    Print() string
}

type TextDocument struct {
    content string
}

func (d *TextDocument) Read() string {
    return d.content
}

func (d *TextDocument) Write(content string) {
    d.content = content
}

func (d *TextDocument) Print() string {
    return "Printing: " + d.content
}
```

If we have a ReadOnlyDocument that should only support reading, the current interface forces us to implement unnecessary methods:

```
type ReadOnlyDocument struct {
    content string
}

func (d *ReadOnlyDocument) Read() string {
    return d.content
}

func (d *ReadOnlyDocument) Write(content string) {
    // Not supported
}

func (d *ReadOnlyDocument) Print() string {
    // Not supported
}
```

To follow the Interface Segregation Principle, we can break the Document interface into smaller, more focused interfaces:

```
type Reader interface {
    Read() string
}

type Writer interface {
    Write(content string)
}

type Printer interface {
    Print() string
}

type TextDocument struct {
    content string
}

// Implement Reader, Writer, and Printer for TextDocument

type ReadOnlyDocument struct {
    content string
}

// Implement only Reader for ReadOnlyDocument
```

Now, our ReadOnlyDocument only depends on the Reader interface, which aligns with the ISP.

## Dependency Inversion Principle (DIP)

The Dependency Inversion Principle states that high-level modules should not depend on low-level modules, but both should depend on abstractions. This principle promotes loose coupling between components, making the code more maintainable and testable.

Consider a simple example where a NotificationService sends notifications using an EmailService:

```
type EmailService struct{}

func (e *EmailService) Send(to string, message string) {
 // Send email
}

type NotificationService struct {
 emailService *EmailService
}

func (n *NotificationService) Notify(to string, message string) {
 n.emailService.Send(to, message)
}
```

In this case, the `NotificationService` directly depends on the `EmailService`, making it difficult to switch to another notification method (e.g., SMS) or test the `NotificationService` in isolation. To follow the Dependency Inversion Principle, we can introduce an interface and depend on that instead:

```
type MessageSender interface {
    Send(to string, message string)
}

type EmailService struct{}

func (e *EmailService) Send(to string, message string) {
    // Send email
}

type SMSService struct{}

func (s *SMSService) Send(to string, message string) {
    // Send SMS
}

type NotificationService struct {
    messageSender MessageSender
}

func (n *NotificationService) Notify(to string, message string) {
    n.messageSender.Send(to, message)
}
```

Now, the NotificationService depends on the MessageSender interface, allowing for more flexibility and easier testing.

### Referance:
https://medium.com/@vishal/understanding-solid-principles-in-golang-a-guide-with-examples-f887172782a3
