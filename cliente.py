from utils import *
import socketTCP 

print('Creando socket - Cliente')
address = ('localhost', 8001)
# armamos el socket, los parámetros que recibe el socket indican el tipo de conexión
# CLIENT
client_socketTCP = socketTCP.SocketTCP()
client_socketTCP.connect(address)
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

# # mandamos un mensajito
# print("... Mandamos cositas")

# # definimos un mensaje y una secuencia indicando el fin del mensaje
# filename = str(input("Archivo a enviar: "))
# message = ""
# with open(filename, "r") as file:
#     message = file.read()

# # socket debe recibir bytes, por lo que encodeamos el mensaje
# send_message = (message + end_of_message).encode()

# # enviamos el mensaje a través del socket
# send_full_message(client_socketTCP, send_message, end_of_message, address, buff_size_client)
# print("... Mensaje enviado")

# # y esperamos una respuesta
# received_message, destination_address = receive_full_mesage(client_socketTCP, buff_size_receive, end_of_message)
# print(' -> Respuesta del servidor: <<' + received_message.decode() + '>>')