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
    """
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

    def set_bus(self,bus_number, Bus_name):
        pass

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