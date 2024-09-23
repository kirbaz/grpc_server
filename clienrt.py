import grpc
import store_pb2
import store_pb2_grpc
import asyncio
import sys
import time

class StoreClient:
    def __init__(self):
        self.store_name = "example_store"  # Название магазина
        self.product_files = []  # Список для накопления файлов

    def add_product_file(self, file_data):
        """Добавляет файл в список."""
        self.product_files.append(file_data)
        print(f"Added file of size: {len(file_data)} bytes")

    async def evaluate_store(self):
        """Отправляет накопленные файлы на сервер и получает оценку."""
        if not self.product_files:
            print("No product files to send.")
            return

        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = store_pb2_grpc.StoreServiceStub(channel)

            # Создание запроса
            request = store_pb2.StoreRequest(store_name=self.store_name, product_files=self.product_files)

            # Отправка запроса и получение ответа
            response = await stub.EvaluateStore(request)
            print(f"Evaluation for store '{self.store_name}': {response.evaluation}")

            # Очистка списка после отправки
            self.product_files.clear()

    async def input_files(self):
        """Асинхронный ввод файлов."""
        while True:
            file_data = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.buffer.read, 1024)
            if file_data:
                self.add_product_file(file_data)
            else:
                await asyncio.sleep(0.1)  # Небольшая задержка, если ничего не прочитано

    async def run(self):
        """Запуск клиента."""
        input_task = asyncio.create_task(self.input_files())
        last_input_time = time.time()

        while True:
            if time.time() - last_input_time > 1:  # Если не было ввода более 1 секунды
                await self.evaluate_store()
                last_input_time = time.time()  # Сброс времени последнего ввода
            await asyncio.sleep(0.1)  # Небольшая задержка для предотвращения излишней загрузки процессора

if __name__ == '__main__':
    client = StoreClient()
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("Client stopped.")
