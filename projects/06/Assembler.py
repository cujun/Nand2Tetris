import logging
import os
import sys

import re




# Regular expression matching assembly command
# TOKEN_RE = re.compile(r'(?:([()~+*]|->|[^\s()~+*]+))')
# VARIABLE_RE = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')

# Symbol table
symbol_table = {}




def error_line():
    logging.warning("Unexpected assembly command.")




def main():
    logging.basicConfig(level=logging.DEBUG)

    # Initializations.
    try:
        lines = list(filter(None, [line.rstrip('\n') for line in open(sys.argv[1])]))
        logging.info("Start assembling [{}].".format(sys.argv[1]))
        filename_asm = (sys.argv[1])[:-4]
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
        pass

        # If new symbol found, register to symbol table.
        pass

    # Second Pass. (Generate Hack binary code)
    with open("{}.hack".format(filename_asm), 'w') as f_hack:
        for parsed_line in parsed_lines:
            # Generate Hack binary code.
            pass

            # Write binary code to .hack
            pass
    
    logging.info("Done.")

if __name__ == '__main__':
    main()
