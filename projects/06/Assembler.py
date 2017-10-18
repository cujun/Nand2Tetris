#!/usr/bin/env python3

import logging
import os
import sys

import re




# Dicts for creating binary code corresponding C instruction
BIN_COMP = {
    '0'     : '0101010',
    '1'     : '0111111',
    '-1'    : '0111010',
    'D'     : '0001100',
    'A'     : '0110000',
    '!D'    : '0001101',
    '!A'    : '0110001',
    '-D'    : '0001111',
    '-A'    : '0110011',
    'D+1'   : '0011111',
    'A+1'   : '0110111',
    'D-1'   : '0001110',
    'A-1'   : '0110010',
    'D+A'   : '0000010',
    'D-A'   : '0010011',
    'A-D'   : '0000111',
    'D&A'   : '0000000',
    'D|A'   : '0010101',
    'M'     : '1110000',
    '!M'    : '1110001',
    '-M'    : '1110011',
    'M+1'   : '1110111',
    'M-1'   : '1110010',
    'D+M'   : '1000010',
    'D-M'   : '1010011',
    'M-D'   : '1000111',
    'D&M'   : '1000000',
    'D|M'   : '1010101',
}
BIN_DEST = {
    'M'     : '001',
    'D'     : '010',
    'MD'    : '011',
    'A'     : '100',
    'AM'    : '101',
    'AD'    : '110',
    'AMD'   : '111',
}
BIN_JUMP = {
    'JGT'   : '001',
    'JEQ'   : '010',
    'JGE'   : '011',
    'JLT'   : '100',
    'JNE'   : '101',
    'JLE'   : '110',
    'JMP'   : '111',
}

# Regular expression matching assembly command
RE_COMMANDS = (
    ( 'RE_INST_A', re.compile(r"^@(\d+|[a-zA-Z_.$:][\w.$:]*)$") ),
    ( 'RE_INST_C', re.compile(r"^([A?M?D?]+=)?[+\-!&|01AMD]+(;J[A-Z]{2})?$") ),
    ( 'RE_LABEL', re.compile(r"^\([a-zA-Z_.$:][\w.$:]*\)$") ),
    ( 'RE_COMMENT', re.compile(r"^//") ),
)

# Symbol table with some predefined symbols
symbol_table = {
    'SP'    : 0x0000,
    'LCL'   : 0x0001,
    'ARG'   : 0x0002,
    'THIS'  : 0x0003,
    'THAT'  : 0x0004,
    'R0'    : 0x0000,
    'R1'    : 0x0001,
    'R2'    : 0x0002,
    'R3'    : 0x0003,
    'R4'    : 0x0004,
    'R5'    : 0x0005,
    'R6'    : 0x0006,
    'R7'    : 0x0007,
    'R8'    : 0x0008,
    'R9'    : 0x0009,
    'R10'   : 0x000A,
    'R11'   : 0x000B,
    'R12'   : 0x000C,
    'R13'   : 0x000D,
    'R14'   : 0x000E,
    'R15'   : 0x000F,
    'SCREEN': 0x4000,
    'KBD'   : 0x6000,
}




def match_regex(s):
    # Please make sure there's no whitespace in s.
    for cmd_type, pattern in RE_COMMANDS:
        if pattern.match(s):
            return cmd_type
    return None

def is_decimal(s):
    if s[0] in ('-', '+'):
        return s[1:].isdecimal()
    return s.isdecimal()

def error_line():
    logging.warning("Unexpected assembly command.")




def main():
    logging.basicConfig(level=logging.DEBUG)

    # Initializations.
    try:
        lines = list(filter(None, [line.strip() for line in open(sys.argv[1])]))
        logging.info("Start assembling [{}].".format(sys.argv[1]))
        filename_asm = (sys.argv[1])[:-4]
        addr_symbol = 0x0010
    except IndexError:
        logging.error("Please properly enter the name of assembly file as an argument.")
        return
    except FileNotFoundError:
        logging.error("Could not read input: [{}].".format(sys.argv[1]))
        return

    # First Pass. (Build symbol table + Syntax check)
    global symbol_table
    parsed_lines = []
    for line in lines:
        # Parse current line.
        curr = re.split(r"//", line)
        curr = ''.join(curr[0].split())
        logging.debug(curr)

        # If new symbol found, register to symbol table.
        parsed_lines = []; parsed_line = None
        typee = match_regex(curr)
        if typee == 'RE_INST_A':
            symbol = curr[1:]
            parsed_line = [typee, symbol]
        elif typee == 'RE_INST_C':
            cmd_split = re.split(r"[=;]", curr)
            parsed_line = [typee]
            for s in cmd_split:
                parsed_line.append(s)
        elif typee == 'RE_LABEL':
            symbol = curr[1:-1]
            if (not is_decimal(symbol)) and (symbol not in symbol_table):
                logging.debug("####Add symbol [{}]".format(symbol))
                symbol_table[symbol] = addr_symbol
                addr_symbol += 1
        if parsed_line:
            logging.debug("####{}".format(parsed_line))
            parsed_lines.append(parsed_line)

    # Second Pass. (Generate Hack binary code)
    '''
    with open("{}.hack".format(filename_asm), 'w') as f_hack:
        for parsed_line in parsed_lines:
            # Generate Hack binary code.
            pass

            # Write binary code to .hack
            pass
    '''
    
    logging.info("Done.")

if __name__ == '__main__':
    main()
