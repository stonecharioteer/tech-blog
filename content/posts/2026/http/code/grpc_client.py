import grpc
import chat_pb2
import chat_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    request = chat_pb2.MessageRequest(name="Vinay", message="Hello gRPC!")
    response = stub.SendMessage(request)
    print(f"Server replied: {response.reply}")


if __name__ == "__main__":
    run()
