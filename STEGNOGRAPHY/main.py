import cv2
from bitarray import bitarray
import requests
import json

def Encoder(Source, Message, Destination): 
    img = cv2.imread(Source)  
    if img is None:  
        print("Error: Image not found")
        return

    # Image details for metadata
    height, width, _ = img.shape
    total_pixels = width * height 

    ba = bitarray() 
    ba.frombytes(Message.encode('utf-8')) 
    ba.extend('0' * 40)  
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

    # Return image metadata
    return {
        "width": width,
        "height": height,
        "message": Message,
        "image_path": Destination  # You might want to specify the URL if hosted somewhere
    }

def send_metadata(metadata, token):
    # Send metadata to API
    url = "https://api.apyhub.com/processor/image/metadata/file"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(metadata))

    # Debugging output
    print("Sending request to:", url)
    print("Headers:", headers)
    print("Payload:", json.dumps(metadata))

    if response.status_code == 200:
        print("Metadata sent successfully:", response.json())
    else:
        print("Failed to send metadata:", response.status_code, response.text)


def Decoder(Source):
    img = cv2.imread(Source)
    height, width, _ = img.shape
    total_pixels = width * height

    ba = bitarray()
    for p in range(height):
        for q in range(width):
            for c in range(3):
                ba.append(img[p][q][c] & 1)

    message_bytes = bytearray()
    for i in range(0, len(ba), 8):
        byte = ba[i:i+8].tobytes()
        message_bytes.append(int.from_bytes(byte, byteorder='big'))

    padding_index = message_bytes.find(0)
    if padding_index != -1:
        message = message_bytes[:padding_index].decode('utf-8')
        print("Hidden Message:", message)
    else:
        print("No Hidden Message Found")

def MetaStego():
    token = "<YOUR_APYHUB_TOKEN_HERE>"  # Place your token here
    metadata = None  # To store the metadata

    while True:
        print("--Welcome to MetaStego--")
        print("1: Encoder")
        print("2: Decoder")
        print("3: Send Metadata")
        print("4: Exit")

        func = input("Choose an option: ")

        if func == '1':
            print("Enter Source Image Path")
            src = input()
            print("Enter Message to Hide")
            message = input()
            print("Enter Destination Image Path")
            dest = input()
            print("Encoding...")
            metadata = Encoder(src, message, dest)  # Store the returned metadata

        elif func == '2':
            print("Enter Source Image Path")
            src = input()
            print("Decoding...")
            Decoder(src)

        elif func == '3':
            if metadata is None:
                print("ERROR: No metadata available. Please encode an image first.")
            else:
                print("Sending metadata...")
                send_metadata(metadata, token)

        elif func == '4':
            print("Exiting MetaStego...")
            break

        else:
            print("ERROR: Invalid option chosen")

if __name__ == "__main__":
    MetaStego()
