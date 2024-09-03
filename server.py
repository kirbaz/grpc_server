# server.py
import grpc
from concurrent import futures
import file_service_pb2
import file_service_pb2_grpc
import zipfile
import io
import os

class FileServiceServicer(file_service_pb2_grpc.FileServiceServicer):
    def ProcessFile(self, request, context):
        file_data = request.file_content

        # Создание временной директории для распаковки
        with zipfile.ZipFile(io.BytesIO(file_data), 'r') as zip_ref:
            zip_ref.extractall('/tmp/unzipped')

        # Пример обработки (проверка наличия .utf8 и .html файлов)
        rating = 0
        for root, dirs, files in os.walk('/tmp/unzipped'):
            for file in files:
                if file.endswith('.utf8') or file.endswith('.html'):
                    rating += 1

        # Очистка временной директории
        import shutil
        shutil.rmtree('/tmp/unzipped')

        response = file_service_pb2.FileResponse(rating=rating)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
