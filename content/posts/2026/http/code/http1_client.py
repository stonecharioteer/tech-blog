import requests

URL = "http://127.0.0.1:8000"

# GET
r = requests.get(f"{URL}/")
print("GET:", r.json())

# POST
r = requests.post(f"{URL}/echo", json={"hello": "world"})
print("POST:", r.json())
