import json
  
# Opening JSON file
f = open('config.json')
  
# returns JSON object as 
# a dictionary
configurations = json.load(f)
  
# Iterating through the json
# list
print(configurations["in_csv_path"])
print(configurations["out_csv_path"])
print(configurations["delay_time_to_read_csv"])
print(configurations["delay_time_to_write_csv"])

print(configurations["max_quantity_bus"])
print(configurations["max_quantity_bus_data"])
print(configurations["max_quantity_gen_data"])
print(configurations["max_quantity_line_data"])
print(configurations["max_quantity_shunt_data"])
print(configurations["max_quantity_2_winding_data"])
  
# Closing file
f.close()