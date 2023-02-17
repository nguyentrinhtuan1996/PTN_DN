# Modbus TCP - IEC 60870-5-104
this code will read the csv,  convert it to context of modbus server and vice versa.
there are 20 object for each bus, bus data, gen data, line data, shunt data, 2 winding data
Each object will be create in input register for input csv and holding register for output
csv when starting program. Time to reload and re_write input csv and output csv is 10 
second and 5 second. These parameters are put in to file config.json.
the modbus table is list blow:

<!-- For 20 object for each object type
                |   Input register      |   Holding register    | type          | Modbus TCP Server     | IEC 60870-5-104 type
------------------------------------------------------------------------------------------------------------------------------------
                |   start   -   end     |   from    -   to      | bit string    |
bus             |   0       -   239     |   0       -   239     | float         |12 x  Ir,HR            |   6 x bit sting 32 bit

bus_data        |   240     -   559     |   240     -   559     | float         |16 x  Ir,HR            |   8 x measurement float
gen_data        |   560     -   759     |   560     -   759     | float         |10 x  Ir,HR            |   5 x measurement float
line_data       |   760     -   1119    |   760     -   1119    | float         |18 x  Ir,HR            |   9 x measurement float
shunt_data      |   1120    -   1279    |   1120    -   1279    | float         |8  x  Ir,HR            |   4 x measurement float
2_winding_data  |   1280    -   1519    |   1280    -   1519    | float         |12 x  Ir,HR            |   6 x measurement float -->

## 1) Install lib
    pip install pyModbusTCP
## 2) run the main.
    python3 main.py
## 3) log in moxa and config (ConfigMoxa.docx).
    Modbus TCP client will read input register from 0 to last address with 
        last_address =    BUS_NAME_MAX_LENGTH           * max_quantity_bus
                        + BUS_DATA_FRAME_LENGTH         * max_quantity_bus_data
                        + GEN_DATA_FRAME_LENGTH         * max_quantity_gen_data
                        + LINE_DATA_FRAME_LENGTH        * max_quantity_line_data
                        + SHUNT_DATA_FRAME_LENGTH       * max_quantity_shunt_data
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
## 4) read and write.
    Log in mGate5114 and config the modbus client to read at IP, where user run this program
    Or check by qModbusMaster in tutorial
### 4.1) IOA of objects
    1st Bus : Bitstring of 32bits at 0
    1st Bus Data: Measurement value(float) at 0
    1st Gen Data: Measurement value(float) at 160
    1st Line Data: Measurement value(float) at 260
    1st Shunt Data: Measurement value(float) at 440
    1st 2 Winding Data: Measurement value(float) at 520
