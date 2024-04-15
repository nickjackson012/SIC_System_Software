BIN_TO_HEX_DICT = {"0000": "0", "0001": "1",
                   "0010": "2", "0011": "3",
                   "0100": "4", "0101": "5",
                   "0110": "6", "0111": "7",
                   "1000": "8", "1001": "9",
                   "1010": "A", "1011": "B",
                   "1100": "C", "1101": "D",
                   "1110": "E", "1111": "F"}

BYTES_IN_MEMORY = 32768

COMMENT_LINE_INDICATOR = "."

DEC_TO_HEX_DICT = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}

HEX_DIGIT_SET = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"}

HEX_TO_BIN_DICT = {"0": "0000", "1": "0001",
                   "2": "0010", "3": "0011",
                   "4": "0100", "5": "0101",
                   "6": "0110", "7": "0111",
                   "8": "1000", "9": "1001",
                   "A": "1010", "B": "1011",
                   "C": "1100", "D": "1101",
                   "E": "1110", "F": "1111"}

HEX_TO_DEC_DICT = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
                   "9": 9, "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}

TO_INDEXED_ADDRESSING_DICT = {"0": "8", "1": "9", "2": "A", "3": "B", "4": "C", "5": "D", "6": "E", "7": "F"}
FROM_INDEXED_ADDRESSING_DICT = {"8": "0", "9": "1", "A": "2", "B": "3", "C": "4", "D": "5", "E": "6", "F": "7"}

LONE_OPCODE_VALIDATION_SET = {"RSUB", "END"}

MINIMUM_BYTE_OPERAND_LENGTH = 1
MAXIMUM_BYTE_OPERAND_LENGTH = 32

MINIMUM_INTEGER = -8388608  # -8,388,608
MAXIMUM_INTEGER = 8388607  # 8,388,607

MAXIMUM_LENGTH_OF_OPERAND = 5

MAXIMUM_LENGTH_OF_START_OPERAND = 4

MINIMUM_MEMORY_ADDRESS_DEC = 0
MAXIMUM_MEMORY_ADDRESS_DEC = 32767

MAXIMUM_NUMBER_OF_LABELS = 500

MINIMUM_RESB = 1
MAXIMUM_RESB = 32768

MINIMUM_RESW = 1
MAXIMUM_RESW = 10922    # 32768//3

MEMORY_ADDRESS_STRING_LENGTH = 4

NUMBER_OF_BITS_IN_A_INTEGER = 24

OBJECT_CODE_TEXT_RECORD_BODY_LENGTH = 60

OPCODE_TO_HEX_DICT = {"ADD": "18", "AND": "40", "COMP": "28", "DIV": "24", "J": "3C", "JEQ": "30",
               "JGT": "34", "JLT": "38", "JSUB": "48", "LDA": "00", "LDCH": "50", "LDL": "08",
               "LDX": "04", "MUL": "20", "OR": "44", "RD": "D8", "RSUB": "4C", "STA": "0C", "STCH": "54",
               "STL": "14", "STSW": "E8", "STX": "10", "SUB": "1C", "TD": "E0", "TIX": "2C", "WD": "DC"}

OPCODE_VALIDATION_SET = {"ADD", "AND", "COMP", "DIV", "J", "JEQ", "JGT", "JLT", "JSUB", "LDA", "LDCH", "LDL",
                         "LDX", "MUL", "OR", "RD", "RSUB", "STA", "STCH", "STL", "STSW", "STX", "SUB",
                         "TD", "TIX", "WD", "START", "END", "BYTE", "WORD", "RESB", "RESW"}

LOC_COLUMN_WIDTH = 9
LABEL_COLUMN_WIDTH = 10
OPCODE_COLUMN_WIDTH = 9
OPERAND_COLUMN_WIDTH = 36
OBJECT_CODE_COLUMN_WIDTH = 36


