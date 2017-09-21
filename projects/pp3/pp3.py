import os
import sys
import logging

import re
from collections import namedtuple
import operator




# File name of input.
INPUT_FILE_NAME = 'input.txt'

# Input pins
INPUT_PINS = set()

# Nand gates which we'll write to output file
NAND_GATES = []

# Index of current pin
INDEX_PIN = None


# Regular expression matching optional whitespace followed by a token
# (if group 1 matches) or an error (if group 2 matches).
# TOKEN_RE = re.compile(r'\s*(?:([A-Za-z01()~+*]|->)|(\S))')
TOKEN_RE = re.compile(r'(?:([()~+*]|->|[^\s()~+*]+))')
VARIABLE_RE = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')

# Special token indicating the end of the input string.
TOKEN_END = '<end of input>'

# Special functions for processing formula parse tree
def add_to_nand(a, b, out):
    global NAND_GATES
    NAND_GATES.append("Nand(a={}, b={}, out={});".format(a, b, out))
def gen_argout(is_root):
    global INDEX_PIN
    arg_out = "out"
    if not is_root:
        arg_out = "pin{}".format(INDEX_PIN)
        INDEX_PIN = INDEX_PIN + 1
    return arg_out
def unary_oper_not(arg_in, is_root):
    """ Unary opeartor about "NOT" function.
    Same as NOT gate implementation with NAND gates in our HDL format.
    """
    arg_out = gen_argout(is_root)
    add_to_nand(arg_in, arg_in, arg_out)
    return arg_out
def binary_oper_and(arg_a, arg_b, is_root):
    """ Binary opeartor about "AND" function.
    Same as AND gate implementation with NAND gates in our HDL format.
    """
    arg_out = gen_argout(is_root)
    arg_temp = gen_argout(False)
    add_to_nand(arg_a, arg_b, arg_temp)
    add_to_nand(arg_temp, arg_temp, arg_out)
    return arg_out
def binary_oper_or(arg_a, arg_b, is_root):
    """ Binary opeartor about "AND" function.
    Same as Or gate implementation with NAND gates in our HDL format.
    """
    arg_out = gen_argout(is_root)
    arg_na = gen_argout(False); arg_nb = gen_argout(False)
    add_to_nand(arg_a, arg_a, arg_na)
    add_to_nand(arg_b, arg_b, arg_nb)
    add_to_nand(arg_na, arg_nb, arg_out)
    return arg_out
def binary_oper_impli(arg_a, arg_b, is_root):
    """ Binary opeartor about "Implication(->)" function.
    """
    arg_out = gen_argout(is_root)
    arg_temp = gen_argout(False)
    add_to_nand(arg_b, arg_b, arg_temp)
    add_to_nand(arg_a, arg_temp, arg_out)
    return arg_out
def binary_oper_nand(arg_a, arg_b, is_root):
    """ Binary opeartor about "NAND" function.
    This exists for the optimization cases like ~(a * b), ~a + ~b.
    """
    arg_out = gen_argout(is_root)
    add_to_nand(arg_a, arg_b, arg_out)
    return arg_out
# Map from unary operator to special function implementing it.
UNARY_OPERATORS = {
            '~': unary_oper_not,
}
# Map from binary operator to special function implementing it.
BINARY_OPERATORS = {
            '*': binary_oper_and,
            '+': binary_oper_or,
            '->': binary_oper_impli,
            '~*': binary_oper_nand,
}

Variable = namedtuple('Variable', 'name')
UnaryOp = namedtuple('UnaryOp', 'op operand')
BinaryOp = namedtuple('BinaryOp', 'left op right')




def tokenize(s):
    """Generate tokens from the string s, followed by TOKEN_END.
    """
    for m in TOKEN_RE.finditer(s):
        if m.group(1):
            yield m.group(1)
        else:
            raise SyntaxError("Unexpected character {!r}".format(m.group(2)))
    yield TOKEN_END


def parse(s):
    """Parse s as a Boolean expression and return the parse tree.
    """
    tokens = tokenize(s)        # Stream of tokens.
    token = next(tokens)        # The current token.

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
        if VARIABLE_RE.match(t):    # Use special(re) match(), not defined match().
            INPUT_PINS.add(t)
            token = next(tokens)    # Corner case!
            return Variable(name=t)
        elif match('('):
            tree = implication()
            if match(')'):
                return tree
            else:
                return False
        else:
            return False

    def unary_expr():
        # Parse a <UnaryExpr> starting at the current token.
        t = token
        if match('~'):
            operand = unary_expr()
            if isinstance(operand, UnaryOp):    # Check superfluous negation.
                return operand.operand
            elif isinstance(operand, BinaryOp) and operand.op == BINARY_OPERATORS['*']:   # NAND optimization 1.
                return BinaryOp(left=operand.left, op=BINARY_OPERATORS['~*'], right=operand.right)
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
            if t == '+' and isinstance(left, UnaryOp) and isinstance(right, UnaryOp):   # NAND optimization 2.
                return BinaryOp(left=left.operand, op=BINARY_OPERATORS['~*'], right=right.operand)
            return BinaryOp(left=left, op=BINARY_OPERATORS[t], right=right)
        else:
            return left

    def conjunction():
        # Parse a <Conjunction> starting at the current token.
        return binary_expr(unary_expr, '*', conjunction)

    def disjunction():
        # Parse a <Disjunction> starting at the current token.
        return binary_expr(conjunction, '+', disjunction)

    def implication():
        # Parse an <Implication> starting at the current token.
        return binary_expr(disjunction, '->', implication)

    tree = implication()
    if token != TOKEN_END:
        return False
    return tree


def evaluate(tree, is_root):
    """Evaluate the expression in the parse tree, so that the evaluated
    output is a chip of serveral Nand gates which implements this expression.
    """
    if isinstance(tree, Variable):  # leaf of tree. (base condition)
        return tree.name
    elif isinstance(tree, UnaryOp):
        sub_res = evaluate(tree.operand, False)
        return tree.op(sub_res, is_root) if sub_res else False
    elif isinstance(tree, BinaryOp):
        left_res = evaluate(tree.left, False); right_res = evaluate(tree.right, False)
        return tree.op(left_res, right_res, is_root) if left_res and right_res else False
    else:
        return False


def error_line(chip_name="???"):
    logging.warning("Unexpected line exists. SKIP [{}] chip!!".format(chip_name))




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        lines = list(filter(None, [line.rstrip('\n') for line in open(INPUT_FILE_NAME)]))
        for line in lines:
            # Initializations
            INPUT_PINS = set()
            NAND_GATES = []
            INDEX_PIN = 0
            print()

            # Split current line into 'Name' and 'Formula' parts
            line_tokenized = list(filter(None, [l.strip() for l in line.split('=')]))
            if len(line_tokenized) != 2:    # SKIP condition
                error_line()
                continue
            name = line_tokenized[0]; formula = line_tokenized[1]

            # Build parse tree
            formula_tree = parse(formula)
            logging.debug(formula_tree)
            if not formula_tree:
                error_line(name)
                continue
            logging.debug("Input pins: {}".format(INPUT_PINS))

            # Evaluate parse tree to generate Nand gates
            if isinstance(formula_tree, Variable) or not evaluate(formula_tree, True):
                error_line(name)
                continue
            logging.debug("Nand gates: {}".format(NAND_GATES))

            # Create chip(.hdl file)
            with open("{}.hdl".format(name), 'w') as f_output:
                res = "// {} Chip\n".format(name)
                res = res + "// Generate by cujun's formula compiler\n\n"
                res = res + "CHIP {} {{\n".format(name)
                res = res + "\tIN {};\n".format(", ".join(INPUT_PINS))
                res = res + "\tOUT out;\n\n\tPARTS:\n"
                res = res + "\t{}\n}}".format("\n\t".join(NAND_GATES))
                f_output.write(res)
                logging.info("[{}] Chip Done.".format(name))
    except IOError:
        logging.error("Could not read input file: {}".format(INPUT_FILE_NAME))
