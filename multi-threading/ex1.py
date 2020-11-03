import threading

#worker function, where the print happens
def worker(number):
  print('Hello world: {}'.format(number))

number = 0
for i in range(4): #for loop to start 4 threads
  number += 1
  thread = threading.Thread(target=worker, args=(number,)) #starts new thread
  thread.start() #start a new thread