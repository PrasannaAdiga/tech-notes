# Files
- Files are great storage that lasts beyond the execution of a program
- Built in open() function opens a file and returns a file object
```
open(path_to_file)
path_to_file = can be absolute or relative
open('/var/log/messages')
```
- Built in read() functin is used to read the file content
- Example:
```
hosts = open('/etc/hosts')
host_file_content = hosts.read()
print(host_file_content)
hosts.close()
```
- seek functin: seek(offset) -  change the current position to the given offset byte in a file while reading

## Automatically closing a file with `with` statement
```
print('Started reading a file')
with open('/etc/hosts') as hosts:
    print('File closed? {}'.format(hosts.closed))
    print(hosts.read())
print('Finished reading a file')
print('File closed? {}'.format(hosts.closed))

OP:
Started reading a file
File closed? False
127.0.0.1 localhost
Finished reading a file
File closed? true
```

## To read file one line at a time
```
with open('file.txt') as file:
    for line in file:
        print(line.rstrip())

OP:
line1
line2
line3
```

## File modes

- open(file, mode)
- mode can be r(read), w(write), x(create a new file and open it for writing), a(open for writing, appending to file)
- Use the function write() to write to a file
```
with open('file.txt', w) as file:
    file.write('line 1')
    file.write('line 2')

with open('file.txt') as file:
    print(file.read())
```

## Error handing
```
try: 
    contacts = open('contacts.txt').read()
except: 
    contacts = '' //If the file is not available assign an empty value
print(len(contacts))        
```

# Modules
- Python modules are files that have a .py extension
- They can implement a set of attributes(variables), methods(functions) and classes(types)
- A module can be included in another python program by using the `import` statement followed by the module name
```
import time
time.method_name()
time.attribute_name
```
- We can import entire module or a single method
```
import module_name
module_name.method_name()

from module_name import method_name1, method_name2
method_name1()
```