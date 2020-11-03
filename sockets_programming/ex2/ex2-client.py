import socket

HEADER = 64 #header size
PORT = 5050 #port
FORMAT = 'utf-8' #format
DISCONNECT_MESSAGE = "!DISCONNECT"  #disconnect message (same as in server)
SERVER = socket.gethostbyname(socket.gethostname()) #ip
ADDR = (SERVER, PORT) #server address

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP protocol
client.connect(ADDR)  #connect

#send message -function
def send(msg):
  #encoding the message
  message = msg.encode(FORMAT)
  #length of the message
  msg_length = len(message)
  #send the HEADER first where it tells to server, how long message is comming
  send_length = str(msg_length).encode(FORMAT) #looks like b'4'
  send_length += b' ' * (HEADER - len(send_length)) #looks like b'4[60 spaces]'
  #sends the header
  client.send(send_length)
  #sends the message
  client.send(message)
  #prints the answer from server
  recv_len = client.recv(HEADER).decode(FORMAT)
  if recv_len:
    recv_len = int(recv_len)
    print(client.recv(recv_len).decode(FORMAT))

#send whatever string you want
print("\n----------SEND MESSAGE TO SERVER-----------")
print("-----SEND DC IF YOU WANT TO DISCONNECT-----")
while True:
  message = str(input("Message to send: "))
  if message == "dc":
    send(DISCONNECT_MESSAGE)
    client.close()
    break
  else:
    send(message)