import httpx

with httpx.Client(http2=True, verify="server.crt") as client:
    r = client.get("https://127.0.0.1:8001/")
    print(r.json())
