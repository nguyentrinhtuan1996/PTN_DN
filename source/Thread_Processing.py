#!/usr/bin/env python3
import os
from CSV_Engine import CSV_Engine_Class
from Modbus_Server import Modbus_Server_Class, modbus_table
import threading
from time import sleep
try:
    from datetime import datetime
except:
    os.system("pip install DateTimeRange")
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
        self.csv_out_engine = CSV_Engine_Class(self.out_csv_path)
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
            self.set_in_csv_to_modbus_table()
            # modbus_table.print_modbus_table()
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
        # for load data
        for vocabulary in self.csv_in_engine.data["Load Data"]:
            print(vocabulary)
            modbus_table.set_load_data(
                bus_number= float(vocabulary["Bus"]),
                P=          float(vocabulary["P"]),
                Q=          float(vocabulary["Q"]),
                ID=         float(vocabulary["ID"]),
            )
        # for load data
        for vocabulary in self.csv_in_engine.data["Generic"]:
            print(vocabulary)
            modbus_table.set_generic(
                field1= float(vocabulary["FIELD1"]),
                field2= float(vocabulary["FIELD2"]),
                field3= float(vocabulary["FIELD3"]),
                field4= float(vocabulary["FIELD4"]),
                field5= float(vocabulary["FIELD5"]),
                field6= float(vocabulary["FIELD6"]),
                field7= float(vocabulary["FIELD7"]),
                field8= float(vocabulary["FIELD8"]),
                field9= float(vocabulary["FIELD9"]),
                field10= float(vocabulary["FIELD10"]),
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
        # for load data
        for vocabulary in self.csv_in_engine.data["Load Data"]:
            print(vocabulary)
            modbus_table.change_load_data(
                bus_number= float(vocabulary["Bus"]),
                P=          float(vocabulary["P"]),
                Q=          float(vocabulary["Q"]),
                ID=         float(vocabulary["ID"]),
            )
        # for load data
        for vocabulary in self.csv_in_engine.data["Generic"]:
            print(vocabulary)
            modbus_table.change_generic(
                field1= float(vocabulary["FIELD1"]),
                field2= float(vocabulary["FIELD2"]),
                field3= float(vocabulary["FIELD3"]),
                field4= float(vocabulary["FIELD4"]),
                field5= float(vocabulary["FIELD5"]),
                field6= float(vocabulary["FIELD6"]),
                field7= float(vocabulary["FIELD7"]),
                field8= float(vocabulary["FIELD8"]),
                field9= float(vocabulary["FIELD9"]),
                field10= float(vocabulary["FIELD10"]),
            )

    def set_out_csv_from_modbus_table(self):
        # print(self.csv_out_engine.data)
        # bus_name
        for obj_count in range(0, len(self.csv_out_engine.data["Bus"])):
            # print(self.csv_out_engine.data["Bus"][obj_count])
            # calculate the bus number address
            bus_number_address = modbus_table.BUS_START_HOLDING_REG + obj_count*modbus_table.BUS_FRAME_LENGTH
            bus_number = modbus_table.holding_registers_table[bus_number_address]
            bus_name = modbus_table.get_bus_name(bus_number)
            self.csv_out_engine.data["Bus"][obj_count]["Bus Name"] = bus_name
            # vocabulary["Bus Name"] = bus_name
            # print(bus_name)

    
        for obj_count in range(0, len(self.csv_out_engine.data["Bus Data"])):
            # print("vo "+str(vocabulary))
            # calculate the bus number address
            bus_number_address = modbus_table.BUS_DATA_START_HOLDING_REG + obj_count*modbus_table.BUS_DATA_FRAME_LENGTH
            # read bus number
            bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[bus_number_address +1],
                modbus_table.holding_registers_table[bus_number_address ]
            )
            bus_data_dict = modbus_table.get_bus_data(bus_number)
            # write to out_csv.data
            if(bus_data_dict != False):
                self.csv_out_engine.data["Bus Data"][obj_count]["Bus_Number"] =            str(bus_data_dict["Bus_Number"])
                self.csv_out_engine.data["Bus Data"][obj_count]["Code"] =                  str(bus_data_dict["Code"])
                self.csv_out_engine.data["Bus Data"][obj_count]["Udm(pu)"] =               str(bus_data_dict["Udm"])
                self.csv_out_engine.data["Bus Data"][obj_count]["Normal_Vmax(pu)"] =       str(bus_data_dict["Normal_Vmax"])
                self.csv_out_engine.data["Bus Data"][obj_count]["Normal_Vmin(pu)"] =       str(bus_data_dict["Normal_Vmin"])
                self.csv_out_engine.data["Bus Data"][obj_count]["Emergency_Vmax(pu)"] =    str(bus_data_dict["Emergency_Vmax"])
                self.csv_out_engine.data["Bus Data"][obj_count]["Emergency_Vmin(pu)"] =    str(bus_data_dict["Emergency_Vmin"])
                self.csv_out_engine.data["Bus Data"][obj_count]["Status"] =                str(bus_data_dict["Status"])
            else:
                print(bus_number, " : this bus number has be changed")

        # gen_data
        for obj_count in range(0, len(self.csv_out_engine.data["Gen Data"])):
            # print("vo " +str(vocabulary))
            # calculate the bus number address
            bus_number_address = modbus_table.GEN_DATA_START_HOLDING_REG + obj_count*modbus_table.GEN_DATA_FRAME_LENGTH
            # read bus number
            bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[bus_number_address +1],
                modbus_table.holding_registers_table[bus_number_address ]
            )
            gen_data_dict = modbus_table.get_gen_data(bus_number)
            # write to out_csv.data
            # print("mod "+str(gen_data_dict))
            if(gen_data_dict != False):
                self.csv_out_engine.data["Gen Data"][obj_count]["Bus_Number"] =  str(gen_data_dict["Bus_Number"])
                self.csv_out_engine.data["Gen Data"][obj_count]["Unit"] =        str(gen_data_dict["Unit"])
                self.csv_out_engine.data["Gen Data"][obj_count]["Pgen"] =        str(gen_data_dict["Pgen"])
                self.csv_out_engine.data["Gen Data"][obj_count]["Qgen"] =        str(gen_data_dict["Qgen"])
                self.csv_out_engine.data["Gen Data"][obj_count]["Status"] =      str(gen_data_dict["Status"])

        # line data
        for obj_count in range(0, len(self.csv_out_engine.data["Line Data"])):
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
            
            if(line_data_dict !=False):
                self.csv_out_engine.data["Line Data"][obj_count]["From_Bus_Number"] = str(line_data_dict["From_Bus_Number"])
                self.csv_out_engine.data["Line Data"][obj_count]["To_Bus_Number"]   = str(line_data_dict["To_Bus_Number"])
                self.csv_out_engine.data["Line Data"][obj_count]["ID"]              = str(line_data_dict["ID"])  
                self.csv_out_engine.data["Line Data"][obj_count]["Imax"]            = str(line_data_dict["Imax"])
                self.csv_out_engine.data["Line Data"][obj_count]["R(pu)"]           = str(line_data_dict["Rpu"])
                self.csv_out_engine.data["Line Data"][obj_count]["X(pu)"]           = str(line_data_dict["Xpu"])
                self.csv_out_engine.data["Line Data"][obj_count]["G(pu)"]           = str(line_data_dict["Gpu"])
                self.csv_out_engine.data["Line Data"][obj_count]["B(pu)"]           = str(line_data_dict["Bpu"])
                self.csv_out_engine.data["Line Data"][obj_count]["Status"]          = str(line_data_dict["Status"])
        
        #  shunt data 
        for obj_count in range(0, len(self.csv_out_engine.data["Shunt Data"])):
            # print("vo " +str(vocabulary))
            # calculate the bus number address
            bus_number_address = modbus_table.SHUNT_DATA_START_HOLDING_REG + obj_count*modbus_table.SHUNT_DATA_FRAME_LENGTH
            bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[bus_number_address +1],
                modbus_table.holding_registers_table[bus_number_address]
            )
            shunt_data_dict = modbus_table.get_shunt_data(bus_number)
            # print("mod " +str(shunt_data_dict))
            if(shunt_data_dict != False):
                #  write to out csv data
                self.csv_out_engine.data["Shunt Data"][obj_count]["Bus_Number"]    = str(shunt_data_dict["Bus_Number"])
                self.csv_out_engine.data["Shunt Data"][obj_count]["G_Shunt(pu)"]   = str(shunt_data_dict["G_Shunt"])
                self.csv_out_engine.data["Shunt Data"][obj_count]["B_Shunt(pu)"]   = str(shunt_data_dict["B_Shunt"])
                self.csv_out_engine.data["Shunt Data"][obj_count]["Status"]        = str(shunt_data_dict["Status"])

        # 2 winding transformer data
        for obj_count in range(0, len(self.csv_out_engine.data["2Winding transformer Data"])):
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
            # print("mod " +str(two_winding_data_dict))
            if(two_winding_data_dict != False):
                # write data to out csv data
                self.csv_out_engine.data["2Winding transformer Data"][obj_count]["From_Bus_Number"]   = str(two_winding_data_dict["From_Bus_Number"])
                self.csv_out_engine.data["2Winding transformer Data"][obj_count]["To_Bus_Number"]     = str(two_winding_data_dict["To_Bus_Number"])
                self.csv_out_engine.data["2Winding transformer Data"][obj_count]["R(pu)"]             = str(two_winding_data_dict["Rpu"])
                self.csv_out_engine.data["2Winding transformer Data"][obj_count]["X(pu)"]             = str(two_winding_data_dict["Xpu"])
                self.csv_out_engine.data["2Winding transformer Data"][obj_count]["Winding_MVA_Base"]  = str(two_winding_data_dict["Winding_MVA_Base"])
                self.csv_out_engine.data["2Winding transformer Data"][obj_count]["Status"]            = str(two_winding_data_dict["Status"])

        # print("csv out engine data: ->")
        # print(self.csv_out_engine.data)
        # print("<-")

        # for load data
        for obj_count in range(0, len(self.csv_out_engine.data["Load Data"])):
            bus_number_address = modbus_table.LOAD_DATA_START_HOLDING_REG + obj_count*modbus_table.LOAD_DATA_FRAME_LENGTH
            bus_number = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[bus_number_address +1],
                modbus_table.holding_registers_table[bus_number_address ]
            )
            load_data_dict = modbus_table.get_load_data(bus_number)
            if (load_data_dict != False):
                self.csv_out_engine.data["Load Data"][obj_count]["Bus"] = str(load_data_dict["Bus"])
                self.csv_out_engine.data["Load Data"][obj_count]["P"] = str(load_data_dict["P"])
                self.csv_out_engine.data["Load Data"][obj_count]["Q"] = str(load_data_dict["Q"])
                self.csv_out_engine.data["Load Data"][obj_count]["ID"] = str(load_data_dict["ID"])
                # print(self.csv_out_engine.data["Load Data"][obj_count])

        # for generic
        for obj_count in range(0, len(self.csv_out_engine.data["Generic"])):
            field1_address = modbus_table.GENERIC_START_HOLDING_REG + obj_count*modbus_table.GENERIC_FRAME_LENGTH
            field1 = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[field1_address +1],
                modbus_table.holding_registers_table[field1_address ]
            )
            field2 = modbus_table.convert_to_real(
                modbus_table.holding_registers_table[field1_address +3],
                modbus_table.holding_registers_table[field1_address +2]
            )

            generic_dict = modbus_table.get_generic(field1,field2)
            if (generic_dict != False):
                self.csv_out_engine.data["Generic"][obj_count]["FIELD1"] = str(generic_dict["Field1"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD2"] = str(generic_dict["Field2"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD3"] = str(generic_dict["Field3"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD4"] = str(generic_dict["Field4"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD5"] = str(generic_dict["Field5"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD6"] = str(generic_dict["Field6"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD7"] = str(generic_dict["Field7"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD8"] = str(generic_dict["Field8"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD9"] = str(generic_dict["Field9"])
                self.csv_out_engine.data["Generic"][obj_count]["FIELD10"] = str(generic_dict["Field10"])
                print(self.csv_out_engine.data["Generic"][obj_count])
        
if __name__ == '__main__':
    main_threads = Thread_Processing_Class()