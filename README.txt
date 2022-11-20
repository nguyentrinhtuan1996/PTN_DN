this code will read the csv in convert it to context of modbus server and vice versa.
there are 100 for each bus, bus data, gen data, line data, shunt data, 2 winding data
Each object will be create in input register for input csv and holding register for output
csv when starting program. Time to reload and re_write input csv and output csv is 10 
second and 5 second. These parameters are put in to file config.json.
the modbus table is list blow:

                |   Input register      |   Holding register
                |   from    -   to      |   from    -   to
bus             |   0       -   1099    |   0       -   1099
bus_data        |   1100    -   2699    |   1100    -   2699    
gen_data        |   2700    -   3699    |   2700    -   3699
line_data       |   3700    -   5499    |   3700    -   5499
shunt_data      |   5500    -   6299    |   5500    -   6299
2_winding_data  |   6300    -   7499    |   6300    -   7499

With this user can config modbus table with IEC 104 server