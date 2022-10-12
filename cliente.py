import socket


class Mascota:
    def __init__(self):
        # inicializamos las variables que definen una mascota
        # los datos que aun no sabemos se ponen como None
        self.especie = None
        self.peso = None
        self.tamanno = None
        self.buena_mascota = True

    @staticmethod
    def parse_mascota(pet_str):
        nueva_mascota = Mascota()
        pet_split = pet_str.split(" ")

        if len(pet_split) > 1:
            nueva_mascota.especie = pet_split[0]
            nueva_mascota.tamanno = pet_split[1]

        return nueva_mascota

    def set_from_str(self, pet_str):
        nueva_mascota = self.parse_mascota(pet_str)
        self.especie = nueva_mascota.especie
        self.peso = nueva_mascota.peso
        self.tamanno = nueva_mascota.tamanno

    def set_peso(self, peso):
        self.peso = peso

    def set_mala_mascota(self):
        print("No, no hay mascotas malas, me niego")

    def is_buena_mascota(self):
        return self.buena_mascota

    def is_chonky(self):
        if self.especie == "gato":
            if self.tamanno == "smol":
                if self.peso > 5:
                    return "está chonky"
                else:
                    return "no está chonky"
            else:
                if self.peso > 7:
                    return "está chonky"
                else:
                    return "no está chonky"
        else:
            return "la verdad es que ni idea, esto es un ejemplo chiquito"

# usamos la clase que recién creamos
mi_gata = Mascota()
mi_gata.set_from_str("gato smol")
mi_gata.set_peso(6)
print(mi_gata.is_chonky())

localIP       = "127.0.0.1"
localPort     = 10000
bufferSize    = 1024
msgFromServer = str(input("Archivo a enviar: "))
bytesToSend   = str.encode(msgFromServer)
sendBuffSize  = 16
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

def send_full_file(file_name, udp_socket, buffsize):
    with open(file_name, "rb") as f:
        while True:
            data = f.read(buffsize)
            if not data:
                break
            udp_socket.sendto(data, (localIP, localPort))

def send_full_message(message, udp_socket, buffsize, address):
    while True:
        data = message[:buffsize]
        if not data:
            break
        udp_socket.sendto(data, address)
        message = message[buffsize:]


# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)   
    print(clientMsg)
    print(clientIP)
    # Sending a reply to client
    send_full_message(bytesToSend, UDPServerSocket, sendBuffSize, address)
    #UDPServerSocket.sendto(bytesToSend, address)

# # CLIENT
# client_socketTCP = SocketType.SocketTCP()
# client_socketTCP.connect(address)
# # test 1
# message = "Mensje de len=16".encode()
# client_socketTCP.send(message)
# # test 2
# message = "Mensaje de largo 19".encode()
# client_socketTCP.send(message)
# # test 3
# message = "Mensaje de largo 19".encode()
# client_socketTCP.send(message)