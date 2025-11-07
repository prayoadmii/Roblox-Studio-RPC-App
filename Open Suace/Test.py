# Note: This Test Script Did Not Up-To-Date

import requests
import time

url = "http://127.0.0.1:2500/API/RpcUpload"

test_data = {
    "Details": "Circuit Maker 2",
    "State": "BlocksLoader",
    "LargeImage": "https://tr.rbxcdn.com/180DAY-68c6ccb926ee3b7c10f1c74ce21d5b55/256/256/Image/Webp/noFilter",
    "SmallImage": "https://tr.rbxcdn.com/30DAY-AvatarHeadshot-8AAC381813DD844829B00A2F1373D2B8-Png/150/150/AvatarHeadshot/Webp/noFilter"
}

try:
    res = requests.post(url, json=test_data)
    print("✅ Server Reply:", res.json())
except Exception as e:
    print("❌ Request Failed:", e)