import socket
from turtle import delay
from pyModbusTCP.server import ModbusServer
from time import sleep

hostname = socket.gethostname()
server_ip_address = socket.gethostbyname(hostname)
server_port = 502

print("Info; Modbus server IP: " + server_ip_address)
server = ModbusServer('localhost', server_port, no_block=True)
server.start()

print("Modbus server has started")
while True:
    sleep(1)
    print(server.is_run)
    pass