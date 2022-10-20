from utils import *
from socketTCP import SocketTCP

print('Creando socket - Cliente')
address = ('localhost', 10000)
# armamos el socket, los parámetros que recibe el socket indican el tipo de conexión
client_socketTCP = SocketTCP()
client_socketTCP.connect(address)

# mandamos un mensajito
print("... Mandamos cositas")

# definimos un mensaje y una secuencia indicando el fin del mensaje
filename = str(input("Archivo a enviar: "))
message = ""
with open(filename, "r") as file:
    message = file.read()

# socket debe recibir bytes, por lo que encodeamos el mensaje
send_message = (message + end_of_message).encode()

# enviamos el mensaje a través del socket
send_full_message(client_socketTCP, send_message, end_of_message, address, buff_size_client)
print("... Mensaje enviado")

# y esperamos una respuesta
received_message, destination_address = receive_full_mesage(client_socketTCP, buff_size_receive, end_of_message)
print(' -> Respuesta del servidor: <<' + received_message.decode() + '>>')