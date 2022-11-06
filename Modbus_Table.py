#!/usr/bin/env python3

class Modbus_Table_Class():
    """
    there are 6 object:
    - Bus: Bus Number, Bus Name
    - Bus_Data: Bus_Number, Code, Udm, Normal, Normal_Vmin, Emergency_Vmax, Status
    - Gen_Data: Bus_Number, Unit, Pgen, Qgen, Status
    - Line_Data: From_Bus_Number, To_Bus_Number, ID, Imax, R,X,G
    - Shunt_Data: Bus_Number, G_Shunt, B_Shunt, Status
    - 2_Winding_Data: From_Bus_Number, To_Bus_Number, R, X, Winding_MVA_Base, Status
    Address for modbus of objects:
                |
    bus
    """
    QUANTITY_BUS = 100
    QUANTITY_BUS_DATA = 100

    # for bus object (11 x 2 byte) 
    BUS_START_INPUT_REG = 0
    BUS_END_INPUT_REG   = QUANTITY_BUS*11 - 1

    BUS_START_HOLDING_REG = 0
    BUS_END_HOLDING_REG = QUANTITY_BUS*11 - 1
    
    # for bus data object ( 12 x 2 bytes) quantity 100
    BUS_DATA_START_DISCRETE_INPUT = 0
    BUS_DATA_END_DISCRETE_INPUT = QUANTITY_BUS_DATA*1

    BUS_DATA_START_INPUT_REG = BUS_END_INPUT_REG + 1
    BUS_DATA_END_INPUT_REG = BUS_DATA_START_INPUT_REG + QUANTITY_BUS_DATA*12 - 1

    BUS_DATA_START_COIL = 0
    BUS_DATA_END_COIL = QUANTITY_BUS_DATA*1

    BUS_DATA_START_HOLDING_REG = BUS_END_HOLDING_REG + 1
    BUS_DATA_END_HOLDING_REG = BUS_DATA_START_HOLDING_REG + QUANTITY_BUS_DATA*12 - 1

    #  for gen data object 
    


    def __init__(self) -> None:
        """
        init tables
        """
        #for CSV input
        self.discrete_inputs_table = {}
        self.input_registers_table = {}
        #for CSV output
        self.coils_table = {}
        self.holding_registers_table = {}

    def set_bus(self,bus_number, bus_name):
        """
        Setting a bus. If this bus is existed, change value for bus, on the contrary,
        engine will create a new. 
        - bus_number : un signed int 16 bit. That will be stored in input register
        (0-)
        - bus_name : a string if length is longer than 10 letter, they will be cut
        - return True if setting successfully
        - return False if failed setting
        """
        return True

    def set_bus_data(self,
        bus_number, 
        code,
        udm,
        normal,
        normal_vmin,
        normal_vmax, 
        emergency_vmax,
        status):
        pass

    def set_gen_data(self,
        bus_number,
        unit,
        pgen,
        qgen,
        status):
        pass

    def set_line_data(self,
        from_bus_number,
        to_bus_number,
        id,
        imax,
        r,
        x,
        g):
        pass

    def set_shunt_data(self,
        bus_number,
        g_shunt,
        b_shunt,
        status):
        pass

    def set_2_winding_data(self,
        from_bus_number,
        to_bus_number,
        r,
        x,
        winding_mva_base,
        status):
        pass