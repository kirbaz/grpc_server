import grpc
import archive_service_pb2
import archive_service_pb2_grpc

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = archive_service_pb2_grpc.ArchiveServiceStub(channel)
        
        # Чтение zip файла
        with open('test.zip', 'rb') as f:
            zip_data = f.read()
        
        request = archive_service_pb2.ZipRequest(zip_archive=zip_data)
        response = await stub.EvaluateZip(request)
        print(f"Evaluation: {response.evaluation}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(run())
