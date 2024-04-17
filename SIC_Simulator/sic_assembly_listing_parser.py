import os.path
import sys

from SIC_Utilities.sic_constants import SIC_DEFAULT_WORKING_DIRECTORY, SIC_ASSEMBLY_LISTING_FILE_EXTENSION
from SIC_Utilities.sic_messaging import print_error, print_status


def sic_assembly_listing_parser(assembly_listing_file_path):
    # STATUS
    print_status("Beginning parsing", assembly_listing_file_path)
    if os.path.exists(assembly_listing_file_path):
        assembly_listing_file = open(assembly_listing_file_path, "rt")

        parsed_listing_dict_list = []
        # line_of_listing_number = 0

        start_found = False

        end_found = False

        for line_of_listing in assembly_listing_file:
            # line_of_listing_number += 1

            memory_address = line_of_listing[:4]
            unparsed_line_of_listing = line_of_listing[:-1]

            if line_of_listing.isspace():
                # Close assembly listing file, print error message, and exit program.
                assembly_listing_file.close()
                # ERROR
                print_error("SIC Assembly Listing Parser Error: Can not have a blank line in the assembly listing file")

                sys.exit()

            if not start_found:
                if line_of_listing[19:28].rstrip() == "START":
                    start_found = True
                else:
                    # Close assembly listing file, print error message, and exit program.
                    assembly_listing_file.close()
                    # ERROR
                    print_error("SIC Assembly Listing Parser Error: START must be the first opcode in the assembly listing",
                                unparsed_line_of_listing)

                    sys.exit()
            else:
                if line_of_listing[19:28].rstrip() == "END":
                    assembly_listing_file.close()
                    # STATUS
                    print_status("Parsing complete", assembly_listing_file_path)
                    return parsed_listing_dict_list

                else:
                    parsed_listing_dict = {memory_address: unparsed_line_of_listing}

                    parsed_listing_dict_list.append(parsed_listing_dict)

        if not end_found:
            # Close assembly listing file, print error message, and exit program.
            assembly_listing_file.close()
            # ERROR
            print_error("SIC Assembly Listing Parser Error: END was not found in assembly listing file")

            sys.exit()

    else:
        # print error message, and exit program.
        # ERROR
        print_error("SIC Assembly Listing Parser Error: Assembly listing file does not exist",)

        sys.exit()


# TEST BED

assembly_listing_file_name = "ReadWriteTest02"

assembly_listing_file_path = (SIC_DEFAULT_WORKING_DIRECTORY +
                              assembly_listing_file_name + "." +
                              SIC_ASSEMBLY_LISTING_FILE_EXTENSION)

parsed_listing_dict_list = sic_assembly_listing_parser(assembly_listing_file_path)

for line in parsed_listing_dict_list:
    print(line)
