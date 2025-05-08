# OOP
- We can define a class which is blueprint whch has single or multiple attributes and methods
```
#!/usr/bin/python3
class Employee:
    name = "Ben"
    designation = "Sales Executive"
    salesMadeThisWeek = 6

    def hasAchievedTarget(self): # default parameter methods will accept to access classes attributes
        if self.salesMadeThisWeek > 5:
            print('Target has been achieved!')
        else:
            print('Target has not been achieved!')    

employeeOne = Employee()
print(employeeOne.hasAchievedTarget())
OP:
Target has been achieved!
```

## Attributes, methods and initialize

### Attributes 
- Class Attributes: 
    - Every object of this class will get the same value. Common for all the intsances of a class
    - Class attributes are accessed through class name `Employee.attribute_name`

    ```
    class Employee:
        numberOfWorkingHours = 40

    employee1 = Employee()
    employee2 = Employee()
    print(employee1.numberOfWorkingHours) // 40
    print(employee2.numberOfWorkingHours) // 40  

    Employee.numberOfWorkingHours = 45 // To change the class attribute use `className.variableName`
    print(employee1.numberOfWorkingHours) // 45
    print(employee2.numberOfWorkingHours) // 45  
    ```
    
- Instance Attributes: 
    - Each object has its own value
    - instance attributes are accessed through `self` `self.attribute_name`

    ```
    class Employee:

    employee1 = Employee()
    employee2 = Employee()

    employee1.name = "John"
    employee2.name = "Cena"

    print(employee1.name) // John
    print(employee2.name) // Cena 
    ```
    
    - It first check if there is a instance attribute with the same name, and if it does not found, then it will try to check if there is any class attribute with the same name. If its not found in both the cases, it throws an error.

### Methods

- Static Method: 
    - static methods are those methods which does not take `self` parameter. These methods are attached to class
    - A method that does not have access to any of the instance attributes of a class is called a static method.
    - Static method uses a decorator @staticmethod to indicate this method will not be taking the default self parameter.

    ```
    class Employee:
    @staticmethod
    def welcomeMessage(): // now python does not throw error even though self parameter is defined because of decorator
        print('Welcome user') 

    employee = Employee()
    employee.welcomeMessage() 
    ```
    - Here @staticmethod is a decorator. Decorator is a function that takes another function and extends their functionality
- Instance Method: 
    - instance methods are those which takes `self` parameter. These methods are attached to each instances
    - A method which can access the instance attributes of a class by making use of self object is called an instance method

    ```
    class Employee:
        def employeeDetails(self):
            pass // pass statement means do nothing

    employee = Employee()
    employee.employeeDetails() 
    ```
### Initialize (init() method)
- An init method is the constructor of a class that can be used to initialize data members of that class.
- It is the first method that is being called on creation of an object.
- We can define init method to fully initialize an object

    ```
    class Employee:
        def __init__(self, name): 
            print("Welcome!")
            self.name = name

        def displayEmployeeDetails():
            print(self.name)    
    
    employee1 = Employee("Mark") # This would print Welcome!
    employee2 = Employee("Mathew") # Welcome!

    employee1.displayEmployeeDetails() // Mark
    employee2.displayEmployeeDetails() // Mathew
    ```

### self parameter
- Every instance method accepts has a default parameter that is being accepted. By convention, this parameter is named self.
- The self parameter is used to refer to the attributes of that instance of the class

```
class Employee:
    def employeeDetails():
        pass // pass statement means do nothing

employee = Employee()
employee.employeeDetails() // This will throw error. TypeError: employeeDetails() takes 0 positional arguments but was given 1
```
Reason this fail is, when we make call `employee.employeeDetails()`, python internally will convert this call as:
```
Employee.employeeDetails(employee)
```
makes a call to this method through class referance by passing the actual object reference as argument. But in the actual method definition we do not have this parameter.

Hence we must define each method with default parameter as `def employeeDetails(self):`


## Abstraction and Encapsulation
- Hiding the implementation details from the end user is called as encapsulation
- Abstraction is the process of steps followed to achieve encapsulation

```
#!/usr/bin/python3
class Library:
    def __init__(self, listOfBooks):
        self.availableBooks = listOfBooks

    def displayAvailableBooks(self):
        print('Available Books: ')
        for availableBook in self.availableBooks:
            print(availableBook)

    def lendBook(self, lendBook):
        if lendBook in self.availableBooks:
            print('You have borrowed the book')
            self.availableBooks.remove(lendBook)
        else:
            print('Sorry, the book is not available in the list')   

    def addBook(self, addBook):
        self.availableBooks.append(addBook)
        print('You have returned the book. Thank you!')

class Customer:
    def requestBook(self):
        print('Enter the name of the book you would like to borrow: ')
        self.book = input()
        return self.book

    def returnBook(self):
        print('Enter the name of the book you would like to return: ')
        self.book = input()
        return self.book


library = Library(['Think and Grow Rich', 'Who Will Cry When You Die', 'For One More Day'])
customer = Customer()     

while True:
    print('Enter 1 to display books')
    print('Enter 2 to request a book')
    print('Enter 3 to return a book')
    print('Enter 4 to quit')

    userChoice = int(input())

    if userChoice is 1: 
        library.displayAvailableBooks()
    elif userChoice is 2:
        requestedBook = customer.requestBook()  
        library.lendBook(requestedBook)
    elif userChoice is 3:
        returnBook = customer.returnBook()
        library.addBook(returnBook)      
    elif userChoice is 4:
        quit()
```

In the above example, we have performed encapsulation within classes and we have hidden all the implementation details
from main program and we have only provided layers of abstraction by calling methods from program which gave an access to the data within class.

## Inheritance

### Single Inheritance
Inherits the property and method from one base class

```
#!/usr/bin/python3
class Apple: (Base Class)
    manufacturer = 'Apple Inc.'
    contactWebsite = 'www.apple.com/contact'

    def contactDetails(self):
        print('To contact us, log on to ',self.contactWebsite)

class Macbook(Apple): # Extends Apple (Derived Class)  
    def __init__(self):
        self.yearOfManufacture = 2017

    def manufactureDetails(self):
        print('This MacBook was manufactured in the year {} by {}'.format(self.yearOfManufacture, self.manufacturer))

macbook = Macbook()

macbook.manufactureDetails() # own methdd
macbook.contactDetails() # inherited method

O/P:
This MacBook was manufactured in the year 2017 by Apple Inc.
To contact us, log on to  www.apple.com/contact
```

### Multiple Inheritance

Inherits the property and method from more than one base class

```
#!/usr/bin/python3
class OS:
    multitasking = True
    name = 'Mac OS'

class Apple:
    website = 'www.apple.com'
    name = 'Apple'

class Macbook(OS, Apple):
    def __init__(self):
        if self.multitasking: # field from first base class
            print('This is a multitasking system. Visit {} for more details'.format(self.website)) # field from second base class
            print('Name: ', self.name) # If there are same fields in multiple base classes, then depending on the 
                                       # order we extends the base class, field will be selected. Here we imported OS first so its name field will be printed

macbook = Macbook()

O/P:
This is a multitasking system. Visit www.apple.com for more details
Name:  Mac OS
```

### Multilevel Inheritance
Class C extends B and class B extends class A. Now Class C has multilevel inheritance, since it has inherited from 2 base classes
```
#!/usr/bin/python3
class MusicalInstrument:
    numberOfMajorKeys = 12

class StringInstrument(MusicalInstrument):
    typeOfWood = 'Tonewood'

class Guitar(StringInstrument):
    def __init__(self):
        self.numberOfString = 6
        print('This guitar consist of {} strings. It is made of {} and it can play {} keys'.format(self.numberOfString, self.typeOfWood, self.numberOfMajorKeys)) 

guitar = Guitar()        

O/P:
This guitar consist of 6 strings. It is made of Tonewood and it can play 12 keys
```

## Access Specifier
- public: use camel case name like `memberName`. Accessible from anywhere.
- protected: user camel case name with single `_` like `_memberName`. Accessible from within the class and its sub classes
- private: user camel case name with double `__` like `__memberName`. Accessible from within the class only.

```
#!/usr/bin/python3
class Car:
    numberOfWheels = 4
    _color = 'Black'
    __yearOfManufacture = 2017 # internally this will be stored as _Car____yearOfManufacture

    def __init__(self):
        print('Private attribute yearOfManufacture: ', self.__yearOfManufacture) 


class BMW(Car):
    def __init__(self):
        print('protected attribute color: ', (self._color))           

car = Car()
print('Public attribute numberOfWheels: ', car.numberOfWheels) 

bmw = BMW()

print('Private attribute yearOfManufacture: ', car._Car__yearOfManufacture) 

O/P:
Private attribute yearOfManufacture:  2017
Public attribute numberOfWheels:  4
protected attribute color:  Black
Private attribute yearOfManufacture:  2017
```

## Polymorphism
In python consider th eoperator `+`, if behaves differently when we try to add 2 integer or when we try to concatenate 2 strings
2 ways to achieve polymorphism:
- Method Overriding: It overides the base class method and have its own logic. Method name and it's signature must be same.
- Method Overloading: It overloads the base class method and have its own logic. Method name must be same but its signature should be different.

### Overriding and the super() method
```
#!/usr/bin/python3
class Employee:
    def setNumberOfWorkingHours(self):
        self.numberOfWorkingHours = 40

    def displayNumberOfWorkingHours(self):
        print(self.numberOfWorkingHours)

class Trainee(Employee):
    def setNumberOfWorkingHours(self): # This is method overriding
        self.numberOfWorkingHours = 45

    def resetNumberOfWorkingHours(self):
        super().setNumberOfWorkingHours() # Call the base classes methods/attributes through super function

employee = Employee()

employee.setNumberOfWorkingHours()
print('Number of working hours of employee: ', end = ' ')
employee.displayNumberOfWorkingHours()

trainee = Trainee()
trainee.setNumberOfWorkingHours()
print('Number of working hours of trainee: ', end = ' ')
trainee.displayNumberOfWorkingHours()

trainee.resetNumberOfWorkingHours()
print('Number of working hours of trainee after reset: ', end = ' ')
trainee.displayNumberOfWorkingHours()

O/P:
Number of working hours of employee:  40
Number of working hours of trainee:  45
Number of working hours of trainee after reset:  40
```

### Daimond shape problem in multiple inheritance

#### Case 1: method() function is not overridden in class B and C
```
#!/usr/bin/python3
class A:
    def method(self):
        print('This method belongs to class A')

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

d = D() # Should have access to class A, B and C
d.method()

O/P:
This method belongs to class A
```

#### Case 2: method() function is overridden in class B but not in class C
```
#!/usr/bin/python3
class A:
    def method(self):
        print('This method belongs to class A')

class B(A):
    def method(self):
        print('This method belongs to class B')

class C(A):
    pass

class D(B, C):
    pass

d = D() # Should have access to class A, B and C
d.method()

O/P:
This method belongs to class B
```

#### Case 1: method() function is overridden in class C but not in class B
```
#!/usr/bin/python3
class A:
    def method(self):
        print('This method belongs to class A')

class B(A):
    pass

class C(A):
    def method(self):
        print('This method belongs to class C')

class D(B, C):
    pass

d = D() # Should have access to class A, B and C
d.method()

O/P:
This method belongs to class C
```

#### Case 1: method() function is overridden in both class B and C
```
#!/usr/bin/python3
class A:
    def method(self):
        print('This method belongs to class A')

class B(A):
    def method(self):
        print('This method belongs to class B')

class C(A):
    def method(self):
        print('This method belongs to class C')

class D(B, C):
    pass

d = D() # Should have access to class A, B and C
d.method()

O/P:
This method belongs to class B
```

In the above example `method resolution order` which is nothing but the order in which the classes are inherited in class C, makes the decision to which overridden function is called. Since Class B is inherited before to class C (class D(B, C)) class B's function will be executed.

### Overloading an Operator
```
#!/usr/bin/python3
class Square():
    def __init__(self, side):
        self.side = side

    def __add__(squareOne, squareTwo): # Overrides the inbuild __add__ function which will be called when we use `+` operator
        return ((4 * squareOne.side) + (4 * squareTwo.side))    

squareOne = Square(5)
squareTwo = Square(10)

print('Sum of sides of both the squares = ', squareOne + squareTwo) # When we use `+` operator the corresponding `__add__` function will be called in case while adding 2 integer or while concatinating 2 string

O/P:
Sum of sides of both the squares =  60
```

## Abstrcact Base Class
Forcing derived classes to implement an abstract method by using abstrct base calsses
```
#!/usr/bin/python3
from abc import ABCMeta, abstractmethod
class Shape(metaclass = ABCMeta): # This shape class is a abstract base class

    @abstractmethod
    def area(self):
        return 0

class Square(Shape):
    side = 4 

    def area(self):
        print('Area of side is ', self.side * self.side)

class Rectangle(Shape):
    length = 5
    width = 4

    def area(self):
        print('Area of rectangle is ', self.length * self.width)        


square = Square()
rectangle = Rectangle()

square.area()
rectangle.area()

O/P:
Area of side is  16
Area of rectangle is  20
```