import random

# definimos variables que tanto el servidor como el cliente van a usar
buff_size_server = 16
buff_size_client = 16
# cambiamos el end_of_message por | en vez de \n para no tener problemas con los saltos de línea del archivo
end_of_message = "|"


# modificamos la función para que sirva para sockets no orientados a conexión
def recv_con_perdidas(socket, buff_size, loss_probability):
    while True:
        # recibimos el mensaje y su dirección de origen
        buffer, address = socket.recvfrom(buff_size)
        # sacamos un número entre 0 y 100 de forma aleatoria
        random_number = random.randint(0, 100)
        # si el random_number es menor o igual a la probabilidad de perdida omitimos el mensaje (hacemos como que no llegó)
        if random_number <= loss_probability:
            continue
        # de lo contrario salimos del loop y retornamos
        else:
            break
    return buffer, address


# modificamos la función para que sirva para sockets no orientados a conexión (notemos que cambió su firma)
def send_con_perdidas(socket, address, message_in_bytes, loss_probability):
    # sacamos un número entre 0 y 100 de forma aleatoria
    random_number = random.randint(0, 100)
    # si el random_number es mayor o igual a la probabilidad de perdida enviamos el mensaje
    if random_number >= loss_probability:
        socket.sendto(message_in_bytes, address)
    else:
        print("oh no, pérdida de: {}".format(message_in_bytes))


# modificamos la función para que sirva para sockets no orientados a conexión
def receive_full_mesage(connection_socket, buff_size, end_of_message):
    # esta función se encarga de recibir el mensaje completo desde el cliente
    # en caso de que el mensaje sea más grande que el tamaño del buffer 'buff_size', esta función va esperar a que
    # llegue el resto

    # recibimos la primera parte del mensaje y su dirección de origen
    buffer, address = connection_socket.recvfrom(buff_size)
    full_message = buffer

    # verificamos si llegó el mensaje completo o si aún faltan partes del mensaje
    is_end_of_message = contains_end_of_message(full_message, end_of_message)

    # si el mensaje llegó completo (o sea que contiene la secuencia de fin de mensaje) removemos la secuencia de fin de mensaje
    if is_end_of_message:
        full_message = full_message[0:(len(full_message) - len(end_of_message))]

    # si el mensaje no está completo (no contiene la secuencia de fin de mensaje)
    else:
        # entramos a un while para recibir el resto y seguimos esperando información
        # mientras el buffer no contenga secuencia de fin de mensaje
        while not is_end_of_message:
            # recibimos un nuevo trozo del mensaje
            buffer, address = connection_socket.recvfrom(buff_size)

            # y lo añadimos al mensaje "completo"
            full_message += buffer

            # verificamos si es la última parte del mensaje
            is_end_of_message = contains_end_of_message(full_message, end_of_message)

            # si el mensaje llegó completo (o sea que contiene la secuencia de fin de mensaje) removemos la secuencia de fin de mensaje
            if is_end_of_message:
                full_message = full_message[0:(len(full_message) - len(end_of_message))]

    # finalmente retornamos el mensaje y la dirección
    return full_message, address


# vemos si message (en bytes) contiene el end_of_message al final
def contains_end_of_message(message, end_of_message):
    if end_of_message.encode() == message[(len(message) - len(end_of_message)):len(message)]:
        return True
    else:
        return False


# creamos una función para enviar el mensaje completo usando sockets no orientados a conexión
# si no hacemos esto el socket va a intentar mandar el mensaje una sola vez y si no cabe en el buffer de llegada parte del mensaje se pierde
def send_full_message(receiver_socket, message, end_of_message, address, receiver_buff_size):
    byte_inicial = 0
    message_sent_so_far = ''.encode()
    while True:
        max_byte = min(len(message), byte_inicial + receiver_buff_size)
        message_slice = message[byte_inicial:max_byte]
        receiver_socket.sendto(message_slice, address)
        message_sent_so_far += message_slice
        if contains_end_of_message(message_sent_so_far, end_of_message):
            break
        byte_inicial += receiver_buff_size