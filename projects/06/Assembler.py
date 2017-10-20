#!/usr/bin/env python3

import logging
import os
import sys

import re




# Costants for creating binary code corresponding C instruction
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
    'null'  : '000',
    'M'     : '001',
    'D'     : '010',
    'MD'    : '011',
    'A'     : '100',
    'AM'    : '101',
    'AD'    : '110',
    'AMD'   : '111',
}
BIN_JUMP = {
    'null'  : '000',
    'JGT'   : '001',
    'JEQ'   : '010',
    'JGE'   : '011',
    'JLT'   : '100',
    'JNE'   : '101',
    'JLE'   : '110',
    'JMP'   : '111',
}

# Regular expressions matching each assembly command
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
    logging.error("Some instruction is not correct, so generated hack file may be a garbage...")




def main():
    logging.basicConfig(level=logging.INFO)

    # Initializations.
    try:
        lines = list(filter(None, [line.strip() for line in open(sys.argv[1])]))
        logging.info("Start assembling <{}>.".format(sys.argv[1]))
        filename_asm = (sys.argv[1])[:-4]
        addr_inst = 0; addr_var = 0x0010
    except IndexError:
        logging.error("Please properly enter the name of assembly file as an argument.")
        return
    except FileNotFoundError:
        logging.error("Could not read input: <{}>.".format(sys.argv[1]))
        return

    # First Pass. (Build symbol table + Syntax check)
    global symbol_table
    parsed_lines = list()
    for line in lines:
        # Parse current line.
        curr = re.split(r"//", line)
        curr = ''.join(curr[0].split())
        logging.debug("[First Pass] curr <{}>".format(curr))
        if len(curr) < 1:
            continue

        # If new symbol found, register to symbol table.
        parsed_line = None
        typee = match_regex(curr)
        if typee == 'RE_INST_A':
            symbol = curr[1:]
            parsed_line = [typee, symbol]
        elif typee == 'RE_INST_C':
            parsed_line = [typee]
            cmd_split = curr.split('=')
            parsed_line.append(cmd_split[0] if len(cmd_split) > 1 else 'null')
            if len(cmd_split) > 1:
                cmd_split[0] = cmd_split[1]
            cmd_split = cmd_split[0].split(';')
            parsed_line.append(cmd_split[0])
            parsed_line.append(cmd_split[1] if len(cmd_split) > 1 else 'null')
        elif typee == 'RE_LABEL':
            symbol = curr[1:-1]
            if (not is_decimal(symbol)) and (symbol not in symbol_table):
                logging.debug("[First Pass] Add symbol <{}:{}>".format(symbol, addr_inst))
                symbol_table[symbol] = addr_inst
        else:
            error_line()
            continue
        if parsed_line:
            logging.debug("[First Pass] Code for later <{}>".format(parsed_line))
            parsed_lines.append(parsed_line)
            addr_inst += 1
    logging.debug("[First Pass] Done")
    # End of First Pass.

    # Second Pass. (Generate Hack binary code)
    with open("{}.hack".format(filename_asm), 'w') as f_hack:
        for parsed_line in parsed_lines:
            logging.debug("[Second Pass] Process <{}>".format(parsed_line))
            # Generate Hack binary code.
            bin_code = ''
            if parsed_line[0] == 'RE_INST_A':
                bin_code = "0"
                if is_decimal(parsed_line[1]):
                    bin_code += "{:015b}".format(int(parsed_line[1]))
                elif parsed_line[1] in symbol_table:
                    bin_code += "{:015b}".format(symbol_table[parsed_line[1]])
                else:
                    bin_code += "{:015b}".format(addr_var)
                    logging.debug("[Second Pass] Add symbol <{}:{}>".format(parsed_line[1], addr_var))
                    symbol_table[parsed_line[1]] = addr_var
                    addr_var += 1
            elif parsed_line[0] == 'RE_INST_C':
                bin_code = "111{}{}{}".format(BIN_COMP.get(parsed_line[2], ''), BIN_DEST.get(parsed_line[1], ''), BIN_JUMP.get(parsed_line[3], ''))
                if len(bin_code) != 16:
                    bin_code = "2" * 16
                    error_line()
            # Write binary code to .hack
            logging.debug("[Second Pass] Gen code <{}>".format(bin_code))
            f_hack.write("{}\n".format(bin_code))
    logging.debug("[Second Pass] Done")
    # End of Second Pass.
    
    logging.info("Done.")

if __name__ == '__main__':
    main()
