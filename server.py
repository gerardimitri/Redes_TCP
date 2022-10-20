# -*- coding: utf-8 -*-
import socket
from socketTCP import SocketTCP
# importamos utils completo
from utils import *

print('Creando socket - Servidor')
# armamos el socket no orientado a conexión
# server_socketTCP = SocketTCP()

# hacemos bind del server socket a la dirección server_address
address = ('localhost', 10000)
# server_socketTCP.bind(server_address)
server_socketTCP = SocketTCP()
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()


# # nos quedamos esperando, como buen server, a que llegue una petición de conexión
# print('... Esperando clientes')
# while True:

#     # luego recibimos el mensaje usando la función receive_full_mesage en su version no orientada a conexión
#     received_message, server_address = receive_full_mesage(server_socketTCP, buff_size_receive, end_of_message)

#     print(' -> Se ha recibido el siguiente mensaje: {}'.format(received_message.decode()))

#     # respondemos lo mismo y le volvemos a añadir el end_of_message
#     response_message = received_message + end_of_message.encode()
#     #send_full_message(server_socket, response_message, end_of_message, server_address, buff_size_client)
#     #print("... Mensaje enviado")
#     # seguimos esperando por si llegan otras conexiones
#     break