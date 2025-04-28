import os
import requests

def get_home_directory():
    return os.path.expanduser("~")

def get_opinedocs_path():
    return os.path.join(get_home_directory(), ".pinetodo.opinedocs")

def download_opinedocs():
    raw_url = "https://raw.githubusercontent.com/openpineapletools/pinetodo/refs/heads/dev/.opinerc/.pinetodo.opinedocs"
    
    response = requests.get(raw_url)
    
    if response.status_code == 200:
        with open(get_opinedocs_path(), "w") as file:
            file.write(response.text)
        print(f"File '.pinetodo.opinedocs' has been downloaded and saved.")
    else:
        print(f"Failed to download the file, status code: {response.status_code}")

def load_opinedocs():
    opinedocs_path = get_opinedocs_path()
    
    if os.path.exists(opinedocs_path):
        with open(opinedocs_path, "r") as f:
            content = f.read()
            print(content)  
    else:
        print(f"File '.pinetodo.opinedocs' not found.")

if __name__ == "__main__":
    opinedocs_path = get_opinedocs_path()
    
    if not os.path.exists(opinedocs_path):
        download_opinedocs()
    else:
        print(f"File '{opinedocs_path}' already exists. Displaying content...")

    load_opinedocs()
