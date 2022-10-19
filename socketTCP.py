import socket

class SocketTCP:
    def __init__(self):
        # inicializamos las variables que definen una mascota
        # los datos que aun no sabemos se ponen como None
        self.socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.origin_address = ('localhost', 10000)
        self.destination_address = ('localhost', 10000)
        self.sequence = 0

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
    
    def connect(self, address):
        self.destination_address = address
        tcp_dict = {}
        tcp_dict['ACK'] = 0
        tcp_dict['SYN'] = 1
        tcp_dict['FIN'] = 0
        tcp_dict['sequence'] = self.sequence
        self.sequence += 1
        tcp_dict['data'] = ""
        message = self.create_segment(tcp_dict)
        self.socketUDP.sendto(message.encode(), address)
        while True:
            buffer, address = self.socketUDP.recvfrom(1024)
            buffer = buffer.decode()
            tcp_dict = self.parse_segment(buffer)
            if tcp_dict['ACK'] == 1:
                break
        print("Connected to server")
    
    def accept(self):
        while True:
            buffer, address = self.socketUDP.recvfrom(1024)
            buffer = buffer.decode()
            tcp_dict = self.parse_segment(buffer)
            if tcp_dict['SYN'] == 1:
                break
        self.destination_address = address
        tcp_dict['ACK'] = 1
        tcp_dict['SYN'] = 0
        tcp_dict['FIN'] = 0
        tcp_dict['sequence'] = self.sequence
        self.sequence += 1
        tcp_dict['data'] = ""
        message = self.create_segment(tcp_dict)
        self.socketUDP.sendto(message.encode(), address)
        print("Connected to client")
        return self
    

    