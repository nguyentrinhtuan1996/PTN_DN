#!/usr/bin/env python3

"""
Modbus/TCP server with virtual data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Map the system date and time to @ 0 to 5 on the "holding registers" space.
Only the reading of these registers in this address space is authorized. All
other requests return an illegal data address except.

Run this as root to listen on TCP privileged ports (<= 1024).
"""

import threading
from pyModbusTCP.server import ModbusServer, DataBank
from Modbus_Table import Modbus_Table_Class
# this global dic will be use by main
modbus_table = Modbus_Table_Class()
"""
this will be modbus table for all csv in and out, global var
"""

class MyDataBank(DataBank):
    """A custom ModbusServerDataBank for override get_holding_registers method."""

    def __init__(self):
        # turn off allocation of memory for standard modbus object types
        # only "holding registers" space will be replaced by dynamic build values.
        super().__init__(virtual_mode=True)
        

    def get_input_registers(self, address, number=1, srv_info=None):
        """ get virtual input register"""
        try:
            return [ modbus_table.input_registers_table[count] for count in range(address, address+number)]
        except KeyError:
            return 

    def get_holding_registers(self, address, number=1, srv_info=None):
        """Get virtual holding registers."""
        try:
            return [modbus_table.holding_registers_table[count] for count in range(address, address+number)]
        except KeyError:
            return 
    def set_holding_registers(self, address, word_list,srv_info=None):
        """Set input register"""
        try:
            for count in range(0,len(word_list)):
                modbus_table.holding_registers_table[address + count] = word_list[count]
            return True
        except KeyError:
            return
    def on_holding_registers_change(self, address, from_value, to_value, srv_info):
        print("Holding " +str(address)+" : from " +str(from_value) + "to " +str(to_value))
        return
    # def set_holding_registers(self, address, word_list, srv_info=None):
    #     return super().set_holding_registers(address, word_list, srv_info)
    # def set_holding_registers(self, address, word_list, srv_info=None):
    #     return super().set_holding_registers(address, word_list, srv_info)

class Modbus_Server_Class():
    def __init__(self) -> None:
        
        self.server =  ModbusServer(host='0.0.0.0', port=502, data_bank=MyDataBank())
        self.thread = threading.Thread(target=self.server.start)
        pass
    
    def start(self):
        """
        this function will be in a infinite loop in another thread
        """
        self.thread.start()

if __name__ == '__main__':

    modbus_server = Modbus_Server_Class()
    print("Starting server")
    modbus_server.start()
    print("Server is online")

    modbus_table.holding_registers_table[1100] = 1
    modbus_table.holding_registers_table[1101] = 2
    modbus_table.holding_registers_table[1102] = 3

    # init modbus server and start it
    # modbus_table = Modbus_Table_Class()
    # modbus_table.set_bus_data(101,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(101,1231,2 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(102,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(103,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(104,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(105,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(106,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(107,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(108,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(109,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(110,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(111,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(112,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(113,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    

