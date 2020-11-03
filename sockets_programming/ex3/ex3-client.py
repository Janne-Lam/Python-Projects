import threading
import socket
import argparse
import os
import time

global HEADER

class Send(threading.Thread):

  """
  Sock = connected socket
  name = username provided by the user
  Send thread listens client input from cmd and sends it to the server.
  """
  def __init__(self, sock, name):
    super().__init__()
    self.sock = sock
    self.name = name

  def run(self):
    HEADER = 64
    while True:
      msg = input() #the message client writes
      msg = str(self.name + ": " + msg)
      #by typing QUIT the program will send quit message to server, close the connection and exit the app
      if msg:
        msg = msg.encode('utf-8')
        msg_len = len(msg)  #message length
        send_len = str(msg_len).encode('utf-8') 
        send_len += b' '* (HEADER - len(send_len))

        self.sock.send(send_len)  #sending message length
        self.sock.send(msg) #sending the actual message

class Receive(threading.Thread):
  """
  sock = connected socket
  name = username provided by the user
  Receiving thread listens incoming messages from the server
  """
  def __init__(self, sock, name):
    super().__init__()
    self.sock = sock
    self.name = name

  def run(self):
    HEADER = 64
    while True:
      #receiving a message from the server
      msg_len = self.sock.recv(HEADER).decode('utf-8')
      if msg_len:
        msg_len = int(msg_len)  #convert message lenght into integer
        msg = self.sock.recv(msg_len).decode('utf-8') #receiving the actual message
        if msg == 'QUIT':
          print('Lost connection to the server.')
          print('\nQuitting')
          self.sock.close()
          os._exit(0)
        else:
          print(msg)

class Client:
  """
  client-server connection
  host = server's IP address
  port = server's port number
  sock = connected socket
  name = username of the Client
  """
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def start(self):
    #trying to connect the server
    print('Trying to connect to {}:{}...'.format(self.host, self.port))
    self.sock.connect((self.host, self.port))
    print('Successfully connected to {}:{}'.format(self.host, self.port))
    print()
    #add your username
    username = input('Enter your username: ')

    #start send and receive threads
    send = Send(self.sock, username)
    receive = Receive(self.sock, username)

    send.start()
    receive.start()

    #send message to server that this client has connected
    print("\rAll set!\n")

if __name__ == '__main__':
  SERVER = socket.gethostbyname(socket.gethostname()) #ip address
  PORT = 5050 #port number

  client = Client(SERVER, PORT)
  client.start()