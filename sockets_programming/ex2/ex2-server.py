import socket
import threading

HEADER = 64 #header size
PORT = 5050 #port number
SERVER = socket.gethostbyname(socket.gethostname()) #server IP
ADDR = (SERVER, PORT) #server address
FORMAT = 'utf-8'  #format
DISCONNECT_MESSAGE = "!DISCONNECT"  #for disconnecting

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #IPv4, TCP protocol
server.bind(ADDR) #bind server

#handle client connections
def handle_client(conn, addr):
  #printing out new connection
  print(f"[NEW CONNECTION {addr} connected.")

  #boolean for connection
  connected = True

  #while loop for connection
  while connected:
    #when client sents message, it has to send headers first where it tells the lenght of coming message
    msg_len = conn.recv(HEADER).decode(FORMAT)
    #if there is a message
    if msg_len:
      #change it to integer
      msg_len = int(msg_len)
      #excepting to recerve message that long the header told
      msg = conn.recv(msg_len).decode(FORMAT)

      #if message is disconnect message (in line 10), change the connected boolean to false, exits loop
      if msg == DISCONNECT_MESSAGE:
        print(f"[{addr}] disconnected")
        connected = False
      #if message is something else than disconnect message, prints the address and message
      #and sends back RECEIVED (so the receiving end knows it received somethink) and the message
      else:
        print(f"[{addr}] {msg}")
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        msg = msg.encode(FORMAT)
        conn.send(send_len)
        conn.send(msg)
    
  conn.close()

#server start function
def start():
  ##start listening server
  server.listen()
  print(f"[LISTENING] Server is listening on {SERVER}")

  #while loop for connections
  while True:
    #waits for incoming connection, if connected, returns new socket and the client address
    conn, addr = server.accept()
    #starts new thread if connected
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    #prints how many clients are connected everytime someone enters the server
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")

#start the server
print("[STARTING] Server is starting...")
start()