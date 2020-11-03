import threading
import socket
import os

class Server(threading.Thread):
  def __init__(self, host, port):
    super().__init__()
    self.connectionsTopic = []
    self.connectionsExample = []
    self.host = host
    self.port = port

  def run(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((self.host, self.port))

    sock.listen()
    print('Listening [{}]'.format(sock.getsockname()))

    while True:
      conn, addr = sock.accept()
      print('Accepted a new connection from {}'.format(conn.getpeername()))

      server_socket = ServerSocket(conn, addr, self)
      server_socket.start()

  def broadcast(self, msg_len, message, source, numb):
    if numb == 1:
      for connection in self.connectionsExample:
        if connection.addr != source:
          connection.send(msg_len, message)
    elif numb == 2:
      for connection in self.connectionsTopic:
        if connection.addr != source:
          connection.send(msg_len, message)

  def remove_connection(self, connection, numb):
    if numb == 1:
      self.connectionsExample.remove(connection)
    elif numb == 2:
      self.connectionsTopic.remove(connection)

class ServerSocket(threading.Thread):
  def __init__(self, conn, addr, server):
    super().__init__()
    self.conn = conn
    self.addr = addr
    self.server = server
    self.header = 64

  def run(self):
    connected = True
    while connected:
      msg_len = self.conn.recv(self.header).decode('utf-8')
      if msg_len:
        int_msg_len = int(msg_len)
        msg = self.conn.recv(int_msg_len).decode('utf-8')
        if msg == 'example':  #topic
          server.connectionsExample.append(self)  #1
        elif msg == 'topic':  #topic 2
          server.connectionsTopic.append(self)  #2

        elif msg != 'example' or 'topic':
          print('{} says {!r}'.format(self.addr, msg))
          if self.server.connectionsExample.__contains__(self):
            self.server.broadcast(msg_len, msg, self.addr, 1)
          elif self.server.connectionsTopic.__contains__(self):
            self.server.broadcast(msg_len, msg, self.addr, 2)
          else:
            connected = False

        else:
          if self.server.connectionsExample.__contains__(self):
            self.server.remove_connection(self, 1)
          elif self.server.connectionsTopic.__contains__(self):
            self.server.remove_connection(self, 2)
          connected = False

  def send(self, msg_len, message):
    self.conn.send(msg_len.encode('utf-8'))
    self.conn.send(message.encode('utf-8'))

if __name__ == '__main__':
  SERVER = socket.gethostbyname(socket.gethostname())
  PORT = 5050

  server = Server(SERVER, PORT)
  server.start()