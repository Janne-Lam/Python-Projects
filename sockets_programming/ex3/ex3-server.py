import threading
import socket
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
      msg = input()
      msg = str(self.name + ": " + msg)
      #by typing QUIT the program will send quit message to server, close the connection and exit the app
      if msg:
        msg = msg.encode('utf-8')
        msg_len = len(msg)
        send_len = str(msg_len).encode('utf-8')
        send_len += b' '* (HEADER - len(send_len))

        self.sock.send(send_len)
        self.sock.send(msg)

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
        msg_len = int(msg_len)
        msg = self.sock.recv(msg_len).decode('utf-8')
        if msg == 'QUIT':
          print('Lost connection to the server.')
          print('\nQuitting')
          self.sock.close()
          os._exit(0)
        else:
          print(msg)

class Server(threading.Thread):
  def __init__(self, host, port):
    super().__init__()
    self.host = host
    self.port = port

  def run(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((self.host, self.port)) #bind the server
    sock.listen() #start listening
    print('Listening at', sock.getsockname())

    while True:
      conn, addr = sock.accept()  #waiting new connections
      print('Accepted a new connetion from {} to {}'.format(addr, conn.getsockname()))
      server_send = Send(conn, 'Server')
      server_send.start()

      server_receive = Receive(conn, 'Server')
      server_receive.start()


if __name__ == '__main__':
  SERVER = socket.gethostbyname(socket.gethostname())
  PORT = 5050

  server = Server(SERVER, PORT)
  server.start()