import os
import sys
import logging

import re
from collections import namedtuple
import operator
from string import ascii_lowercase, ascii_uppercase


# Regular expression matching optional whitespace followed by a token
# (if group 1 matches) or an error (if group 2 matches).
# TOKEN_RE = re.compile(r'\s*(?:([A-Za-z01()~+*]|->)|(\S))')
# TOKEN_RE = re.compile(r'(?:(([a-zA-Z][a-zA-Z0-9]*)|[()~+*]|->))')
TOKEN_RE = re.compile(r'(?:([()~+*]|->|\S+))')
VARIABLE_RE = re.compile(r'[a-zA-Z][a-zA-Z0-9]+')

# Special token indicating the end of the input string.
TOKEN_END = '<end of input>'

# File name of input
INPUT_FILE_NAME = 'input.txt'

# Map from unary operator to function implementing it.
UNARY_OPERATORS = {
            '~': operator.not_,
}

# Map from binary operator to function implementing it.
BINARY_OPERATORS = {
            '*': operator.and_,
            '+': operator.or_,
            '->': lambda a, b: not a or b,
}

# Input pins
INPUT_PINS = []

# Nand gates which we'll write to output file
NAND_GATES = []


def tokenize(s):
    """Generate tokens from the string s, followed by TOKEN_END."""
    for m in TOKEN_RE.finditer(s):
        if m.group(1):
            yield m.group(1)
        else:
            raise SyntaxError("Unexpected character {!r}".format(m.group(2)))
    yield TOKEN_END


if __name__ == '__main__':
    try:
        lines = list(filter(None, [line.rstrip('\n') for line in open(INPUT_FILE_NAME)]))
        for line in lines:
            print()
            # Parse current line
            line_tokenized = list(filter(None, [l.strip() for l in line.split('=')]))
            if len(line_tokenized) != 2:    # SKIP condition
                logging.warning("Unexpected input line exists. SKIP!!")
                continue
            name = line_tokenized[0]; formula = line_tokenized[1]
            formula_tokenized = tokenize(formula);  # Parse formula
            '''
            for token in formula_tokenized:
                print(token)
            '''

            # Build parse tree

            # Create chip
            f_output = open("{}.hdl".format(name), 'w')
            f_output.write("// {} Chip\n".format(name))
            f_output.write("// Generate by cujun's formula compiler\n\n")
            f_output.write("CHIP {} ".format(name))
            f_output.write("{\n")
            # TO DO: Print input pins
            input_pins = "  IN " + "\n"
            f_output.write(input_pins)
            f_output.write("  OUT out;\n\n")
            f_output.write("  PARTS:\n")
            # TO DO: Print Nands
            f_output.write("}")
            print("[{}] Chip Done.".format(name))
    except IOError:
        logging.error("Could not read file: {}".format(INPUT_FILE_NAME))
