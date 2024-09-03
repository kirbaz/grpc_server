# client.py
import grpc
import file_service_pb2
import file_service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)

        with open('sample.zip', 'rb') as f:
            file_content = f.read()
        
        request = file_service_pb2.FileRequest(file_content=file_content)
        response = stub.ProcessFile(request)

        print("File Rating: ", response.rating)

if __name__ == '__main__':
    run()
