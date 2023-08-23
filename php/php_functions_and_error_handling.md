# Functions in PHP

To create a function in php, we use the function keyword followed by the name of the function. Then we have some brackets where we put the functions arguments which we'll get to in a moment then some curly braces. Inside these braces, we put the code that we want to execute when the function is called. Then we call a function by putting its name followed by brackets.

When we declare a function with one or more arguments, we can include a default value for them. This means that when we call the function, we can omit that argument and its value will be the default we supplied. We can still pass in an argument and override this default,however.

To access data outside of the function, we need to return a value from it. To return a value we use the return statement followed by the value we want to return. When we call the function the return value can be accessed by using it directly or by assigning it to a variable. The return statement returns immediately from the function. Any code after the return statement isn't executed.

# Error Handling in PHP
PHP provides both errors and exceptions for handling errors which can be slightly confusing. Errors are generally used for language level errors like syntax errors. Exceptions are the errors you get when using classes and objects. We can use try-catch blocks to handle any errors or exceptions. 