import requests

r = requests.get("http://127.0.0.1:8002/events", stream=True)

for line in r.iter_lines():
    if line:
        print(line.decode("utf-8"))
