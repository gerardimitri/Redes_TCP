from audioop import add
import socket
from utils import * 

print('Creando socket - Cliente')
my_address = ('localhost', 10000)
# armamos el socket, los parámetros que recibe el socket indican el tipo de conexión
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

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
send_full_message(client_socket, send_message, end_of_message, my_address, buff_size_client)
print("... Mensaje enviado")

# y esperamos una respuesta
received_message, destination_address = receive_full_mesage(client_socket, buff_size_client, end_of_message)
print(' -> Respuesta del servidor: <<' + received_message.decode() + '>>')