import grpc
from concurrent import futures
import store_pb2
import store_pb2_grpc
import asyncio

class StoreService(store_pb2_grpc.StoreServiceServicer):
    async def EvaluateStore(self, request, context):
        # Обработка запроса в зависимости от названия магазина
        print(f"Received request for store: {request.store_name}")
        print(f"Product files: {len(request.product_files)} files received.")

        # Пример логики оценки
        if request.store_name == "example_store":
            evaluation = 1  # Оценка 1 для example_store
        else:
            evaluation = 0  # Оценка 0 для других магазинов

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
