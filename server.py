import grpc
from concurrent import futures
import store_pb2
import store_pb2_grpc
import asyncio

class StoreService(store_pb2_grpc.StoreServiceServicer):
    async def EvaluateStore(self, request, context):
     store_name = request.store_name  # Получаем название магазина
     product_files = request.product_files  # Получаем массив файлов

     print(f"Received request for store: {store_name}")
     print(f"Product files: {len(product_files)} files received.")

     with tempfile.TemporaryDirectory() as temp_dir:
        for product_file in product_files:
            file_data = product_file.file_data
            file_name = product_file.file_name

            # Сохранение файла с оригинальным именем
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, 'wb') as f:
                f.write(file_data)

            # Чтение и обработка файла
            with open(file_path, 'rb') as f:
                content = f.read()
                print(f"Content of {file_path}:")
                print(content)  # Здесь вы можете добавить свою логику обработки

    # Пример логики оценки
    evaluation = 1 if store_name == "example_store" else 0
    return store_pb2.StoreResponse(evaluation=evaluation)


async def serve():
    server = grpc.aio.server()
    store_pb2_grpc.add_StoreServiceServicer_to_server(StoreService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("Server started on port 50051.")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
