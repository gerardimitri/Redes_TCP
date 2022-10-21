from base64 import decode
from itertools import count
from multiprocessing.connection import wait
import random
import socket
from time import sleep

class SocketTCP:
    def __init__(self):
        # inicializamos las variables que definen una mascota
        # los datos que aun no sabemos se ponen como None
        self.socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.origin_address = (None, None)
        self.destination_address = (None, None)
        self.sequence = 0
        self.timeout = 5

    def parse_segment(self, segment):
        # parseamos el segmento
        # segmento = [sequence, data, checksum]
        segment = segment.split("|||")
        dict_segment = {}
        dict_segment['SYN'] = int(segment[0])
        dict_segment['ACK'] = int(segment[1])
        dict_segment['FIN'] = int(segment[2])
        dict_segment['sequence'] = int(segment[3])
        dict_segment['data'] = segment[4]
        return dict_segment
    
    def create_segment(self, dict_segment):
        # creamos el segmento
        # segmento = [sequence, data, checksum]
        segment = ""
        segment += str(dict_segment['SYN']) + "|||"
        segment += str(dict_segment['ACK']) + "|||"
        segment += str(dict_segment['FIN']) + "|||"
        segment += str(dict_segment['sequence']) + "|||"
        segment += dict_segment['data']
        return segment
    
    def bind(self, address):
        self.origin_address = address
        self.socketUDP.bind(address)
    
    # Función que inicia la conexión desde un objeto socketTCP 
    # con otro que se encuentra escuchando en la dirección address.
    # Dentro de esta función deberá implementar el lado del cliente
    # del 3-way handshake. Por simplicidad, haga que su número de secuencia
    # inicial sea elegido aleatoriamente entre 0 y 100.
    def connect(self, address):
        self.destination_address = address
        tcp_dict = {}
        tcp_dict['SYN'] = 1
        tcp_dict['ACK'] = 0
        tcp_dict['FIN'] = 0
        self.sequence = random.randint(0, 100)
        tcp_dict['sequence'] = self.sequence
        tcp_dict['data'] = ""
        message = self.create_segment(tcp_dict)
        while True:
            print(f"Sending SYN to {address}")
            self.socketUDP.sendto(message.encode(), address)
            print("message sent")
            print("waiting for response")
            buffer, address = self.socketUDP.recvfrom(1024)
            buffer = buffer.decode()
            tcp_dict = self.parse_segment(buffer)
            if tcp_dict['SYN'] == 1 \
                and tcp_dict['ACK'] == 1 \
                    and tcp_dict['FIN'] == 0 \
                        and tcp_dict['sequence'] == self.sequence+1:
                print(f"Received SYN-ACK from {address}")
                break
            else:
                continue
        tcp_dict['ACK'] = 1
        tcp_dict['SYN'] = 0
        tcp_dict['FIN'] = 0
        tcp_dict['sequence'] = tcp_dict['sequence']+1
        self.sequence = tcp_dict['sequence']
        message = self.create_segment(tcp_dict)
        print(f"Sending ACK to {address}")
        self.socketUDP.sendto(message.encode(), address)
        print("message sent")
        print("Connection established")
        return self

    # Función que se encuentra esperando una petición de tipo SYN. 
    # Dentro de esta función deberá implementar el lado del servidor 
    # del 3-way handshake. Si el handshake termina de forma exitosa, 
    # esta función deberá retornar un nuevo objeto del tipo socketTCP 
    # junto a la dirección donde se encuentra escuchando (bind) dicho objeto. 
    # La dirección del nuevo socket debe ser distinta a la del socket que 
    # llamó a accept(). 
    # Cuide que su nuevo socket esté correctamente asociado a la nueva 
    # dirección y que recuerde los números de secuencia, pues es este 
    # nuevo socket el que será utilizado posteriormente para enviar y recibir mensajes.
    def accept(self):
        while True:
            print("waiting for SYN")
            buffer, address = self.socketUDP.recvfrom(1024)
            buffer = buffer.decode()
            tcp_dict = self.parse_segment(buffer)
            if tcp_dict['SYN'] == 1 \
                and tcp_dict['ACK'] == 0 \
                    and tcp_dict['FIN'] == 0:
                print(f"Received SYN from {address}")
                break
            else:
                continue
        tcp_dict['ACK'] = 1
        tcp_dict['SYN'] = 1
        tcp_dict['FIN'] = 0
        tcp_dict['sequence'] = tcp_dict['sequence']+1
        self.sequence = tcp_dict['sequence']
        message = self.create_segment(tcp_dict)
        while True:
            print(f"Sending SYN-ACK to {address}")
            self.socketUDP.sendto(message.encode(), address)
            print("message sent")
            print("waiting for ACK")
            buffer, address = self.socketUDP.recvfrom(1024)
            buffer = buffer.decode()
            tcp_dict = self.parse_segment(buffer)
            print(tcp_dict)
            if tcp_dict['ACK'] == 1 and \
                tcp_dict['SYN'] == 0 and \
                    tcp_dict['FIN'] == 0 and \
                        tcp_dict['sequence'] == self.sequence+1:
                self.sequence = tcp_dict['sequence']
                print("ACK received")
                break
            else:
                continue
        print("Connected to client")
        new_socket = self
        new_socket.origin_address = self.origin_address
        new_socket.destination_address = address
        new_socket.origin_address = (new_socket.origin_address[0], new_socket.origin_address[1]+1)
        new_socket.sequence = tcp_dict['sequence']
        return new_socket, address
    
    # Esta función será la encargada de manejar Stop & Wait 
    # desde el lado del emisor tal como vimos en la versión 
    # simplificada mostrada en el video. Su función send deberá 
    # encargarse de dividir el mensaje message en trozos de 
    # tamaño máximo 16 bytes.
    def send(self, message):
        self.socketUDP.settimeout(self.timeout)
        decoded_message = message.decode()
        print("----->" + decoded_message)
        message = decoded_message.encode()
        byte_inicial = 0
        message_sent_so_far = ''.encode()
        buff_size = 16
        while len(message) > byte_inicial:
            tcp_dict = {}
            tcp_dict['ACK'] = 0
            tcp_dict['SYN'] = 0
            tcp_dict['FIN'] = 0
            tcp_dict['sequence'] = self.sequence
            max_byte = min(len(message), byte_inicial + buff_size)
            tcp_dict['data'] = message[byte_inicial:max_byte].decode()
            print(f"Sending {tcp_dict['data']} to {self.destination_address}")
            expected_size_to_send = len(tcp_dict['data'])
            message_to_send = self.create_segment(tcp_dict).encode()
            try:
                self.socketUDP.sendto(message_to_send, self.destination_address)
                print(f"Sending {expected_size_to_send} bytes to {self.destination_address}")
                buffer, address = self.socketUDP.recvfrom(1024)
                buffer = buffer.decode()
                tcp_dict = self.parse_segment(buffer)
                print(tcp_dict)
                if tcp_dict['ACK'] == 1 and \
                    tcp_dict['SYN'] == 0 and \
                        tcp_dict['FIN'] == 0 and \
                            tcp_dict['sequence'] == self.sequence + expected_size_to_send:
                    print("ACK received")
                    self.sequence += expected_size_to_send
                    message_sent_so_far += message[byte_inicial:max_byte]
                    byte_inicial += expected_size_to_send 
            except socket.timeout:
                print("Timeout")
                print("Resending message")
                continue


    def recv(self, buff_size):
        self.socketUDP.settimeout(self.timeout)
        message = ''.encode()
        counter = 0
        while len(message) < buff_size:
            if counter == 3:
                print("Connection lost")
                break
            try:
                buffer, address = self.socketUDP.recvfrom(1024)
                buffer = buffer.decode()
                tcp_dict = self.parse_segment(buffer)
                if tcp_dict['sequence'] == self.sequence:
                    tcp_dict['ACK'] = 1
                    tcp_dict['SYN'] = 0
                    tcp_dict['FIN'] = 0
                    tcp_dict['sequence'] = self.sequence + len(tcp_dict['data'])
                    message_to_send = self.create_segment(tcp_dict).encode()
                    self.socketUDP.sendto(message_to_send, self.destination_address)
                    self.sequence = tcp_dict['sequence']
                    message += tcp_dict['data'].encode()

                # cierre de conexión
                if tcp_dict['FIN'] == 1:
                    tcp_dict['ACK'] = 1
                    tcp_dict['SYN'] = 0
                    tcp_dict['FIN'] = 1
                    tcp_dict['sequence'] = self.sequence + 1
                    message_to_send = self.create_segment(tcp_dict).encode()
                    self.socketUDP.sendto(message_to_send, self.destination_address)
                    self.sequence = tcp_dict['sequence']
                    message += tcp_dict['data'].encode()
                    break
                # si len de data es 16 y es el ultimo mensaje se queda en loop infinito
                if len(tcp_dict['data']) < 16:
                    break
            except socket.timeout:
                print("Timeout")
                print("Resending message")
                counter += 1
                continue
        return message

    def close(self):
        self.socketUDP.settimeout(self.timeout)
        tcp_dict = {}
        tcp_dict['ACK'] = 0
        tcp_dict['SYN'] = 0
        tcp_dict['FIN'] = 1
        tcp_dict['sequence'] = self.sequence
        tcp_dict['data'] = ''
        message_to_send = self.create_segment(tcp_dict).encode()
        counter = 0
        closed = False
        while True:
            try:
                self.socketUDP.sendto(message_to_send, self.destination_address)
                print("FIN sent")
                buffer, address = self.socketUDP.recvfrom(1024)
                buffer = buffer.decode()
                tcp_dict = self.parse_segment(buffer)
                print(tcp_dict)
                if tcp_dict['ACK'] == 1 and \
                    tcp_dict['SYN'] == 0 and \
                        tcp_dict['FIN'] == 1 and \
                            tcp_dict['sequence'] == self.sequence + 1:
                    print("FIN-ACK received")
                    self.sequence += 1
                    closed = True
                    break
                else:
                    continue
            except socket.timeout:
                counter += 1
                print("Timeout")
                if counter == 3:
                    print("Force closing")
                    break
                else:
                    continue
        tcp_dict['ACK'] = 1
        tcp_dict['SYN'] = 0
        tcp_dict['FIN'] = 0
        tcp_dict['sequence'] = self.sequence + 1
        message_to_send = self.create_segment(tcp_dict).encode()
        if closed:
            for _ in range(3):
                self.socketUDP.sendto(message_to_send, self.destination_address)
                print("ACK sent")
                sleep(self.timeout)        
        # self.socketUDP.sendto(message_to_send, self.destination_address)
        # print("ACK sent")
        self.socketUDP.close()
        print("Connection closed")