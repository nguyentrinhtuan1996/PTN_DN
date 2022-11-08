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
from datetime import datetime
from Convert_Engine import Convent_Engine_Class

class MyDataBank(DataBank):
    """A custom ModbusServerDataBank for override get_holding_registers method."""

    def __init__(self):
        # turn off allocation of memory for standard modbus object types
        # only "holding registers" space will be replaced by dynamic build values.
        super().__init__(virtual_mode=True)
        self.convert_engine = Convent_Engine_Class()

    def get_holding_registers(self, address, number=1, srv_info=None):
        """Get virtual holding registers."""
        # populate virtual registers dict with current datetime values
        now = datetime.now()
        float_2byte = self.convert_engine.float_to_int16_IEEE(-2.25)
        v_regs_d = {0: float_2byte["First Byte"], 1: float_2byte["Second Byte"]}
        # build a list of virtual registers to return to server data handler
        # return None if any of virtual registers is missing
        try:
            return [v_regs_d[a] for a in range(address, address+number)]
        except KeyError:
            return


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='localhost', help='Host (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=502, help='TCP port (default: 502)')
    args = parser.parse_args()
    # init modbus server and start it
    server = ModbusServer(host='0.0.0.0', port=args.port, data_bank=MyDataBank())
    server.start()
# python data.py --host 0.0.0.0
