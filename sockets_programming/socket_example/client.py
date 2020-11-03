import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
  message = msg.encode(FORMAT)
  msg_length = len(message)
  send_length = str(msg_length).encode(FORMAT)
  send_length += b' ' * (HEADER - len(send_length))

  #sending the header where tells the lenght of the coming message
  client.send(send_length)
  client.send(message)

  #echo from server
  print(client.recv(2048).decode(FORMAT))

print("\n----------SEND MESSAGE TO SERVER-----------")
print("-----SEND DC IF YOU WANT TO DISCONNECT-----")
while True:
  message = str(input("Message to send: "))
  if message == "dc":
    send(DISCONNECT_MESSAGE)
    break
  else:
    send(message)


