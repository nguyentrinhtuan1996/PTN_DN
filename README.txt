this code will read the csv in convert it to context of modbus server and vice versa.
there are 100 for each bus, bus data, gen data, line data, shunt data, 2 winding data
Each object will be create in input register for input csv and holding register for output
csv when starting program. Time to reload and re_write input csv and output csv is 10 
second and 5 second. These parameters are put in to file config.json.
the modbus table is list blow:

                |   Input register      |   Holding register    | type          | Modbus TCP Server     | IEC 60870-5-104
------------------------------------------------------------------------------------------------------------------------------------
                |   from    -   to      |   from    -   to      | bit string    |
bus             |   0       -   239    |   0       -   1099    | float         |12   Ir,HR             |   6 x bit sting 32 bit
bus_data        |   240    -   2699    |   1100    -   2699    | float         |16   Ir,HR             |   8 x measurement float
gen_data        |   2700    -   3699    |   2700    -   3699    | float         |10   Ir,HR             |   5 x measurement float
line_data       |   3700    -   5499    |   3700    -   5499    | float         |18   Ir,HR             |   9 x measurement float
shunt_data      |   5500    -   6299    |   5500    -   6299    | float         |8    Ir,HR             |   4 x measurement float
2_winding_data  |   6300    -   7499    |   6300    -   7499    | float         |12   Ir,HR             |   6 x measurement float

With this user can config modbus table with IEC 104 server

1) run the main.
2) log in moxa and config (ConfigMoxa.docx).
    Modbus TCP client will read input register from 0 to last address with 
        last_address =    BUS_NAME_MAX_LENGTH       * max_quantity_bus
                        + BUS_DATA_FRAME_LENGTH     * max_quantity_bus_data
                        + GEN_DATA_FRAME_LENGTH     * max_quantity_gen_data
                        + LINE_DATA_FRAME_LENGTH    * max_quantity_line_data
                        + SHUNT_DATA_FRAME_LENGTH   * max_quantity_shunt_data
                        + TWO_WINDING_DATA_FRAME_LENGTH * max_quantity_2_winding_data
        with 
            BUS_FRAME_LENGTH = 12
            BUS_DATA_FRAME_LENGTH = 16
            GEN_DATA_FRAME_LENGTH = 10
            LINE_DATA_FRAME_LENGTH = 18
            SHUNT_DATA_FRAME_LENGTH = 8
            TWO_WINDING_DATA_FRAME_LENGTH = 12
            and {
                "max_quantity_bus"          :20,
                "max_quantity_bus_data"     :20,
                "max_quantity_gen_data"     :20,
                "max_quantity_line_data"    :20,
                "max_quantity_shunt_data"   :20,
                "max_quantity_2_winding_data":20
            } from config.json
    Modbus TCP client will write holding register from 0 to last_address as above

    IEC60870-5-104 server will has
    
        Bit string of 32bit has IOA from 0 to LIOABS within:
            LIOABS = BUS_NAME_MAX_LENGTH * max_quantity_bus /2

        Measurement value float has IOA from 0 to LIOAMVF within:
            LIOAMVF =   ( BUS_DATA_FRAME_LENGTH     * max_quantity_bus_data
                        + GEN_DATA_FRAME_LENGTH     * max_quantity_gen_data
                        + LINE_DATA_FRAME_LENGTH    * max_quantity_line_data
                        + SHUNT_DATA_FRAME_LENGTH   * max_quantity_shunt_data
                        + TWO_WINDING_DATA_FRAME_LENGTH * max_quantity_2_winding_data)
                        /2
3) read and write.
