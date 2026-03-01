import requests
import random
import time

API_URL = "http://127.0.0.1:5000/api/data"

while True:
    data = {
        "temperature": random.randint(20, 90),
        "current": random.randint(5, 25),
        "voltage": random.randint(210, 260),
        "vibration": random.randint(1, 10),
        "humidity": random.randint(30, 90),
        "oil_color": random.randint(1, 5)
    }

    response = requests.post(API_URL, json=data)

    print("Status:", response.status_code)
    print("Response:", response.json())
    print("-" * 50)

    time.sleep(5)