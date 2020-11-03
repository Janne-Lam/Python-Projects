import threading
import time
import inspect

var = 0
lock = threading.Lock()

class Thread(threading.Thread):
  def __init__(self, t, *args):
    threading.Thread.__init__(self, target=t, args=args)
    self.start()

def increament():  
  global var
  cal = inspect.getouterframes(inspect.currentframe())[1][3]
  print('inside {}()'.format(cal))  #print the function which is calling this function
  print(threading.currentThread())  #print the current thread
  
  #using the try-catch-finally to acquire and release the lcok
  try:
    lock.acquire()
    print('Lock acquired')
    var += 1  #increase the value of the global variable by 1
    print('Hello world: {}'.format(var))
    time.sleep(0.3) #to observe the threading better

  except Exception as e:
    print(str(e))

  #releasing the lock
  finally:
    lock.release()

#Function where we call Counter classes function increament
def hello_world():
  while var < 7:
    increament() #function where the print happens

def main():
  #starting two threads running same function
  for i in range(2):
    thread = Thread(hello_world)

if __name__ == '__main__':
  main()