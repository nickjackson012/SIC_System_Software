from SIC_Simulator.sic_register_model import REGISTER_DICT, REGISTER_A, REGISTER_PC, REGISTER_X, REGISTER_SW
from SIC_Utilities import sic_integer
from SIC_Utilities.sic_constants import HEX_TO_OPCODE_DICT, BYTES_IN_WORD, INITIALIZATION_CHARACTER, \
    FROM_INDEXED_ADDRESSING_DICT, MINIMUM_MEMORY_ADDRESS_DEC, MAXIMUM_MEMORY_ADDRESS_DEC, MAXIMUM_INTEGER, \
    MINIMUM_INTEGER, SW_LESS_THAN, SW_EQUAL, SW_GREATER_THAN
from SIC_Utilities.sic_converter import hex_string_to_dec, dec_to_hex_string
from SIC_Utilities.sic_messaging import print_error, print_status


# This function will replace the initialized state character("-") with the hex value "F".
# The initialization character is used for visual aid when the memory model and registers are printed.
# Filling unassigned memory with hex value F is a more accurate representation of the state of memory on hardware.
def replace_initialized_state_character(hex_string):
    return hex_string.replace("-", "F")


# This function will test to see if a memory address is in the range of memory provided in the simulator(0000-7FFF).
def test_for_memory_address_in_range(memory_address_hex_string):
    is_in_memory_address_range = False
    memory_address_dec_value = hex_string_to_dec(memory_address_hex_string)

    if MINIMUM_MEMORY_ADDRESS_DEC <= memory_address_dec_value <= MAXIMUM_MEMORY_ADDRESS_DEC:
        is_in_memory_address_range = True
    else:
        # NOTE: Raise exception?
        pass
    return is_in_memory_address_range


# This function checks to see if a memory address hex string has indexed addressing called.
# It checks for an indexed addressing flag (8, 9, A, B, C, D, E, F) in the [X] position of the instruction format.
# INSTRUCTION FORMAT: [OPCODE 8 bits][X][ADDRESS 15 bits]
def test_for_indexed_addressing(memory_address_hex_string):
    is_indexed_addressing = False

    indexed_addressing_flag_character = memory_address_hex_string[0]

    if indexed_addressing_flag_character > "7":
        is_indexed_addressing = True

    return is_indexed_addressing


# This function
def create_indexed_address(memory_address_hex_string, REGISTER_DICT):
    indexed_addressing_flag_character = memory_address_hex_string[0]

    # Remove the indexed addressing flag from the indexed addressing flag character
    unflagged_character = FROM_INDEXED_ADDRESSING_DICT[indexed_addressing_flag_character]

    memory_address_hex_string = unflagged_character + memory_address_hex_string[1:]
    memory_address_dec_value = hex_string_to_dec(memory_address_hex_string)

    x_register_hex_string = REGISTER_DICT[REGISTER_X].get_hex_string()
    x_register_dec_value = hex_string_to_dec(x_register_hex_string)

    memory_address_hex_string = dec_to_hex_string(memory_address_dec_value + x_register_dec_value)

    return memory_address_hex_string


def execute_operation(REGISTER_DICT, MEMORY_MODEL):
    # PROGRAM COUNTER
    # Verify that the PC register holds an in-range memory address
    if not test_for_memory_address_in_range(REGISTER_DICT[REGISTER_PC].get_hex_string()):
        print_error("PROGRAM COUNTER FAULT: Halting program execution",
                    "PC REGISTER" + REGISTER_DICT[REGISTER_PC].get_hex_string() + "\n")
        return False

    pc_register_dec_value = hex_string_to_dec(REGISTER_DICT[REGISTER_PC].get_hex_string())

    # OPCODE
    # Look up operation code in memory and validate
    opcode_hex_string = MEMORY_MODEL.get_byte(pc_register_dec_value)

    opcode_mnemonic = HEX_TO_OPCODE_DICT.get(opcode_hex_string)

    # Verify that the opcode is supported by the simulator.
    if opcode_mnemonic is None:
        print_error("UNRECOGNIZED OPCODE FAULT: Halting program execution",
                    "OPCODE:" + opcode_hex_string + "\n")
        return False

    # MEMORY ADDRESS
    # Build the memory address
    memory_address_hex_string = MEMORY_MODEL.get_bytes(pc_register_dec_value + 1, 2)

    # Test for indexed addressing
    is_indexed_addressing = test_for_indexed_addressing(memory_address_hex_string)

    if is_indexed_addressing:
        memory_address_hex_string = create_indexed_address(memory_address_hex_string, REGISTER_DICT)

    memory_address_dec_value = hex_string_to_dec(memory_address_hex_string)

    # Increment PC Register
    REGISTER_DICT[REGISTER_PC].set_hex_string(dec_to_hex_string(pc_register_dec_value + BYTES_IN_WORD))

    match opcode_mnemonic:
        case "ADD":
            # A <- (A) + (m..m+2)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = sic_integer.hex_string_to_dec(register_a_hex_string)

            # Build the value held at memory location.
            word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)

            # Convert to decimal value and do the arithmetic.
            word_dec_value = sic_integer.hex_string_to_dec(word_hex_string)

            sum_dec_value = register_a_dec_value + word_dec_value

            if not MINIMUM_INTEGER <= sum_dec_value <= MAXIMUM_INTEGER:
                print_error("INTEGER OUT OF RANGE: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(sic_integer.dec_to_hex_string(sum_dec_value))

            continue_execution = True
            return continue_execution
        case "AND":
            # A <- (A) & (m..m+2)
            pass
        case "COMP":
            # (A) : (m..m+2)
            pass
        case "DIV":
            # A <- (A) / (m + m..2)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = sic_integer.hex_string_to_dec(register_a_hex_string)

            # Build the value held at memory location.
            word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)

            # Convert to decimal value and do the arithmetic.
            word_dec_value = sic_integer.hex_string_to_dec(word_hex_string)

            if word_dec_value == 0:
                print_error("DIVISION BY ZERO FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            quotient_dec_value = register_a_dec_value // word_dec_value

            if not MINIMUM_INTEGER <= quotient_dec_value <= MAXIMUM_INTEGER:
                print_error("INTEGER OUT OF RANGE FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(sic_integer.dec_to_hex_string(quotient_dec_value))

            continue_execution = True
            return continue_execution
        case "J":
            # PC <- m
            pass
        case "JEQ":
            # PC <- m if CC set to =
            pass
        case "JGT":
            # PC <- m if CC set to >
            pass
        case "JLT":
            # PC <- m if CC set to <
            status_word = REGISTER_DICT[REGISTER_SW].get_hex_string()
            if status_word == SW_LESS_THAN:
                REGISTER_DICT[REGISTER_PC].set_hex_string(memory_address_hex_string)

            continue_execution = True
            return continue_execution
        case "JSUB":
            # L <- (PC); PC <- m
            pass
        case "LDA":
            # A <- (m..m+2)
            # Build the value held at memory location.
            word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)

            REGISTER_DICT[REGISTER_A].set_hex_string(word_hex_string)

            continue_execution = True
            return continue_execution
        case "LDCH":
            # A[rightmost byte] <- (m)
            pass
        case "LDL":
            # L <- (m..m+2)
            pass
        case "LDX":
            # X <- (m..m+2)
            # Build the value held at memory location.
            word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)

            REGISTER_DICT[REGISTER_X].set_hex_string(word_hex_string)

            continue_execution = True
            return continue_execution
        case "MUL":
            # A <- (A) * (m..m+2)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = sic_integer.hex_string_to_dec(register_a_hex_string)

            # Build the value held at memory location.
            word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)

            # Convert to decimal value and do the arithmetic.
            word_dec_value = sic_integer.hex_string_to_dec(word_hex_string)

            product_dec_value = register_a_dec_value * word_dec_value

            if not MINIMUM_INTEGER <= product_dec_value <= MAXIMUM_INTEGER:
                print_error("INTEGER OUT OF RANGE: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(sic_integer.dec_to_hex_string(product_dec_value))

            continue_execution = True
            return continue_execution
        case "OR":
            # A <- (A) | (m..m+2)
            pass
        case "RD":
            # A[rightmost byte] <- data from device specified by (m)
            pass
        case "RSUB":
            # PC <- L
            # IMPLEMENT
            pass
        case "STA":
            # m..m+2 <- (A)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            index = 0
            start_index = 0
            end_index = 2

            while index < BYTES_IN_WORD:
                MEMORY_MODEL.set_byte(memory_address_dec_value + index, register_a_hex_string[start_index:end_index])
                index += 1
                start_index += 2
                end_index += 2

            continue_execution = True
            return continue_execution
        case "STCH":
            # m <- (A)[rightmost byte]
            pass
        case "STL":
            # m..m+2 <- (L)
            pass
        case "STSW":
            # m..m+2 <- (SW)
            pass
        case "STX":
            # m..m+2 <- (X)
            pass
        case "SUB":
            # A <- (A) - (m..m+2)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = sic_integer.hex_string_to_dec(register_a_hex_string)

            # Build the value held at memory location.
            word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)

            # Convert to decimal value and do the arithmetic.
            word_dec_value = sic_integer.hex_string_to_dec(word_hex_string)

            difference_dec_value = register_a_dec_value - word_dec_value

            if not MINIMUM_INTEGER <= difference_dec_value <= MAXIMUM_INTEGER:
                print_error("INTEGER OUT OF RANGE: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(sic_integer.dec_to_hex_string(difference_dec_value))

            continue_execution = True
            return continue_execution
        case "TD":
            # Test device specified by (m)
            pass
        case "TIX":
            # X <- (X) + 1; (X):(m..m+2)
            # Increment the value in the X register by 1
            register_x_dec_value = hex_string_to_dec(REGISTER_DICT[REGISTER_X].get_hex_string()) + 1
            register_x_hex_string = dec_to_hex_string(register_x_dec_value)
            REGISTER_DICT[REGISTER_X].set_hex_string(register_x_hex_string)
            # Compare the incremented value in register X with the value stored at the memory address
            memory_value_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, 3)
            memory_value_dec_value = sic_integer.hex_string_to_dec(memory_value_hex_string)
            # Set status word register based on the comparison
            if register_x_dec_value < memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_LESS_THAN)
            elif register_x_dec_value == memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_EQUAL)
            elif register_x_dec_value > memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_GREATER_THAN)

            continue_execution = True
            return continue_execution
        case "WD":
            # Device specified by (m) <- (A)[rightmost byte]
            pass
        case "XOS":
            # End processing and exit to the operating system
            print_status("Program execution terminated normally\n")
            continue_execution = False
            return continue_execution
