## Queue (FIFO)

We can implement a queue by using below DS:
- List: Add an item from beginning with O(n) and remove an item from end with o(1). Or add an item at end with o(1) and remove an item from beginning with O(n)
- LinkedList: Adding or Removing at begining is O(1). And adding at end is O(1) but removing at end is O(n). So best combination is to use add(enqueue) at the end and removing(dequeue) at the beginning. Linked List has head and tail pointers, whereas Queue will have first and last pointers.

### Implement Queue using LinkedList
```
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Queue:
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_queue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next
        
    def enqueue(self, value):
        new_node = Node(value)
        if self.first is None:
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1
        return True

    def dequeue(self):
        if self.length == 0:
            return None
        temp = self.first
        if self.length == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
            temp.next = None
        self.length -= 1
        return temp

 

 
my_queue = Queue(1)
my_queue.enqueue(2)

# (2) Items - Returns 2 Node
print(my_queue.dequeue().value)
# (1) Item -  Returns 1 Node
print(my_queue.dequeue().value)
# (0) Items - Returns None
print(my_queue.dequeue())



"""
    EXPECTED OUTPUT:
    ----------------
    1
    2
    None

"""
```