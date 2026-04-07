import requests
import random
import time

URL = "https://your-render-url/heartbeat"

TENANT_ID = "tenant-1"

while True:
    data = {
        "tenant_id": TENANT_ID,
        "device_name": "device-" + str(random.randint(1,10)),
        "cpu": random.randint(10, 95),
        "memory": random.randint(20, 90),
        "disk": random.randint(5, 100)
    }

    r = requests.post(URL, json=data)
    print(r.json())

    time.sleep(2)