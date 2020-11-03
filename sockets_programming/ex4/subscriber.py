import threading
import socket
import os
import time
import select

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
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4 & TCP

  def start(self):
    input('Subscribe to channel: ')
    print('Trying to connect to {}:{}'.format(self.host, self.port))
    try:
      self.sock.connect((self.host, self.port))
    except Exception:
      print('Cannot connect to {}:{}'.format(self.host, self.port))
    finally:
      print('Successfully connected to {}:{}'.format(self.host, self.port))
      receive = Receive(self.sock)
      receive.start()


if __name__ == '__main__':
  SERVER = socket.gethostbyname(socket.gethostname())
  PORT = 5050

  client = Client(SERVER, PORT)
  client.start()