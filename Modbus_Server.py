#!/usr/bin/env python3

"""
Modbus/TCP server with virtual data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Map the system date and time to @ 0 to 5 on the "holding registers" space.
Only the reading of these registers in this address space is authorized. All
other requests return an illegal data address except.

Run this as root to listen on TCP privileged ports (<= 1024).
"""

import argparse
from pyModbusTCP.server import ModbusServer, DataBank
from pyModbusTCP.server import DataHandler
from pyModbusTCP.constants import EXP_ILLEGAL_FUNCTION
from datetime import datetime
from Convert_Engine import Convent_Engine_Class

from Modbus_Table import Modbus_Table_Class

class MyDataBank(DataBank,Modbus_Table_Class):
    """A custom ModbusServerDataBank for override get_holding_registers method."""

    def __init__(self):
        # turn off allocation of memory for standard modbus object types
        # only "holding registers" space will be replaced by dynamic build values.
        super().__init__(virtual_mode=True)
        self.convert_engine = Convent_Engine_Class()

    def get_discrete_inputs(self, address, number=1, srv_info=None):
    
        # build a list of virtual registers to return to server data handler
        # return None if any of virtual registers is missing
        try:
            return [ modbus_table.discrete_inputs_table[count] for count in range(address, address+number)]
        except KeyError:
            return 

    def get_input_registers(self, address, number=1, srv_info=None):
        try:
            return [ modbus_table.input_registers_table[count] for count in range(address, address+number)]
        except KeyError:
            return 

    def get_coils(self, address, number=1, srv_info=None):

        # build a list of virtual registers to return to server data handler
        # return None if any of virtual registers is missing
        try:
            return [modbus_table.coils_table[count] for count in range(address, address+number)]
        except KeyError:
            return 

    def get_holding_registers(self, address, number=1, srv_info=None):
        """Get virtual holding registers."""
        # populate virtual registers dict with current datetime values
        now = datetime.now()

        # build a list of virtual registers to return to server data handler
        # return None if any of virtual registers is missing
        try:
            return [modbus_table.holding_registers_table[count] for count in range(address, address+number)]
        except KeyError:
            return 

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='localhost', help='Host (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=502, help='TCP port (default: 502)')
    args = parser.parse_args()
    # init modbus server and start it
    modbus_table = Modbus_Table_Class()
    modbus_table.set_bus_data(101,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(101,1231,2 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(102,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(103,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(104,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(105,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(106,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(107,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(108,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(109,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(110,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(111,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(112,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.set_bus_data(113,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    modbus_table.print_modbus_table()
    server = ModbusServer(host='0.0.0.0', port=args.port, data_bank=MyDataBank())
    
    server.start()
# python data.py --host 0.0.0.0
