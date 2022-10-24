import socketTCP
# definimos variables que tanto el servidor como el cliente van a usar
buff_size_server = 16
buff_size_client = 16
buff_size_receive = 1024
# cambiamos el end_of_message por | en vez de \n para no tener problemas con los saltos de línea del archivo
end_of_message = "/"

# modificamos la función para que sirva para sockets no orientados a conexión
def receive_full_mesage(connection_socket, buff_size, end_of_message):
    connection_socket = connection_socket.socketUDP
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
        tcp_dict = {}
        tcp_dict['ACK'] = 0
        tcp_dict['SYN'] = 0
        tcp_dict['FIN'] = 0
        tcp_dict['sequence'] = receiver_socket.sequence
        receiver_socket.sequence += 1
        max_byte = min(len(message), byte_inicial + receiver_buff_size)
        tcp_dict['data'] = message[byte_inicial:max_byte].decode()
        message_to_send = receiver_socket.create_segment(tcp_dict).encode()
        receiver_socket.socketUDP.sendto(message_to_send, address)
        message_sent_so_far += message_to_send
        if contains_end_of_message(message_sent_so_far, end_of_message):
            break
        byte_inicial += receiver_buff_size
