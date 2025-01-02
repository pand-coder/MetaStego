"""
main.py
This script implements a simple steganography tool for hiding messages in images and also provides metadata of encoded image.

Author: Pavan Shanmukha Madhav Gunda 
Date: 2024 - 09 - 28

Usage: 
- Run the script to interactively encode or decode messages and view the metadata.
- Ensure all the libraries are installed.
"""

import cv2
from bitarray import bitarray
import requests
import json
import os

class InputValidator:
    @staticmethod
    def validate_image_path(path: str, must_exist: bool = True) -> bool:
        """Validates if the path is a valid image file"""
        if not path:
            raise ValueError("Path cannot be empty")
            
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        if not path.lower().endswith(valid_extensions):
            raise ValueError(f"File must be one of: {', '.join(valid_extensions)}")
            
        if must_exist and not os.path.exists(path):
            raise FileNotFoundError(f"File does not exist: {path}")
            
        return True
    
    @staticmethod
    def validate_message(message: str) -> bool:
        """Validates the input message"""
        if not message:
            raise ValueError("Message cannot be empty")
        
        if len(message.encode('utf-8')) > 1000:  # size limit
            raise ValueError("Message is too long (max 1000 bytes)")
            
        return True
    
    @staticmethod
    def validate_destination_path(path: str) -> bool:
        """Validates the destination path"""
        try:
            # Check if directory exists
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                raise ValueError(f"Directory does not exist: {directory}")
                
            # Check if path is writable
            if os.path.exists(path):
                if not os.access(path, os.W_OK):
                    raise PermissionError(f"No write permission for: {path}")
                    
            return True
        except Exception as e:
            raise ValueError(f"Invalid destination path: {str(e)}")

def get_validated_input(prompt_text: str, validator_func, error_msg: str = None):
    """Generic function to get validated input"""
    while True:
        try:
            user_input = input(prompt_text).strip()
            validator_func(user_input)
            return user_input
        except (ValueError, FileNotFoundError, PermissionError) as e:
            print(f"Error: {str(e)}")
            if error_msg:
                print(error_msg)

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
    if img is None:
        print("Error: Image not found")
        return
    
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
    validator = InputValidator()

    while True:
        print("--Welcome to MetaStego--")
        print("1: Encoder")
        print("2: Decoder")
        print("3: Send Metadata")
        print("4: Exit")

        try :
            func = input("Choose an option: ")

            if func == '1':
                # Get and validate source image
                src = get_validated_input(
                    "Enter Source Image Path: ",
                    validator.validate_image_path,
                    "Please provide a valid image file path"
                )
                
                # Get and validate message
                message = get_validated_input(
                    "Enter Message to Hide: ",
                    validator.validate_message,
                    "Please provide a valid message"
                )
                
                # Get and validate destination
                dest = get_validated_input(
                    "Enter Destination Image Path: ",
                    validator.validate_destination_path,
                    "Please provide a valid destination path"
                )

                print("Encoding...")
                metadata = Encoder(src, message, dest)  # Store the returned metadata

            elif func == '2':
                src = get_validated_input(
                    "Enter Source Image Path: ",
                    validator.validate_image_path,
                    "Please provide a valid image file path"
                )

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
                print("ERROR: Invalid option. Please choose 1-4.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    MetaStego()
