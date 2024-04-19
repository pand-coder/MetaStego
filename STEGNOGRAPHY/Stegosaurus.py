import cv2
import numpy as np
def Encoder(Source, Message, Destination):
    img = cv2.imread(Source)
    width, height, _ = img.shape
    total_pixels = width * height

    Message += "pavan"
    b_message = ''.join([format(ord(i), "08b") for i in Message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
        return

    index = 0
    for p in range(height):
        for q in range(width):
            if index < req_pixels:
                for c in range(3):
                    if index < req_pixels:
                        img[p][q][c] = int(bin(img[p][q][c])[2:9] + b_message[index], 2)
                        index += 1

    cv2.imwrite(Destination, img)
    print("Image Encoded Successfully")


    cv2.imwrite(Destination, img)
    print("Image Encoded Successfully")

def Decoder(Source):
    img = cv2.imread(Source)
    height, width, _ = img.shape
    total_pixels = width * height

    hidden_bits = ""
    for p in range(height):
        for q in range(width):
            for c in range(3):
                hidden_bits += (bin(img[p][q][c])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    Message = ""
    for i in range(len(hidden_bits)):
        if Message[-5:] == "pavan":
            break
        else:
            Message += chr(int(hidden_bits[i], 2))

    if "pavan" in Message:
        print("Hidden Message:", Message[:-5])
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
