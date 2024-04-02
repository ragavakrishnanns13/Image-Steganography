import socket
from PIL import Image


def hide_message(image_file, message):
    image = Image.open(image_file)
    width, height = image.size
    pixels = image.load()

    #to convert message to binary
    message_bin = ''.join(format(ord(c), '08b') for c in message)

    #to make sure message can fit in the image
    if len(message_bin) > width * height:
        raise ValueError('Message too long to hide in image')
    # hides message in image
    index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Hide message in LSB of red channel
            if index < len(message_bin):
                pixels[x, y] = (r & 0b11111110 | int(message_bin[index]), g, b)
                index += 1

    
    image.save('hidden.png')



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1002))  

msg=input("enter msg:")


msglen = len(msg)
client.send(str(msglen).encode())


hide_message('image.png',msg)
file = open('hidden.png', "rb")
image_data = file.read(2048)

while image_data:
    client.send(image_data)
    image_data = file.read(2048)

file.close()
client.close()

