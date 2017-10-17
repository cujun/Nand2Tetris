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
    ( 'RE_INST_A', re.compile(r"^@(\d+|[a-zA-Z_.$:][\w.$:]*)(//.*)?$") ),
    ( 'RE_INST_C', re.compile(r"^([A?M?D?]=)?[+\-!&|01AMD]+(;J[A-Z]{2})?(//.*)?$") ),
    ( 'RE_LABEL', re.compile(r"^\([a-zA-Z_.$:][\w.$:]*\)(//.*)?$") ),
    ( 'RE_COMMENT', re.compile(r"^//") ),
)

# Symbol table
symbol_table = dict()




def error_line():
    logging.warning("Unexpected assembly command.")




def main():
    logging.basicConfig(level=logging.DEBUG)

    # Initializations.
    try:
        lines = list(filter(None, [line.strip() for line in open(sys.argv[1])]))
        logging.info("Start assembling [{}].".format(sys.argv[1]))
        filename_asm = (sys.argv[1])[:-4]
    except IndexError:
        logging.error("Please properly enter the name of assembly file as an argument.")
        return
    except FileNotFoundError:
        logging.error("Could not read input: [{}].".format(sys.argv[1]))
        return

    for line in lines:
        logging.debug(line)
        curr = "".join(line.split())
        for key, pattern in RE_COMMANDS:
            if pattern.match(curr):
                logging.debug(key)
    # First Pass. (Build symbol table + Syntax check)
    global symbol_table
    parsed_lines = []
    for line in lines:
        # Parse current line.
        pass

        # If new symbol found, register to symbol table.
        pass

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
