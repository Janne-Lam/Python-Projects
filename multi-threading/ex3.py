import threading
import time
import inspect

var = 0
global lock
lock = threading.Lock()

"""
class Counter, where it increases the value of var by 1 and prints
"hello world" then ran
"""
class HelloWorld(threading.Thread):
  def __init__(self):
    super().__init__()
    print('Inside hello_world')
    global lock
    self.lock = lock #when initializing class, init lock

  def run(self):  
    lock.acquire() #acquire the lock
    print('lock acquired')
    try:
      global var
      var += 1
      print('Hello world: {}'.format(var))  #printing "hello world: " + the variable

    except Exception as e:
      print('Excetion: {}'.format(e))
    
    finally:
      self.lock.release() #release the lock after printing

if __name__ == '__main__':
  for i in range(4):
    thread = HelloWorld() #the thread with params
    thread.start()  #start the thread