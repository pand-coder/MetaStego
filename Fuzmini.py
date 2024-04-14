import requests

# Target URL
target_url = "https://chat.openai.com/"

# List of common hidden files and directories
hidden_paths = [
    ".htaccess",
    ".htpasswd",
    ".git",
    ".svn",
    ".DS_Store",
    "login.php",
    "home.php",
    "logout.php",
    "robots.txt"
]

# Function to fuzz the target URL
def fuzz_url(url, path):
    target = url + path
    try:
        response = requests.get(target)
        if response.status_code == 200:
            print(f"Found: {target}")
            print(response.text)  # Print the contents of the file
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Main fuzzer loop
def main():
    for path in hidden_paths:
        fuzz_url(target_url, path)

if _name_ == "_main_":
    main()
