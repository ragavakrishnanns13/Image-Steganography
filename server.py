import socket
from PIL import Image


def extract_message(image_file):
    image = Image.open(image_file)
    width, height = image.size
    pixels = image.load()


    message_bin = ''
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            message_bin += str(r & 0b00000001)

    #to convert binary message to string
    message = ''
    for i in range(0, len(message_bin), 8):
        message += chr(int(message_bin[i:i+8], 2))

    return message



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1002))  # 127.0.0.1
server.listen(1)

client_socket, client_address = server.accept()

data = client_socket.recv(1024)

msglen = int(data.decode())

file = open('server_image.png', "wb")
image_chunk = client_socket.recv(2048)  # stream-based protocol




while image_chunk:
    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)
    

print(extract_message('hidden.png')[:msglen])

file.close()

client_socket.close()

