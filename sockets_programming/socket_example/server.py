import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) #binding the server

def handle_client(conn, addr):
  print(f"[NEW CONNECTION {ADDR} connected.")
  connected = True #boolean if need to exit the loop with disconnect message

  while connected:
    #receiving the message header, where is the message lenght
    msg_len = conn.recv(HEADER).decode(FORMAT)
    if msg_len:
      msg_len = int(msg_len)
      #receiving the message
      msg = conn.recv(msg_len).decode(FORMAT)
      #if the clients sends disconnect message exit the loop and the server doesn't echo it back
      if msg == DISCONNECT_MESSAGE:
        print(f"[{ADDR}] disconnected")
        connected = False
      else:
        #prints the message in servers terminal
        print(f"[{ADDR}] {msg}")
        #echoes message back
        conn.send(f"RECEIVED: {msg}".encode(FORMAT))
    
  conn.close()

def start():
  #start listening the server
  server.listen()
  print(f"[LISTENING] Server is listening on {SERVER}")

  #can handle multiple clients
  while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")

print("[STARTING] Server is starting...")
start()

