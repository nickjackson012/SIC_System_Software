from SIC_Simulator.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY
from SIC_Simulator.sic_memory_model import initialize_memory
from SIC_Simulator.sic_object_code_parser import sic_object_code_parser
from SIC_Utilities.sic_constants import SIC_OBJECT_CODE_FILE_EXTENSION
from SIC_Utilities.sic_converter import hex_string_to_dec


# This function will intialize the memory model and
# then load program object code into the memory model
def load_program_object_code(parsed_object_code_dict_list):
    memory_model_dict = initialize_memory()
    for parsed_object_code_dict in parsed_object_code_dict_list:
        if parsed_object_code_dict["record_type"] == "text":
            address_hex_string = parsed_object_code_dict["start_address"]
            address_dec = hex_string_to_dec(address_hex_string)
            byte_list = parsed_object_code_dict["byte_list"]

            for byte in byte_list:
                memory_model_dict[address_dec] = byte
                address_dec += 1

    return memory_model_dict


# TEST BED
#
# object_code_file_name = "ReadWrite"
#
# object_code_file_path = (SIC_DEFAULT_WORKING_DIRECTORY +
#                          object_code_file_name + "." +
#                          SIC_OBJECT_CODE_FILE_EXTENSION)
#
# object_code_file = open(object_code_file_path, "rt")
#
# parsed_object_code_dict_list = sic_object_code_parser(object_code_file)
#
# print(load_program(parsed_object_code_dict_list))
