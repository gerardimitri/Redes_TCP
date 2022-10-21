# -*- coding: utf-8 -*-

import socketTCP
# importamos utils completo
from utils import *

print('Creando socket - Servidor')
# armamos el socket no orientado a conexión
# server_socketTCP = SocketTCP()

# hacemos bind del server socket a la dirección server_address
address = ('localhost', 8001)
# server_socketTCP.bind(server_address)
# SERVER
server_socketTCP = socketTCP.SocketTCP()
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()

# test 1
buff_size = 16
full_message = connection_socketTCP.recv(buff_size)
print("Test 1 received:", full_message)
if full_message == "Mensje de len=16".encode(): print("Test 1: Passed")
else: print("Test 1: Failed")

# test 2
buff_size = 19
full_message = connection_socketTCP.recv(buff_size)
print("Test 2 received:", full_message)
if full_message == "Mensaje de largo 19".encode(): print("Test 2: Passed")
else: print("Test 2: Failed")

# test 3
buff_size = 14
message_part_1 = connection_socketTCP.recv(buff_size)
message_part_2 = connection_socketTCP.recv(buff_size)
print("Test 3 received:", message_part_1 + message_part_2)
if (message_part_1 + message_part_2) == "Mensaje de largo 19".encode(): print("Test 3: Passed")
else: print("Test 3: Failed")

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