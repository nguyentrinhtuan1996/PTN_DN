#!/usr/bin/env python3
from CSV_Engine import CSV_Engine_Class
from Modbus_Server import Modbus_Server_Class, modbus_table
import threading
from time import sleep
from datetime import datetime
import json

# Opening JSON file
f = open('config.json')
# returns JSON object as 
# a dictionary
configurations = json.load(f)
# Closing file
f.close()

class Thread_Processing_Class():
    def __init__(self, in_csv_path = configurations["in_csv_path"],out_csv_path= configurations["out_csv_path"]) -> None:
        # save paths to work
        self.in_csv_path = in_csv_path
        self.out_csv_path = out_csv_path
        # CSV engine
        self.csv_in_engine = CSV_Engine_Class(self.in_csv_path)
        self.csv_out_engine = CSV_Engine_Class(self.in_csv_path)
        # import data from input csv
        self.csv_in_engine.import_csv()
        # self.csv_out_engine.import_csv()
        self.csv_out_engine.data = self.csv_in_engine.data

        # modbus server
        self.modbus_server = Modbus_Server_Class()

        # create threads
        self.thread_read_input_csv = threading.Thread(
            target=self.thread_loop_read_csv
        )
        self.thread_write_output_csv = threading.Thread(
            target=self.thread_loop_write_csv
        )
        # start threads
        self.modbus_server.start()
        self.thread_read_input_csv.start()
        self.thread_write_output_csv.start()
    
    def thread_loop_read_csv(self):
        self.csv_in_engine.import_csv()
        self.set_in_csv_to_modbus_table()
        while True:
            print(datetime.now())
            print(" Read input csv")
            self.csv_in_engine.import_csv()
            self.update_in_csv_to_modbus_table()
            sleep(configurations["delay_time_to_read_csv"])

    def thread_loop_write_csv(self):
        while True:
            sleep(configurations["delay_time_to_write_csv"])
            print(datetime.now())
            print(" write output vsc")
            self.set_out_csv_from_modbus_table()
            self.csv_out_engine.export_csv(self.out_csv_path)

    def set_in_csv_to_modbus_table(self):
        # bus name
        for vocabulary in self.csv_in_engine.data["Bus"]:
            # print(vocabulary)
            modbus_table.set_bus(
                bus_number= int(vocabulary["Bus Number"]),
                bus_name=   str(vocabulary["Bus Name"])
            )
        # bus data
        for vocabulary in self.csv_in_engine.data["Bus Data"]:
            # print(vocabulary)
            modbus_table.set_bus_data(
                bus_number=     float(vocabulary["Bus_Number"]),
                code=           float(vocabulary["Code"]),
                udm=            float(vocabulary["Udm(pu)"]),
                normal_vmax=    float(vocabulary["Normal_Vmax(pu)"]),
                normal_vmin=    float(vocabulary["Normal_Vmin(pu)"]),
                emergency_vmax= float(vocabulary["Emergency_Vmax(pu)"]),
                emergency_vmin= float(vocabulary["Emergency_Vmin(pu)"]),
                status=         float(vocabulary["Status"])
            )
        #  Gen Data
        for vocabulary in self.csv_in_engine.data["Gen Data"]:
            # print(vocabulary)
            modbus_table.set_gen_data(
                bus_number=     float(vocabulary["Bus_Number"]),
                unit=           float(vocabulary["Unit"]),
                pgen=           float(vocabulary["Pgen"]),
                qgen=           float(vocabulary["Qgen"]),
                status=         float(vocabulary["Status"])
            )
        # Line Data
        for vocabulary in self.csv_in_engine.data["Line Data"]:
            # print(vocabulary)
            modbus_table.set_line_data(
                from_bus_number=    float(vocabulary["From_Bus_Number"]),
                to_bus_number=      float(vocabulary["To_Bus_Number"]),
                ID=                 float(vocabulary["ID"]),
                Imax=               float(vocabulary["Imax"]),
                Rpu=                float(vocabulary["R(pu)"]),
                Xpu=                float(vocabulary["X(pu)"]),
                Gpu=                float(vocabulary["G(pu)"]),
                Bpu=                float(vocabulary["B(pu)"]),
                status=             float(vocabulary["Status"])
            )
        # Shunt data
        for vocabulary in self.csv_in_engine.data["Shunt Data"]:
            # print(vocabulary)
            modbus_table.set_shunt_data(
                bus_number= float(vocabulary["Bus_Number"]),
                g_shunt=    float(vocabulary["G_Shunt(pu)"]),
                b_shunt=    float(vocabulary["B_Shunt(pu)"]),
                status=     float(vocabulary["Status"])
            )
        # 2Winding transformer Data
        for vocabulary in self.csv_in_engine.data["2Winding transformer Data"]:
            # print(vocabulary)
            modbus_table.set_two_winding_data(
                from_bus_number=    float(vocabulary["From_Bus_Number"]),
                to_bus_number=      float(vocabulary["To_Bus_Number"]), 
                Rpu=                float(vocabulary["R(pu)"]),
                Xpu=                float(vocabulary["X(pu)"]),
                winding_MVA_base=   float(vocabulary["Winding_MVA_Base"]),
                status=             float(vocabulary["Status"])
            )
 
    def update_in_csv_to_modbus_table(self):
        # bus name
        for vocabulary in self.csv_in_engine.data["Bus"]:
            # print(vocabulary)
            modbus_table.change_bus(
                bus_number= int(vocabulary["Bus Number"]),
                bus_name=   str(vocabulary["Bus Name"])
            )
        # bus data
        for vocabulary in self.csv_in_engine.data["Bus Data"]:
            # print(vocabulary)
            modbus_table.change_bus_data(
                bus_number=     float(vocabulary["Bus_Number"]),
                code=           float(vocabulary["Code"]),
                udm=            float(vocabulary["Udm(pu)"]),
                normal_vmax=    float(vocabulary["Normal_Vmax(pu)"]),
                normal_vmin=    float(vocabulary["Normal_Vmin(pu)"]),
                emergency_vmax= float(vocabulary["Emergency_Vmax(pu)"]),
                emergency_vmin= float(vocabulary["Emergency_Vmin(pu)"]),
                status=         float(vocabulary["Status"])
            )
        #  Gen Data
        for vocabulary in self.csv_in_engine.data["Gen Data"]:
            # print(vocabulary)
            modbus_table.change_gen_data(
                bus_number=     float(vocabulary["Bus_Number"]),
                unit=           float(vocabulary["Unit"]),
                pgen=           float(vocabulary["Pgen"]),
                qgen=           float(vocabulary["Qgen"]),
                status=         float(vocabulary["Status"])
            )
        # Line Data
        for vocabulary in self.csv_in_engine.data["Line Data"]:
            # print(vocabulary)
            modbus_table.change_line_data(
                from_bus_number=    float(vocabulary["From_Bus_Number"]),
                to_bus_number=      float(vocabulary["To_Bus_Number"]),
                ID=                 float(vocabulary["ID"]),
                Imax=               float(vocabulary["Imax"]),
                Rpu=                float(vocabulary["R(pu)"]),
                Xpu=                float(vocabulary["X(pu)"]),
                Gpu=                float(vocabulary["G(pu)"]),
                Bpu=                float(vocabulary["B(pu)"]),
                status=             float(vocabulary["Status"])
            )
        # Shunt data
        for vocabulary in self.csv_in_engine.data["Shunt Data"]:
            # print(vocabulary)
            modbus_table.change_shunt_data(
                bus_number= float(vocabulary["Bus_Number"]),
                g_shunt=    float(vocabulary["G_Shunt(pu)"]),
                b_shunt=    float(vocabulary["B_Shunt(pu)"]),
                status=     float(vocabulary["Status"])
            )
        # 2Winding transformer Data
        for vocabulary in self.csv_in_engine.data["2Winding transformer Data"]:
            # print(vocabulary)
            modbus_table.change_two_winding_data(
                from_bus_number=    float(vocabulary["From_Bus_Number"]),
                to_bus_number=      float(vocabulary["To_Bus_Number"]), 
                Rpu=                float(vocabulary["R(pu)"]),
                Xpu=                float(vocabulary["X(pu)"]),
                winding_MVA_base=   float(vocabulary["Winding_MVA_Base"]),
                status=             float(vocabulary["Status"])
            )

    def set_out_csv_from_modbus_table(self):

        # bus_name
        obj_count = 0 
        for vocabulary in self.csv_out_engine.data["Bus"]:
            # print(vocabulary)
            # calculate the bus number address
            bus_number_address = modbus_table.BUS_START_HOLDING_REG + obj_count*modbus_table.BUS_FRAME_LENGTH
            bus_number = modbus_table.holding_registers_table[bus_number_address]
            bus_name = modbus_table.get_bus_name(bus_number)
            vocabulary["Bus Name"] = bus_name
            obj_count +=1
            # print(bus_name)

        # bus_data
        obj_count = 0
        for vocabulary in self.csv_out_engine.data["Bus Data"]:
            # print("vo "+str(vocabulary))
            # calculate the bus number address
            bus_number_address = modbus_table.BUS_DATA_START_HOLDING_REG + obj_count*modbus_table.BUS_DATA_FRAME_LENGTH
            # read bus number
            bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[bus_number_address +1],
                modbus_table.holding_registers_table[bus_number_address ]
            )
            bus_data_dict = modbus_table.get_bus_data(bus_number)
            obj_count +=1
            # write to out_csv.data
            # print("mod "+str(bus_data_dict))
            if(bus_data_dict != False):
                vocabulary["Bus_Number"] =            str(bus_data_dict["Bus_Number"])
                vocabulary["Code"] =                  str(bus_data_dict["Code"])
                vocabulary["Udm(pu)"] =               str(bus_data_dict["Udm"])
                vocabulary["Normal_Vmax(pu)"] =       str(bus_data_dict["Normal_Vmax"])
                vocabulary["Normal_Vmin(pu)"] =       str(bus_data_dict["Normal_Vmin"])
                vocabulary["Emergency_Vmax(pu)"] =    str(bus_data_dict["Emergency_Vmax"])
                vocabulary["Emergency_Vmin(pu)"] =    str(bus_data_dict["Emergency_Vmin"])
                vocabulary["Status"] =                str(bus_data_dict["Status"])

        # gen_data
        obj_count = 0
        for vocabulary in self.csv_out_engine.data["Gen Data"]:
            # print("vo " +str(vocabulary))
            # calculate the bus number address
            bus_number_address = modbus_table.GEN_DATA_START_HOLDING_REG + obj_count*modbus_table.GEN_DATA_FRAME_LENGTH
            # read bus number
            bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[bus_number_address +1],
                modbus_table.holding_registers_table[bus_number_address ]
            )
            gen_data_dict = modbus_table.get_gen_data(bus_number)
            obj_count +=1
            # write to out_csv.data
            # print("mod "+str(gen_data_dict))
            if(gen_data_dict != False):
                vocabulary["Bus_Number"] =  str(gen_data_dict["Bus_Number"])
                vocabulary["Unit"] =        str(gen_data_dict["Unit"])
                vocabulary["Pgen"] =        str(gen_data_dict["Pgen"])
                vocabulary["Qgen"] =        str(gen_data_dict["Qgen"])
                vocabulary["Status"] =      str(gen_data_dict["Status"])

        # line data
        obj_count = 0
        for vocabulary in self.csv_out_engine.data["Line Data"]:
            # print("vo " +str(vocabulary))
            # calculate the bus number address
            from_bus_number_address = modbus_table.LINE_DATA_START_HOLDING_REG + obj_count*modbus_table.LINE_DATA_FRAME_LENGTH
            # read bus number
            from_bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[from_bus_number_address +1],
                modbus_table.holding_registers_table[from_bus_number_address ]
            )
            to_bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[from_bus_number_address +3],
                modbus_table.holding_registers_table[from_bus_number_address +2]
            )
            ID = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[from_bus_number_address +5],
                modbus_table.holding_registers_table[from_bus_number_address +4]

            )
            line_data_dict = modbus_table.get_line_data(from_bus_number,to_bus_number,ID)
            obj_count +=1
            
            # print("mod " +str(line_data_dict))
            # print("")

            if(line_data_dict !=False):
                vocabulary["From_Bus_Number"] = str(line_data_dict["From_Bus_Number"])
                vocabulary["To_Bus_Number"]   = str(line_data_dict["To_Bus_Number"])
                vocabulary["ID"]              = str(line_data_dict["ID"])  
                vocabulary["Imax"]            = str(line_data_dict["Imax"])
                vocabulary["R(pu)"]           = str(line_data_dict["Rpu"])
                vocabulary["X(pu)"]           = str(line_data_dict["Xpu"])
                vocabulary["G(pu)"]           = str(line_data_dict["Gpu"])
                vocabulary["B(pu)"]           = str(line_data_dict["Bpu"])
                vocabulary["Status"]           = str(line_data_dict["Status"])
        
        #  shunt data 
        obj_count = 0
        for vocabulary in self.csv_out_engine.data["Shunt Data"]:
            # print("vo " +str(vocabulary))
            # calculate the bus number address
            bus_number_address = modbus_table.SHUNT_DATA_START_HOLDING_REG + obj_count*modbus_table.SHUNT_DATA_FRAME_LENGTH
            bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[bus_number_address +1],
                modbus_table.holding_registers_table[bus_number_address]
            )
            shunt_data_dict = modbus_table.get_shunt_data(bus_number)
            # print("mod " +str(shunt_data_dict))
            obj_count +=1
            if(shunt_data_dict != False):
                #  write to out csv data
                vocabulary["Bus_Number"]    = str(shunt_data_dict["Bus_Number"])
                vocabulary["G_Shunt(pu)"]   = str(shunt_data_dict["G_Shunt"])
                vocabulary["B_Shunt(pu)"]   = str(shunt_data_dict["B_Shunt"])
                vocabulary["Status"]        = str(shunt_data_dict["Status"])

        # 2 winding transformer data
        obj_count = 0
        for vocabulary in self.csv_out_engine.data["2Winding transformer Data"]:
            # print("vo " +str(vocabulary))
            # calculate the addresses
            from_bus_number_address = modbus_table.TWO_WINDING_DATA_START_HOLDING_REG + obj_count*modbus_table.TWO_WINDING_DATA_FRAME_LENGTH
            from_bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[from_bus_number_address +1],
                modbus_table.holding_registers_table[from_bus_number_address ]
            )
            to_bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[from_bus_number_address +3],
                modbus_table.holding_registers_table[from_bus_number_address +2]
            )
            two_winding_data_dict = modbus_table.get_two_winding_data(
                from_bus_number,
                to_bus_number
            )
            obj_count +=1
            # print("mod " +str(two_winding_data_dict))
            if(two_winding_data_dict != False):
                # write data to out csv data
                vocabulary["From_Bus_Number"]   = str(two_winding_data_dict["From_Bus_Number"])
                vocabulary["To_Bus_Number"]     = str(two_winding_data_dict["To_Bus_Number"])
                vocabulary["R(pu)"]             = str(two_winding_data_dict["Rpu"])
                vocabulary["X(pu)"]             = str(two_winding_data_dict["Xpu"])
                vocabulary["Winding_MVA_Base"]  = str(two_winding_data_dict["Winding_MVA_Base"])
                vocabulary["Status"]            = str(two_winding_data_dict["Status"])

if __name__ == '__main__':
    main_threads = Thread_Processing_Class()