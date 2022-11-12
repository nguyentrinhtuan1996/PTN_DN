#!/usr/bin/env python3
from Convert_Engine import Convent_Engine_Class
class Modbus_Table_Class(Convent_Engine_Class):
    """
    there are 6 object:
    - Bus: Bus Number(1 int16), Bus Name(10 int16)
    - Bus_Data: Bus_Number(1 int16), Code(1 int16), Udm(1 float32), Normal(1 float32), Normal_Vmin(1 float32) , Emergency_Vmax(1 float32), Status(1 bool)
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
    QUANTITY_GEN_DATA = 100
    QUANTITY_LINE_DATA = 100
    QUANTITY_SHUNT_DATA = 100
    QUANTITY_2_WINDING_DATA = 100

    # for bus object (11 x 2 byte) 
    bus_object_number = 0
    BUS_NAME_MAX_LENGTH = 10
    BUS_FRAME_LENGTH = 11

    BUS_START_INPUT_REG = 0
    BUS_END_INPUT_REG   = QUANTITY_BUS*BUS_FRAME_LENGTH - 1

    BUS_START_HOLDING_REG = 0
    BUS_END_HOLDING_REG = QUANTITY_BUS*BUS_FRAME_LENGTH - 1
    
    # for bus data object ( 12 x 2 bytes) quantity 100
    bus_data_object_number = 0
    BUS_DATA_FRAME_LENGTH = 16

    BUS_DATA_START_INPUT_REG = BUS_END_INPUT_REG + 1
    BUS_DATA_END_INPUT_REG = BUS_DATA_START_INPUT_REG + QUANTITY_BUS_DATA*BUS_DATA_FRAME_LENGTH - 1

    BUS_DATA_START_HOLDING_REG = BUS_END_HOLDING_REG + 1
    BUS_DATA_END_HOLDING_REG = BUS_DATA_START_HOLDING_REG + QUANTITY_BUS_DATA*BUS_DATA_FRAME_LENGTH - 1

    #  for gen data object (13 X 2 bytes)
    gen_data_object_number = 0
    GEN_DATA_FRAME_LENGTH = 10

    GEN_DATA_START_INPUT_REG = BUS_DATA_END_INPUT_REG +1
    GEN_DATE_END_INPUT_REG = GEN_DATA_START_INPUT_REG + QUANTITY_GEN_DATA*GEN_DATA_FRAME_LENGTH -1

    GEN_DATA_START_HOLDING_REG = BUS_DATA_END_HOLDING_REG +1
    GEN_DATA_END_HOLDING_REG = GEN_DATA_START_HOLDING_REG + QUANTITY_GEN_DATA*GEN_DATA_FRAME_LENGTH -1

    # for line data object
    line_data_object_number = 0
    LINE_DATA_FRAME_LENGTH = 18

    LINE_DATA_START_INPUT_REG = GEN_DATE_END_INPUT_REG +1
    LINE_DATA_END_INPUT_REG = LINE_DATA_START_INPUT_REG + QUANTITY_LINE_DATA*LINE_DATA_FRAME_LENGTH -1

    LINE_DATA_START_HOLDING_REG = GEN_DATA_END_HOLDING_REG +1
    LINE_DATA_END_HOLDING_REG = LINE_DATA_START_HOLDING_REG + QUANTITY_LINE_DATA*LINE_DATA_FRAME_LENGTH -1

    # for shunt data object
    shunt_data_object_number = 0
    SHUNT_DATA_FRAME_LENGTH = 8

    SHUNT_DATA_START_INPUT_REG = LINE_DATA_END_INPUT_REG +1
    SHUNT_DATA_END_INPUT_REG = SHUNT_DATA_START_INPUT_REG + QUANTITY_SHUNT_DATA*SHUNT_DATA_FRAME_LENGTH -1

    SHUNT_DATA_START_HOLDING_REG = LINE_DATA_END_HOLDING_REG +1
    SHUNT_DATA_END_HOLDING_REG = SHUNT_DATA_START_HOLDING_REG + QUANTITY_SHUNT_DATA*SHUNT_DATA_FRAME_LENGTH -1

    # for 2 winding data
    two_winding_data_object_number = 0
    TWO_WINDING_DATA_FRAME_LENGTH = 12

    TWO_WINDING_DATA_START_INPUT_REG = SHUNT_DATA_END_INPUT_REG +1
    TWO_WINDING_DATA_END_INPUT_REG = TWO_WINDING_DATA_START_INPUT_REG + QUANTITY_2_WINDING_DATA*TWO_WINDING_DATA_FRAME_LENGTH -1

    TWO_WINDING_DATA_START_HOLDING_REG = SHUNT_DATA_END_HOLDING_REG +1
    TWO_WINDING_DATA_END_HOLDING_REG = TWO_WINDING_DATA_START_HOLDING_REG + QUANTITY_2_WINDING_DATA*TWO_WINDING_DATA_FRAME_LENGTH -1

    BUS_NUMBER = "Bus Number"
    BUS_NAME = "Bus Name"
    CODE = "Code"
    

    def __init__(self) -> None:
        """
        init tables
        """
        # these below array are raw data (16 bit registers) to load into modbus server
        #for CSV input
        self.discrete_inputs_number = 0
        self.discrete_inputs_table = []
        self.input_registers_number = 0
        self.input_registers_table = []
        #for CSV output
        self.coils_number = 0
        self.coils_table = []
        self.holding_registers_number = 0
        self.holding_registers_table = []
        # init modbus table

        # for input register
        for count in range(0, self.TWO_WINDING_DATA_END_INPUT_REG +1):
            self.input_registers_table.append(0)
        # for holding register 
        for count in range(0, self.TWO_WINDING_DATA_END_HOLDING_REG +1):
            self.holding_registers_table.append(0)
        
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
        # correct the bus_name
        if (len(bus_name) >10):
            bus_name = bus_name[:10]
        # var to check if this bus number is existing 
        
        for count in range (0, self.bus_object_number):
            # calculate the address of bus number
            bus_number_address = self.BUS_START_INPUT_REG + count*self.BUS_FRAME_LENGTH
            # found weather this bus number is existing 
            if(self.input_registers_table[bus_number_address] == bus_number):
                # read bus_name from modbus table
                # bus_name_list = list(bus_number)
                for count1 in range(0,self.BUS_NAME_MAX_LENGTH):
                    if (count1 < len(bus_name)):
                        self.input_registers_table[bus_number_address + count1 +1] = ord(bus_name[count1])
                        self.holding_registers_table[bus_number_address + count1 +1] = ord(bus_name[count1])
                    else:
                        self.input_registers_table[bus_number_address + count1 +1] = 0
                        self.holding_registers_table[bus_number_address + count1 +1] = 0

                # print(self.input_registers_table)
                return True
        # if there is no this bus number
        
        # calculate the address
        bus_number_address = self.BUS_START_INPUT_REG +  self.bus_object_number*self.BUS_FRAME_LENGTH
        # add bus number
        self.input_registers_table[bus_number_address] = bus_number
        self.holding_registers_table[bus_number_address] = bus_number
        # add bus_name
        for count1 in range(0,self.BUS_NAME_MAX_LENGTH):
            if (count1 < len(bus_name)):
                self.input_registers_table[bus_number_address + count1 +1] = ord(bus_name[count1])
                self.holding_registers_table[bus_number_address + count1 +1] = ord(bus_name[count1])
            else:
                self.input_registers_table[bus_number_address + count1 +1] = 0
                self.holding_registers_table[bus_number_address + count1 +1] = 0

        self.bus_object_number +=1
        # print(self.input_registers_table)
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
        """
        Set bus data with spec:
        - bus_number : int
        - code : int
        - udm : float
        - normal: float
        - normal_vmin : float
        - normal_vmax : float
        - emergency_vmax : float
        - status : bool
        """
        #  var to check this bus data is existed 
        
        # find to check
        for count in range(0, self.bus_data_object_number):
            #  calculate the address of bus data
            bus_data_address = self.BUS_DATA_START_INPUT_REG + count*self.BUS_DATA_FRAME_LENGTH
            bus_number_dict = self.convert_to_fp32(bus_number)

            # found if this bus data is existed
            if( self.input_registers_table[bus_data_address] == bus_number_dict["Second Byte"] and
                self.input_registers_table[bus_data_address +1] == bus_number_dict["First Byte"]):
                
                # for code
                code_dict = self.convert_to_fp32(code)
                self.input_registers_table[bus_data_address +2] = code_dict["Second Byte"]
                self.input_registers_table[bus_data_address +3] = code_dict["First Byte"]
                self.holding_registers_table[bus_data_address +2] = code_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +3] = code_dict["First Byte"]
                
                # for udm
                udm_dict = self.convert_to_fp32(udm)
                self.input_registers_table[bus_data_address +4] = udm_dict["Second Byte"]
                self.input_registers_table[bus_data_address +5] = udm_dict["First Byte"]
                self.holding_registers_table[bus_data_address +4] = udm_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +5] = udm_dict["First Byte"]
                #  for normal
                normal_dict = self.convert_to_fp32(normal)
                self.input_registers_table[bus_data_address +6] = normal_dict["Second Byte"]
                self.input_registers_table[bus_data_address +7] = normal_dict["First Byte"]
                self.holding_registers_table[bus_data_address +6] = normal_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +7] = normal_dict["First Byte"]
                #  for normal_vmin
                normal_vmin_dict = self.convert_to_fp32(normal_vmin)
                self.input_registers_table[bus_data_address +8] = normal_vmin_dict["Second Byte"]
                self.input_registers_table[bus_data_address +9] = normal_vmin_dict["First Byte"]
                self.holding_registers_table[bus_data_address +8] = normal_vmin_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +9] = normal_vmin_dict["First Byte"]
                # for normal_vmax 
                normal_vmax_dict = self.convert_to_fp32(normal_vmax)
                self.input_registers_table[bus_data_address +10] = normal_vmax_dict["Second Byte"]
                self.input_registers_table[bus_data_address +11] = normal_vmax_dict["First Byte"]
                self.holding_registers_table[bus_data_address +10] = normal_vmax_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +11] = normal_vmax_dict["First Byte"]
                #  for emergency_vmax
                emergency_vmax_dict = self.convert_to_fp32(emergency_vmax)
                self.input_registers_table[bus_data_address +12] = emergency_vmax_dict["Second Byte"]
                self.input_registers_table[bus_data_address +13] = emergency_vmax_dict["First Byte"]
                self.holding_registers_table[bus_data_address +12] = emergency_vmax_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +13] = emergency_vmax_dict["First Byte"]
                # for status
                status_dict = self.convert_to_fp32(status)
                self.input_registers_table[bus_data_address +14] = status_dict["Second Byte"]
                self.input_registers_table[bus_data_address +15] = status_dict["First Byte"]
                self.holding_registers_table[bus_data_address +14] = status_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +15] = status_dict["First Byte"]

                return True
        
        # if there is no this bus_number 
        # calculate the address
        bus_data_address = self.BUS_DATA_START_INPUT_REG + self.bus_data_object_number*self.BUS_DATA_FRAME_LENGTH

        # add bus_number
        bus_number_dict = self.convert_to_fp32(bus_number)
        self.input_registers_table[bus_data_address] = bus_number_dict["Second Byte"]
        self.input_registers_table[bus_data_address +1] = bus_number_dict["First Byte"]
        self.holding_registers_table[bus_data_address] = bus_number_dict["Second Byte"]
        self.holding_registers_table[bus_data_address +1] = bus_number_dict["First Byte"]
        
        # for code
        code_dict = self.convert_to_fp32(code)
        self.input_registers_table[bus_data_address +2] = code_dict["Second Byte"]
        self.input_registers_table[bus_data_address +3] = code_dict["First Byte"]
        self.holding_registers_table[bus_data_address +2] = code_dict["Second Byte"]
        self.holding_registers_table[bus_data_address +3] = code_dict["First Byte"]
        
        # for udm
        udm_dict = self.convert_to_fp32(udm)
        self.input_registers_table[bus_data_address +4] = udm_dict["Second Byte"]
        self.input_registers_table[bus_data_address +5] = udm_dict["First Byte"]
        self.holding_registers_table[bus_data_address +4] = udm_dict["Second Byte"]
        self.holding_registers_table[bus_data_address +5] = udm_dict["First Byte"]
        #  for normal
        normal_dict = self.convert_to_fp32(normal)
        self.input_registers_table[bus_data_address +6] = normal_dict["Second Byte"]
        self.input_registers_table[bus_data_address +7] = normal_dict["First Byte"]
        self.holding_registers_table[bus_data_address +6] = normal_dict["Second Byte"]
        self.holding_registers_table[bus_data_address +7] = normal_dict["First Byte"]
        #  for normal_vmin
        normal_vmin_dict = self.convert_to_fp32(normal_vmin)
        self.input_registers_table[bus_data_address +8] = normal_vmin_dict["Second Byte"]
        self.input_registers_table[bus_data_address +9] = normal_vmin_dict["First Byte"]
        self.holding_registers_table[bus_data_address +8] = normal_vmin_dict["Second Byte"]
        self.holding_registers_table[bus_data_address +9] = normal_vmin_dict["First Byte"]
        # for normal_vmax 
        normal_vmax_dict = self.convert_to_fp32(normal_vmax)
        self.input_registers_table[bus_data_address +10] = normal_vmax_dict["Second Byte"]
        self.input_registers_table[bus_data_address +11] = normal_vmax_dict["First Byte"]
        self.holding_registers_table[bus_data_address +10] = normal_vmax_dict["Second Byte"]
        self.holding_registers_table[bus_data_address +11] = normal_vmax_dict["First Byte"]
        #  for emergency_vmax
        emergency_vmax_dict = self.convert_to_fp32(emergency_vmax)
        self.input_registers_table[bus_data_address +12] = emergency_vmax_dict["Second Byte"]
        self.input_registers_table[bus_data_address +13] = emergency_vmax_dict["First Byte"]
        self.holding_registers_table[bus_data_address +12] = emergency_vmax_dict["Second Byte"]
        self.holding_registers_table[bus_data_address +13] = emergency_vmax_dict["First Byte"]
        # for status
        status_dict = self.convert_to_fp32(status)
        self.input_registers_table[bus_data_address +14] = status_dict["Second Byte"]
        self.input_registers_table[bus_data_address +15] = status_dict["First Byte"]
        self.holding_registers_table[bus_data_address +14] = status_dict["Second Byte"]
        self.holding_registers_table[bus_data_address +15] = status_dict["First Byte"]

        #  increase bus data object number
        self.bus_data_object_number +=1
        return True

    def set_gen_data(self,
        bus_number,
        unit,
        pgen,
        qgen,
        status):
        """
        Set gen data with :
        - bus_number : int16
        - unit : int16
        - pgen : float
        - qgen : float
        - status: bool
        """
        for count in range(0, self.gen_data_object_number):
            #  calculate the address of gen data
            gen_data_address = self.GEN_DATA_START_INPUT_REG + count*self.GEN_DATA_FRAME_LENGTH
            bus_number_dict = self.convert_to_fp32(bus_number)
            
            #  find this gen data
            if( self.input_registers_table[gen_data_address] == bus_number_dict["Second Byte"] and
                self.input_registers_table[gen_data_address +1] == bus_number_dict["First Byte"]):
                # change unit
                unit_dict = self.convert_to_fp32(unit)
                self.input_registers_table[gen_data_address +2] = unit_dict["Second Byte"]
                self.input_registers_table[gen_data_address +3] = unit_dict["First Byte"]
                self.holding_registers_table[gen_data_address +2] = unit_dict["Second Byte"]
                self.holding_registers_table[gen_data_address +3] = unit_dict["First Byte"]
                # change pgen
                pgen_dict = self.convert_to_fp32(pgen)
                self.input_registers_table[gen_data_address +4] = pgen_dict["Second Byte"]
                self.input_registers_table[gen_data_address +5] = pgen_dict["First Byte"]
                self.holding_registers_table[gen_data_address +4] = pgen_dict["Second Byte"]
                self.holding_registers_number[gen_data_address +5] = pgen_dict["First Byte"]
                # change the qgen
                qgen_dict = self.convert_to_fp32(qgen)
                self.input_registers_table[gen_data_address +6] = qgen_dict["Second Byte"]
                self.input_registers_table[gen_data_address +7] = qgen_dict["First Byte"]
                self.holding_registers_table[gen_data_address +6] = qgen_dict["Second Byte"]
                self.holding_registers_table[gen_data_address +7] = qgen_dict["First Byte"]
                #  change status
                status_dict = self.convert_to_fp32(status)
                self.input_registers_table[gen_data_address +8] = status_dict["Second Byte"]
                self.input_registers_table[gen_data_address +9] = status_dict["First Byte"]
                self.holding_registers_table[gen_data_address +8] = status_dict["Second Byte"]
                self.holding_registers_table[gen_data_address +9] = status_dict["First Byte"]

                return True
        
        # if there is no this gen_data
        #  calculate the address
        gen_data_address = self.GEN_DATA_START_INPUT_REG + self.gen_data_object_number*self.GEN_DATA_FRAME_LENGTH
        
        # add bus_number
        bus_number_dict = self.convert_to_fp32(bus_number)
        self.input_registers_table[gen_data_address] = bus_number_dict["Second Byte"]
        self.input_registers_table[gen_data_address +1] = bus_number_dict["First Byte"]
        self.holding_registers_table[gen_data_address] = bus_number_dict["Second Byte"]
        self.holding_registers_table[gen_data_address +1] = bus_number_dict["First Byte"]

        # change unit
        unit_dict = self.convert_to_fp32(unit)
        self.input_registers_table[gen_data_address +2] = unit_dict["Second Byte"]
        self.input_registers_table[gen_data_address +3] = unit_dict["First Byte"]
        self.holding_registers_table[gen_data_address +2] = unit_dict["Second Byte"]
        self.holding_registers_table[gen_data_address +3] = unit_dict["First Byte"]
        # change pgen
        pgen_dict = self.convert_to_fp32(pgen)
        self.input_registers_table[gen_data_address +4] = pgen_dict["Second Byte"]
        self.input_registers_table[gen_data_address +5] = pgen_dict["First Byte"]
        self.holding_registers_table[gen_data_address +4] = pgen_dict["Second Byte"]
        self.holding_registers_table[gen_data_address +5] = pgen_dict["First Byte"]
        # change the qgen
        qgen_dict = self.convert_to_fp32(qgen)
        self.input_registers_table[gen_data_address +6] = qgen_dict["Second Byte"]
        self.input_registers_table[gen_data_address +7] = qgen_dict["First Byte"]
        self.holding_registers_table[gen_data_address +6] = qgen_dict["Second Byte"]
        self.holding_registers_table[gen_data_address +7] = qgen_dict["First Byte"]
        #  change status
        status_dict = self.convert_to_fp32(status)
        self.input_registers_table[gen_data_address +8] = status_dict["Second Byte"]
        self.input_registers_table[gen_data_address +9] = status_dict["First Byte"]
        self.holding_registers_table[gen_data_address +8] = status_dict["Second Byte"]
        self.holding_registers_table[gen_data_address +9] = status_dict["First Byte"]
        #  increase the the object number
        self.gen_data_object_number +=1
        return True

    def set_line_data(self,
        from_bus_number,
        to_bus_number,
        ID,
        Imax,
        Rpu,
        Xpu,
        Gpu,
        Bpu,
        status):
        """
        set a line data with arguments:
        - from_bus_number : int16
        - to_bus_number : int16
        - ID
        - Imax,
        - Rpu,
        - Xpu,
        - Gpu,
        - Bpu,
        - status
        """
        for count in range(0, self.line_data_object_number):
            #  calculate addresses
            line_data_address = self.LINE_DATA_START_INPUT_REG + count*self.LINE_DATA_FRAME_LENGTH
            from_bus_number_dict = self.convert_to_fp32(from_bus_number)
            to_bus_number_dict = self.convert_to_fp32(to_bus_number)

            if( self.input_registers_table[line_data_address] == from_bus_number_dict["Second Byte"] and
                self.input_registers_table[line_data_address +1] == from_bus_number_dict["First Byte"] and
                self.input_registers_table[line_data_address +2] == to_bus_number_dict["Second Byte"] and
                self.input_registers_table[line_data_address +3] == to_bus_number_dict["First Byte"]):
                # change ID
                ID_dict = self.convert_to_fp32(ID)
                self.input_registers_table[line_data_address +4] = ID_dict["Second Byte"]
                self.input_registers_table[line_data_address +5] = ID_dict["First Byte"]
                self.holding_registers_table[line_data_address +4] = ID_dict["Second Byte"]
                self.holding_registers_table[line_data_address +5] = ID_dict["First Byte"]
                # change Imax
                Imax_dict = self.convert_to_fp32(Imax)
                self.input_registers_table[line_data_address +6] = Imax_dict["Second Byte"]
                self.input_registers_table[line_data_address +7] = Imax_dict["First Byte"]
                self.holding_registers_table[line_data_address +6] = Imax_dict["Second Byte"]
                self.holding_registers_table[line_data_address +7] = Imax_dict["First Byte"]
                # change Rpu
                Rpu_dict = self.convert_to_fp32(Rpu)
                self.input_registers_table[line_data_address +8] = Rpu_dict["Second Byte"]
                self.input_registers_table[line_data_address +9] = Rpu_dict["First Byte"]
                self.holding_registers_table[line_data_address +8] = Rpu_dict["Second Byte"]
                self.holding_registers_table[line_data_address +9] = Rpu_dict["First Byte"]
                # change Xpu
                Xpu_dict = self.convert_to_fp32(Xpu)
                self.input_registers_table[line_data_address +10] = Xpu_dict["Second Byte"]
                self.input_registers_table[line_data_address +11] = Xpu_dict["First Byte"]
                self.holding_registers_table[line_data_address +10] = Xpu_dict["Second Byte"]
                self.holding_registers_table[line_data_address +11] = Xpu_dict["First Byte"]
                # change Gpu
                Gpu_dict = self.convert_to_fp32(Gpu)
                self.input_registers_table[line_data_address +12] = Gpu_dict["Second Byte"]
                self.input_registers_table[line_data_address +13] = Gpu_dict["First Byte"]
                self.holding_registers_table[line_data_address +12] = Gpu_dict["Second Byte"]
                self.holding_registers_table[line_data_address +13] = Gpu_dict["First Byte"]
                # change Bpu
                Bpu_dict = self.convert_to_fp32(Bpu)
                self.input_registers_number[line_data_address +14] = Bpu_dict["Second Byte"]
                self.input_registers_number[line_data_address +15] = Bpu_dict["First Byte"]
                self.holding_registers_table[line_data_address +14] = Bpu_dict["Second Byte"]
                self.holding_registers_table[line_data_address +15] = Bpu_dict["First Byte"]
                #  change status
                status_dict = self.convert_to_fp32(status)
                self.input_registers_number[line_data_address +16] = status_dict["Second Byte"]
                self.input_registers_number[line_data_address +17] = status_dict["First Byte"]
                self.holding_registers_table[line_data_address +16] = status_dict["Second Byte"]
                self.holding_registers_table[line_data_address +17] = status_dict["First Byte"]

                return True
        # if there is no this line data
        #  calculate the address
        line_data_address = self.LINE_DATA_START_INPUT_REG + self.line_data_object_number*self.LINE_DATA_FRAME_LENGTH
        # add from_bus_number
        from_bus_number_dict = self.convert_to_fp32(from_bus_number)
        self.input_registers_table[line_data_address] = from_bus_number_dict["Second Byte"] 
        self.input_registers_table[line_data_address +1] = from_bus_number_dict["First Byte"]
        self.holding_registers_table[line_data_address] = from_bus_number_dict["Second Byte"] 
        self.holding_registers_table[line_data_address +1] = from_bus_number_dict["First Byte"]
        # add to bus number
        to_bus_number_dict = self.convert_to_fp32(to_bus_number)
        self.input_registers_table[line_data_address +2] = to_bus_number_dict["Second Byte"]
        self.input_registers_table[line_data_address +3] = to_bus_number_dict["First Byte"]
        self.holding_registers_table[line_data_address +2] = to_bus_number_dict["Second Byte"]
        self.holding_registers_table[line_data_address +3] = to_bus_number_dict["First Byte"]
        # change ID
        ID_dict = self.convert_to_fp32(ID)
        self.input_registers_table[line_data_address +4] = ID_dict["Second Byte"]
        self.input_registers_table[line_data_address +5] = ID_dict["First Byte"]
        self.holding_registers_table[line_data_address +4] = ID_dict["Second Byte"]
        self.holding_registers_table[line_data_address +5] = ID_dict["First Byte"]
        # change Imax
        Imax_dict = self.convert_to_fp32(Imax)
        self.input_registers_table[line_data_address +6] = Imax_dict["Second Byte"]
        self.input_registers_table[line_data_address +7] = Imax_dict["First Byte"]
        self.holding_registers_table[line_data_address +6] = Imax_dict["Second Byte"]
        self.holding_registers_table[line_data_address +7] = Imax_dict["First Byte"]
        # change Rpu
        Rpu_dict = self.convert_to_fp32(Rpu)
        self.input_registers_table[line_data_address +8] = Rpu_dict["Second Byte"]
        self.input_registers_table[line_data_address +9] = Rpu_dict["First Byte"]
        self.holding_registers_table[line_data_address +8] = Rpu_dict["Second Byte"]
        self.holding_registers_table[line_data_address +9] = Rpu_dict["First Byte"]
        # change Xpu
        Xpu_dict = self.convert_to_fp32(Xpu)
        self.input_registers_table[line_data_address +10] = Xpu_dict["Second Byte"]
        self.input_registers_table[line_data_address +11] = Xpu_dict["First Byte"]
        self.holding_registers_table[line_data_address +10] = Xpu_dict["Second Byte"]
        self.holding_registers_table[line_data_address +11] = Xpu_dict["First Byte"]
        # change Gpu
        Gpu_dict = self.convert_to_fp32(Gpu)
        self.input_registers_table[line_data_address +12] = Gpu_dict["Second Byte"]
        self.input_registers_table[line_data_address +13] = Gpu_dict["First Byte"]
        self.holding_registers_table[line_data_address +12] = Gpu_dict["Second Byte"]
        self.holding_registers_table[line_data_address +13] = Gpu_dict["First Byte"]
        # change Bpu
        Bpu_dict = self.convert_to_fp32(Bpu)
        self.input_registers_table[line_data_address +14] = Bpu_dict["Second Byte"]
        self.input_registers_table[line_data_address +15] = Bpu_dict["First Byte"]
        self.holding_registers_table[line_data_address +14] = Bpu_dict["Second Byte"]
        self.holding_registers_table[line_data_address +15] = Bpu_dict["First Byte"]
        #  change status
        status_dict = self.convert_to_fp32(status)
        self.input_registers_table[line_data_address +16] = status_dict["Second Byte"]
        self.input_registers_table[line_data_address +17] = status_dict["First Byte"]
        self.holding_registers_table[line_data_address +16] = status_dict["Second Byte"]
        self.holding_registers_table[line_data_address +17] = status_dict["First Byte"]
        #  increase the object number
        self.line_data_object_number +=1

        return True

    def set_shunt_data(self,
        bus_number,
        g_shunt,
        b_shunt,
        status):
        """
        Set a shunt data with arguments:
        - bus_number : in16
        - g_shunt : float
        - b_shunt : float
        - status : bool
        """
        for count in range(0, self.shunt_data_object_number):
            #  calculate the address
            shunt_data_address = self.SHUNT_DATA_START_INPUT_REG + count*self.SHUNT_DATA_FRAME_LENGTH
            bus_number_dict = self.convert_to_fp32(bus_number)

            # found if this shunt data is existed
            if( self.input_registers_table[shunt_data_address] == bus_number_dict["Second Byte"] and
                self.input_registers_table[shunt_data_address +1] == bus_number_dict["First Byte"]):
                #  change the g_shunt
                g_shunt_dict = self.convert_to_fp32(g_shunt)
                self.input_registers_table[shunt_data_address +2] = g_shunt_dict["Second Byte"]
                self.input_registers_table[shunt_data_address +3] = g_shunt_dict["First Byte"]
                self.holding_registers_table[shunt_data_address +2] = g_shunt_dict["Second Byte"]
                self.holding_registers_table[shunt_data_address +3] = g_shunt_dict["First Byte"]
                #  change b_shunt
                b_shunt_dict = self.convert_to_fp32(b_shunt)
                self.input_registers_table[shunt_data_address +4] = b_shunt_dict["Second Byte"]
                self.input_registers_table[shunt_data_address +5] = b_shunt_dict["First Byte"]
                self.holding_registers_table[shunt_data_address +4] = b_shunt_dict["Second Byte"]
                self.holding_registers_table[shunt_data_address +5] = b_shunt_dict["First Byte"]
                # for status
                status_dict = self.convert_to_fp32(status)
                self.input_registers_table[shunt_data_address +6] = status_dict["Second Byte"]
                self.input_registers_table[shunt_data_address +7] = status_dict["First Byte"]
                self.holding_registers_table[shunt_data_address +6] = status_dict["Second Byte"]
                self.holding_registers_table[shunt_data_address +7] = status_dict["First Byte"]

                return True
        
        # if there is no this shunt data
        # calculate address
        shunt_data_address = self.SHUNT_DATA_START_INPUT_REG + self.shunt_data_object_number*self.SHUNT_DATA_FRAME_LENGTH
        # add bus_number
        bus_number_dict = self.convert_to_fp32(bus_number)
        self.input_registers_table[shunt_data_address] = bus_number_dict["Second Byte"]
        self.input_registers_table[shunt_data_address +1] = bus_number_dict["First Byte"]
        self.holding_registers_table[shunt_data_address] = bus_number_dict["Second Byte"]
        self.holding_registers_table[shunt_data_address +1] = bus_number_dict["First Byte"]
        #  change the g_shunt
        g_shunt_dict = self.convert_to_fp32(g_shunt)
        self.input_registers_table[shunt_data_address +2] = g_shunt_dict["Second Byte"]
        self.input_registers_table[shunt_data_address +3] = g_shunt_dict["First Byte"]
        self.holding_registers_table[shunt_data_address +2] = g_shunt_dict["Second Byte"]
        self.holding_registers_table[shunt_data_address +3] = g_shunt_dict["First Byte"]
        #  change b_shunt
        b_shunt_dict = self.convert_to_fp32(b_shunt)
        self.input_registers_table[shunt_data_address +4] = b_shunt_dict["Second Byte"]
        self.input_registers_table[shunt_data_address +5] = b_shunt_dict["First Byte"]
        self.holding_registers_table[shunt_data_address +4] = b_shunt_dict["Second Byte"]
        self.holding_registers_table[shunt_data_address +5] = b_shunt_dict["First Byte"]
        # for status
        status_dict = self.convert_to_fp32(status)
        self.input_registers_table[shunt_data_address +6] = status_dict["Second Byte"]
        self.input_registers_table[shunt_data_address +7] = status_dict["First Byte"]
        self.holding_registers_table[shunt_data_address +6] = status_dict["Second Byte"]
        self.holding_registers_table[shunt_data_address +7] = status_dict["First Byte"]
        #  increase the shunt data object 
        self.shunt_data_object_number +=1
        return True

    def set_two_winding_data(self,
        from_bus_number,
        to_bus_number,
        Rpu,
        Xpu,
        winding_MVA_base,
        status):
        """
        Set 2winding_data with arguments:
        - from_bus_number : int16
        - to_bus_number: int16
        - Rpu; float
        - Xpu: float
        - winding_MVA_base: int16
        - status: bool
        """
        #  find to check
        for count in range(0, self.two_winding_data_object_number):
            # calculate address of 2winding_data
            two_winding_data_address = self.TWO_WINDING_DATA_START_INPUT_REG + count*self.TWO_WINDING_DATA_FRAME_LENGTH
            from_bus_number_dict = self.convert_to_fp32(from_bus_number)
            to_bus_number_dict = self.convert_to_fp32(to_bus_number)

            if( self.input_registers_table[two_winding_data_address] == from_bus_number_dict["Second Byte"] and
                self.input_registers_table[two_winding_data_address +1] == from_bus_number_dict["First Byte"] and
                self.input_registers_table[two_winding_data_address +2] == to_bus_number_dict["Second Byte"] and
                self.input_registers_table[two_winding_data_address +3] == to_bus_number_dict["First Byte"]):
                #  change Rpu
                Rpu_dict = self.convert_to_fp32(Rpu)
                self.input_registers_table[two_winding_data_address +4] = Rpu_dict["Second Byte"]
                self.input_registers_table[two_winding_data_address +5] = Rpu_dict["First Byte"]
                self.holding_registers_table[two_winding_data_address +4] = Rpu_dict["Second Byte"]
                self.holding_registers_table[two_winding_data_address +5] = Rpu_dict["First Byte"]
                # change Xpu
                Xpu_dict = self.convert_to_fp32(Xpu)
                self.input_registers_table[two_winding_data_address +6] = Xpu_dict["Second Byte"]
                self.input_registers_table[two_winding_data_address +7] = Xpu_dict["First Byte"]
                self.holding_registers_table[two_winding_data_address +6] = Xpu_dict["Second Byte"]
                self.holding_registers_table[two_winding_data_address +7] = Xpu_dict["First Byte"]
                # change Winding MVA Base
                winding_MVA_base_dict = self.convert_to_fp32(winding_MVA_base)
                self.input_registers_table[two_winding_data_address +8] = winding_MVA_base_dict["Second Byte"]
                self.holding_registers_table[two_winding_data_address +9] = winding_MVA_base_dict["First Byte"]
                self.holding_registers_table[two_winding_data_address +8] = winding_MVA_base_dict["Second Byte"]
                self.holding_registers_table[two_winding_data_address +9] = winding_MVA_base_dict["First Byte"]
                # for status
                status_dict = self.convert_to_fp32(status)
                self.input_registers_table[two_winding_data_address +10] = status_dict["Second Byte"]
                self.input_registers_table[two_winding_data_address +11] = status_dict["First Byte"]
                self.holding_registers_table[two_winding_data_address +10] = status_dict["Second Byte"]
                self.holding_registers_table[two_winding_data_address +11] = status_dict["First Byte"]
                
                return True
        # if there is no 2winding data
        # calculate address
        two_winding_data_address = self.TWO_WINDING_DATA_START_INPUT_REG + self.two_winding_data_object_number*self.TWO_WINDING_DATA_FRAME_LENGTH
        # from bus number
        from_bus_number_dict = self.convert_to_fp32(from_bus_number)
        self.input_registers_table[two_winding_data_address] = from_bus_number_dict["Second Byte"]
        self.input_registers_table[two_winding_data_address +1] = from_bus_number_dict["First Byte"]
        self.holding_registers_table[two_winding_data_address] = from_bus_number_dict["Second Byte"]
        self.holding_registers_table[two_winding_data_address +1] = from_bus_number_dict["First Byte"]
        # add to bus number
        to_bus_number_dict = self.convert_to_fp32(to_bus_number)
        self.input_registers_table[two_winding_data_address +2] = to_bus_number_dict["Second Byte"]
        self.input_registers_table[two_winding_data_address +3] = to_bus_number_dict["First Byte"]
        self.holding_registers_table[two_winding_data_address +2] = to_bus_number_dict["Second Byte"]
        self.holding_registers_table[two_winding_data_address +3] = to_bus_number_dict["First Byte"]
        #  change Rpu
        Rpu_dict = self.convert_to_fp32(Rpu)
        self.input_registers_table[two_winding_data_address +4] = Rpu_dict["Second Byte"]
        self.input_registers_table[two_winding_data_address +5] = Rpu_dict["First Byte"]
        self.holding_registers_table[two_winding_data_address +4] = Rpu_dict["Second Byte"]
        self.holding_registers_table[two_winding_data_address +5] = Rpu_dict["First Byte"]
        # change Xpu
        Xpu_dict = self.convert_to_fp32(Xpu)
        self.input_registers_table[two_winding_data_address +6] = Xpu_dict["Second Byte"]
        self.input_registers_table[two_winding_data_address +7] = Xpu_dict["First Byte"]
        self.holding_registers_table[two_winding_data_address +6] = Xpu_dict["Second Byte"]
        self.holding_registers_table[two_winding_data_address +7] = Xpu_dict["First Byte"]
        # change Winding MVA Base
        winding_MVA_base_dict = self.convert_to_fp32(winding_MVA_base)
        self.input_registers_table[two_winding_data_address +8] = winding_MVA_base_dict["Second Byte"]
        self.holding_registers_table[two_winding_data_address +9] = winding_MVA_base_dict["First Byte"]
        self.holding_registers_table[two_winding_data_address +8] = winding_MVA_base_dict["Second Byte"]
        self.holding_registers_table[two_winding_data_address +9] = winding_MVA_base_dict["First Byte"]
        # for status
        status_dict = self.convert_to_fp32(status)
        self.input_registers_table[two_winding_data_address +10] = status_dict["Second Byte"]
        self.input_registers_table[two_winding_data_address +11] = status_dict["First Byte"]
        self.holding_registers_table[two_winding_data_address +10] = status_dict["Second Byte"]
        self.holding_registers_table[two_winding_data_address +11] = status_dict["First Byte"]
        # increase the object
        self.two_winding_data_object_number +=1
        
        return True

    def print_modbus_table(self):
        # print input register table
        for count in range(0,len(self.input_registers_table)):
            if (self.input_registers_table[count] !=None):
                print("Input register [{index}]:{value} - {value1}".format( 
                    index = count, 
                    value = self.input_registers_table[count],
                    value1 = bin(self.input_registers_table[count])
                ))
        # print holding register table
        for count in range(0,len(self.holding_registers_table)):
            if (self.holding_registers_table[count] !=None):
                print("Holding register [{index}]:{value} - {value1}".format( 
                    index = count, 
                    value = self.holding_registers_table[count], 
                    value1 = bin(self.holding_registers_table[count])
                ))
    
    def get_bus_name(self, bus_number):
        """
        get the bus name that is store in to bus number
        - bus_number
        - return (string) bus name
        - return False if there is no this bus_number
        """
        for count in range(0, self.bus_object_number):
            # calculate the address of bus number
            bus_number_address = self.BUS_START_HOLDING_REG + count*self.BUS_FRAME_LENGTH
            # found weather this bus number is existing 
            if(self.holding_registers_table[bus_number_address] == bus_number):
                bus_name = ''
                # read bus_name from modbus table
                for count1 in range(1,self.BUS_NAME_MAX_LENGTH +1):
                    bus_name = bus_name + chr((self.holding_registers_table[bus_number_address + count1]))
                return bus_name
        # this bus number is not existing
        return False
    
    def get_bus_data(self, bus_number):
        for count in range(0, self.bus_data_object_number):
            # calculate the address of bus number
            bus_data_address = self.BUS_DATA_START_HOLDING_REG + count*self.BUS_DATA_FRAME_LENGTH
            bus_number_dict = self.convert_to_fp32(bus_number)
            #  find weather this bus number is existing 
            if( self.input_registers_table[bus_data_address] == bus_number_dict["Second Byte"] and
                self.input_registers_table[bus_data_address +1] == bus_number_dict["First Byte"]):
                bus_data_dict = {}
                # Bus_Number
                bus_data_dict["Bus_Number"] = self.convert_to_real(
                    self.holding_registers_table[bus_data_address +1],
                    self.holding_registers_table[bus_data_address ]
                )
                # Code
                bus_data_dict["Code"] = self.convert_to_real(
                    self.holding_registers_table[bus_data_address +3],
                    self.holding_registers_table[bus_data_address +2]
                )
                # Udm
                bus_data_dict["Udm"] =  self.convert_to_real(
                    self.holding_registers_table[bus_data_address +5],
                    self.holding_registers_table[bus_data_address +4]
                )
                # Normal
                bus_data_dict["Normal"] = self.convert_to_real(
                    self.holding_registers_table[bus_data_address +7],
                    self.holding_registers_table[bus_data_address +6]
                )
                #  Normal_Vmin
                bus_data_dict["Normal_Vmin"] = self.convert_to_real(
                    self.holding_registers_table[bus_data_address +9],
                    self.holding_registers_table[bus_data_address +8]
                )
                # Normal_Vmax
                bus_data_dict["Normal_Vmax"] = self.convert_to_real(
                    self.holding_registers_table[bus_data_address +11],
                    self.holding_registers_table[bus_data_address +10]
                )
                # for Emergency_Vmax
                bus_data_dict["Emergency_Vmax"] = self.convert_to_real(
                    self.holding_registers_table[bus_data_address +13],
                    self.holding_registers_table[bus_data_address +12]
                )
                # for status
                bus_data_dict["Status"] =self.convert_to_real(
                    self.holding_registers_table[bus_data_address +15],
                    self.holding_registers_table[bus_data_address +14]
                )
                
                return bus_data_dict
        # not found this bus data
        return False

    def get_gen_data(self, bus_number):
        for count in range(0, self.gen_data_object_number):
            # calculate the address if gen data
            gen_data_address = self.GEN_DATA_START_HOLDING_REG + count*self.GEN_DATA_FRAME_LENGTH
            bus_number_dict = self.convert_to_fp32(bus_number)
            #  if found this bus number is existing
            if( self.input_registers_table[gen_data_address] == bus_number_dict["Second Byte"] and
                self.input_registers_table[gen_data_address +1] == bus_number_dict["First Byte"]):
                gen_data_dict = {}
                # Bus_Number 
                gen_data_dict["Bus_Number"] = self.convert_to_real(
                    self.holding_registers_table[gen_data_address +1],
                    self.holding_registers_table[gen_data_address ]
                )
                # Unit
                gen_data_dict["Unit"] = self.convert_to_real(
                    self.holding_registers_table[gen_data_address +3],
                    self.holding_registers_table[gen_data_address +2]
                )
                # Pgen
                gen_data_dict["Pgen"] = self.convert_to_real(
                    self.holding_registers_table[gen_data_address +5],
                    self.holding_registers_table[gen_data_address +4]
                )
                # Qgen
                gen_data_dict["Qgen"] = self.convert_to_real(
                    self.holding_registers_table[gen_data_address +7],
                    self.holding_registers_table[gen_data_address +6]
                )
                # Status
                gen_data_dict["Status"] = self.convert_to_real(
                    self.holding_registers_table[gen_data_address +9],
                    self.holding_registers_table[gen_data_address +8]
                )

                return gen_data_dict
        # if not found gen data
        return False
                
    def get_line_data(self, from_bus_number, to_bus_number):
        for count in range(0, self.line_data_object_number):
            # calculate the address
            line_data_address = self.LINE_DATA_START_HOLDING_REG + count*self.LINE_DATA_FRAME_LENGTH
            from_bus_number_dict = self.convert_to_fp32(from_bus_number)
            to_bus_number_dict = self.convert_to_fp32(to_bus_number)
            # if found this bus line data
            if( self.input_registers_table[line_data_address] == from_bus_number_dict["Second Byte"] and
                self.input_registers_table[line_data_address +1] == from_bus_number_dict["First Byte"] and
                self.input_registers_table[line_data_address +2] == to_bus_number_dict["Second Byte"] and
                self.input_registers_table[line_data_address +3] == to_bus_number_dict["First Byte"]):
                    line_data_dict = {}
                    # from_bus_number
                    line_data_dict["From_Bus_Number"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address +1],
                        self.holding_registers_table[line_data_address]
                    )

                    #  to_bus_number
                    line_data_dict["To_Bus_Number"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address +3],
                        self.holding_registers_table[line_data_address +2]
                    )
                    # ID
                    line_data_dict["ID"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address +5],
                        self.holding_registers_table[line_data_address +4]
                    )
                    #  Imax
                    line_data_dict["Imax"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address +7],
                        self.holding_registers_table[line_data_address +6]
                    )
                    # Rpu
                    line_data_dict["Rpu"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address +9],
                        self.holding_registers_table[line_data_address +8]
                    )
                    # Xpu
                    line_data_dict["Xpu"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address +11],
                        self.holding_registers_table[line_data_address +10]
                    )
                    #  Gpu
                    line_data_dict["Gpu"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address +13], 
                        self.holding_registers_table[line_data_address +12] 
                    )
                    #  Bpu 
                    line_data_dict["Bpu"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address + 15],
                        self.holding_registers_table[line_data_address + 14]
                    )
                    # status
                    line_data_dict["Status"] = self.convert_to_real(
                        self.holding_registers_table[line_data_address + 17],
                        self.holding_registers_table[line_data_address + 16]
                    )
                    return line_data_dict

        return False

    def get_shunt_data(self, bus_number):
        for count in range(0, self.shunt_data_object_number):
            # calculate the address
            bus_number_address = self.SHUNT_DATA_START_HOLDING_REG + count*self.SHUNT_DATA_FRAME_LENGTH
            bus_number_dict = self.convert_to_fp32(bus_number)
            # find the bus_number
            if( self.input_registers_table[bus_number_address] == bus_number_dict["Second Byte"] and
                self.input_registers_table[bus_number_address +1] == bus_number_dict["First Byte"]):
                shunt_data_dict = {}
                # Bus_Number   
                shunt_data_dict["Bus_Number"] = self.convert_to_real(
                    self.holding_registers_table[bus_number_address +1],
                    self.holding_registers_table[bus_number_address ]
                )
                # G_Shunt
                shunt_data_dict["G_Shunt"] = self.convert_to_real(
                    self.holding_registers_table[bus_number_address +3],
                    self.holding_registers_table[bus_number_address +2]
                )
                #  B_Shunt
                shunt_data_dict["B_Shunt"] = self.convert_to_real(
                    self.holding_registers_table[bus_number_address +5],
                    self.holding_registers_table[bus_number_address +4]
                )
                #  status
                shunt_data_dict["Status"] = self.convert_to_real(
                    self.holding_registers_table[bus_number_address +7],
                    self.holding_registers_table[bus_number_address +6]
                )

                return shunt_data_dict
        return False
    
    def get_two_winding_data(self,from_bus_number, to_bus_number):
        for count in range(0, self.two_winding_data_object_number):
            # calculate the address
            two_winding_data_address = self.TWO_WINDING_DATA_START_HOLDING_REG + count*self.TWO_WINDING_DATA_FRAME_LENGTH
            from_bus_number_dict = self.convert_to_fp32(from_bus_number)
            to_bus_number_dict = self.convert_to_fp32(to_bus_number)
            # if found this twp winding data
            if(self.input_registers_table[two_winding_data_address] == from_bus_number_dict["Second Byte"] and
                self.input_registers_table[two_winding_data_address +1] == from_bus_number_dict["First Byte"] and
                self.input_registers_table[two_winding_data_address +2] == to_bus_number_dict["Second Byte"] and
                self.input_registers_table[two_winding_data_address +3] == to_bus_number_dict["First Byte"]):

                two_winding_data_dict = {}
                # from bus number
                two_winding_data_dict["From_Bus_Number"] = self.convert_to_real(
                    self.holding_registers_table[two_winding_data_address +1],
                    self.holding_registers_table[two_winding_data_address ]
                )
                #  to bus number 
                two_winding_data_dict["To_Bus_Number"] = self.convert_to_real(
                    self.holding_registers_table[two_winding_data_address +3],
                    self.holding_registers_table[two_winding_data_address +2]
                )
                #  Rpu
                two_winding_data_dict["Rpu"] = self.convert_to_real(
                    self.holding_registers_table[two_winding_data_address +5],
                    self.holding_registers_table[two_winding_data_address +4]
                )
                # Xpu
                two_winding_data_dict["Xpu"] = self.convert_to_real(
                    self.holding_registers_table[two_winding_data_address +7],
                    self.holding_registers_table[two_winding_data_address +6]
                )
                # Winding MVA Base
                two_winding_data_dict["Winding_MVA_Base"] = self.convert_to_real(
                    self.holding_registers_table[two_winding_data_address +9],
                    self.holding_registers_table[two_winding_data_address +8]
                )
                # Status
                two_winding_data_dict["Status"] = self.convert_to_real(
                    self.holding_registers_table[two_winding_data_address +11],
                    self.holding_registers_table[two_winding_data_address +10]
                )

                return two_winding_data_dict

        return False

if __name__ == '__main__':
    modbus_table = Modbus_Table_Class()
    # modbus_table.set_bus(101,'123345')
    # modbus_table.set_bus_data(101,1,1.02 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_bus_data(101,1,1.0001 ,3.5 ,4.5 ,5.5 ,6.5 ,1)
    # modbus_table.set_gen_data(101,2,1.02 ,3.5 ,0)
    # modbus_table.set_line_data(101,102,1,1.1,1.1,1,1,1,1)
    # modbus_table.set_shunt_data(101,1,1,1)
    # modbus_table.set_two_winding_data(101,102,1,1,1,0)
    # modbus_table.print_modbus_table()


    # modbus_table.set_bus(103,'you see')
    # modbus_table.set_bus(101,'buzz')
    # modbus_table.set_bus(102,'123 zo')
    # print(modbus_table.get_bus_name(101))
    # print(modbus_table.get_bus_data(101))
    # print(modbus_table.get_gen_data(101))
    # print(modbus_table.get_line_data(101,102))
    # print(modbus_table.get_shunt_data(101))
    # print(modbus_table.get_two_winding_data(from_bus_number=101,to_bus_number=102)) 

    # print(modbus_table.convert_to_fp32(101))
    # print(modbus_table.convert_to_fp32(102))