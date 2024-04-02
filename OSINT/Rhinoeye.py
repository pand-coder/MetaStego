import requests
import base64
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
print("               , _.-~~-.__            __.,----.                   ")
print("      (';    __( )         ~~~'--..--~~         '.               ")
print("(    . \"..-'  ')|                     .       \\  '.            ")
print(" \\\\ |\.'                    ;       .  ;       ;   ;           ")
print("  \\ \\'   /9)                 '       .  ;           ;         ")
print("   ; )           )    (        '       .  ;     '    .        ")
print("    )    _  __.-'-._   ;       '       . ,     /\\    ;        ")
print("    '-'\"'--'      ; \"-. '.    '            _.-(  \".  (        ")
print("                  ;    \\,)    )--,..----';'    >  ;   .       ")
print("                   \\   ( |   /           (    /   .   ;       ")
print("     ,   ,          )  | ; .(      .    , )  /     \\  ;       ")
print(",;;.';.-.;._,;/;,;)/;.;.);.;,,;,;,,;/;;,),;.,/,;.).,;,    ")
print("           =============================================================   ")                                       
print("                                   RHINOEYE                               ") 
print("           =============================================================   ")
print("                                   VERSION 0.0.1                               ") 
print("           =============================================================   ")
print("                                   OSINTBOT                             ")
print("                             ======================                        ")
print("                        Author:  PAVAN SHANMUKHA MADHAV GUNDA                        ")
print("                             ======================                        ")
name=input("Enter your name:")
print("Hello",name)
print("Choose any of the following options from the below:")
def ip2location_api():
    # IP2Location API
    ip2location_url = 'https://api.ip2location.io/'
    ip2location_api_key = 'YOUR_ip2_location_api_key'

    # Get IP address from user
    ip_address = input("Enter an IP address: ")

    # Make API request
    ip2location_response = requests.get(f'{ip2location_url}?key={ip2location_api_key}&ip={ip_address}')
    print('IP2Location Response:')
    print(ip2location_response.json())

def picarta_ai_api():
    # Picarta.ai API
    print("EXIF DATA OF IMAGE (KEEP THE IMAGE LOCAL ON MACHINE)")
    picarta_url = "https://picarta.ai/classify"
    api_token = "'YOUR_API_KEY_HERE'"  # Register to get the token
    headers = {"Content-Type": "application/json"}

    # Read the image from a local file
    with open("lake.png", "rb") as image_file:
        img_path = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare the payload
    payload = {
        "TOKEN": api_token,
        "IMAGE": img_path
    }

    # Send the POST request with the payload as JSON data
    response = requests.post(picarta_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print("Request failed with status code:", response.status_code)

def ip2whois_api():
    # IP2Whois API
    ip2whois_url = 'https://api.ip2whois.com/v2'
    ip2whois_api_key = ''YOUR_API_KEY_HERE''

    # Get domain from user
    domain = input("Enter a domain name: ")

    # Make API request
    ip2whois_response = requests.get(f'{ip2whois_url}?key={ip2whois_api_key}&domain={domain}')
    print('\nIP2Whois Response:')
    print(ip2whois_response.json())


def get_phone_number_info(phone_number):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, None)

        # Get the region of phone number
        region = geocoder.description_for_number(parsed_number, "en")

        # Get the timezone
        tz = timezone.time_zones_for_number(parsed_number)

        print(f"Phone Number: {phone_number}")
        print(f"Region: {region}")
        print(f"Timezone: {tz}")
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"Error: {e}")


#Menu function for choosing option 
def menu():
    while True:
        print("\n===== OSINT OPERATIONS =====")
        print("1. IP address info")
        print("2. Exif dat")
        print("3. Domain Name")
        print("4. Phone number info")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            ip2location_api()
        elif choice == '2':
            picarta_ai_api()
        elif choice == '3':
            ip2whois_api()
        elif choice == '4':
            phone_number = input("Enter the phone number: ")
            get_phone_number_info(phone_number)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
