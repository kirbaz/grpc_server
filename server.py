import grpc
from concurrent import futures
import asyncio
import zipfile
import io

import archive_service_pb2
import archive_service_pb2_grpc

class ArchiveServiceServicer(archive_service_pb2_grpc.ArchiveServiceServicer):
    async def EvaluateZip(self, request, context):
        zip_archive = request.zip_archive
        
        # Проверяем переданный zip файл
        with zipfile.ZipFile(io.BytesIO(zip_archive), 'r') as zip_ref:
            if any(info.file_size > 0 for info in zip_ref.infolist()):
                evaluation = 1
            else:
                evaluation = 0
        
        return archive_service_pb2.EvaluationResponse(evaluation=evaluation)

async def serve():
    server = grpc.aio.server()
    archive_service_pb2_grpc.add_ArchiveServiceServicer_to_server(ArchiveServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print('Starting server on port 50051...')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
