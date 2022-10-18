from audioop import add
import socket
from utils import * 

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
end_of_message = "|"

# socket debe recibir bytes, por lo que encodeamos el mensaje
send_message = (message + end_of_message).encode()

# enviamos el mensaje a través del socket
send_full_message(client_socket, send_message, end_of_message, my_address, buff_size_client)
print("... Mensaje enviado")

# y esperamos una respuesta
received_message, destination_address = receive_full_mesage(client_socket, buff_size_client, end_of_message)
print(' -> Respuesta del servidor: <<' + received_message.decode() + '>>')