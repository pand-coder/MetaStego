import cv2
from bitarray import bitarray
def Encoder(Source, Message, Destination): 
    img = cv2.imread(Source)
    if img is None:
        print("Error: Image not found")
        return

    if len(img.shape) == 2:
        print("Grayscale")
    elif len(img.shape) == 3:
        print("RGB or BGR")
    elif len(img.shape) == 4:
        print("RGBA")
    width, height, _ = img.shape
    total_pixels = width * height

    ba = bitarray()
    ba.frombytes(Message.encode('utf-8'))
    ba.extend('0' * 40)  # Padding to mark end of message
    req_pixels = len(ba)

    if req_pixels > total_pixels * 3:
        print("ERROR: Need larger file size")
        return

    index = 0
    for p in range(height):
        for q in range(width):
            if index < req_pixels:
                for c in range(3):
                    if index < req_pixels:
                        img[p][q][c] = (img[p][q][c] & 0xFE) | ba[index]
                        index += 1

    cv2.imwrite(Destination, img)
    print("Image Encoded Successfully")

def Decoder(Source):
    img = cv2.imread(Source)
    height, width, _ = img.shape
    total_pixels = width * height

    ba = bitarray()
    for p in range(height):
        for q in range(width):
            for c in range(3):
                ba.append(img[p][q][c] & 1)

    # Extract the message bytes
    message_bytes = bytearray()
    for i in range(0, len(ba), 8):
        byte = ba[i:i+8].tobytes()
        message_bytes.append(int.from_bytes(byte, byteorder='big'))

    # Find the end-of-message padding
    padding_index = message_bytes.find(0)
    if padding_index != -1:
        message = message_bytes[:padding_index].decode('utf-8')
        print("Hidden Message:", message)
    else:
        print("No Hidden Message Found")



def Stegosaurus():
    while True:
        print("                         .       .")
        print("                        / `.   .' \\")
        print("                .---.  <    > <    >  .---.")
        print("                |    \\  \\ - ~ ~ - /  /    |")
        print("                 ~-..-~             ~-..-~")
        print("             \\~~~\\.'                    `./~~~/")
        print("              \\__/                        \\__/")
        print("               /                  .-    .  \\")
        print("        _._ _.-    .-~ ~-.       /       }   \\/~~~/")
        print("    _.-'q  }~     /       }     {        ;    \\__/")
        print("   {'__,  /      (       /      {       /      `. ,~~|   .     .")
        print("    `''''='~~-.__(      /_      |      /- _      `..-'   \\\\   //")
        print("                / \\   =/  ~~--~~{    ./|    ~-.     `-..__\\\\_//_.-'")
        print("               {   \\  +\\         \\  =\\ (        ~ - . _ _ _..---~")
        print("               |  | {   }         \\   \\_\\")
        print("              '---.o___,'       .o___,' ")
        print("        =============================================================   ")                                       
        print("                                STEGOSAURUS                               ") 
        print("        =============================================================   ")
        print("        =============================================================   ")
        print("        ============================================================                        ")
        print("                     Author:  PAVAN SHANMUKHA MADHAV GUNDA                        ")
        print("        =============================================================                        ") 
        print("--Welcome to Stegosauraus--")
        print("1: Encoder")
        print("2: Decoder")
        print("3: Exit")

        func = input("Choose an option: ")

        if func == '1':
            print("Enter Source Image Path")
            src = input()
            print("Enter Message to Hide")
            message = input()
            print("Enter Destination Image Path")
            dest = input()
            print("Encoding...")
            Encoder(src, message, dest)

        elif func == '2':
            print("Enter Source Image Path")
            src = input()
            print("Decoding...")
            Decoder(src)

        elif func == '3':
            print("Exiting Stegosauraus...")
            break

        else:
            print("ERROR: Invalid option chosen")


if __name__ == "__main__":
    Stegosaurus()

