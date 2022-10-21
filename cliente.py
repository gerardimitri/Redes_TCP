from utils import *
import socketTCP 
import sys

host = sys.argv[1]
port = int(sys.argv[2])

print('Creando socket - Cliente')
address = (host, port)
# definimos un mensaje de prueba
# filename = str(input("Archivo a enviar: "))
message = str(input("Archivo a enviar: "))
# with open(filename, "r") as file:
#     message = file.read()

# CLIENT
client_socketTCP = socketTCP.SocketTCP()
client_socketTCP.connect(address)
# test 0
message = message.encode()
client_socketTCP.send(message)
# test 1
message = "Mensje de len=16".encode()
client_socketTCP.send(message)
# test 2
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message)
# test 3
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message)

# cierre de conexión
client_socketTCP.close()