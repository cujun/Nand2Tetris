import os
import sys
import logging

import re
from collections import namedtuple
import operator
from string import ascii_lowercase, ascii_uppercase

import copy




# Regular expression matching optional whitespace followed by a token
# (if group 1 matches) or an error (if group 2 matches).
# TOKEN_RE = re.compile(r'\s*(?:([A-Za-z01()~+*]|->)|(\S))')
# TOKEN_RE = re.compile(r'(?:(([a-zA-Z][a-zA-Z0-9]*)|[()~+*]|->))')
TOKEN_RE = re.compile(r'(?:([()~+*]|->|[^\s()~+*]+))')
VARIABLE_RE = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')

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

Constant = namedtuple('Constant', 'value')
Variable = namedtuple('Variable', 'name')
UnaryOp = namedtuple('UnaryOp', 'op operand')
BinaryOp = namedtuple('BinaryOp', 'left op right')




def tokenize(s):
    """Generate tokens from the string s, followed by TOKEN_END."""
    for m in TOKEN_RE.finditer(s):
        if m.group(1):
            yield m.group(1)
        else:
            raise SyntaxError("Unexpected character {!r}".format(m.group(2)))
    yield TOKEN_END


def parse(s):
    """Parse s as a Boolean expression and return the parse tree."""
    tokens = tokenize(s)        # Stream of tokens.
    token = next(tokens)        # The current token.
    print("toekn:[{}]".format(token))

    def error(expected):
        # Current token failed to match, so raise syntax error.
        raise SyntaxError("Expected {} but found {!r}"
                          .format(expected, token))

    def match(valid_tokens):
        # If the current token is found in valid_tokens, consume it
        # and return True. Otherwise, return False.
        nonlocal token
        if token in valid_tokens:
            token = next(tokens)
            return True
        else:
            return False

    def term():
        # Parse a <Term> starting at the current token.
        nonlocal token
        t = token
        if VARIABLE_RE.match(t):    # Not match()
            INPUT_PINS.add(t)
            token = next(tokens)    # Corner case!!
            return Variable(name=t)
        elif match('('):
            tree = disjunction()
            if match(')'):
                return tree
            else:
                error("')'")
        else:
            error("term")

    def unary_expr():
        # Parse a <UnaryExpr> starting at the current token.
        t = token
        if match('~'):
            operand = unary_expr()
            return UnaryOp(op=UNARY_OPERATORS[t], operand=operand)
        else:
            return term()

    def binary_expr(parse_left, valid_operators, parse_right):
        # Parse a binary expression starting at the current token.
        # Call parse_left to parse the left operand; the operator must
        # be found in valid_operators; call parse_right to parse the
        # right operand.
        left = parse_left()
        t = token
        if match(valid_operators):
            right = parse_right()
            return BinaryOp(left=left, op=BINARY_OPERATORS[t], right=right)
        else:
            return left

    def implication():
        # Parse an <Implication> starting at the current token.
        return binary_expr(unary_expr, '->', implication)

    def conjunction():
        # Parse a <Conjunction> starting at the current token.
        return binary_expr(implication, '*', conjunction)

    def disjunction():
        # Parse a <Disjunction> starting at the current token.
        return binary_expr(conjunction, '+', disjunction)

    tree = disjunction()
    if token != TOKEN_END:
        error("end of input")
    return tree




if __name__ == '__main__':
    try:
        lines = list(filter(None, [line.rstrip('\n') for line in open(INPUT_FILE_NAME)]))
        for line in lines:
            # Initializations
            INPUT_PINS = set()  # Input pins
            NAND_GATES = []     # Nand gates which we'll write to output file
            print()

            # Split current line into 'Name' and 'Formula' parts
            line_tokenized = list(filter(None, [l.strip() for l in line.split('=')]))
            if len(line_tokenized) != 2:    # SKIP condition
                logging.warning("Unexpected input line exists. SKIP!!")
                continue
            name = line_tokenized[0]; formula = line_tokenized[1]
            '''
            print("@@@@@@@@@")
            tt = tokenize(formula)
            for ttt in tt:
                print(ttt)
            print("@@@@@@@@@")
            '''

            # Build parse tree
            print(parse(formula))
            print("Input pins: {}".format(INPUT_PINS))

            # Process parse tree to generate Nand gates
            ## TO DO

            # Create chip
            f_output = open("{}.hdl".format(name), 'w')
            f_output.write("// {} Chip\n".format(name))
            f_output.write("// Generate by cujun's formula compiler\n\n")
            f_output.write("CHIP {} ".format(name))
            f_output.write("{\n")
            # TO DO: Print input pins
            input_pins = "  IN " + ";\n"
            f_output.write(input_pins)
            f_output.write("  OUT out;\n\n")
            f_output.write("  PARTS:\n")
            # TO DO: Print Nands
            f_output.write("}")
            print("[{}] Chip Done.".format(name))
    except IOError:
        logging.error("Could not read file: {}".format(INPUT_FILE_NAME))
