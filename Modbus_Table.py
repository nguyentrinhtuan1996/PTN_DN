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
    BUS_END_INPUT_REG   = QUANTITY_BUS*(BUS_NAME_MAX_LENGTH + 1) - 1

    BUS_START_HOLDING_REG = 0
    BUS_END_HOLDING_REG = QUANTITY_BUS*(BUS_NAME_MAX_LENGTH + 1) - 1
    
    # for bus data object ( 12 x 2 bytes) quantity 100
    bus_data_object_number = 0
    BUS_DATA_FRAME_LENGTH = 12

    BUS_DATA_START_DISCRETE_INPUT = 0
    BUS_DATA_END_DISCRETE_INPUT = QUANTITY_BUS_DATA*1 -1

    BUS_DATA_START_INPUT_REG = BUS_END_INPUT_REG + 1
    BUS_DATA_END_INPUT_REG = BUS_DATA_START_INPUT_REG + QUANTITY_BUS_DATA*12 - 1

    BUS_DATA_START_COIL = 0
    BUS_DATA_END_COIL = QUANTITY_BUS_DATA*1 -1

    BUS_DATA_START_HOLDING_REG = BUS_END_HOLDING_REG + 1
    BUS_DATA_END_HOLDING_REG = BUS_DATA_START_HOLDING_REG + QUANTITY_BUS_DATA*12 - 1

    #  for gen data object (13 X 2 bytes)
    GEN_DATA_START_DISCRETE_INPUT = BUS_DATA_END_DISCRETE_INPUT +1 
    GEN_DATA_END_DISCRETE_INPUT = GEN_DATA_START_DISCRETE_INPUT + QUANTITY_GEN_DATA*1 -1 

    GEN_DATA_START_INPUT_REG = BUS_DATA_END_INPUT_REG +1
    GEN_DATE_END_INPUT_REG = GEN_DATA_START_INPUT_REG + QUANTITY_GEN_DATA*5 -1

    GEN_DATA_START_COIL = BUS_DATA_END_COIL +1
    GEN_DATA_END_COIL = GEN_DATA_START_COIL + QUANTITY_GEN_DATA*1 -1

    GEN_DATA_START_HOLDING_REG = BUS_DATA_END_HOLDING_REG +1
    GEN_DATA_END_HOLDING_REG = GEN_DATA_START_HOLDING_REG + QUANTITY_GEN_DATA*5 -1

    # for line data object
    LINE_DATA_START_DISCRETE_INPUT = GEN_DATA_END_DISCRETE_INPUT +1
    LINE_DATA_END_DISCRETE_INPUT = LINE_DATA_START_DISCRETE_INPUT + QUANTITY_LINE_DATA*1 -1

    LINE_DATA_START_INPUT_REG = GEN_DATE_END_INPUT_REG +1
    LINE_DATA_END_INPUT_REG = LINE_DATA_START_INPUT_REG + QUANTITY_LINE_DATA*13 -1

    LINE_DATA_START_COIL = GEN_DATA_END_COIL +1
    LINE_DATA_END_COIL = LINE_DATA_START_COIL + QUANTITY_LINE_DATA*1 -1

    LINE_DATA_START_HOLDING_REG = GEN_DATA_END_HOLDING_REG +1
    LINE_DATA_END_HOLDING_REG = LINE_DATA_START_HOLDING_REG + QUANTITY_LINE_DATA*13 -1

    # for shunt data object
    SHUNT_DATA_START_DISCRETE_INPUT = LINE_DATA_END_DISCRETE_INPUT +1
    SHUNT_DATA_END_DISCRETE_INPUT = SHUNT_DATA_START_DISCRETE_INPUT + QUANTITY_SHUNT_DATA*1 -1

    SHUNT_DATA_START_INPUT_REG = LINE_DATA_END_INPUT_REG +1
    SHUNT_DATA_END_INPUT_REG = SHUNT_DATA_START_INPUT_REG + QUANTITY_SHUNT_DATA*3 -1

    SHUNT_DATA_START_COIL = LINE_DATA_END_COIL +1
    SHUNT_DATA_END_COIL = SHUNT_DATA_START_COIL + QUANTITY_SHUNT_DATA*1 -1

    SHUNT_DATA_START_HOLDING_REG = LINE_DATA_END_HOLDING_REG +1
    SHUNT_DATA_END_HOLDING_REG = SHUNT_DATA_START_HOLDING_REG + QUANTITY_SHUNT_DATA*3 -1

    # for 2 winding data
    TWO_WINDING_DATA_START_DISCRETE_INPUT = SHUNT_DATA_END_DISCRETE_INPUT +1
    TWO_WINDING_DATA_END_DISCRETE_INPUT = TWO_WINDING_DATA_START_DISCRETE_INPUT + QUANTITY_2_WINDING_DATA*1 -1 

    TWO_WINDING_DATA_START_INPUT_REG = SHUNT_DATA_END_INPUT_REG +1
    TWO_WINDING_DATA_END_INPUT_REG = TWO_WINDING_DATA_START_INPUT_REG + QUANTITY_2_WINDING_DATA*7 -1

    TWO_WINGDING_DATA_START_COIL = SHUNT_DATA_END_COIL +1
    TWO_WINGDING_DATA_END_COIL = TWO_WINGDING_DATA_START_COIL + QUANTITY_2_WINDING_DATA*1 -1

    TWO_WINDING_DATA_START_HOLDING_REG = SHUNT_DATA_END_HOLDING_REG +1
    TWO_WINDING_DATA_END_HOLDING_REG = TWO_WINDING_DATA_START_HOLDING_REG + QUANTITY_2_WINDING_DATA*7 -1

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
        # discrete_inputs_table
        for count in range(0, self.TWO_WINDING_DATA_END_DISCRETE_INPUT +1):
            self.discrete_inputs_table.append(0)
        # for input register
        for count in range(0, self.TWO_WINDING_DATA_END_INPUT_REG +1):
            self.input_registers_table.append(0)
        # for coils table
        for count in range(0, self.TWO_WINGDING_DATA_END_COIL +1):
            self.coils_table.append(0)
        # for holding register 
        for count in range(0, self.TWO_WINDING_DATA_END_HOLDING_REG +1):
            self.holding_registers_table.append(0)
        
        # print("Length of discrete input table :" + str(len(self.discrete_inputs_table)))

    def get_bus_name(self, bus_number):
        """
        get the bus name that is store in to bus number
        - bus_number
        - return (string) bus name
        - return False if there is no this bus_number
        """
        for count in range (0, self.QUANTITY_BUS):
            # calculate the address of bus number
            bus_number_address = self.BUS_START_INPUT_REG + count*11
            # found weather this bus number is existing 
            if(self.input_registers_table[bus_number_address] == bus_number):
                bus_name = ''
                # read bus_name from modbus table
                for count1 in range(1,self.BUS_NAME_MAX_LENGTH +1):
                    bus_name = bus_name + chr((self.input_registers_table[bus_number_address + count1]))
                return bus_name
        # this bus number is not existing
        return False

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
        this_bus_number_is_existed = False
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
        if (this_bus_number_is_existed == False):
            # calculate the address
            bus_number_address = self.BUS_START_INPUT_REG +  self.bus_object_number*self.BUS_FRAME_LENGTH
            # add bus number
            self.input_registers_table[bus_number_address] = bus_number
            self.holding_registers_table[bus_number_address] = bus_number
            # add bus_name
            for count2 in range(0,len(bus_name)):
                self.input_registers_table[bus_number_address + count2 + 1] = ord(bus_name[count2])
                self.holding_registers_table[bus_number_address + count2 + 1] = ord(bus_name[count2])

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
        this_bus_data_is_existed = False
        # find to check
        for count in range(0, self.bus_data_object_number):
            #  calculate the address of bus data
            bus_data_address = self.BUS_DATA_START_INPUT_REG + count*self.BUS_DATA_FRAME_LENGTH
            status_address = self.BUS_DATA_START_DISCRETE_INPUT = + count*self.BUS_DATA_FRAME_LENGTH
            # found if this bus data is existed
            if(self.input_registers_table[bus_data_address] == bus_number):
                
                self.input_registers_table[bus_data_address +1] = code
                # for udm
                udm_dict = self.float_to_int16_IEEE(udm)
                self.input_registers_table[bus_data_address +2] = udm_dict["First Byte"]
                self.input_registers_table[bus_data_address +3] = udm_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +2] = udm_dict["First Byte"]
                self.holding_registers_table[bus_data_address +3] = udm_dict["Second Byte"]
                #  for normal
                normal_dict = self.float_to_int16_IEEE(normal)
                self.input_registers_table[bus_data_address +4] = normal_dict["First Byte"]
                self.input_registers_table[bus_data_address +5] = normal_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +4] = normal_dict["First Byte"]
                self.holding_registers_table[bus_data_address +5] = normal_dict["Second Byte"]
                #  for normal_vmin
                normal_vmin_dict = self.float_to_int16_IEEE(normal_vmin)
                self.input_registers_table[bus_data_address +6] = normal_vmin_dict["First Byte"]
                self.input_registers_table[bus_data_address +7] = normal_vmin_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +6] = normal_vmin_dict["First Byte"]
                self.holding_registers_table[bus_data_address +7] = normal_vmin_dict["Second Byte"]
                # for normal_vmax 
                normal_vmax_dict = self.float_to_int16_IEEE(normal_vmax)
                self.input_registers_table[bus_data_address +8] = normal_vmax_dict["First Byte"]
                self.input_registers_table[bus_data_address +9] = normal_vmax_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +8] = normal_vmax_dict["First Byte"]
                self.holding_registers_table[bus_data_address +9] = normal_vmax_dict["Second Byte"]
                #  for emergency_vmax
                emergency_vmax_dict = self.float_to_int16_IEEE(emergency_vmax)
                self.input_registers_table[bus_data_address +10] = emergency_vmax_dict["First Byte"]
                self.input_registers_table[bus_data_address +11] = emergency_vmax_dict["Second Byte"]
                self.holding_registers_table[bus_data_address +10] = emergency_vmax_dict["First Byte"]
                self.holding_registers_table[bus_data_address +11] = emergency_vmax_dict["Second Byte"]
                # for status
                self.discrete_inputs_table[status_address] = status
                self.coils_table[status_address] = status

                return True
        

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


if __name__ == '__main__':
    modbus_table =Modbus_Table_Class()
    # modbus_table.set_bus(101,'123345')
    # modbus_table.set_bus(101,'123')
    # modbus_table.set_bus(102,'njna')

#     modbus_table.set_bus(103,'njna1asdasd')
#     modbus_table.set_bus(101,'123')
#     modbus_table.set_bus(102,'123asdaad')
    # print(modbus_table.get_bus_name(101))
    # print(modbus_table.get_bus_name(102))
#     # print(chr(98))