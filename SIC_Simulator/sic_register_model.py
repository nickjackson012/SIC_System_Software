from SIC_Utilities.sic_constants import HEX_TO_BIN_DICT, BIN_TO_HEX_DICT

NUMBER_OF_HEX_DIGITS = 6
NUMBER_OF_BIN_DIGITS = 24


class RegisterContentsError(Exception):
    pass


class SICRegisterModel:
    def __init__(self, register_name):
        self.register_name = register_name
        self.hex_string = "FFFFFF"
        self.bin_string = "111111111111111111111111"

    def get_register_name(self):
        return self.register_name

    def get_formatted_register_name(self):
        return self.register_name.rjust(2)

    def hex_to_bin(self, hex_string):
        bin_string = ""
        # Register holds 24 bits
        # range(start, stop, step)
        for hex_digit in hex_string:
            bin_string += HEX_TO_BIN_DICT[hex_digit]
        return bin_string

    def set_hex_string(self, hex_string):
        # Ensure all hex digits are uppercase and pad string with 0 if necessary
        hex_string = hex_string.upper().rjust(NUMBER_OF_HEX_DIGITS, "0")
        # Error Check for length and hex digits
        error_found = False
        if len(hex_string) != NUMBER_OF_HEX_DIGITS:
            error_found = True
        for digit in hex_string:
            if digit not in HEX_TO_BIN_DICT:
                error_found = True
        if error_found:
            raise RegisterContentsError

        # hex_string is okay, set the value
        self.hex_string = hex_string

        # Set self.register_bin_string
        self.bin_string = self.hex_to_bin(hex_string)

    def bin_to_hex(self, bin_string):
        hex_string = ""
        # Register holds 24 bits
        # range(start, stop, step)
        for index in range(0, 24, 4):
            hex_string += BIN_TO_HEX_DICT[bin_string[index:index + 4]]
        return hex_string

    # Set self.register_bin_string
    def set_bin_string(self, bin_string):
        # Pad bin string with 0 if necessary
        bin_string.rjust(NUMBER_OF_BIN_DIGITS, "0")
        # Error Check for length and hex digits
        error_found = False
        if len(bin_string) != NUMBER_OF_BIN_DIGITS:
            error_found = True
        for digit in bin_string:
            if digit != "0" and digit != "1":
                error_found = True
                print("digit", digit)
        if error_found:
            raise RegisterContentsError

        # bin_string is okay, set the value
        self.bin_string = bin_string

        # Set self.register_hex_string
        # Convert bin_string to hex
        self.hex_string = self.bin_to_hex(bin_string)

    def get_bin_string(self):
        return self.bin_string

    def get_hex_string(self):
        return self.hex_string

    def get_formatted_bin_string(self):
        formatted_bin_string = ""
        for index in range(len(self.bin_string)):
            if index % 8 == 0:
                formatted_bin_string += "  " + self.bin_string[index]
            elif index % 4 == 0:
                formatted_bin_string += " " + self.bin_string[index]
            else:
                formatted_bin_string += self.bin_string[index]

        return formatted_bin_string.strip()

    def get_formatted_hex_string(self):
        formatted_hex_string = ""
        for index in range(len(self.hex_string)):
            if index % 2 == 0:
                formatted_hex_string += " " + self.hex_string[index]
            else:
                formatted_hex_string += self.hex_string[index]

        return formatted_hex_string.strip()


REGISTER_A = "A"
REGISTER_X = "X"
REGISTER_L = "L"
REGISTER_PC = "PC"
REGISTER_SW = "SW"

REGISTER_DICT = {REGISTER_A: SICRegisterModel(REGISTER_A),
                 REGISTER_X: SICRegisterModel(REGISTER_X),
                 REGISTER_L: SICRegisterModel(REGISTER_L),
                 REGISTER_PC: SICRegisterModel(REGISTER_PC),
                 REGISTER_SW: SICRegisterModel(REGISTER_SW)}


def dump_registers():
    output_string = ""
    for register_name, register in REGISTER_DICT.items():
        output_string += ("REGISTER " + register.get_formatted_register_name() + " :" +
                          "   HEX [" + register.get_formatted_hex_string() + "]" +
                          "   BIN [" + register.get_formatted_bin_string() + "]\n")

    print(output_string)

# TEST BED
# register_a = SICRegisterModel()
# register_a.set_register_hex_string("1AB4Ff")
# register_a.set_bin_string("000000000000000000000001")
