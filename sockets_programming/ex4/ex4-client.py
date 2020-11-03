import threading
import socket
import os
import time
import select

class Send(threading.Thread):

  def __init__(self, sock, name):
    super().__init__()
    self.sock = sock
    self.name = name

  def run(self):
    HEADER = 64
    while True:
      msg = input('{}: '.format(self.name))
      msg = str(self.name + ": " + msg)
      #by typing QUIT the program will send quit message to server, close the connection and exit the app
      if msg != '':
        #Send message to server
        msg = msg.encode('utf-8')
        msg_len = len(msg)
        send_len = str(msg_len).encode('utf-8')
        send_len += b' '*(HEADER - len(send_len))
        self.sock.send(send_len)
        self.sock.send(msg)
      else:
        print('\nQuitting...')
        time.sleep(1)
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):
  def __init__(self, sock):
    super().__init__()
    self.sock = sock

  def run(self):
    HEADER = 64
    while True:
      #receiving a message from the server
      msg_len = self.sock.recv(HEADER).decode('utf-8')
      if msg_len:
        msg_len = int(msg_len)
        msg = self.sock.recv(msg_len).decode('utf-8')
        if msg:
          print(msg)
        else:
          print('Lost connection to the server.')
          print('\nQuitting')
          self.sock.close()
          os._exit(0)

class Client:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def start(self):
    HEADER = 64
    #trying to connect the server
    print('Trying to connect to {}:{}...'.format(self.host, self.port))

    looping = True
    while looping:
      sub_or_pub = input('Subscribe = s or Publish = p ?: ')
      if sub_or_pub == 'p':
        username = input('Enter your username: ')
        topic = str(input('Enter topic: '))
        try:
          if topic == 'example' or 'topic':    
            looping = False
            self.sock.connect((self.host, self.port))
            print('Successfully connected to {}:{}'.format(self.host, self.port))
            print()
            topic = topic.encode('utf-8')
            t_len = len(topic)
            send_t_len = str(t_len).encode('utf-8')
            send_t_len += b' '*(64 - len(send_t_len))
            self.sock.send(send_t_len)
            self.sock.send(topic)
            send = Send(self.sock, username)
            send.start()
          else:
            print('Wrong topic')
        except Exception:
          os._exit(0)
          
      elif sub_or_pub == 's':    
        topic = str(input('Enter topic: '))
        try:
          if topic == 'example' or 'topic':
            looping = False
            self.sock.connect((self.host, self.port))
            print('Successfully connected to {}:{}'.format(self.host, self.port))
            print()
            topic = topic.encode('utf-8')
            t_len = len(topic)
            send_t_len = str(t_len).encode('utf-8')
            send_t_len += b' '*(HEADER - len(send_t_len))
            self.sock.send(send_t_len)
            self.sock.send(topic) 
            resv = Receive(self.sock)
            resv.start()
          else:
            print('Wrong topic')
        except Exception:
          os._exit(0)
      else:
        print('Try again.')

    #send message to server that this client has connected
    print("Connected to server as '{}' and topic is '{}'".format(sub_or_pub, topic))

if __name__ == '__main__':
  SERVER = socket.gethostbyname(socket.gethostname())
  PORT = 5050

  client = Client(SERVER, PORT)
  client.start()