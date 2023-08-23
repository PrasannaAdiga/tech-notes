# PHP

## Installation
Install the XAMPP software on your system and then run the Apache server which comes with it.
Edit the configuration of this Apache, to point to your any of the local folder, where we can write php files.

## Hello-world program
Just write a below `hellp.php` file under the folder which is configured in the Apache server.

```
<?php
echo "Hello, world!";
```
Access the above program in the browser with the url: `localhost/hellp.php` which will print `Hello, world!`

--- 

## Variables
See the below program:
```
<?php
$message = "Hello world!"; (defines a variable with $ sign)
echo $message;
```
Variables in php are represented by a dollar sign followed by the name of the variable. You can use a mixture of lowercase and uppercase letters, numbers and underscores for the name.

Use **var_dump** function to check wha value a variable contains like var_dump($message)

**Types of variables:**
- Strings: ex - $message = "Hello world!";  We can use single ot double quotes for the strings.
- Numbers: ex - $count = 10
- Floats: ex - $pi = 3.142
- Booleans: ex - $logged_in = true
- Null: It is used to represent a variable, that has no value. Ex - $user_id(no value assigned to it) or $user_id = null

PHP is a `loosely typed language`, agaisnt the strongly typed language like Java, where we no need to define type of variables. 

Php supports automatic `implicit type conversion instead of explicit type conversion`, where it can convert int type to float type and does the multiplication operation.

We can use `.` operator for the string concatination like `echo $name . " " . $message`

**Variable interpolation**: We can directly insert variable into the string if we are using double quotes instead of using string concatination. For example: `echo "Hello $name"`

Finally, if you want to insert a variable into a string and it's not clear where the variable ends. For example, if you have some letter characters straight after it, then you can surround the variable with curly braces, like this: `echo "Hello {$name}"`

---

## Arrays
2 ways to create an array in PHP. 
- We can use square brackets, followed by the list of values separated by commas, like `$count = [1, 2, 3];`.
- Alternatively, we can use the array function by writing the word array again followed by the list of values separated by commas inside round brackets like `$count = array(1, 2, 3);`

We can access each elements of an array by its index like $count[0], $count[1] etc. We can use        `var_dump($count[0])` to see the content of an array index.


The indexes are created automatically starting from zero. However, it's possible to manually specify the indexes when we create an array. To specify an element's index, write the index followed by an equal sign
and a greater than sign then the value of the element. The index can be any whole number you like. They don't have to be sequential. And you don't have to specify the index for all the elements. Any that aren't specified will be assigned automatically continuing on from the previous one.
```
$articles = [1 => "first post", 3 => "second post", "third index"];
```
You can also use a string as an index. Arrays with string indexes are sometimes referred to as associative arrays.
```
$articles = ["two" => "first post", "four" => "second post", "six" => "third post"];
```

Arrays can contain elements of any type.
```
$values = [
  "message": "Hello world!",
  "count": 50,
  "status": false,
  "result": null
]

var_dump($values);
```

You can also assign other variables as values of an array.
```
$count = 3;
$price = 9.99;
$values = [$count, $price];
```

We can also have multi-dimensional array like below:
```
$alice = [
  "name": "Alice",
  "age": 20
]

$bob = [
  "name": "bob",
  "age": 30
]

$people = [$alice, $bob];

$alice_age = $people[0]["age"]; ==>> to access 2 dimensional array
```
---

### looping over array
A loop allows us to run some code on each element of the array regardless of how many elements it has.
There are different types of loops in php, but the famous one is foreach loop.
```
$articles = ["first post", "second post", "third post"];
```
- foreach
```
foreach(articals as article) {
  echo article, ", ";
}
```

To access the index of each array element, we add another variable to the for each loop. 
```
foreach(articals as $index => article) {
  echo $index . " - " . article, ", ";
}
```

## Control Structures

### if

Add an array with no elements in it like $articles = [];

Call an empty function on this, which will return a boolean value depending on whether a variable is empty or not like `empty($articles)`

Now we can use if condition to check this like below:
```
if(empty($articles)) {
  echo 'The array is empty!';
} else {
  echo 'The array is not empty!';
}
```

```
$hour = 1;
if($hour < 12>) {
  echo 'good morning';
} elseif ($hour < 18>) {
  echo 'good afternoon';
} elseif ($hour < 22>) {
  echo 'good evening';
} else {
  echo 'good night!';
}

```

If you only have one statement in a code block, you can omit the curly braces in the if block.

We can use `==` operator to compare 2 variables like `var_dump(3 == 4)'

### for loop
```
for ($i=1; $i <=10; $i++) {
  echo $i . ", ";
}
```

### While loop
```
$month = 1;
while ($month <= 12>) {
    echo $month, ", ";
    $month = $month + 1;
}
```

### Switch
We can use switch statements instead of if-elseif-else blocks

with a switch statement once a case has matched the value it doesn't just execute the code for that case
rather it will continue down to the end of the switch statement. We need to do add a break command at the end of each block, to fix this.

```
$day = "Tue";

switch($day) {
  case "Mon":
    echo "Monday";
    break;
  case "Tue":
    echo "Tuesday";  
    break;
  case "Wed":
    echo "Wednesay";
    break;
  default:
    echo "Error";
    break;
}
```

---
