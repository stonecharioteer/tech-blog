from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from HTTP/2"}


if __name__ == "__main__":
    import asyncio
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["127.0.0.1:8001"]
    config.certfile = "server.crt"
    config.keyfile = "server.key"
    config.alpn_protocols = ["h2", "http/1.1"]

    asyncio.run(serve(app, config))
