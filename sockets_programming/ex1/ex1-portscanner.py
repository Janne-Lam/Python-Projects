import socket

for port in range(0, 100):
  try:
    print("There is", socket.getservbyport(port, 'tcp'), "service in port number", port)
  except Exception:
    print("There is no service in port number", port)