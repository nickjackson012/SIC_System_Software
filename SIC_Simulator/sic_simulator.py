import os
import sys

from SIC_Simulator.sic_assembly_listing_parser import sic_assembly_listing_parser
from SIC_Simulator.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY
from SIC_Simulator.sic_memory_model import dump_memory, initialize_memory
from SIC_Simulator.sic_object_code_parser import sic_object_code_parser
from SIC_Utilities.sic_constants import SIC_OBJECT_CODE_FILE_EXTENSION, SIC_ASSEMBLY_LISTING_FILE_EXTENSION
from SIC_Utilities.sic_messaging import print_status, print_error

LOAD_MENU = "(l)oad, (q)uit"
RUN_MENU = "(s)tep, (d)ump, (r)un, (q)uit"
QUIT_CONFIRM = "Are you sure you want to quit? (y)es, (n)o"
SIC_PROMPT = "SIC> "
UNRECOGNIZED_COMMAND = "Unrecognized command"


class SICSimulatorError(Exception):
    pass


# This function is used to verify the existence of a program object code file(*.obj)
# and its corresponding assembly listing file
# If they exist, they are opened
def verify_and_open_program_files(program_file_name):
    program_file_dict = {}
    object_code_file_name = "." + SIC_OBJECT_CODE_FILE_EXTENSION
    assembly_listing_file_name = "." + SIC_ASSEMBLY_LISTING_FILE_EXTENSION
    # Check if file extension is present in file name
    # Verify that the file extension matches SIC_OBJECT_CODE_FILE_EXTENSION
    token_list = program_file_name.split(".")
    if len(token_list) == 1:
        object_code_file_name = token_list[0].strip() + object_code_file_name
        assembly_listing_file_name = token_list[0].strip() + assembly_listing_file_name
    elif len(token_list) == 2:
        if token_list[1].strip() == SIC_OBJECT_CODE_FILE_EXTENSION:
            object_code_file_name = token_list[0].strip() + object_code_file_name
            assembly_listing_file_name = token_list[0].strip() + assembly_listing_file_name

        else:
            raise SICSimulatorError("Invalid file extension")
    else:
        raise SICSimulatorError("Invalid file name")

    # Build a full file path using the configured default working directory
    object_code_file_path = SIC_DEFAULT_WORKING_DIRECTORY + object_code_file_name

    # check to see if the file exists
    if os.path.exists(object_code_file_path):
        # open the file in read mode
        object_code_file = open(object_code_file_path, "rt")

        program_file_dict["object_code_file"] = object_code_file
    else:
        raise SICSimulatorError("Object code file does not exist\n" + object_code_file_path)

    # Build a full file path using the configured default working directory
    assembly_listing_file_path = SIC_DEFAULT_WORKING_DIRECTORY + assembly_listing_file_name

    # check to see if the file exists
    if os.path.exists(assembly_listing_file_path):
        # open the file in read mode
        assembly_listing_file = open(assembly_listing_file_path, "rt")

        program_file_dict["assembly_listing_file"] = assembly_listing_file
    else:
        raise SICSimulatorError("Assembly listing file does not exist\n" + assembly_listing_file_path)

    # Return the program file dictionary
    return program_file_dict

# This function will initialize the memory model and then
# load program object code into the memory model
def load_program_object_code(parsed_object_code_dict_list):
    memory_model_dict = initialize_memory()

    # Load object code into memory model

    return memory_model_dict


memory_model_dict = {}

parsed_object_code_dict_list = []
parsed_listing_dict_list = []

mode = "LOAD"
while True:
    while mode == "LOAD":
        print(LOAD_MENU)
        command = input(SIC_PROMPT)

        match command.upper():
            case "L":
                try:
                    print("Enter program file name")
                    program_file_name = input(SIC_PROMPT)

                    # Verify and open program files
                    program_file_dict = verify_and_open_program_files(program_file_name)

                    parsed_object_code_dict_list = sic_object_code_parser(program_file_dict["object_code_file"])

                    parsed_listing_dict_list = sic_assembly_listing_parser(program_file_dict["assembly_listing_file"])

                    # Initialize memory and load program
                    memory_model_dict = load_program_object_code(parsed_object_code_dict_list)
                    # Initialize registers

                    print_status(program_file_name + " loaded and ready to run")
                    mode = "RUN"
                except SICSimulatorError as ex:
                    print_error(str(ex))
            case "Q":
                print(QUIT_CONFIRM)
                command = input(SIC_PROMPT)

                if command.upper() == "Y":
                    sys.exit()

            case _:
                print(UNRECOGNIZED_COMMAND)

    while mode == "RUN":
        print(RUN_MENU)
        command = input(SIC_PROMPT)

        match command.upper():
            case "S":
                mode = "LOAD"
            case "D":
                dump_memory(memory_model_dict)
            case "R":
                mode = "LOAD"
            case "Q":
                print(QUIT_CONFIRM)
                command = input(SIC_PROMPT)

                if command.upper() == "Y":
                    sys.exit()

            case _:
                print(UNRECOGNIZED_COMMAND)
