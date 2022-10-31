from modbus_tcp_server.network import ModbusTCPServer
from modbus_tcp_server.data_source import BaseDataSource

class CustomDB(BaseDataSource):

    def __init__(self):
        self.holding_registers = {1,2,3,4,5}
        self.coils = {1,1,1,1,1}

    def get_analog_input(self, unit_id: int, address: int) -> int:
        return 0

    def get_discrete_input(self, unit_id: int, address: int) -> bool:
        return False

    def get_holding_register(self, unit_id: int, address: int) -> int:
        return self.holding_registers.get((unit_id, address), 0)

    def get_coil(self, unit_id: int, address: int) -> bool:
        return self.coils.get((unit_id, address), False)

    def set_holding_register(self, unit_id: int, address: int, value: int) -> None:
        self.holding_registers[(unit_id, address)] = value

    def set_coil(self, unit_id: int, address: int, value: bool) -> None:
        self.coils[(unit_id, address)] = value


c_db = CustomDB()

at = ModbusTCPServer('localhost', 502, c_db).start()
print("Modbus TCP/IP server started")