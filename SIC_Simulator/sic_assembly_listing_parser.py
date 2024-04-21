import os.path
import sys

from SIC_Simulator.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY
from SIC_Utilities.sic_constants import SIC_ASSEMBLY_LISTING_FILE_EXTENSION
from SIC_Utilities.sic_messaging import print_error, print_status


class SICAssemblyListingParserError(Exception):
    pass


# This function opens and reads an assembly listing file (*.lst).
# It processes each line of code one at a time
# It parses out all the relevant assembly listing tokens and stores them in a line of listing dictionary.
# It returns a list containing all the parsed line of listing dictionaries.
def sic_assembly_listing_parser(assembly_listing_file):
    parsed_listing_dict_list = []

    start_found = False

    end_found = False

    for line_of_listing in assembly_listing_file:

        memory_address = line_of_listing[:4]
        unparsed_line_of_listing = line_of_listing[:-1]

        if line_of_listing.isspace():
            # Close assembly listing file, print error message, and exit program.
            assembly_listing_file.close()
            # ERROR
            raise SICAssemblyListingParserError("Can not have a blank line in the assembly listing file")

        if not start_found:
            if line_of_listing[19:28].rstrip() == "START":
                start_found = True
            else:
                # Close assembly listing file and throw exception.
                assembly_listing_file.close()
                # ERROR
                raise SICAssemblyListingParserError("START must be the first opcode in the assembly listing file.")
        else:
            if line_of_listing[19:28].rstrip() == "END":
                assembly_listing_file.close()
                return parsed_listing_dict_list

            else:
                parsed_listing_dict = {memory_address: unparsed_line_of_listing}

                parsed_listing_dict_list.append(parsed_listing_dict)

    if not end_found:
        # Close assembly listing file, print error message, and exit program.
        assembly_listing_file.close()
        raise SICAssemblyListingParserError("END was not found in the assembly listing file")



# TEST BED

# assembly_listing_file_name = "ReadWrite"
#
# assembly_listing_file_path = (SIC_DEFAULT_WORKING_DIRECTORY +
#                               assembly_listing_file_name + "." +
#                               SIC_ASSEMBLY_LISTING_FILE_EXTENSION)
#
# parsed_listing_dict_list = sic_assembly_listing_parser(assembly_listing_file_path)
#
# for line in parsed_listing_dict_list:
#     print(line)
