# grpc_server
grpc serv

Для создания gRPC сервера и клиента на Python, который принимает zip-файл, распаковывает его, обрабатывает файлы внутри и возвращает оценку (0 или 1), вам нужно выполнить следующие шаги:

1. Установить необходимые пакеты:
Bash

pip install grpcio grpcio-tools

2. Определить .proto файл, который описывает сервис и сообщения:

3. Сгенерировать gRPC классы на Python:


python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. file_service.proto

4. Написать код сервера:

5. Написать код клиента:

6. Сгенерировать и протестировать zip-файл:
# Создайте zip файл с необходимыми файлами для теста
echo "Sample UTF8 File" > test.utf8
echo "<html><body>Sample HTML File</body></html>" > test.html
zip sample.zip test.utf8 test.html
rm test.utf8 test.html

# Запустите сервер:
python server.py

# В другом терминале запустите клиент:
python client.py
