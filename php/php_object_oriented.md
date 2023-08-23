# Object Oriented in PHP

## Class/Object
With object oriented programming, we can encapsulate code into classes. A class is like a blueprint or a template. We can then use this template to create objects of that class.

Define a class and then create an instance of this class by new keyword followed by class name and optional paranthesis which is recommeded to have.
```
Item.php

<?php
class Item
{

}
```

```
example.php

<?php
require 'Item.php';

$my_item = new Item();
var_dump($my_item);

$item2 = new Item();
var_dump($item2);

```

## Object Attributes

Objects of a class have certain attributes or properties. For example, a user has a username maybe an email address and so on. Properties are declared as variables inside the class definition. We use access specifiers to set the visibility of these variables like public, private etc. To access a property of an object, we use a dash and the greater than symbol. If you don't specify a value for a property, by default,
it's set to null. When we declare a property in the class, we can optionally give it a default value. PHP allows to assign a new property on the object that we haven't defined in its class definition. 

```
example.php

<?php
require 'Item.php';

$my_item = new Item();
$my_item->name = 'Example';
$my_item->description = 'A new description';
$my_item->price = 2.99;

var_dump($my_item);

```

```
Item.php

<?php

class Item
{
    public $name;
    public $description = 'This is the default';
}

```

## Object Functions/Methods
In addition to properties, we can add functions to a class. These are referred to as class methods. Methods are simply functions that an individual object can perform. Functions inside classes are defined in exactly the same way you would define a regular function. Then we call the functions in the same way we'd access a property by using the hyphen and greater than symbol on the object variable. Inside a method, we can use a special variable called `$this`, which represents the current object. We can access properties and call methods using `$this` object variable.

```
example.php

<?php

require 'Item.php';

$my_item = new Item();
$my_item->name = 'An example';

$item2 = new Item();
$item2->name = 'Another example';

echo $my_item->getName(), " ", $item2->getName();

```

```
Item.php

<?php

class Item
{

    public $name;

    public $description = 'This is the default';

    function sayHello() {
        echo "Hello";
    }

    function getName() {
        return $this->name;
    }
}

```

## Object initialization/ the constructor method

There's a special type of method we can add to a class called a constructor. If we add a method like construct prefixed with two underscored characters (__construct), then this method is called whenever we create a new object of this class. You can use the constructor method for whatever you like but it's commonly used to initialize properties. As with any function, we can pass data into it using arguments.

Adding a constructor to a class is optional but if you do add one, it has to have this name. As with any function, you can add as many arguments as you like and make some of them optional if you need to. You can place the constructor method wherever you like, but it's common to put it before any other methods.

```
example.php

<?php

require 'Item.php';

$my_item = new Item('Huge', 'A big item');
var_dump($my_item);

```

```
Item.php

<?php

class Item
{
    public $name;

    public $description = 'This is the default';

    function __construct($name, $description) {
        $this->name = $name;
        $this->description = $description;
    }

    function sayHello() {
        echo "Hello";
    }

    function getName() {
        return $this->name;
    }
}

```
We also have `__destruct` function which will run, once we are done using all the object of a class. So it will be called when no other references to a certain object and can be used for clean up closing connections etc. 


### Magic Methods in PHP
- We can use `__CLASS__` variable to get the name of the current class that you are in.
- We can use `__get` and `__set` methods instead of typing multiple setters and getters methods for variables
```
public function __get($property) {
    if(property_exists($this, $property)) {
        return $this->$property;
    }
}

echo $user->__get('name');
```
 

## Access Control in PHP(Public and Private)
We can declare attributes/properties in a class as public or private. When we declare them as public, which means they can be accessible from outside of the class from anywhere. But when we declare them as private, then they can accessible only from within the same class or else it will throw an error. Doing private is useful if you have a property that you want to use internally inside the class, but you don't want code using the class to be able to change its value.

We can restrict the visibility of methods too. By default, a method is public if you don't specify it otherwise. If we specify a method as private, then it can only be accessed from within that class from other methods.

```
example.php

<?php

require 'Item.php';

$my_item = new Item('Huge', 'A big item');

var_dump($my_item->getName()); ==> Thows an error here since getName can not be accessible.

```

```
Item.php

<?php

class Item
{
    private $name;

    public $description = 'This is the default';

    public function __construct($name, $description) {
        $this->name = $name;
        $this->description = $description;
    }

    public function sayHello()
    {
        echo "Hello";
    }

    private function getName()
    {
        return $this->name;
    }
}

```

## Static properties and methods
The values of object properties and the results of calling object methods are specific to a particular object. 

In addition to this, we can also create static properties and methods. A static property or method can be accessed without first creating an object of the class. To make it static, we add the static keyword to a property. The order of keywords before the property doesn't matter to php, you can put public static or static public if you like. The static property is not tied to a specific object rather to the whole class. We can also have static methods.

To refer to a static variable or method inside a class, we use the static keyword with two colons before the property or method(`static::$count`) or self keyword(`self::$count`). To refer to a static method or property from outside the class, we use the class name, two colons, then the property or method(`Item::$count`).

```
example.php

<?php

require 'Item.php';

$my_item = new Item('Huge', 'A big item');
$item2 = new Item('Small', 'A tiny item');

Item::showCount();

$my_item->name = "A new name";
echo $my_item->getName();
```

```
Item.php

<?php

class Item
{
    public $name;

    public $description = 'This is the default';

    public static $count = 0;

    public function __construct($name, $description) {
        $this->name = $name;
        $this->description = $description;
        static::$count++;
    }

    public function sayHello() {
        echo "Hello";
    }

    public function getName() {
        return $this->name;
    }

    public static function showCount() {
        echo static::$count;
    }
}

```

## Constants in PHP
To create a constant in php, we use the define function passing in a name and a value for the constant. For example `define("MAXIMUM", 100)`. What you can't do with constants is change their value. Once defined their value remains constant, hence they're called constants. We will get an error, if we try to define the same constant again. 

Constants are also used inside classes commonly to define values for use with the classes methods. However we can't use the defined function inside a class. To define a constant inside a class, we use the const keyword like `const MAXIMUM = 100. Constants are traditionally defined at the top of a class definition. To use this constant, we access it in the same way as a static property or method, specifying the class name,
two colons and the name of the constant like `Item::MAXIMUM`. Like static properties and methods, constants
aren't tied to a specific instance of the class. As for visibility, by default, constants are public. But you can change this as with properties and methods if you need to.

```
example.php
<?php

require 'Item.php';

$my_item = new Item();

$count = 0;
$count++;

define('MAXIMUM', 100); ==> Use define function to define a constant in a php code
define('COLOUR', 'red');

echo Item::MAX_LENGTH;

```

```
Item.php

<?php

class Item
{
    public CONST MAX_LENGTH = 24; ==> Use CONST to define a constant inside a method

    public $name;

    public $description;

    public function getName()
    {
        return $this->name;
    }

    public function setName($name)
    {
        $this->name = $name;
    }
}

```

## Inheritance in PHP

Inheritance is simply a way of reusing code and avoiding repetition. We do this by putting `extends` keyword after the class name followed by the name of the class we're extending. When one class extends another, all of the properties and methods of the class being extended are inherited by the class that's extending it.

```
example.php

<?php

require 'Item.php';
require 'Book.php';

$my_item = new Item();
$my_item->name = "TV";

echo $my_item->getListingDescription();


echo "<br>";


$book = new Book();
$book->name = 'Hamlet';
$book->author = 'Shakespeare';

echo $book->getListingDescription();

```

```
Item.php

<?php

class Item
{
    public $name;

    public function getListingDescription()
    {
        return $this->name;
    }
}
```

```
Book.php
<?php

class Book extends Item
{
    public $author;
}
```
Here Item class is refered as Parent class whereas Book class is refered as child class.

## Method Overriding in PHP

We can change how a method in the parent class works by overriding what it does in the child class. This is called method overriding. We can access the parent classes’ version of the method in child class through parent keyword followed by two colons and the name of the method(`parent::getDescription`).

```
example.php

<?php

require 'Item.php';
require 'Book.php';

$my_item = new Item();
$my_item->name = "TV";

echo $my_item->getListingDescription();

echo "<br>";

$book = new Book();
$book->name = 'Hamlet';
$book->author = 'Shakespeare';

echo $book->getListingDescription();
```

```
Item.php
<?php

class Item
{
    public $name;

    public function getListingDescription()
    {
        return "Item: " . $this->name;
    }
}
```

```
Book.php
<?php

class Book extends Item
{
    public $author;

    public function getListingDescription()
    {
        return parent::getListingDescription() . " by " . $this->author;
    }
}

```

## ## Access Control in PHP(Protected)
What if we want to make certain property inaccessible from outside the class but also be able to access it
inside methods in child classes? For such cases we make a property as `Protected`, so that child classes can see these properties from parent.

```
example.php

<?php

require 'Item.php';
require 'Book.php';

$my_item = new Item();

echo $my_item->code;

$book = new Book();

echo $book->getCode();

```

```
Item.php
<?php

class Item
{
    public $name;

    protected $code = 1234;

    public function getListingDescription()
    {
        return "Item: " . $this->name;
    }
}
```

```
Book.php
<?php

class Book extends Item
{
    public $author;

    public function getListingDescription()
    {
        return parent::getListingDescription() . " by " . $this->author;
    }

    public function getCode()
    {
        return $this->code;
    }
}
```