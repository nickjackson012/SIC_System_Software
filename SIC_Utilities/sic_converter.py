from SIC_Utilities.sic_constants import DEC_TO_HEX_DICT, MINIMUM_MEMORY_ADDRESS_DEC, MAXIMUM_MEMORY_ADDRESS_DEC, \
    MEMORY_ADDRESS_STRING_LENGTH, HEX_TO_DEC_DICT, HEX_DIGIT_SET


class SICConverterError(Exception):
    pass


def dec_to_hex_string(dec_value: int):

    if not isinstance(dec_value, int):
        raise SICConverterError("Cannot convert non-integer value passed to dec_to_hex_string function.")

    hex_digit_list = []
    quotient = dec_value
    while quotient != 0:
        remainder = quotient % 16
        if remainder < 10:
            hex_digit_list.insert(0, str(remainder))
        else:
            hex_digit_list.insert(0, DEC_TO_HEX_DICT[remainder])

        quotient = quotient // 16

    hex_string = ""
    for hex_digit in hex_digit_list:
        hex_string += hex_digit
    return hex_string

# NOTE: Do we want to check for out of range and other errors?
#       Do we want to read and write memory functions?
def dec_to_memory_address_hex_string(dec_value: int):
    if not isinstance(dec_value, int):
        raise SICConverterError("Cannot convert non-integer value passed to dec_to_memory_address_hex_string function.")

    if MINIMUM_MEMORY_ADDRESS_DEC > dec_value or dec_value > MAXIMUM_MEMORY_ADDRESS_DEC:
        raise SICConverterError("Memory address must be in the range of 0 to 32767")
    hex_digit_list = list(dec_to_hex_string(dec_value))

    # pad hex_string_list with 0's
    while len(hex_digit_list) < MEMORY_ADDRESS_STRING_LENGTH:
        hex_digit_list.insert(0, "0")

    hex_string = ""
    for hex_digit in hex_digit_list:
        hex_string += hex_digit
    return hex_string


def hex_string_to_dec(hex_string: str):

    if not isinstance(hex_string, str):
        raise SICConverterError("Cannot convert non-string value passed to hex_string_to_dec function.")

    hex_digit_list = list(hex_string)
    reversed_hex_digit_list = list(reversed(hex_digit_list))
    dec_value = 0

    for index in range(len(reversed_hex_digit_list)):
        hex_digit = reversed_hex_digit_list[index]

        if hex_digit not in HEX_TO_DEC_DICT:
            raise SICConverterError("Invalid hex digit (0-9 A-F")

        dec_value += HEX_TO_DEC_DICT[hex_digit] * 16 ** index

    return dec_value


def test_for_hex(hex_string):
    for character in hex_string:
        if character not in HEX_DIGIT_SET:
            return False

    return True
