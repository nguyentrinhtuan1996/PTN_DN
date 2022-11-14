from CSV_Engine import CSV_Engine_Class
from Modbus_Server import Modbus_Server_Class, modbus_table


class Thread_Processing_Class():

    def __init__(self, in_csv_path, out_csv_path) -> None:
        # save paths to work
        self.in_csv_path = in_csv_path
        self.out_csv_path = out_csv_path
        # CSV engine
        self.csv_in_engine = CSV_Engine_Class(self.in_csv_path)
        self.csv_out_engine = CSV_Engine_Class(self.in_csv_path)
        self.csv_in_engine.import_csv()
        self.csv_out_engine.import_csv()
        # modbus server
        self.modbus_server = Modbus_Server_Class()

        # create threads
        # start modbus server
        self.modbus_server.start()
        # return True
    
    def read_in_csv_to_modbus_table(self):
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
            print(vocabulary)
            modbus_table.set_shunt_data(
                bus_number= float(vocabulary["Bus_Number"]),
                g_shunt=    float(vocabulary["G_Shunt(pu)"]),
                b_shunt=    float(vocabulary["B_Shunt(pu)"]),
                status=     float(vocabulary["Status"])
            )
        # 2Winding transformer Data
        for vocabulary in self.csv_in_engine.data["2Winding transformer Data"]:
            print(vocabulary)
            modbus_table.set_two_winding_data(
                from_bus_number=    float(vocabulary["From_Bus_Number"]),
                to_bus_number=      float(vocabulary["To_Bus_Number"]), 
                Rpu=                float(vocabulary["R(pu)"]),
                Xpu=                float(vocabulary["X(pu)"]),
                winding_MVA_base=   float(vocabulary["Winding_MVA_Base"]),
                status=             float(vocabulary["Status"])
            )

    
if __name__ == '__main__':
    main_thread = Thread_Processing_Class(
        in_csv_path="a\savnw.csv",
        out_csv_path= "savnw_out.csv"
    )
    main_thread.csv_out_engine.data = main_thread.csv_in_engine.data
    main_thread.csv_out_engine.export_csv("export_data.csv")
    main_thread.read_in_csv_to_modbus_table()