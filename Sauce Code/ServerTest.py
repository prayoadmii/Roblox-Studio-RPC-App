import requests

url = "http://127.0.0.1:1234/StudioRPC/Update"
payload = {
    "Details": "This Is A Test Script",
    "State": "Data From Test Script!",
    "LargeImage": None,
    "SmallImage": None,
    "BigImageToolHover": "Roblox Studio",
    "SmallImageHover": "Roblox Studio"
}

if __name__ == "__main__":
    response = requests.post(url, json=payload)
